from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

from pagination_manager import PaginationManager
from parsers.html_parser import parse_agents_html

@dataclass
class RealtorClient:
    base_url: str
    rate_limiter: Optional[Any] = None
    session: Optional[requests.Session] = None
    user_agent: Optional[str] = None
    cookie: Optional[str] = None
    logger: Optional[Any] = None

    def __post_init__(self) -> None:
        if self.session is None:
            self.session = requests.Session()
        self.pagination = PaginationManager()
        if self.logger is None:
            # Lazy import to avoid circular dependency
            from utils.logger import get_logger

            self.logger = get_logger(self.__class__.__name__)

    def _build_headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        if self.user_agent:
            headers["User-Agent"] = self.user_agent
        return headers

    def _build_cookies(self) -> Dict[str, str]:
        cookies: Dict[str, str] = {}
        if self.cookie:
            cookies["KP_UIDz-ssn"] = self.cookie
        return cookies

    def _fetch_page(self, zip_code: str, page_number: int) -> str:
        url = f"{self.base_url}/{zip_code}"
        if page_number > 1:
            url = f"{url}/pg-{page_number}"
        params: Dict[str, str] = {}

        if self.logger:
            self.logger.debug("Fetching URL %s (page %d)", url, page_number)

        if self.rate_limiter:
            self.rate_limiter.wait()

        try:
            response = self.session.get(
                url,
                headers=self._build_headers(),
                cookies=self._build_cookies(),
                params=params,
                timeout=15,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            if self.logger:
                self.logger.warning("Request error for %s: %s", url, exc)
            return ""

        return response.text

    def search_agents_by_zip(
        self, zip_code: str, max_records: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Fetch and parse agents for a single zip code."""
        agents: List[Dict[str, Any]] = []
        page_number = 1

        while True:
            html = self._fetch_page(zip_code, page_number)
            if not html:
                break

            page_agents = parse_agents_html(html, zip_code=zip_code)
            if not page_agents:
                if self.logger:
                    self.logger.debug(
                        "No agents found on page %d for zip %s", page_number, zip_code
                    )
                break

            agents.extend(page_agents)

            if max_records is not None and len(agents) >= max_records:
                agents = agents[:max_records]
                break

            if not self.pagination.should_continue(
                page_number=page_number,
                agents_on_page=len(page_agents),
                total_agents=len(agents),
                max_agents=max_records,
            ):
                break

            page_number += 1

        if self.logger:
            self.logger.info(
                "Fetched %d raw agents for zip %s", len(agents), zip_code
            )
        return agents