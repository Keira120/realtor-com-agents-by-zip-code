from typing import Any, Dict

from src.realtor_client import RealtorClient
from src.parsers.html_parser import parse_agents_html

class DummyResponse:
    def __init__(self, text: str, status_code: int = 200) -> None:
        self.text = text
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if not (200 <= self.status_code < 300):
            raise Exception("HTTP error")

class DummySession:
    def __init__(self, html: str) -> None:
        self.html = html
        self.last_url: str | None = None
        self.calls = 0

    def get(self, url: str, headers: Dict[str, Any], cookies: Dict[str, Any], params, timeout: int) -> DummyResponse:
        self.last_url = url
        self.calls += 1
        return DummyResponse(self.html)

class DummyRateLimiter:
    def __init__(self) -> None:
        self.calls = 0

    def wait(self) -> None:
        self.calls += 1

class DummyLogger:
    def __init__(self) -> None:
        self.infos: list[str] = []
        self.warnings: list[str] = []

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.infos.append(msg % args if args else msg)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.warnings.append(msg % args if args else msg)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        pass

SAMPLE_HTML = """
<div class="agent-card">
  <a class="agent-name" href="https://example.com/agents/90049/1">Test Agent</a>
  <span class="listing-count">Listings: 5</span>
  <span class="sold-count">Sold: 12</span>
  <span class="office-phone">(555) 000-0000</span>
  <span class="mobile-phone">111-111-1111, 222-222-2222</span>
  <span class="areas-serviced">Area A, Area B</span>
  <span class="zip-codes">90049, 90210</span>
  <span class="office-name">Test Office</span>
  <a class="company-website" href="https://office.example.com">Company</a>
  <span class="review-count">Reviews: 3</span>
  <img class="agent-photo" src="https://example.com/photo.jpg"/>
  <a href="mailto:test@example.com">test@example.com</a>
</div>
"""

def test_realtor_client_uses_session_and_parses_agents() -> None:
    dummy_session = DummySession(SAMPLE_HTML)
    rate_limiter = DummyRateLimiter()
    logger = DummyLogger()
    client = RealtorClient(
        base_url="https://example.com/agents",
        session=dummy_session,
        rate_limiter=rate_limiter,
        user_agent="test-agent",
        cookie="cookie-value",
        logger=logger,
    )

    agents = client.search_agents_by_zip("90049", max_records=1)

    assert dummy_session.calls >= 1
    assert "90049" in (dummy_session.last_url or "")
    assert rate_limiter.calls >= 1
    assert len(agents) == 1
    raw = agents[0]
    parsed = parse_agents_html(SAMPLE_HTML, zip_code="90049")[0]
    assert raw["name"] == parsed["name"]
    assert raw["profile_url"] == parsed["profile_url"]