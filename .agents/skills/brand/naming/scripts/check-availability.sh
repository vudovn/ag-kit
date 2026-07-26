#!/usr/bin/env bash
# check-availability.sh — Quick availability check for a product name
# Usage: bash check-availability.sh <name> [platforms...]
# Platforms: domain, npm, pypi, github, crates, rubygems, wp, telegram
# If no platforms specified, checks domain + github + npm

set -euo pipefail

NAME="${1:?Usage: check-availability.sh <name> [platforms...]}"
shift
PLATFORMS=("$@")
[[ ${#PLATFORMS[@]} -eq 0 ]] && PLATFORMS=(domain github npm)

have() { command -v "$1" >/dev/null 2>&1; }
# Centralized HTTP probe so a missing curl degrades to "000" everywhere instead of crashing.
http_code() { have curl && curl -s -o /dev/null -w "%{http_code}" "$1" 2>/dev/null || echo "000"; }

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

ok()   { echo -e "  ${GREEN}AVAILABLE${NC}  $1"; }
taken(){ echo -e "  ${RED}TAKEN${NC}      $1"; }
warn() { echo -e "  ${YELLOW}UNCLEAR${NC}    $1"; }

echo "Checking availability for: ${NAME}"
echo "---"

for platform in "${PLATFORMS[@]}"; do
  case "$platform" in
    domain)
      for tld in com dev io; do
        if have whois; then
          result=$(whois "${NAME}.${tld}" 2>&1 || true)
          # Registration markers win FIRST. A registered domain's whois always carries
          # these fields; its boilerplate/TOS text often contains "available"/"not found"
          # in unrelated sentences — matching those first caused false "AVAILABLE" hits.
          if echo "$result" | grep -qiE "^[[:space:]]*(Domain Name|Creation Date|Created On|Created|Registry Expiry|Registrar|Name Server|nserver|Updated Date):"; then
            taken "${NAME}.${tld}"
          elif echo "$result" | grep -qiE "no match|not found|no object found|no data found|not been registered|no entries|status: *free|available for registration|domain not found"; then
            ok "${NAME}.${tld}"
          else
            warn "${NAME}.${tld} (whois ambiguous — verify at registrar; ccTLDs .dev/.md/.ai/.io often unreliable)"
          fi
        else
          code=$(http_code "https://${NAME}.${tld}")
          if [ "$code" = "000" ]; then
            warn "${NAME}.${tld} (no whois, no HTTP response — may be available)"
          else
            taken "${NAME}.${tld} (HTTP ${code} — site is live)"
          fi
        fi
      done
      ;;
    npm)
      if ! have npm; then
        warn "npm: ${NAME} (npm not installed — skipped)"
      else
        result=$(npm view "$NAME" 2>&1 || true)
        if echo "$result" | grep -qi "not found\|404\|E404"; then
          ok "npm: ${NAME}"
        else
          taken "npm: ${NAME}"
        fi
      fi
      ;;
    pypi)
      code=$(http_code "https://pypi.org/project/${NAME}/")
      if [ "$code" = "404" ]; then
        ok "PyPI: ${NAME}"
      elif [ "$code" = "000" ]; then
        warn "PyPI: ${NAME} (no HTTP response — verify manually)"
      else
        taken "PyPI: ${NAME} (HTTP ${code})"
      fi
      ;;
    github)
      code=$(http_code "https://github.com/${NAME}")
      if [ "$code" = "404" ]; then
        ok "GitHub org: ${NAME}"
      elif [ "$code" = "000" ]; then
        warn "GitHub org: ${NAME} (no HTTP response — verify manually)"
      else
        taken "GitHub org: ${NAME} (HTTP ${code})"
      fi
      ;;
    crates)
      code=$(http_code "https://crates.io/api/v1/crates/${NAME}")
      if [ "$code" = "404" ]; then
        ok "crates.io: ${NAME}"
      elif [ "$code" = "000" ]; then
        warn "crates.io: ${NAME} (no HTTP response — verify manually)"
      else
        taken "crates.io: ${NAME} (HTTP ${code})"
      fi
      ;;
    rubygems)
      code=$(http_code "https://rubygems.org/api/v1/gems/${NAME}.json")
      if [ "$code" = "404" ]; then
        ok "RubyGems: ${NAME}"
      elif [ "$code" = "000" ]; then
        warn "RubyGems: ${NAME} (no HTTP response — verify manually)"
      else
        taken "RubyGems: ${NAME} (HTTP ${code})"
      fi
      ;;
    wp)
      if ! have curl; then
        warn "WP plugin: ${NAME} (curl not installed — skipped)"
      else
        result=$(curl -s "https://api.wordpress.org/plugins/info/1.2/?action=plugin_information&slug=${NAME}" 2>/dev/null || echo "error")
        if echo "$result" | grep -qi "not found"; then
          ok "WP plugin: ${NAME}"
        else
          taken "WP plugin: ${NAME}"
        fi
      fi
      ;;
    telegram)
      body=$(have curl && curl -sL "https://t.me/${NAME}" 2>/dev/null || echo "")
      if echo "$body" | grep -q "tgme_page_title"; then
        taken "Telegram: @${NAME}"
      else
        warn "Telegram: @${NAME} (no public profile found — may be available, verify in app)"
      fi
      ;;
    *)
      echo "  Unknown platform: $platform (valid: domain, npm, pypi, github, crates, rubygems, wp, telegram)"
      ;;
  esac
done

echo "---"
echo "Note: automated checks can give false positives. Always verify manually before committing."
