#!/bin/zsh
# generate_index_md.sh
# Lists all files in a folder and writes an INDEX.md manifest.
#
# Usage: ./generate_index_md.sh <FOLDER_PATH>
#
# Inputs:
#   FOLDER_PATH — Path to the folder to index
#
# Outputs:
#   INDEX.md written in the specified folder.
#
# Example:
#   ./generate_index_md.sh ./_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/Scaffold

FOLDER="${1:?Usage: $0 <FOLDER_PATH>}"

INDEX_FILE="$FOLDER/INDEX.md"
FOLDER_NAME=$(basename "$FOLDER")

{
  echo "# Index: $FOLDER_NAME"
  echo ""
  echo "Generated: $(date +%Y-%m-%d)"
  echo ""
  echo "| File | Size |"
  echo "|------|------|"

  find "$FOLDER" -maxdepth 1 -type f ! -name "INDEX.md" | sort | while read f; do
    fname=$(basename "$f")
    fsize=$(wc -c < "$f" | tr -d ' ')
    echo "| $fname | ${fsize} bytes |"
  done
} > "$INDEX_FILE"

echo "Wrote $INDEX_FILE"
