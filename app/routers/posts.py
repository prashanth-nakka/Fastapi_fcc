from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, database, OAuth2
from typing import List
'''Post Routes'''

router = APIRouter(prefix='/posts', tags=['Posts'])


# GET METHODS
#'''Get All Posts'''
@router.get('/', response_model=List[schemas.user_response])
def get_posts(db: Session = Depends(database.get_db)):
    '''returns all the posts fom the data source'''
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # return posts
    # return {"data": f"{posts_data}"}
    '''using ORM'''
    try:
        posts = db.query(models.Post).all()
        return posts
    except Exception as err:
        return err


# @router.get('/posts/latest')
# def get_latest_post():
#     '''returns latest posts from the data source'''
#     cursor.execute("""SELECT * FROM posts ORDER BY created_at desc""")
#     latest_post = cursor.fetchone()
#     return {"data": latest_post}


# '''Get Posts by Id'''
@router.get('/{id}', response_model=schemas.user_response)
def get_postsById(id: int,
                  response: Response,
                  db: Session = Depends(database.get_db)):
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
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post: {id} not found")
        return post
    except Exception as err:
        return err


# POST METHODS
# '''Create New Posts'''
@router.post('/posts',
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.user_response)
def create_post(post: schemas.CreatePost,
                db: Session = Depends(database.get_db),
                get_current_user: str = Depends(OAuth2.current_user)):
    '''loads/appends the newly created posts to the data source'''
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
    '''using ORM'''
    try:
        new_post = models.Post(**post.dict())
        db.add(new_post)  # To add a new record to the Data Source
        db.commit()
        db.refresh(
            new_post)  # To display the newly added record/post in Data Source
        return new_post
    except Exception as err:
        return err


# UPDATE METHODS
# '''Updates the existing post by the specified id'''
@router.put('/{id}', response_model=schemas.user_response)
def update_posts(id: int,
                 post: schemas.UpdatePost,
                 db: Session = Depends(database.get_db)):
    '''Updates the existing post by the specified id'''
    # cursor.execute(
    #     """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #     (
    #         post.title,
    #         post.content,
    #         post.published,
    #         str(id),
    #     ))
    # updated_post = cursor.fetchone()
    # # for updating in the Data Source
    # conn.commit()
    '''uisng ORM'''
    try:
        post_query = db.query(models.Post).filter(models.Post.id == id)
        actual_post = post_query.first()
        if not actual_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post: {id} does not exists")
        post_query.update(post.dict(), synchronize_session=False)
        db.commit()
        return post_query.first()
    except Exception as err:
        return err


# DELETE METHODS
# '''Deletes the Posts by the Id provided'''
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(database.get_db)):
    '''Deletes the Posts based on the Id provided'''
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,
    #                (str(id), ))
    # delete_post = cursor.fetchone()
    # # *** Committing the changes to Data Source
    # conn.commit()
    '''using ORM'''
    # query to select 1 record specified by Id from end-user
    try:
        post = db.query(models.Post).filter(models.Post.id == id)
        if not post.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post: {id} does not exists")
        post.delete(synchronize_session=False)
        db.commit()  # To make changes in Data Source
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as err:
        return err