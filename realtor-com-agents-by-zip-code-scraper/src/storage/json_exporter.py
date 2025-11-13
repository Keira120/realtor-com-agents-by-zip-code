import json
from pathlib import Path
from typing import Any, Dict, List

def export_agents_to_json(agents: List[Dict[str, Any]], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(agents, f, ensure_ascii=False, indent=2)