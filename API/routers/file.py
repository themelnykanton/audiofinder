# -*- coding: utf-8 -*-
import os
import time
from fastapi import APIRouter, Depends, Form
from fastapi import FastAPI, File, UploadFile, Security
import hashlib

from starlette.concurrency import run_in_threadpool

from API.routers.auth import get_current_active_user
from analyser import analyser
from API.request_bodies import Language


router = APIRouter(
    prefix="/analyser",
    tags=["analyser"],
    responses={404: {"description": "Not found"}},
    dependencies=[Security(get_current_active_user)]
)


@router.post("/audio_text")
async def create_upload_file(language: Language = Depends(), file: UploadFile = File(...)):
    file_name = hashlib.md5(str(time.time()).encode()).hexdigest()
    with open(rf'Resource\{file_name}.mp3', 'wb+') as f:
        f.write(file.file.read())
        f.close()

    text = await run_in_threadpool(lambda: analyser(f'{file_name}', language=language.language))
    await run_in_threadpool(lambda: os.remove(rf'Resource\{file_name}.mp3'))
    await run_in_threadpool(lambda: os.remove(rf'Resource\{file_name}.wav'))

    return text
