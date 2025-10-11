from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.user_schema import User, UserUpdate
from app.models.user import UserModel
from app.db.session import SessionLocal
from app.utils.security import get_current_user
from app.crud.user_crud import get_users_query, is_superuser, update_user, get_user
from app.crud.customer_crud import create_customer, get_customer
from app.utils.dict_tools import filter_dict_keys

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users/{user_id}", response_model=User)
def get_user_endpoint(
    user_id: UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):

    if user_id == current_user["user_id"] or is_superuser(db, current_user["user_id"]):
        return get_user(db, user_id)

    raise HTTPException(status_code=404, detail="User not found or you do not have access")


@router.get("/users/", response_model=list[User])
def list_users_endpoint(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Only superuser can list all users

    users = get_users_query(db)
    current_user = users.filter(UserModel.id == current_user["user_id"]).first()
    if current_user.role != "superuser":
        raise HTTPException(status_code=403, detail="Not authorized to list users")

    return users.all()


@router.patch("/users/{user_id}/", response_model=User)
def update_user_endpoint(
    user_id: UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    is_current_user_superuser = is_superuser(db, current_user["user_id"])

    # Only superuser or self can update
    # TODO add user Customer role, so the user can update users within the same customer
    if current_user["user_id"] != user_id and not is_current_user_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")

    db_user = get_user(db, user_id)
    current_user = get_user(db, current_user["user_id"])
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Field-level restrictions
    allowed_fields = set()
    if is_current_user_superuser:
        allowed_fields = {"first_name", "last_name", "email", "status", "customer_id", "role"}
    else:
        # Normal user: only allow basic profile fields
        allowed_fields = {"first_name", "last_name", "password", "status"}

    update_data = user_update.model_dump(exclude_unset=True)
    customer = None
    # if new customer name is provided, create new customer and user is not superuser
    # super user cannot have customers
    if (
        not is_current_user_superuser
        and user_update.new_customer_name
        and db_user.status == "pending"
    ):
        customer = create_customer(db, user_update.new_customer_name)
        update_data["status"] = "active"  # activate user when creating customer

    # Ensure customer exists
    elif user_update.customer_id:
        customer = get_customer(session=db, customer_id=user_update.customer_id)
        if not customer:
            raise HTTPException(status_code=400, detail="Invalid customer_id")

    filtered_update_data = filter_dict_keys(update_data, allowed_fields)
    filtered_update_data["customer_id"] = customer.id if customer else None
    update_user(db, db_user, filtered_update_data)

    return db_user
