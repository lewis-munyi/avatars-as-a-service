from typing import Any

from sqlalchemy.orm import Session

from avatars_as_a_service.models import Avatar
from avatars_as_a_service.schemas import Avatar as AvatarSchema
from avatars_as_a_service.schemas import (AvatarRequest, AvatarResponse,
                                          AvatarResult)


def search_dall_e(avatar: AvatarSchema, db: Session, cache=True) -> AvatarResult:
    result = avatar.dall_e_search()

    if (
        avatar.description is not None
    ):  # Directly search for description without caching
        return result

    if cache:
        write_to_cache(result, db)

    return result


def write_to_cache(result: AvatarResult, db: Session) -> bool:
    try:
        # existing_model = db.query(Avatar).filter(Avatar.image_hash == result.image_hash).first()
        #
        # if existing_model:  # Item exists
        #     existing_model.delete()

        avatar_model = Avatar(**dict(result))
        db.add(avatar_model)
        db.commit()
    except Exception as e:
        raise RuntimeError("An unexpected DB error occurred: " + str(e))


def search_cache(
    avatar: AvatarSchema, db: Session, skip: int = 0, limit: int = 100
) -> Any:
    return db.query(Avatar).filter(Avatar.image_hash == avatar.hash_avatar()).first()


def avatar_search(request: AvatarRequest, db: Session) -> AvatarResponse:
    search_result: AvatarResult
    cache_hit: bool = False
    prompt: str = request.properties.generate_prompt()

    if request.disable_cache:  # Search dall-e and don't cache the result
        search_result: AvatarResult = search_dall_e(
            avatar=request.properties, db=db, cache=False
        )

    else:  # Search cache
        query_result = search_cache(avatar=request.properties, db=db)
        if (
            query_result is None
        ):  # Cache miss: Browse image and attempt to cache the result
            search_result: AvatarResult = search_dall_e(
                avatar=request.properties, db=db, cache=True
            )
        else:  # Cache hit
            cache_hit: bool = True
            search_result = AvatarResult()
            search_result.image_hash = query_result.image_hash
            search_result.image_url = query_result.image_url

    result = AvatarResponse()
    result.data = search_result
    result.cache_hit = cache_hit
    result.prompt = prompt
    return result
