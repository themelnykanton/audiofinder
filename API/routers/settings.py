from fastapi import Depends, APIRouter, Security

from API.request_bodies import fake_db
from API.routers.auth import User, get_current_active_user

router = APIRouter(
    prefix="/settings",
    tags=["settings"],
    responses={404: {"description": "Not found"}},
    dependencies=[Security(get_current_active_user)]
)


@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "FakeSettings", "owner": current_user.username}]


@router.get('/languages/')
async def get_available_languages():
    return fake_db
