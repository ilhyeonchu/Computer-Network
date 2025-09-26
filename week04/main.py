from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()

db = []


class Paste(BaseModel):
    content: str


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/paste/{paste_id}")
def get_paste(paste_id: int):
    if paste_id < len(db):
        return {"paste_id": paste_id, "paste": db[paste_id]}
    else:
        return {"paste_id": paste_id, "paste": None}


@app.post("/paste/")
def post_paste(paste: Paste):
    db.append(paste)
    paste_id = len(db) - 1
    return {"paste_id": paste_id, "paste": db[paste_id]}


# 글을 삭제하더라도 db의 길이나 paste_id를 줄이지 않고
# 이 두 값은 계속 선형적으로 증가하므로 id의 값보다 db의 길이가
# 무조건 같거나 더 크므로 그걸 기준으로 글이 있는지 판단
@app.put("/paste/{paste_id}")
def put_paste(paste_id: int, paste: Paste):
    if paste_id < len(db):  # db의 길이보다 id의 값이 작으므로 글이 존재
        db[paste_id] = paste  # 글의 내용을 입력 받은 내용인 paste: Paste로 수정
        return {"paste_id": paste_id, "paste": db[paste_id]}
    else:
        # post_paste(paste)
        return "None"  # db의 길이보다 id의 값이 크므로 글이 없고 "None" return


# 글을 삭제
# put과 같은 방법으로 글의 존재 유무를 확인
# 완벽한 삭제가 아닌 기존의 글을 "None"으로 변경
# 실제로는 id의 값이나 db의 길이에 변화가 없음
@app.delete("/paste/{paste_id}")
def delete_paste(paste_id: int, response: Response):
    if paste_id < len(db):  # 글이 존재
        db[paste_id] = "None"  # 글의 내용을 "None"으로 변경
        response.status_code = 200  # 성공했으니 응답으로 200을 보냄
    else:  # 글이 존재하지 않음
        response.status_code = 404  # 오류이므로 응답으로 404을 보냄
        return "None"  # "None" 반환
