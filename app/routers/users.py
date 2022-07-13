from typing import List
from fastapi import Depends, status, HTTPException, APIRouter
from .. import models, schemas, utlis, database
from sqlalchemy.orm import Session
'''USER MODULE'''
router = APIRouter()


# '''Creates New User'''
@router.post('/users',
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,
                db: Session = Depends(database.get_db)):
    '''Creates New User'''
    # hashed password = user.password
    hashed_password = utlis.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get All Users
@router.get('/users', response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


# '''Gets user details by the Id provided'''
@router.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    '''Gets user details by the Id provided'''
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id} user not found")
    return user
