from fastapi import FastAPI
from avatars_as_a_service.search import avatar_search
from avatars_as_a_service.schemas import AvatarRequest, AvatarResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/query")
def search(req: AvatarRequest) -> AvatarResponse:
    return avatar_search(request=req)