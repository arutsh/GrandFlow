from sqlalchemy.orm import Session
from app.models.mapping import DonorTemplateModel
from app.models.mapping import DonorFieldModel


def create_donor_template(
    session: Session,
    name: str,
) -> DonorTemplateModel:
    """
    Create a donor template.
    """
    donor_template = DonorTemplateModel(name=name)
    session.add(donor_template)
    session.commit()
    session.refresh(donor_template)
    return donor_template


def get_donor_template(session: Session, template_id: int) -> DonorTemplateModel | None:
    return session.query(DonorTemplateModel).filter(DonorTemplateModel.id == template_id).first()


def list_donor_templates(session: Session, limit: int = 100):
    return session.query(DonorTemplateModel).limit(limit).all()


def list_donor_fields(session: Session, template_id: int):
    return (
        session.query(DonorFieldModel)
        .filter(DonorFieldModel.donor_template_id == template_id)
        .all()
    )


def update_donor_template(
    session: Session, template_id: int, name: str
) -> DonorTemplateModel | None:
    existing_template = get_donor_template(session, template_id)
    if not existing_template:
        return None
    existing_template.name = name
    session.commit()
    session.refresh(existing_template)
    return existing_template


def delete_donor_template(session: Session, template_id: int) -> bool:
    template = get_donor_template(session, template_id)
    if template:
        session.delete(template)
        session.commit()
        return True
    return False


def create_donor_field(
    session: Session,
    donor_template_id: int,
    field_name: str,
):

    donor_field = DonorFieldModel(
        donor_template_id=donor_template_id,
        field_name=field_name,
    )
    session.add(donor_field)
    session.commit()
    session.refresh(donor_field)
    return donor_field


def bulk_create_donor_fields(
    session: Session,
    donor_template_id: int,
    field_names: list[str],
):

    donor_fields = [
        DonorFieldModel(
            donor_template_id=donor_template_id,
            field_name=field_name,
        )
        for field_name in field_names
    ]
    session.add_all(donor_fields)
    session.commit()
    for donor_field in donor_fields:
        session.refresh(donor_field)
    return donor_fields
