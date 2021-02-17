from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from drivr import crud, schema, security
from drivr.api import deps

router = APIRouter()


@router.post(
    "/",
    summary="Authenticate the user",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": schema.Token},
        400: {"model": schema.Detail},
    },
)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(deps.db_session),
):
    """Authenticate and create the access token."""

    user = crud.users.authenticate(
        db=db,
        email=form.username,
        password=form.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password.",
        )

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user.",
        )

    return {
        "access_token": security.create_access_token(subject=user.id),
        "token_type": "bearer",
    }
