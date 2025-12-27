from sqlalchemy.orm import Session
from uuid import UUID
from app.models.mapping import SemanticFieldMappingModel


def list_semantic_field_mappings(
    session: Session,
    ids: list[UUID] | None = None,
    limit: int = 100,
):
    query = session.query(SemanticFieldMappingModel)
    if ids:
        query = query.filter(SemanticFieldMappingModel.id.in_(ids))
    return query.limit(limit).all()


def create_semantic_field_mapping(
    session: Session,
    user_id: UUID,
    raw_value: str,
    mapped_to: str,
    source: str,
    confindence: float | None = None,
    meta_data: dict | None = None,
) -> SemanticFieldMappingModel:
    """
    Create a semantic field mapping.
    """

    mapping = SemanticFieldMappingModel(
        raw_value=raw_value,
        mapped_to=mapped_to,
        mapped_key=mapped_to,
        source=source,
        confidence=confindence,
        meta_data=meta_data,
        created_by=user_id,
        updated_by=user_id,
    )
    session.add(mapping)
    session.commit()
    session.refresh(mapping)
    return mapping


def bulk_create_semantic_field_mappings(
    session: Session,
    user_id: UUID,
    mappings: list[dict],
) -> list[SemanticFieldMappingModel]:
    """
    Bulk create semantic field mappings.
    """

    mapping_models = [
        SemanticFieldMappingModel(
            raw_value=mapping["raw_value"],
            normalized_value=mapping["normalized_value"],
            mapped_to=mapping["mapped_to"],
            mapped_key=mapping["mapped_key"] or "",
            source=mapping["source"],
            confidence=mapping.get("confidence"),
            meta_data=mapping.get("meta_data"),
            created_by=user_id,
            updated_by=user_id,
        )
        for mapping in mappings
    ]
    # Use add_all so SQLAlchemy tracks the instances in the session
    # (bulk_save_objects bypasses the unit-of-work and leaves instances
    # in a non-persistent state, which makes session.refresh() fail).
    session.add_all(mapping_models)
    session.commit()

    # Now refresh to populate defaults (like server-generated PKs)
    for mapping in mapping_models:
        session.refresh(mapping)
    return mapping_models


def update_semantic_field_mapping(
    session: Session,
    existing_mapping: SemanticFieldMappingModel,
    new_raw_value: str | None = None,
    new_mapped_to: str | None = None,
    new_confidence: float | None = None,
    new_meta_data: dict | None = None,
) -> SemanticFieldMappingModel | None:
    if new_raw_value is not None:
        existing_mapping.raw_value = new_raw_value
    if new_mapped_to is not None:
        existing_mapping.mapped_to = new_mapped_to
    if new_confidence is not None:
        existing_mapping.confidence_score = new_confidence
    if new_meta_data is not None:
        existing_mapping.meta_data = {
            **(existing_mapping.meta_data or {}),
            **new_meta_data,
        }
    session.commit()
    session.refresh(existing_mapping)
    return existing_mapping


def delete_semantic_field_mapping(session: Session, mapping: SemanticFieldMappingModel) -> bool:
    session.delete(mapping)
    session.commit()
    return True
