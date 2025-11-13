from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup

def _extract_int(text: Optional[str]) -> Optional[int]:
    if not text:
        return None
    digits = "".join(ch for ch in text if ch.isdigit())
    if not digits:
        return None
    return int(digits)

def parse_agents_html(html: str, zip_code: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Parse Realtor-like HTML and return a list of raw agent dictionaries.

    This parser is resilient and uses generic selectors so it can work with
    simplified HTML used in tests and modest changes in the real site.
    """
    soup = BeautifulSoup(html, "html.parser")
    agents: List[Dict[str, Any]] = []

    # Primary heuristic: cards with a generic 'agent-card' class
    cards = soup.select(".agent-card")
    if not cards:
        # Fallback heuristics
        cards = soup.select("[data-testid*='agent-card'], article")

    for card in cards:
        name_el = card.select_one(".agent-name, a.agent-name, a[data-testid='agent-name']")
        profile_link_el = name_el if name_el and name_el.has_attr("href") else card.select_one(
            "a.agent-profile-link, a[href*='realestateagents']"
        )
        email_el = card.select_one("a[href^='mailto:']")
        listing_el = card.select_one(".listing-count")
        sold_el = card.select_one(".sold-count")
        office_phone_el = card.select_one(".office-phone")
        mobile_phones_el = card.select_one(".mobile-phone, .mobile-phones")
        areas_el = card.select_one(".areas-serviced")
        zips_el = card.select_one(".zip-codes-serviced, .zip-codes")
        office_name_el = card.select_one(".office-name, .company-name")
        company_website_el = card.select_one(".company-website[href]")
        photo_el = card.select_one("img.agent-photo, img[data-testid='agent-photo']")

        raw: Dict[str, Any] = {
            "name": name_el.get_text(strip=True) if name_el else None,
            "profile_url": profile_link_el["href"] if profile_link_el and profile_link_el.has_attr("href") else None,
            "email": email_el.get_text(strip=True) if email_el else None,
            "listing_count": _extract_int(listing_el.get_text(strip=True) if listing_el else None),
            "sold_count": _extract_int(sold_el.get_text(strip=True) if sold_el else None),
            "office_phone": office_phone_el.get_text(strip=True) if office_phone_el else None,
            "mobile_phones_raw": mobile_phones_el.get_text(strip=True) if mobile_phones_el else None,
            "areas_serviced_raw": areas_el.get_text(strip=False) if areas_el else None,
            "zip_codes_serviced_raw": zips_el.get_text(strip=True) if zips_el else None,
            "office_name": office_name_el.get_text(strip=True) if office_name_el else None,
            "company_website": company_website_el["href"] if company_website_el and company_website_el.has_attr("href") else None,
            "review_count": _extract_int(
                (card.select_one(".review-count") or card.select_one(".reviews"))
                .get_text(strip=True)
                if (card.select_one(".review-count") or card.select_one(".reviews"))
                else None
            ),
            "photo_url": photo_el["src"] if photo_el and photo_el.has_attr("src") else None,
            "zip_code_context": zip_code,
        }

        agents.append(raw)

    return agents