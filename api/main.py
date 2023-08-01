from typing import Union
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from src.object_pdf import Pseudo_pdf
import aiofiles
from fastapi.responses import FileResponse
from random import randint
import os
from pydantic import BaseModel
from typing import Annotated

""" 
    This script creates the API needed to pseudonymize a pdf file.
    Command to run uvicorn API : "uvicorn api.main:app --reload"
"""

app = FastAPI()
db = {}

origins = [
    "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def remove_file(path: str) -> None:
    os.unlink(path)


@app.post("/upload-pdf/")
async def upload_script(
    background_tasks: BackgroundTasks,
    LOC: bool = Form(True),
    PER: bool = Form(True),
    file: UploadFile = File(...),
):
    """
    This POST method receives a pdf file and saves the pseudonymized version in the db.
    input :
    background_tasks : is used by FastAPI to do tasks after the return
    LOC : bool, indicates whether or not locations should be pseudonymized
    PER : bool, indicates whether or not people's names should be pseudonymized
    file : UploadFile to upload a pdf file
    """
    params = {"LOC": LOC, "PER": PER}
    if file:
        filename = str(randint(0, 1000000)) + ".pdf"
        file_path = "data/" + filename
        output_path = file_path[:-4] + "update.pdf"
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write
        background_tasks.add_task(remove_file, file_path)
        background_tasks.add_task(remove_file, output_path)
        try:
            object = Pseudo_pdf(file_path, output_path, as_image=True, params=params)
            object.load_file_save()
            return FileResponse(output_path)
        except:
            return {
                "message": "There was an error pseudonymizing the file. Deleting file from database."
            }
    else:
        return {"message": "There was an error uploading the file {}".format(filename)}
