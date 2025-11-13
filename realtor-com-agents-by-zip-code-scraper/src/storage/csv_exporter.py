import csv
from pathlib import Path
from typing import Any, Dict, Iterable, List

from parsers.agent_normalizer import AgentNormalizer

def _determine_fieldnames(agents: Iterable[Dict[str, Any]]) -> List[str]:
    agents_list = list(agents)
    if not agents_list:
        return []
    preferred_order = AgentNormalizer.FIELD_ORDER
    # Start with preferred order, then append any additional keys
    keys_in_data = set().union(*(a.keys() for a in agents_list))
    fieldnames: List[str] = [f for f in preferred_order if f in keys_in_data]
    for key in sorted(keys_in_data):
        if key not in fieldnames:
            fieldnames.append(key)
    return fieldnames

def export_agents_to_csv(agents: List[Dict[str, Any]], output_path: Path) -> None:
    fieldnames = _determine_fieldnames(agents)
    if not fieldnames:
        raise ValueError("No agents to export.")

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for agent in agents:
            writer.writerow(agent)