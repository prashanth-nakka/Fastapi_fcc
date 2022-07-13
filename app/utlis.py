from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    '''returns hashed password for security purpose'''
    return pwd_context.hash(password)


def verify(password, hashed_password):
    '''converts and verifies the password which is provided
        by the client and which is stored in DB '''
    return pwd_context.verify(password, hashed_password)