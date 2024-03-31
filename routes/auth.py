from datetime import datetime
from fastapi import APIRouter, UploadFile,File
from models.users import User
from config.database import usersCollection,imageCollection
from schemas.schemas import individual_serial, list_serial
from fastapi.responses import JSONResponse
import base64
from PIL import Image
authRoute=APIRouter()

@authRoute.post("/signup")
async def signup(user:User):
    try:
        user.name=user.name.lower()
        user.email=user.email.lower()
        user.accountno=list(str(datetime.timestamp(datetime.now())).split('.'))[0]
        users=list_serial(usersCollection.find({'$or':[{"email":user.email},{"phoneNum":user.phoneNum}]}))
        print(users)
        if(len(users)>0):
            return JSONResponse(content={
                "message":"User already exists with same email or phone number",
                "status":"failure",
                "isError":False
                })
        else:
            insertedUser=usersCollection.insert_one(dict(user))
            return JSONResponse(content={
                "message":"user inserted",
                "payload": user.accountno,
                "status":"success",
                "isError":False
                  })
    except Exception as e:
        return JSONResponse(content={
            "message":str(e),
            "status":"failure",
            "isError":True
        })


@authRoute.post("/upload")
async def upload(accountno:str,file:UploadFile=File(...)):
    try:
        user=usersCollection.find_one({'accountno':accountno})
        if user==None:
            return JSONResponse(content={
                "message":"Error",
                "status":"failure",
                "isError":False
            })
        file.filename=accountno+".jpg"
        encoded_image=""
        contents=await file.read()
        encoded_image = base64.b64encode(contents)
        # print(encoded_image.decode("utf-8"))
        imageObj={}
        imageObj['image']=  encoded_image.decode("utf-8")
        imageObj['accountno']=accountno
        imageCollection.insert_one(imageObj)
        usersCollection.update_one({"accountno":accountno},{"$set":{"isPhoneNumVerified":True}})
        return JSONResponse(content={
            "message":"Image Uploaded",
            "status":"success",
            "isError":False
        })
    except Exception as e:
        return JSONResponse(content={
            "message":str(e),
            "status":"failure",
            "isError":True
        })
@authRoute.post("/login")
async def login(accountNo:str):
    try:
        user=usersCollection.find_one({"accountno":accountNo})
        if user==None:
            return JSONResponse(content={
            "message":"Account not found",
            "status":"failure",
            "isError":False
        })
        return JSONResponse(content={
            "message":"Account details are",
            "status":"success",
            "payload":individual_serial(user),
            "isError":True
        })
    except Exception as e:
        return JSONResponse(content={
            "message":str(e),
            "status":"failure",
            "isError":True
        })