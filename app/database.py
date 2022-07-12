from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db" # for SQLITE DB

# formats for connection string,
# SQLALCHEMY_DATABASE_URL = "postgresql://<user>:<password>@<ip-address/host_name>/<db_name>"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# To Talk to DB we need session_maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Sql Alchemy Dependency
def get_db():
    db = SessionLocal()
    # Generator
    try:
        yield db
    finally:
        db.close()
