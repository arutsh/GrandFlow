from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


class DonorTemplateCreate(BaseModel):
    name: str = Field(min_length=2)


class DonorTemplate(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class DonorFieldCreate(BaseModel):
    donor_template_id: int
    field_name: str = Field(min_length=1)


class DonorField(BaseModel):
    id: int
    donor_template_id: int
    field_name: str

    model_config = {"from_attributes": True}


class MappingSuggestion(BaseModel):
    ngo_field: str
    donor_field: str
    confidence: float


class MappingRequest(BaseModel):
    ngo_fields: List[str]
    donor_template_id: int


class MappingResponse(BaseModel):
    suggestions: List[MappingSuggestion]


class NgoMappingCreate(BaseModel):
    ngo_id: str
    ngo_field: str
    donor_field_id: int
    confidence: float


class NgoMapping(BaseModel):
    id: int
    ngo_id: str
    ngo_field: str
    donor_field_id: int
    confidence: float

    model_config = {"from_attributes": True}
