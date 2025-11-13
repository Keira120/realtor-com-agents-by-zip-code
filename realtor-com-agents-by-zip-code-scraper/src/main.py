import argparse
import json
from pathlib import Path
from typing import List, Optional

from config import get_settings
from utils.logger import get_logger
from utils.rate_limiter import RateLimiter
from realtor_client import RealtorClient
from agent_extractor import AgentExtractor
from storage.json_exporter import export_agents_to_json
from storage.csv_exporter import export_agents_to_csv

logger = get_logger(__name__)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Realtor.com Agents by Zip Code Scraper CLI"
    )
    parser.add_argument(
        "--zip-codes",
        type=str,
        help="Comma-separated list of zip codes to scrape (e.g. 90049,90210).",
    )
    parser.add_argument(
        "--zip-file",
        type=str,
        help="Path to JSON file containing a list of zip codes.",
    )
    parser.add_argument(
        "--settings",
        type=str,
        default=None,
        help="Path to YAML settings file (overrides defaults).",
    )
    parser.add_argument(
        "--output-format",
        type=str,
        default="json",
        choices=["json", "csv"],
        help="Output format for scraped agents.",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        default=None,
        help="Output file path. Defaults to ./data/agents.<format>.",
    )
    parser.add_argument(
        "--trial-limit",
        type=int,
        default=None,
        help="Optional limit on the total number of agents for a trial run.",
    )
    parser.add_argument(
        "--cookie",
        type=str,
        default=None,
        help="Optional KP_UIDz-ssn cookie value.",
    )
    parser.add_argument(
        "--user-agent",
        type=str,
        default=None,
        help="Optional User-Agent string override.",
    )
    return parser.parse_args()

def load_zip_codes(args: argparse.Namespace, project_root: Path) -> List[str]:
    if args.zip_codes:
        zip_codes = [z.strip() for z in args.zip_codes.split(",") if z.strip()]
        if not zip_codes:
            raise ValueError("No valid zip codes provided in --zip-codes.")
        return zip_codes

    if args.zip_file:
        path = Path(args.zip_file)
        if not path.is_absolute():
            path = project_root / path
        if not path.exists():
            raise FileNotFoundError(f"Zip code file not found: {path}")
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Zip code file must contain a JSON list of zip codes.")
        zip_codes = [str(z).strip() for z in data if str(z).strip()]
        if not zip_codes:
            raise ValueError("Zip code file contained no valid zip codes.")
        return zip_codes

    # Fallback: try sample input file
    sample_path = project_root / "data" / "input_zip_codes.sample.json"
    if sample_path.exists():
        logger.info("No zip codes provided, using sample file: %s", sample_path)
        with sample_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list) and data:
            return [str(z).strip() for z in data if str(z).strip()]

    raise ValueError(
        "You must provide zip codes via --zip-codes or --zip-file. "
        "See data/input_zip_codes.sample.json for an example."
    )

def resolve_output_path(
    args: argparse.Namespace, project_root: Path, output_format: str
) -> Path:
    if args.output_path:
        path = Path(args.output_path)
        if not path.is_absolute():
            path = project_root / path
        return path
    default_dir = project_root / "data"
    default_dir.mkdir(parents=True, exist_ok=True)
    return default_dir / f"agents.{output_format}"

def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    args = parse_args()

    settings = get_settings(args.settings)
    if args.trial_limit is not None:
        settings.trial_limit = args.trial_limit

    cookie = args.cookie or settings.cookie
    user_agent = args.user_agent or settings.user_agent

    rate_limiter = RateLimiter(calls_per_minute=settings.rate_limit_rpm)
    client = RealtorClient(
        base_url=settings.base_url,
        rate_limiter=rate_limiter,
        user_agent=user_agent,
        cookie=cookie,
        logger=logger,
    )
    extractor = AgentExtractor(client=client, logger=logger)

    try:
        zip_codes = load_zip_codes(args, project_root)
    except Exception as exc:
        logger.error("Failed to load zip codes: %s", exc)
        raise SystemExit(1)

    output_format = args.output_format.lower()
    output_path = resolve_output_path(args, project_root, output_format)

    logger.info("Starting scrape for zip codes: %s", ", ".join(zip_codes))
    try:
        agents = extractor.extract_for_zip_codes(
            zip_codes=zip_codes,
            max_per_zip=None,
            trial_limit=settings.trial_limit,
        )
    except Exception as exc:
        logger.error("Scraping failed: %s", exc, exc_info=True)
        raise SystemExit(1)

    if not agents:
        logger.warning("No agents were extracted. Exiting without writing output.")
        raise SystemExit(0)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_format == "json":
        export_agents_to_json(agents, output_path)
    else:
        export_agents_to_csv(agents, output_path)

    logger.info(
        "Scraping complete. Wrote %d agents to %s",
        len(agents),
        output_path,
    )

if __name__ == "__main__":
    main()