# from typing import Optional
# from random import randrange
# from typing import List
# from .utlis import hash
# from .schemas import *
# from sqlalchemy.orm import Session
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import posts, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Data base Connection (Postgres)
# Connection String => conn = psycopg2.connect(host, database, user, password)
while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi',
                                user='postgres',
                                password='12345',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connected!")
        break
    except Exception as error:
        print("Connecting to Database Failed!")
        print("Error was ", error)
        time.sleep(2)

# Routers
'''importing posts routers'''
app.include_router(posts.router)
'''importing users routers'''
app.include_router(users.router)

#--------------------------------Commented Code-----------------------------------------
# Sample data source for CRUD operations

# posts_data = [{
#     "title": "Sports",
#     "content": "Cricket, Foot ball, Base Ball",
#     "id": 1
# }, {
#     "title": "Programming Languages",
#     "content": "Python, Java, C#",
#     "id": 2
# }, {
#     "title": "Food",
#     "content": "Pizza, Biryani, Tandoori",
#     "id": 3
# }]

# def find_postById(id):
#     '''returns the posts which is found by the id provided'''
#     for p in posts_data:
#         if p["id"] == id:
#             return p

# def find_index_id(id):
#     '''returns index of the posts if id == posts['id']'''
#     for i, p in enumerate(posts_data):
#         if p['id'] == id:
#             return i

# sample decorator
# @app.get('/')
# async def root():
#     pass

# Testing_route(sqlalchemy)
# @app.get('/sqlalchemy')
# def test_db(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}
