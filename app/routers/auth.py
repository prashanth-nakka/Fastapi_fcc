from email import utils
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import OAuth2, schemas, models, database, utlis
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['User Login'])


@router.post('/login')
def UserLogin(user_credentials: OAuth2PasswordRequestForm = Depends(),
              db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    if not utlis.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    # return a token
    access_token = OAuth2.create_access_token(data={'user_id': user.id})
    return {"access_token": access_token, "token_type": "bearer"}
