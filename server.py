
from fastapi import FastAPI,Form,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
import uvicorn
client = MongoClient('mongodb://localhost:27017/')
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )
@app.get('/')
async def get():
    return {'200' : "Success"}

@app.post('/timesheetupload')
async def timesheetupload(empid:str =Form(), file : UploadFile = File(...)):
    pass


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload = True ,debug = True)