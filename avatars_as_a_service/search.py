from sqlalchemy.orm import Session

from avatars_as_a_service.models import Avatar
from avatars_as_a_service.schemas import Avatar as AvatarSchema, AvatarResult, AvatarRequest, AvatarResponse


def search_dall_e(avatar: AvatarSchema, cache=True) -> AvatarResult:
    result = avatar.dall_e_2_search()

    if avatar.description is not None:  # Directly search for description without caching
        return result

    if cache:
        if not write_to_cache(result):
            print("Unable to cache result")

    return result

def write_to_cache(result: AvatarResult) -> bool:
    # Todo: Attempt to write result to cache
    # This method should write an Avatar model to the table. It takes an AvatarResult object nad returns tru if it writes it
    # successfully and false if it does not
    # Find the DB design here: https://lewismunyi.hashnode.dev/preview/658af8db7aed99cfccfa584f#heading-enhanced-database-design
    try:
        pass
    except:
        print("Error accessing the DB")

    return False


def search_cache(avatar: AvatarSchema, db: Session, skip: int = 0, limit: int = 100) -> AvatarResult or None:
    # Todo: Search cache and convert to AvatarResult or None object
    # This function should get an AvatarSchema object and search for its hash = avatar.hash_avatar() in the database/aaas.sqlite.db database.
    # If found, it should get the record and generate an AvatarResult object(id, created_at, image_hash, image_url), else it should return null
    # Find the DB design here: https://lewismunyi.hashnode.dev/preview/658af8db7aed99cfccfa584f#heading-enhanced-database-design
    print(db.query(Avatar).offset(skip).limit(limit).all())
    return None


def avatar_search(request: AvatarRequest) -> AvatarResponse:
    search_result: AvatarResult
    cache_hit: bool = False                                           # Only true if a query is returned from the DB not OpenAI
    prompt: str = request.properties.generate_prompt()

    if request.disable_cache:  # Search Dall-e
        search_result = search_dall_e(avatar=request.properties, cache=False)  # Search dall-e and don't cache the result

    else:  # Search cache
        query_result = search_cache(avatar=request.properties)
        if query_result is None:                                      # Cache miss
            search_result = search_dall_e(avatar=request.properties)  # Browse image and attempt to cache the result
        else:                                                         # Cache hit
            cache_hit = True
            search_result = query_result

    result = AvatarResponse()
    result.data = search_result
    result.cache_hit = cache_hit
    result.prompt = prompt
    return result