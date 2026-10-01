#!/usr/bin/env bash
# Render editable HTML figures to vector assets without Inkscape.

set -euo pipefail
cd "$(dirname "$0")"

for command_name in python3 rsvg-convert pdfcrop; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "$command_name is required to render the figures." >&2
    exit 127
  fi
done

output_dir="figures"
mkdir -p "$output_dir"

if command -v chromium >/dev/null 2>&1; then
  browser=(chromium)
  windows_browser=0
elif command -v google-chrome >/dev/null 2>&1; then
  browser=(google-chrome)
  windows_browser=0
elif [ -x "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe" ]; then
  browser=("/mnt/c/Program Files/Google/Chrome/Application/chrome.exe")
  windows_browser=1
else
  browser=()
  windows_browser=0
fi

for html in figs/*.html; do
  name="$(basename "$html" .html)"
  case "$name" in
    # drawn by the website scripts in paper mode (scripts/gen_web_figs.py); the old HTML here is superseded
    figure_nested-rings|figure_coleman-boat|*-paper|figure-options-gallery) continue ;;
  esac
  svg="$output_dir/$name.svg"
  pdf="$output_dir/$name.pdf"
  svg_count="$(grep -o '<svg\b' "$html" | wc -l)"
  if [ "$svg_count" -eq 1 ]; then
    python3 scripts/extract_svg.py "$html" "$svg"
    rsvg-convert --format pdf1.5 --output "$pdf" "$svg"
  else
    if [ "${#browser[@]}" -eq 0 ]; then
      echo "Chrome or Chromium is required to compose $html." >&2
      exit 127
    fi
    html_path="$(pwd)/$html"
    raw_path="$(pwd)/$output_dir/.$name.raw.pdf"
    if [ "$windows_browser" -eq 1 ]; then
      uri="file:///$(wslpath -w "$html_path" | tr '\\' '/')"
      output_arg="--print-to-pdf=$(wslpath -w "$raw_path")"
    else
      uri="file://$html_path"
      output_arg="--print-to-pdf=$raw_path"
    fi
    "${browser[@]}" --headless=new --disable-gpu --no-pdf-header-footer \
      --allow-file-access-from-files "$output_arg" "$uri" >/dev/null 2>&1
    pdfcrop --margins 0 "$raw_path" "$pdf" >/dev/null
    rm -f "$raw_path"
  fi
  printf 'Rendered %s\n' "$pdf"
done
