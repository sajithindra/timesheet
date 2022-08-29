
from fastapi import FastAPI,Form,File, UploadFile
from io import BytesIO
import pandas as pd 
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
    try : 
        contents = file.file.read()
        buffer=BytesIO(contents)
        df = pd.read_csv(buffer)
        df['empid'] = empid
    except Exception as e :
        print ("Error is "+ str(e))
        return False
    finally : 
        file.file.close()

    try:
        client.bhrama.timesheet.insert_many(df.to_dict('records'))
    except Exception as e:
        print(str(e))
        return False
    return True

@app.get('/timesheet')
async def timesheet():
    filter = {}
    project = {
        '_id':0
    }
    try:
        timesheet =list(client.bhrama.timesheet.find(filter,project))
    except Exception as e:
        print(str(e))
    df=pd.DataFrame(timesheet)
    df=df.groupby(['empid','Date']).sum().reset_index()
    return df.to_dict('records')

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload = True ,debug = True)