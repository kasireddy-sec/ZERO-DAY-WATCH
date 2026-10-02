from typing import Literal
from pydantic import BaseModel, Field, HttpUrl

class Evidence(BaseModel):
    source_id: str
    source_name: str
    url: str
    title: str
    observed_at: str
    claim: str
    quote: str = ""
    tier: int = 3
    content_hash: str = ""

class Analysis(BaseModel):
    is_security_issue: bool = False
    title: str = ""
    vendor: str | None = None
    product: str | None = None
    affected_versions: list[str] = []
    cve_ids: list[str] = []
    alternate_ids: list[str] = []
    previously_unknown: bool | None = None
    active_exploitation: bool | None = None
    exploitation_status: Literal["confirmed","reported","none","unknown"] = "unknown"
    poc_available: bool | None = None
    patch_available: bool | None = None
    mitigation_available: bool | None = None
    fixed_versions: list[str] = []
    impact: str = ""
    mitigation: str = ""
    recommended_action: str = ""
    zero_day_candidate: bool = False
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence: list[dict] = []

class Article(BaseModel):
    source_id: str
    source_name: str
    tier: int
    url: str
    title: str
    published: str | None = None
    text: str
    content_hash: str
    links: list[str] = []
