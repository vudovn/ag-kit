import os
import re
import argparse
import sys
import io


def configure_utf8_output() -> None:
    """Best-effort UTF-8 stdout/stderr on Windows without dropping diagnostics."""
    if sys.platform != "win32":
        return

    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name)
        try:
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
            continue
        except Exception:
            pass

        buffer = getattr(stream, "buffer", None)
        if buffer is not None:
            setattr(
                sys,
                stream_name,
                io.TextIOWrapper(buffer, encoding="utf-8", errors="backslashreplace"),
            )

WHEN_TO_USE_PATTERNS = [
    re.compile(r"^##\s+When\s+to\s+Use", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^##\s+Use\s+this\s+skill\s+when", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^##\s+When\s+to\s+Use\s+This\s+Skill", re.MULTILINE | re.IGNORECASE),
]

def has_when_to_use_section(content):
    return any(pattern.search(content) for pattern in WHEN_TO_USE_PATTERNS)

import yaml

def parse_frontmatter(content, rel_path=None):
    """
    Parse frontmatter using PyYAML for robustness.
    Returns a dict of key-values and a list of error messages.
    """
    fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return None, ["Missing or malformed YAML frontmatter"]
    
    fm_text = fm_match.group(1)
    fm_errors = []
    try:
        metadata = yaml.safe_load(fm_text) or {}
        
        # Identification of the specific regression issue for better reporting
        if "description" in metadata:
            desc = metadata["description"]
            if not desc or (isinstance(desc, str) and not desc.strip()):
                fm_errors.append("description field is empty or whitespace only.")
            elif desc == "|":
                fm_errors.append("description contains only the YAML block indicator '|', likely due to a parsing regression.")
        
        return metadata, fm_errors
    except yaml.YAMLError as e:
        return None, [f"YAML Syntax Error: {e}"]

def validate_skills(skills_dir, strict_mode=False):
    configure_utf8_output()

    print(f"🔍 Validating skills in: {skills_dir}")
    print(f"⚙️  Mode: {'STRICT (CI)' if strict_mode else 'Standard (Dev)'}")
    
    errors = []
    warnings = []
    skill_count = 0
    
    # Pre-compiled regex
    security_disclaimer_pattern = re.compile(r"AUTHORIZED USE ONLY", re.IGNORECASE)

    valid_risk_levels = ["none", "safe", "critical", "offensive", "unknown"]
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')  # YYYY-MM-DD format

    for root, dirs, files in os.walk(skills_dir):
        # Skip .disabled or hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        if "SKILL.md" in files:
            skill_count += 1
            skill_path = os.path.join(root, "SKILL.md")
            rel_path = os.path.relpath(skill_path, skills_dir)
            
            try:
                with open(skill_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                errors.append(f"❌ {rel_path}: Unreadable file - {str(e)}")
                continue
            
            # 1. Frontmatter Check
            metadata, fm_errors = parse_frontmatter(content, rel_path)
            if not metadata:
                errors.append(f"❌ {rel_path}: Missing or malformed YAML frontmatter")
                continue # Cannot proceed without metadata
            
            if fm_errors:
                for fe in fm_errors:
                    errors.append(f"❌ {rel_path}: YAML Structure Error - {fe}")

            # 2. Metadata Schema Checks
            if "name" not in metadata:
                errors.append(f"❌ {rel_path}: Missing 'name' in frontmatter")
            elif metadata["name"] != os.path.basename(root):
                errors.append(f"❌ {rel_path}: Name '{metadata['name']}' does not match folder name '{os.path.basename(root)}'")

            if "description" not in metadata or metadata["description"] is None:
                errors.append(f"❌ {rel_path}: Missing 'description' in frontmatter")
            else:
                # agentskills-ref checks for short descriptions
                desc = metadata["description"]
                if not isinstance(desc, str):
                    errors.append(f"❌ {rel_path}: 'description' must be a string, got {type(desc).__name__}")
                elif len(desc) > 300: # increased limit for multi-line support
                    errors.append(f"❌ {rel_path}: Description is oversized ({len(desc)} chars). Must be concise.")

            # Risk Validation (Quality Bar)
            if "risk" not in metadata:
                msg = f"⚠️  {rel_path}: Missing 'risk' label (defaulting to 'unknown')"
                if strict_mode: errors.append(msg.replace("⚠️", "❌"))
                else: warnings.append(msg)
            elif metadata["risk"] not in valid_risk_levels:
                errors.append(f"❌ {rel_path}: Invalid risk level '{metadata['risk']}'. Must be one of {valid_risk_levels}")

            # Source Validation
            if "source" not in metadata:
                msg = f"⚠️  {rel_path}: Missing 'source' attribution"
                if strict_mode: errors.append(msg.replace("⚠️", "❌"))
                else: warnings.append(msg)

            # Date Added Validation (optional field)
            if "date_added" in metadata:
                if not date_pattern.match(metadata["date_added"]):
                    errors.append(f"❌ {rel_path}: Invalid 'date_added' format. Must be YYYY-MM-DD (e.g., '2024-01-15'), got '{metadata['date_added']}'")
            else:
                msg = f"ℹ️  {rel_path}: Missing 'date_added' field (optional, but recommended)"
                if strict_mode: warnings.append(msg)
                # In normal mode, we just silently skip this

            # 3. Content Checks (Triggers)
            if not has_when_to_use_section(content):
                msg = f"⚠️  {rel_path}: Missing '## When to Use' section"
                if strict_mode: errors.append(msg.replace("⚠️", "❌"))
                else: warnings.append(msg)

            # 4. Security Guardrails
            if metadata.get("risk") == "offensive":
                if not security_disclaimer_pattern.search(content):
                    errors.append(f"🚨 {rel_path}: OFFENSIVE SKILL MISSING SECURITY DISCLAIMER! (Must contain 'AUTHORIZED USE ONLY')")

            # 5. Dangling Links Validation
            # Look for markdown links: [text](href)
            links = re.findall(r'\[[^\]]*\]\(([^)]+)\)', content)
            for link in links:
                link_clean = link.split('#')[0].strip()
                # Skip empty anchors, external links, and edge cases
                if not link_clean or link_clean.startswith(('http://', 'https://', 'mailto:', '<', '>')):
                    continue
                if os.path.isabs(link_clean):
                    continue
                
                # Check if file exists relative to this skill file
                target_path = os.path.normpath(os.path.join(root, link_clean))
                if not os.path.exists(target_path):
                    errors.append(f"❌ {rel_path}: Dangling link detected. Path '{link_clean}' (from '...({link})') does not exist locally.")

    # Reporting
    print(f"\n📊 Checked {skill_count} skills.")
    
    if warnings:
        print(f"\n⚠️  Found {len(warnings)} Warnings:")
        for w in warnings:
            print(w)

    if errors:
        print(f"\n❌ Found {len(errors)} Critical Errors:")
        for e in errors:
            print(e)
        return False

    if strict_mode and warnings:
        print("\n❌ STRICT MODE: Failed due to warnings.")
        return False

    print("\n✨ All skills passed validation!")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Antigravity Skills")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings (for CI)")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills_path = os.path.join(base_dir, "skills")
    
    success = validate_skills(skills_path, strict_mode=args.strict)
    if not success:
        sys.exit(1)
