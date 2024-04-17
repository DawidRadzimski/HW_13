from fastapi import APIRouter, Depends, status, UploadFile, File
import pickle
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from part_1.src.database.db import get_db
from part_1.src.database.models import User
from part_1.src.repository import users as repository_users
from part_1.src.services.auth import auth_service, Auth
from part_1.src.conf.config import settings
from part_1.src.schemas import UserDb

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user


@router.patch("/avatar", response_model=UserDb)
async def update_avatar_user(
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    cloudinary.uploader.upload(
        file.file, public_id=f"ContactsApp/{current_user.username}", overwrite=True
    )
    src_url = cloudinary.CloudinaryImage(f"ContactsApp/{current_user.username}").build_url(
        width=250, height=250, crop="fill"
    )
    user = await repository_users.update_avatar(current_user.username, src_url, db)
    Auth.r.set(f"user:{user.username}", pickle.dumps(user))
    return user