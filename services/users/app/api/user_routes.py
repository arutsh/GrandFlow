from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4, UUID
from app.schemas.user_schema import User, UserCreate, UserUpdate
from app.models.user import UserModel
from app.models.customer import CustomerModel
from app.db.session import SessionLocal
from app.utils.security import get_current_user
from app.crud.user_crud import get_users_query, is_superuser, update_user, get_user
from app.crud.customer_crud import create_customer, get_customer
from app.utils.dict_tools import filter_dict_keys
from app.services.event_publisher import get_publisher
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=User)
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    if user.customer_id:
        customer = db.query(CustomerModel).filter(CustomerModel.id == user.customer_id).first()
        if not customer:
            raise HTTPException(status_code=400, detail="Invalid customer_id")

    db_user = UserModel(id=str(uuid4()), **user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    try:
        publisher = get_publisher()
        await publisher.publish(
            "user.created",
            {
                "user_id": str(db_user.id),
                "email": db_user.email,
                "first_name": db_user.first_name,
                "last_name": db_user.last_name,
                "status": db_user.status,
                "customer_id": str(db_user.customer_id) if db_user.customer_id else None,
                "role": db_user.role,
            },
        )
    except Exception as e:
        logger.error("user_created_event_failed", user_id=str(db_user.id), error=str(e))

    return db_user


@router.get("/users/{user_id}", response_model=User)
def get_user_endpoint(user_id: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/", response_model=list[User])
def list_users_endpoint(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Only superuser can list all users

    users = get_users_query(db)
    current_user = users.filter(UserModel.id == current_user["user_id"]).first()
    if current_user.role != "superuser":
        raise HTTPException(status_code=403, detail="Not authorized to list users")

    return users.all()


@router.post("/users/by_ids/", response_model=list[User])
def get_users_by_ids_endpoint(
    user_ids: list[UUID],
    db: Session = Depends(get_db),
):
    # NOTE: this end point is for internal service use only,
    # hence no need to check current_user permissions
    # calling service should ensure proper authorization

    return get_users_query(db, user_ids).all()


@router.patch("/users/{user_id}/", response_model=User)
async def update_user_endpoint(
    user_id: UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    is_current_user_superuser = is_superuser(db, current_user["user_id"])

    if current_user["user_id"] != user_id and not is_current_user_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")

    db_user = get_user(db, user_id)
    current_user = get_user(db, current_user["user_id"])
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    allowed_fields = set()
    if is_current_user_superuser:
        allowed_fields = {"first_name", "last_name", "email", "status", "customer_id", "role"}
    else:
        allowed_fields = {"first_name", "last_name", "password", "status"}

    update_data = user_update.model_dump(exclude_unset=True)
    customer = None
    if (
        not is_current_user_superuser
        and user_update.new_customer_name
        and db_user.status == "pending"
    ):
        customer = create_customer(db, user_update.new_customer_name)
        update_data["status"] = "active"

    elif user_update.customer_id:
        customer = get_customer(session=db, customer_id=user_update.customer_id)
        if not customer:
            raise HTTPException(status_code=400, detail="Invalid customer_id")

    filtered_update_data = filter_dict_keys(update_data, allowed_fields)
    filtered_update_data["customer_id"] = customer.id if customer else None
    update_user(db, db_user, filtered_update_data)

    try:
        publisher = get_publisher()
        await publisher.publish(
            "user.updated",
            {
                "user_id": str(db_user.id),
                "email": db_user.email,
                "first_name": db_user.first_name,
                "last_name": db_user.last_name,
                "status": db_user.status,
                "customer_id": str(db_user.customer_id) if db_user.customer_id else None,
                "role": db_user.role,
            },
        )
    except Exception as e:
        logger.error("user_updated_event_failed", user_id=str(db_user.id), error=str(e))

    return db_user
