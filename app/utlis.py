from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    '''returns hashed password for security purpose'''
    return pwd_context.hash(password)