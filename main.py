from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # optional fileds
    rating: Optional[int] = None


# Sample data source for CRUD operations

posts_data = [{
    "Title": "sports",
    "Content": "Cricket, Foot ball, Base Ball",
    "id": 1
}, {
    "Title": "Programming Languages",
    "Content": "Python, Java, C#",
    "id": 2
}]


def find_postById(id):
    '''returns the posts which is found by the id provided'''
    for p in posts_data:
        if p["id"] == id:
            return p


# sample decorator
@app.get('/')
async def root():
    pass


# GET METHODS
@app.get('/posts')
def get_posts():
    '''returns all the posts fom the data source'''
    return {"data": f"{posts_data}"}


@app.get('/posts/latest')
def get_latest_post():
    '''returns latest posts from the data source'''
    post = posts_data[len(posts_data) - 1]  # indexing
    return {"Latest Post": post}


@app.get('/posts/{id}')
def get_postsById(id: int, response: Response):
    '''returns posts based on Id provided'''
    post = find_postById(id)
    # if not post:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"message": f"Post with {id} not found"}
    # else:
    #     return {"Post_detail": f"Post: {post}"}
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} not found")
    return {"Post_detail": f"Post: {post}"}


# POST METHODS
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    '''loads/appends the newly created posts to the data source'''
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000)
    posts_data.append(post_dict)
    # print(post.dict())   for printing in the form of DICT() Format
    return {"new_post": post_dict}