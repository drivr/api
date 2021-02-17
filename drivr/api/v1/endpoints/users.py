from typing import List, Optional

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from drivr import crud, model, schema
from drivr.api import deps

router = APIRouter()


@router.get(
    "/",
    summary="Get all the registered users.",
    response_model=List[schema.User],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
    db: Session = Depends(deps.db_session),
    _=Depends(deps.get_authenticated_active_user),
):
    """GET method."""

    return crud.users.all(db=db, skip=skip, limit=limit)


@router.post(
    "/",
    summary="Create a new user.",
    status_code=status.HTTP_201_CREATED,
    response_model=schema.User,
    responses={
        409: {"model": schema.Detail},
    },
)
async def create_user(
    schema: schema.UserCreate,
    db: Session = Depends(deps.db_session),
):
    """POST method."""

    if user := crud.users.get_by_email(db=db, email=schema.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The email '{user.email} is alredy registered.",
        )

    return crud.users.create(db=db, schema=schema)


@router.put(
    "/{id}",
    summary="Edit an existing user.",
    status_code=status.HTTP_200_OK,
    response_model=schema.User,
    responses={404: {"model": schema.Detail}},
)
async def edit_user(
    id: int,
    schema: schema.UserUpdate,
    db: Session = Depends(deps.db_session),
    moderator: model.User = Depends(deps.get_authenticated_moderator),
):
    """PUT method."""

    if user := crud.users.get(db=db, id=id):
        return crud.users.update(db=db, user=user, schema=schema)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No user found for the ID provided.",
    )


@router.delete(
    "/{id}",
    summary="Remove an existing user.",
    status_code=status.HTTP_200_OK,
    response_model=schema.User,
)
async def delete_user(
    id: int,
    db: Session = Depends(deps.db_session),
    moderator: model.User = Depends(deps.get_authenticated_moderator),
):
    """DELETE method."""

    if user := crud.users.get(db=db, id=id):
        return crud.users.remove(db=db, model=user)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No user found for the ID provided.",
    )
