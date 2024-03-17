from datetime import datetime
from fastapi import APIRouter, UploadFile,File
from models.users import User
from config.database import usersCollection
from schemas.schemas import individual_serial, list_serial
from fastapi.responses import JSONResponse

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
async def upload(file:UploadFile=File(...)):
    file.filename=f"useraccountno.jpg"
    contents=await file.read()
    with open(f"images/{file.filename}","wb") as f:
        f.write(contents)
    
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