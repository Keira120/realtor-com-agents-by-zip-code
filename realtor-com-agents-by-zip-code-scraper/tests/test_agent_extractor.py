from typing import Any, Dict, List

from src.agent_extractor import AgentExtractor

class FakeLogger:
    def __init__(self) -> None:
        self.messages: List[str] = []

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.messages.append(msg % args if args else msg)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.messages.append(msg % args if args else msg)

class FakeRealtorClient:
    def __init__(self) -> None:
        self.calls: List[str] = []

    def search_agents_by_zip(self, zip_code: str, max_records=None) -> List[Dict[str, Any]]:
        self.calls.append(zip_code)
        return [
            {
                "name": f"Agent {zip_code}",
                "profile_url": f"https://example.com/agents/{zip_code}/1",
                "email": f"{zip_code}@example.com",
                "listing_count": 3,
                "sold_count": 7,
                "office_phone": "123-456-7890",
                "mobile_phones_raw": "111-111-1111, 222-222-2222",
                "areas_serviced_raw": "Area A, Area B",
                "zip_codes_serviced_raw": f"{zip_code}, 99999",
                "office_name": "Office X",
                "company_website": "https://office.example.com",
                "review_count": 10,
                "photo_url": "https://example.com/photo.jpg",
                "zip_code_context": zip_code,
            }
        ]

def test_agent_extractor_normalizes_and_limits_trial() -> None:
    client = FakeRealtorClient()
    logger = FakeLogger()
    extractor = AgentExtractor(client=client, logger=logger)

    zip_codes = ["90049", "90210", "90402"]
    agents = extractor.extract_for_zip_codes(zip_codes, trial_limit=2)

    assert len(agents) == 2
    assert {a["Zip codes serviced"] for a in agents} == {"90049, 99999", "90210, 99999"}
    assert "Agent 90049" in agents[0]["Agent name"]
    assert client.calls[:2] == ["90049", "90210"]