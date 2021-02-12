from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/",
    summary="Get all the registered users.",
)
async def get_users():
    ...


@router.post(
    "/",
    summary="Create a new user.",
)
async def create_user():
    ...


@router.put(
    "/",
    summary="Edit an existing user.",
)
async def edit_user():
    ...


@router.delete(
    "/",
    summary="Remove an existing user.",
)
async def delete_user():
    ...
