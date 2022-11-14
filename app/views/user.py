from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.crud import user as crud_user
from app.dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud_user.get_user(db, user_id=user.id):
        raise HTTPException(status_code=400, detail="User ID already registered")
    if crud_user.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if crud_user.get_user_by_code_and_phone(db, country_code=user.country_code, phone_number=user.phone_number):
        raise HTTPException(status_code=400, detail="Phone number already registered")

    return crud_user.create_user(db=db, user=user)


@router.get("/", response_model=list[schemas.User], summary="Get users and notifications")
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User, summary="Get user and notifications")
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud_user.delete_user(db, user_id=user_id)
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_in: schemas.UserUpdate, db: Session = Depends(get_db)):
    if not crud_user.get_user(db, user_id=user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if crud_user.get_user_by_email(db, email=user_in.email, user_id=user_id):
        raise HTTPException(status_code=400, detail="Email already registered")
    if crud_user.get_user_by_code_and_phone(
        db,
        country_code=user_in.country_code,
        phone_number=user_in.phone_number,
        user_id=user_id,
    ):
        raise HTTPException(status_code=400, detail="Phone number already registered")

    return crud_user.update_user(db, user_id=user_id, user_in=user_in)


users_router = router
