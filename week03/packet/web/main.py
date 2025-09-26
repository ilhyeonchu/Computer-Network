from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

#데이터 모델

class User(BaseModel):
    username: str
    password: str

class Post(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime

class PostCreate(BaseModel):
    title: str
    content: str
    author: str

# 메모리 저장소
users = []
posts = []
logged_in_users = [] # 현재 로그인한 사용자들

# 기본 페이지

@app.get("/")
def home():
    return {
        "message": "간단한 게시판 API",
        "users" : len(users),
        "posts" : len(posts),
        "online_users": len(logged_in_users)
    }

# 회원가입
@app.post("/register")
def register(user:User):
    # 중복 체크
    for existing_user in users:
        if existing_user["username"] == user.username:
            raise HTTPException(status_code=400, detail= "이미 존재하는 사용자 입니다.")
    
    users.append({"username": user.username, "password": user.password})
    return {"message": f"{user.username}님이 회원가입되었습니다."}

# 로그인
@app.post("/login")
def login(user: User):
    # 사용자 확인
    for existing_user in users:
        if existing_user["username"]== user.username and existing_user["password"] == user.password:
            if user.username not in logged_in_users:
                logged_in_users.append(user.username)
            return {"message": f"{user.username}님이 로그인하셨습니다."}
    raise HTTPException(status_code=401,detail="아이디 또는 비밀번호가 틀렸습니다.")

# 로그아웃
@app.post("/logout/{username}")
def logout(username: str):
    if username in logged_in_users:
        logged_in_users.remove(username)
        return {"message": f"{username}님이 로그아웃하셨습니다."}
    else:
        raise HTTPException(status_code=400, detail="로그인하지 않은 사용자입니다.")
    
# 게시글 목록 조회
@app.get("/posts", response_model=List[Post])
def get_posts():
    return posts

# 게시글 작성
@app.post("/posts")
def create_post(post: PostCreate):
    # 로그인 체크
    if post.author not in logged_in_users:
        raise HTTPException(status_code=401,detail="로그인이 필요합니다.")
    
    new_post= {
        "id":len(posts)+1,
        "title": post.title,
        "content": post.content,
        "author":post.author,
        "created_at": datetime.now()
    }

    posts.append(new_post)
    return {"message": "게시글이 작성되었습니다.", "post": new_post}

# 게시글 조회

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

# 게시글 삭제

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, author: str):
    # 로그인 체크
    if author not in logged_in_users:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    
    for i, post in enumerate(posts):
        if post["id"] == post_id:
            if post["author"] == author:
                deleted_post = posts.pop(i)
                return {"message": f"'{deleted_post['title']}' 게시글이 삭제되었습니다." }
            else:
                raise HTTPException(status_code=403, detail="자신의 게시글만 삭제할 수 있습니다.")
    
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

# 로그인한 사용자 목록
@app.get("/online-users")
def get_online_users():
    return {"online_users": logged_in_users}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)