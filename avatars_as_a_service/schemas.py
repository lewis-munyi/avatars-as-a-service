import os

from typing import Union
from openai import OpenAI
from pydantic import BaseModel

from avatars_as_a_service.enums.AvatarFeatures import (
    Mood,
    HeadShape,
    EyeColor,
    SkinTone,
    SmileType,
    NoseType,
)


class Avatar(BaseModel):
    skin_tone: SkinTone | None
    head_shape: HeadShape | None = None
    eye_color: EyeColor | None = None
    smile_type: SmileType | None = None
    nose_type: NoseType | None = None
    glasses: bool | None = False
    mood: Mood | None = Mood.FUN
    description: str | None = None

    # Method used to generate a prompt string from the various properties supplied
    def generate_prompt(self) -> str:
        if self.description and self.description != "":
            # If a description is provided then it will override the other Avatar properties
            return self.description

        prompt = "create an avatar for a person with the following description: "

        if self.skin_tone:
            prompt += f"{self.skin_tone.value} skin color/complexion, "

        if self.head_shape:
            prompt += f"a {self.head_shape.value} head, "

        if self.eye_color:
            prompt += f"{self.eye_color.value} eyes, "

        if self.smile_type:
            prompt += f"a {self.smile_type.value} smile, "

        if self.nose_type:
            prompt += f"a {self.nose_type.value} nose, "

        if self.glasses:
            prompt += "and with a pair of glasses, "

        if self.mood:
            if self.mood.value == "fun":
                prompt += "and make it fun and/or cartoon-y."
            else:
                prompt += "and make it official and/or office appropriate."

        return prompt

    # TODO: remove this from Avatar class and make it a util
    def dall_e_2_search(self):
        try:
            print("api key:")
            print(os.getenv("OPENAI_API_KEY"))
            client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
            )
            response = client.images.generate(
                model="dall-e-2",
                prompt=self.generate_prompt(),
                size="256x256",
                quality="standard",
                n=1,
            )

            res = AvatarResult()
            res.image_url = response.data[0].url
            res.image_hash = self.hash_avatar()
            return res
        # TODO: raise Exception
        except Exception as e:
            print(str(e))

    def hash_avatar(self) -> str:
        if self.description:
            return ""

        features = (
            f"{self.head_shape}+{self.eye_color}+{self.skin_tone}+{self.glasses}+"
        )
        f"{self.smile_type}+{self.nose_type}+{self.mood}"
        return str(hash(features))


class AvatarResult(BaseModel):
    image_url: str = None
    image_hash: str = None


class AvatarRequest(BaseModel):
    properties: Avatar
    disable_cache: bool = True


class AvatarResponse(BaseModel):
    data: AvatarResult = None
    prompt: str = None
    cache_hit: bool = False
