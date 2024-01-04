from fastapi import FastAPI, Depends
from avatars_as_a_service.database.connection import get_db
from avatars_as_a_service.search import avatar_search
from avatars_as_a_service.schemas import AvatarRequest, AvatarResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/query")
def search(req: AvatarRequest, db: Depends(get_db)) -> AvatarResponse:
    return avatar_search(request=req, db=db)