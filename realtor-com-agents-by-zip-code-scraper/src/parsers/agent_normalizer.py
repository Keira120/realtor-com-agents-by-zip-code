from typing import Any, Dict, Optional

class AgentNormalizer:
    """
    Convert raw parsed agent dictionaries into the final structured schema
    described in the project README.
    """

    FIELD_ORDER = [
        "Agent name",
        "Website",
        "Email",
        "Listing count",
        "Sold count",
        "Office Phone",
        "Mobile Phones",
        "Areas serviced",
        "Zip codes serviced",
        "Office / Company name",
        "Company Website",
        "Review count",
        "Agent Photo",
    ]

    def _clean_phones(self, raw: Optional[str]) -> str:
        if not raw:
            return ""
        parts = [p.strip() for p in raw.replace(";", ",").split(",")]
        parts = [p for p in parts if p]
        return ", ".join(parts)

    def _clean_areas(self, raw: Optional[str]) -> str:
        if not raw:
            return ""
        return " ".join(raw.split())

    def _clean_zip_codes(self, raw: Optional[str], context_zip: Optional[str]) -> str:
        if raw and raw.strip():
            # Normalize delimiters to comma-separated values
            parts = [p.strip() for p in raw.replace(";", ",").split(",")]
            parts = [p for p in parts if p]
            return ", ".join(parts)
        # Fallback to the context zip code if provided
        return context_zip or ""

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        agent_name = raw.get("name") or ""
        website = raw.get("profile_url") or ""
        email = raw.get("email") or ""
        listing_count = raw.get("listing_count") or 0
        sold_count = raw.get("sold_count") or 0
        office_phone = raw.get("office_phone") or ""
        mobile_phones = self._clean_phones(raw.get("mobile_phones_raw"))
        areas_serviced = self._clean_areas(raw.get("areas_serviced_raw"))
        zip_codes_serviced = self._clean_zip_codes(
            raw.get("zip_codes_serviced_raw"),
            raw.get("zip_code_context"),
        )
        office_name = raw.get("office_name") or ""
        company_website = raw.get("company_website")
        review_count = raw.get("review_count") or 0
        photo_url = raw.get("photo_url")

        normalized: Dict[str, Any] = {
            "Agent name": agent_name,
            "Website": website,
            "Email": email,
            "Listing count": int(listing_count),
            "Sold count": int(sold_count),
            "Office Phone": office_phone,
            "Mobile Phones": mobile_phones,
            "Areas serviced": areas_serviced,
            "Zip codes serviced": zip_codes_serviced,
            "Office / Company name": office_name,
            "Company Website": company_website,
            "Review count": int(review_count),
            "Agent Photo": photo_url,
        }
        return normalized