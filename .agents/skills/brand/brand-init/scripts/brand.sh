#!/usr/bin/env bash
# brand.sh — scaffold and index brand packages. Dependency-free (no YAML library).
# See references/brand-package-spec.md.
#
#   brand.sh init --name "Cofoundy" [--slug cofoundy] [--one-liner "…"] [--out DIR]
#                 [--date YYYY-MM-DD] [--register brands/registry.yaml]
#   brand.sh list [--registry brands/registry.yaml]
#   brand.sh set  --package DIR --key one_liner --value "…"
set -euo pipefail

slugify() { printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g'; }
err() { echo "brand.sh: $*" >&2; exit 1; }

cmd="${1:-}"; shift || true
name=""; slug=""; oneliner=""; out=""; date=""; registry=""; package=""; key=""; value=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --name) name="$2"; shift 2;;
    --slug) slug="$2"; shift 2;;
    --one-liner) oneliner="$2"; shift 2;;
    --out) out="$2"; shift 2;;
    --date) date="$2"; shift 2;;
    --register|--registry) registry="$2"; shift 2;;
    --package) package="$2"; shift 2;;
    --key) key="$2"; shift 2;;
    --value) value="$2"; shift 2;;
    *) err "unknown arg: $1";;
  esac
done
[[ -n "$date" ]] || date="$(date +%F)"

case "$cmd" in
  init)
    [[ -n "$name" ]] || err "init needs --name"
    [[ -n "$slug" ]] || slug="$(slugify "$name")"
    [[ -n "$out" ]]  || out="brand"
    [[ -e "$out/brand.yaml" ]] && err "package already exists at $out/ (refusing to overwrite)"
    mkdir -p "$out/assets"
    # heredoc with no var expansion of the body except where intended
    {
      echo "schema_version: 1"
      echo "slug: $slug"
      echo "name: $name"
      echo "one_liner: ${oneliner}"
      echo "tagline: \"\""
      echo "archetype: \"\""
      echo "status: draft"
      echo "stage: \"\""
      echo "industry: \"\""
      echo "languages: [en]"
      echo "links:"
      echo "  domain: \"\""
      echo "  repo: \"\""
      echo "created: $date"
      echo "updated: $date"
      echo "version: 1"
      echo "artifacts:"
      for a in context naming strategy architecture identity voice messaging positioning story guidelines audit; do
        echo "  $a: false"
      done
    } > "$out/brand.yaml"
    echo "created package: $out/ (brand.yaml + assets/)"
    if [[ -n "$registry" ]]; then
      regdir="$(dirname "$registry")"; mkdir -p "$regdir"
      [[ -f "$registry" ]] || printf 'schema_version: 1\nbrands:\n' > "$registry"
      if grep -qE "^[[:space:]]*-[[:space:]]*slug:[[:space:]]*$slug$" "$registry"; then
        echo "registry: $slug already present in $registry (skipped)"
      else
        relpath="$out"
        {
          echo "  - slug: $slug"
          echo "    name: $name"
          echo "    one_liner: ${oneliner}"
          echo "    path: $relpath"
          echo "    status: draft"
          echo "    created: $date"
        } >> "$registry"
        echo "registry: registered $slug in $registry"
      fi
    fi
    ;;
  list)
    [[ -n "$registry" ]] || registry="brands/registry.yaml"
    [[ -f "$registry" ]] || err "no registry at $registry"
    awk '
      /^[[:space:]]*-[[:space:]]*slug:/ { if (s!="") print s" · "n" · "o" · "p" ["st"]"; s=$0; sub(/.*slug:[[:space:]]*/,"",s); n=o=p=st="" }
      /^[[:space:]]+name:/      { v=$0; sub(/.*name:[[:space:]]*/,"",v); n=v }
      /^[[:space:]]+one_liner:/ { v=$0; sub(/.*one_liner:[[:space:]]*/,"",v); o=v }
      /^[[:space:]]+path:/      { v=$0; sub(/.*path:[[:space:]]*/,"",v); p=v }
      /^[[:space:]]+status:/    { v=$0; sub(/.*status:[[:space:]]*/,"",v); st=v }
      END { if (s!="") print s" · "n" · "o" · "p" ["st"]" }
    ' "$registry"
    ;;
  set)
    [[ -n "$package" && -n "$key" ]] || err "set needs --package and --key"
    f="$package/brand.yaml"; [[ -f "$f" ]] || err "no brand.yaml in $package"
    if grep -qE "^$key:" "$f"; then
      tmp="$(mktemp)"; sed -E "s|^($key:).*|\\1 $value|" "$f" > "$tmp" && mv "$tmp" "$f"
      echo "set $key in $f"
    else
      err "key '$key' not found in $f"
    fi
    ;;
  ""|-h|--help|help) sed -n '2,12p' "$0";;
  *) err "unknown command: $cmd (init|list|set)";;
esac
