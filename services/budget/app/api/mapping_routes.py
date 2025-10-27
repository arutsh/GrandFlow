from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
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
from app.crud.budget_donor_template_crud import (
    bulk_create_donor_fields,
    create_donor_template,
    get_donor_template,
    list_donor_templates,
    create_donor_field,
    list_donor_fields,
)
from app.schemas.budget_line_schema import BudgetCategoryCreate, BudgetCategory
from app.crud.budget_category_crud import create_budget_category, list_budget_categories
from app.services.user_client import (
    get_valid_user,
)
from app.core.exceptions import DomainError

router = APIRouter(prefix="/donor-mapping", tags=["Donor Mapping"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_validated_user(user=Depends(get_current_user)):
    """
    FastAPI dependency that validates the user and returns the user object.
    Raises DomainError if validation fails.
    """
    try:
        return get_valid_user(user["user_id"], user["token"])
    except ValueError as e:
        raise DomainError(str(e))


# --- Templates ---
@router.post("/templates", response_model=DonorTemplate)
def create_template(
    payload: DonorTemplateCreate,
    db: Session = Depends(get_db),
    valid_user=Depends(get_validated_user),
):
    return create_donor_template(db, payload)


@router.get("/templates", response_model=List[DonorTemplate])
def list_templates(db: Session = Depends(get_db), valid_user=Depends(get_validated_user)):
    return list_donor_templates(db)


# --- Fields ---
@router.post("/fields", response_model=DonorField)
def create_field(
    payload: DonorFieldCreate, db: Session = Depends(get_db), valid_user=Depends(get_validated_user)
):
    template = get_donor_template(db, payload.donor_template_id)
    if not template:
        raise HTTPException(404, "Template not found")
    return create_donor_field(db, payload.donor_template_id, payload.field_name)


@router.post("/fields/bulk", response_model=List[DonorField])
def bulk_create_field_endpoint(
    template_id: int,
    field_names: List[str],
    db: Session = Depends(get_db),
    valid_user=Depends(get_validated_user),
):
    template = get_donor_template(db, template_id)
    if not template:
        raise HTTPException(404, "Template not found")
    return bulk_create_donor_fields(db, template_id, field_names)


@router.post("/categories", response_model=BudgetCategory)
def create_budget_category_endpoint(
    payload: BudgetCategoryCreate,
    db: Session = Depends(get_db),
    valid_user=Depends(get_validated_user),
):
    return create_budget_category(
        db,
        user_id=valid_user["id"],
        name=payload.name,
        code=payload.code,
        donor_template_id=payload.donor_template_id,
    )


@router.get("/categories", response_model=List[BudgetCategory])
def list_budget_categories_view(
    db: Session = Depends(get_db), valid_user=Depends(get_validated_user)
):
    return list_budget_categories(db)


@router.get("/categories/{template_id}", response_model=List[BudgetCategory])
def list_budget_categories_by_template(
    template_id: int, db: Session = Depends(get_db), valid_user=Depends(get_validated_user)
):
    return list_budget_categories(db, template_id)


@router.get("/fields/{template_id}", response_model=List[DonorField])
def list_fields(
    template_id: int, db: Session = Depends(get_db), valid_user=Depends(get_validated_user)
):
    return list_donor_fields(db, template_id)


# --- AI suggestions ---
@router.post("/suggest", response_model=MappingResponse)
def suggest(
    payload: MappingRequest, db: Session = Depends(get_db), valid_user=Depends(get_validated_user)
):
    donor_fields = list(
        db.execute(
            select(DonorFieldModel.field_name).where(
                DonorFieldModel.donor_template_id == payload.donor_template_id
            )
        )
        .scalars()
        .all()
    )
    # donor_fields = [row[0] for row in donor_fields]
    suggestions = suggest_mapping(payload.ngo_fields, donor_fields)
    return MappingResponse(suggestions=[MappingSuggestion(**s) for s in suggestions])


# --- Persist mappings ---
@router.post("/mappings", response_model=NgoMapping)
def save_mapping(
    payload: NgoMappingCreate, db: Session = Depends(get_db), valid_user=Depends(get_validated_user)
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
def list_mappings(
    ngo_id: str, db: Session = Depends(get_db), valid_user=Depends(get_validated_user)
):
    return db.query(NgoMappingModel).filter(NgoMappingModel.ngo_id == ngo_id).all()
