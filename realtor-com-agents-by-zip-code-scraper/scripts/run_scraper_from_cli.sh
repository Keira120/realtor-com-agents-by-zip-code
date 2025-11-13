set -euo pipefail

# Simple helper to run the scraper from the project root.
# Example:
#   ./scripts/run_scraper_from_cli.sh --zip-codes 90049,90210 --output-format csv

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR%/scripts}"

cd "$PROJECT_ROOT"
python src/main.py "$@"