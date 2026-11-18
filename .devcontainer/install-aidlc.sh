#!/bin/sh
set -eu

version=2.11.4
installer_sha256=3ccd128b79c9cc7607fa811c4c6d1dedd888e516af29d942b5b8679f48ebdb83
tmp_dir=$(mktemp -d)
trap 'rm -f "$tmp_dir/install.sh"; rmdir "$tmp_dir"' EXIT

curl -fsSL --retry 2 \
  "https://github.com/awslabs/aidlc-workflows/releases/download/v${version}/install.sh" \
  -o "$tmp_dir/install.sh"
printf '%s  %s\n' "$installer_sha256" "$tmp_dir/install.sh" | sha256sum --check
sh "$tmp_dir/install.sh" --version "$version" --yes
