from fastapi import FastAPI
from avatars_as_a_service.schemas import AvatarRequest, AvatarResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.post("/query")
def search(req: AvatarRequest) -> AvatarResponse:
    avatar = req.properties

    res = AvatarResponse()
    res.data = avatar.dall_e_2_search()  # Get OpenAi Payload Image URL
    res.prompt = avatar.generate_prompt()

    return res