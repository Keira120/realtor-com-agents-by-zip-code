from typing import Any, Dict, Iterable, List, Optional

from parsers.agent_normalizer import AgentNormalizer

class AgentExtractor:
    """
    High-level orchestrator that calls the Realtor client and normalizes output
    into the final agent schema.
    """

    def __init__(self, client: Any, logger: Any) -> None:
        self.client = client
        self.logger = logger

    def extract_for_zip_codes(
        self,
        zip_codes: Iterable[str],
        max_per_zip: Optional[int] = None,
        trial_limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        all_agents: List[Dict[str, Any]] = []
        normalizer = AgentNormalizer()

        remaining_trial = trial_limit

        for zip_code in zip_codes:
            if remaining_trial is not None and remaining_trial <= 0:
                self.logger.info(
                    "Trial limit reached, stopping before zip %s", zip_code
                )
                break

            self.logger.info("Processing zip code %s", zip_code)
            raw_agents = self.client.search_agents_by_zip(
                zip_code=zip_code,
                max_records=max_per_zip,
            )

            for raw in raw_agents:
                normalized = normalizer.normalize(raw)
                all_agents.append(normalized)
                if remaining_trial is not None:
                    remaining_trial -= 1
                    if remaining_trial <= 0:
                        self.logger.info(
                            "Trial limit reached after zip %s (%d agents total)",
                            zip_code,
                            len(all_agents),
                        )
                        return all_agents

        return all_agents