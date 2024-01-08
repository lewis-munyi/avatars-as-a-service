from fastapi import FastAPI, Depends
from avatars_as_a_service.database.connection import get_db, init_db
from avatars_as_a_service.search import avatar_search
from avatars_as_a_service.schemas import AvatarRequest, AvatarResponse
from sqlalchemy.orm import Session

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/query")
def search(req: AvatarRequest, db: Session = Depends(get_db)) -> AvatarResponse:
    return avatar_search(request=req, db=db)