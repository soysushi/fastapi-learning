from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()


#creating what a post model will look like

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

#saving the posts in a dictionary

my_posts = [{"title": "title of post1", "content": "content of post 1", "id": 1}, 
            {"title": "favourite foods", "content": "chips, steak, lobster", "id": 2}]

def find_post(id):
    for p in my_posts: 
        if p["id"] == id:
            return p

def find_index_post(id):
    for index, p in enumerate(my_posts):
        if p['id'] == id:
            return index

@app.get("/")
def root():
    return {"message": "Welcome to my api"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts} #auto serialize to json

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post_variable: Post): # pydantic will validate based on Post
    post_dict = post_variable.dict()
    post_dict['id'] = randrange(0, 10000000000)
    my_posts.append(post_dict)
    return {"data": my_posts}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id: {id} was not found"}
    return{"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting a post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exists")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exists")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}