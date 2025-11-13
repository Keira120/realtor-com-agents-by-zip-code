from src.parsers.html_parser import parse_agents_html
from src.parsers.agent_normalizer import AgentNormalizer

SAMPLE_HTML = """
<div class="agent-card">
  <a class="agent-name" href="https://example.com/agents/90049/1">Jane Doe</a>
  <span class="listing-count">Listings: 11</span>
  <span class="sold-count">Sold: 48</span>
  <span class="office-phone">(310) 270-xxxx</span>
  <span class="mobile-phone">(310) 279-xxxx, (310) 633-xxxx</span>
  <span class="areas-serviced">
    Los Angeles, Beverly Hills, Malibu, Santa Monica, West Hollywood,
    Venice, Marina del Rey, Pacific Palisades, Brentwood, Bel Air,
  </span>
  <span class="zip-codes">90049, 90068, 90210, 90265, 90402, 90401, 90403, 90069, 90291, 90292, 90272</span>
  <span class="office-name">Brentwood</span>
  <a class="company-website" href="https://company.example.com">Company</a>
  <span class="review-count">0 reviews</span>
  <img class="agent-photo" src="https://example.com/photo.jpg"/>
  <a href="mailto:Jane@example.com">Jane@example.com</a>
</div>
"""

def test_html_parser_extracts_raw_agent_data() -> None:
    agents = parse_agents_html(SAMPLE_HTML, zip_code="90049")
    assert len(agents) == 1
    agent = agents[0]
    assert agent["name"] == "Jane Doe"
    assert agent["profile_url"] == "https://example.com/agents/90049/1"
    assert agent["listing_count"] == 11
    assert agent["sold_count"] == 48
    assert agent["office_phone"].startswith("(310)")
    assert "mobile_phones_raw" in agent
    assert "areas_serviced_raw" in agent
    assert "zip_codes_serviced_raw" in agent
    assert agent["office_name"] == "Brentwood"
    assert agent["company_website"] == "https://company.example.com"
    assert agent["review_count"] == 0
    assert agent["photo_url"] == "https://example.com/photo.jpg"
    assert agent["email"] == "Jane@example.com"
    assert agent["zip_code_context"] == "90049"

def test_agent_normalizer_produces_expected_schema() -> None:
    raw = parse_agents_html(SAMPLE_HTML, zip_code="90049")[0]
    normalizer = AgentNormalizer()
    normalized = normalizer.normalize(raw)

    assert normalized["Agent name"] == "Jane Doe"
    assert normalized["Website"] == "https://example.com/agents/90049/1"
    assert normalized["Email"] == "Jane@example.com"
    assert normalized["Listing count"] == 11
    assert normalized["Sold count"] == 48
    assert normalized["Office Phone"].startswith("(310)")
    assert "Mobile Phones" in normalized
    assert "Areas serviced" in normalized
    assert "Zip codes serviced" in normalized
    assert normalized["Office / Company name"] == "Brentwood"
    assert normalized["Company Website"] == "https://company.example.com"
    assert normalized["Review count"] == 0
    assert normalized["Agent Photo"] == "https://example.com/photo.jpg"