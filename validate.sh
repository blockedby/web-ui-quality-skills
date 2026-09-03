#!/bin/sh
# Dependency-free repository validation.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$ROOT/scripts/validate_repository.py"
