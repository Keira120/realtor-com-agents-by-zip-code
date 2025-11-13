from dataclasses import dataclass
from typing import Optional

@dataclass
class PaginationManager:
    """
    Simple helper to decide when to continue paginating.

    This does not rely on site-specific next-page markers; instead, it uses
    generic conditions such as: presence of results and optional max limit.
    """

    min_agents_per_page: int = 1
    max_pages: Optional[int] = 50

    def should_continue(
        self,
        page_number: int,
        agents_on_page: int,
        total_agents: int,
        max_agents: Optional[int],
    ) -> bool:
        if max_agents is not None and total_agents >= max_agents:
            return False
        if agents_on_page < self.min_agents_per_page:
            return False
        if self.max_pages is not None and page_number >= self.max_pages:
            return False
        return True