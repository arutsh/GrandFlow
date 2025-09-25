from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field


# Donor Template Schemas
class DonorTemplateBase(BaseModel):
    name: str = Field(min_length=2)


class DonorTemplateCreate(DonorTemplateBase):
    pass


class DonorTemplate(DonorTemplateBase):
    id: int

    model_config = {"from_attributes": True}


# Donor Field Schemas
class DonorFieldBase(BaseModel):
    donor_template_id: int
    field_name: str = Field(min_length=1)


class DonorFieldCreate(DonorFieldBase):
    pass


class DonorField(DonorFieldBase):
    id: int

    model_config = {"from_attributes": True}


# NGO Mapping Schemas
class MappingSuggestion(BaseModel):
    ngo_field: str
    donor_field: str
    confidence: float


class MappingRequest(BaseModel):
    ngo_fields: List[str]
    donor_template_id: int


class MappingResponse(BaseModel):
    suggestions: List[MappingSuggestion]


class NgoMappingBase(BaseModel):
    ngo_id: str
    ngo_field: str
    donor_field_id: int
    confidence: float


class NgoMappingCreate(NgoMappingBase):
    pass


class NgoMapping(NgoMappingBase):
    id: int

    model_config = {"from_attributes": True}
