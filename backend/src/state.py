from typing import Optional, List
from pydantic import BaseModel, Field


class AppliancePreferences(BaseModel):
    categories: List[str] = Field(default_factory=list)
    budget: Optional[str] = Field(
        default=None,
        description="String representation of budget, e.g. 'under 1000' or 'between 400 and 800'",
    )
    mandatory_filters: List[str] = Field(default_factory=list)
    soft_preferences: List[str] = Field(default_factory=list)
