from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# from app.db.session import get_db
from app.schemas.mapping_schema import (
    DonorTemplateCreate,
    DonorTemplate,
    DonorFieldCreate,
    DonorField,
    MappingRequest,
    MappingResponse,
    MappingSuggestion,
    NgoMappingCreate,
    NgoMapping,
)
from app.models.mapping import (
    DonorTemplateModel,
    DonorFieldModel,
    NgoMappingModel,
)
from app.services.mapping_service import suggest_mapping
from app.db.session import SessionLocal
from app.utils.security import get_current_user


router = APIRouter(prefix="/donor-mapping", tags=["Donor Mapping"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Templates ---
@router.post("/templates", response_model=DonorTemplate)
def create_template(
    payload: DonorTemplateCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    t = DonorTemplateModel(name=payload.name)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@router.get("/templates", response_model=List[DonorTemplate])
def list_templates(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(DonorTemplateModel).all()


# --- Fields ---
@router.post("/fields", response_model=DonorField)
def create_field(
    payload: DonorFieldCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    template = db.get(DonorTemplateModel, payload.donor_template_id)
    if not template:
        raise HTTPException(404, "Template not found")
    f = DonorFieldModel(**payload.model_dump())
    db.add(f)
    db.commit()
    db.refresh(f)
    return f


@router.get("/fields/{template_id}", response_model=List[DonorField])
def list_fields(template_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(DonorFieldModel).filter(DonorFieldModel.donor_template_id == template_id).all()


# --- AI suggestions ---
@router.post("/suggest", response_model=MappingResponse)
def suggest(payload: MappingRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    donor_fields = (
        db.query(DonorFieldModel.field_name)
        .filter(DonorFieldModel.donor_template_id == payload.donor_template_id)
        .all()
    )
    donor_fields = [row[0] for row in donor_fields]
    suggestions = suggest_mapping(payload.ngo_fields, donor_fields)
    return MappingResponse(suggestions=[MappingSuggestion(**s) for s in suggestions])


# --- Persist mappings ---
@router.post("/mappings", response_model=NgoMapping)
def save_mapping(
    payload: NgoMappingCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    # Optionally verify donor_field_id exists:
    fld = db.get(DonorFieldModel, payload.donor_field_id)
    if not fld:
        raise HTTPException(404, "Donor field not found")

    m = NgoMappingModel(**payload.model_dump())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@router.get("/mappings/by-ngo/{ngo_id}", response_model=List[NgoMapping])
def list_mappings(ngo_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(NgoMappingModel).filter(NgoMappingModel.ngo_id == ngo_id).all()
