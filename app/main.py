# from typing import Optional
# from random import randrange
from fastapi import Depends, FastAPI, Response, status, HTTPException
import psycopg2
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

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


# Schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # optional fileds
    # rating: Optional[int] = None


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
@app.get('/')
async def root():
    pass


# Testing_route(sqlalchemy)
# @app.get('/sqlalchemy')
# def test_db(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}


# GET METHODS
@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    '''returns all the posts fom the data source'''
    '''using ORM'''
    try:
        posts = db.query(models.Post).all()
        return posts
    except Exception as err:
        return err
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # return posts
    # return {"data": f"{posts_data}"}


# UPDATE METHODS
@app.put('/posts/{id}')
def update_posts(id: int, post: Post):
    '''Updates the existing post by the specified id'''
    cursor.execute(
        """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
        (
            post.title,
            post.content,
            post.published,
            str(id),
        ))
    updated_post = cursor.fetchone()
    # for updating in the Data Source
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post: {id} does not exists")
    return {"data": updated_post}


@app.get('/posts/latest')
def get_latest_post():
    '''returns latest posts from the data source'''
    cursor.execute("""SELECT * FROM posts ORDER BY created_at desc""")
    latest_post = cursor.fetchone()
    return {"data": latest_post}


@app.get('/posts/{id}')
def get_postsById(id: int, response: Response, db: Session = Depends(get_db)):
    '''returns posts based on Id provided'''
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id), ))
    # post = cursor.fetchone()
    # print(post_test)
    # post = find_postById(id)
    # if not post:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"message": f"Post with {id} not found"}
    # else:
    #     return {"Post_detail": f"Post: {post}"}
    '''using ORM'''
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post: {id} not found")
    return {"Post_detail": {post}}


# POST METHODS
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    '''loads/appends the newly created posts to the data source'''
    '''using ORM'''
    new_post = models.Post(**post.dict())
    db.add(new_post)  # To add a new record to the Data Source
    db.commit()
    db.refresh(
        new_post)  # To display the newly added record/post in Data Source
    return {"data": new_post}
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published))
    # # for returning only one record which we created
    # new_post = cursor.fetchone()
    # # for pushing the new changes to the data source, for saving the created post
    # conn.commit()
    # return {"data": new_post}
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 10000)
    # posts_data.append(post_dict)
    # # print(post.dict())   for printing in the form of DICT() Format
    # return {"new_post": post_dict}


# DELETE METHODS
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    '''Deletes the Posts based on the Id provided'''
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,
                   (str(id), ))
    delete_post = cursor.fetchone()
    # *** Committing the changes to Data Source
    conn.commit()
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post: {id} does not exists")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
