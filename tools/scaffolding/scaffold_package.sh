#!/bin/zsh
# scaffold_package.sh
# Creates a package folder with all 9 lifecycle subfolders per SPEC.md Section 1.1.
#
# Usage: ./scaffold_package.sh <EXECUTION_ROOT> <PKG_ID> <PkgLabel>
#
# Inputs:
#   EXECUTION_ROOT — Path to project execution root
#   PKG_ID         — Package identifier (e.g., PKG-001)
#   PkgLabel       — Human-readable label (e.g., "Architectural Design")
#
# Outputs:
#   Package folder with 9 subfolders. Reports created vs already-existed.
#
# Example:
#   ./scaffold_package.sh ./execution PKG-001 "Architectural Design"

EXROOT="${1:?Usage: $0 <EXECUTION_ROOT> <PKG_ID> <PkgLabel>}"
PKG_ID="${2:?Usage: $0 <EXECUTION_ROOT> <PKG_ID> <PkgLabel>}"
PKG_LABEL="${3:?Usage: $0 <EXECUTION_ROOT> <PKG_ID> <PkgLabel>}"

PKG_DIR="$EXROOT/${PKG_ID}_${PKG_LABEL}"

SUBDIRS=(
  "0_References"
  "0_References/_Archive"
  "1_Working"
  "1_Working/_Archive"
  "2_Checking"
  "2_Checking/From"
  "2_Checking/To"
  "3_Issued"
  "3_Issued/_Archive"
)

created=0
existed=0

for sub in "${SUBDIRS[@]}"; do
  target="$PKG_DIR/$sub"
  if [ -d "$target" ]; then
    existed=$((existed + 1))
  else
    mkdir -p "$target"
    created=$((created + 1))
  fi
done

echo "Package: $PKG_DIR"
echo "Created: $created subfolders"
echo "Already existed: $existed subfolders"
