from datetime import datetime
import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
from config.database import otpCollection
from models.otp import Otp
from models.botDto import botDto
from bson import ObjectId
import pyotp
botRoute=APIRouter()

@botRoute.post("/send-telegram-otp")
async def verifyChatId(body:botDto):
    try:
        dbOtp=otpCollection.find_one({'$and':[{"identifier":body.chatId},{"service":"telegram"}]})
        secretKey=pyotp.random_base32()
        totp = pyotp.TOTP(secretKey)
        otp={}
        otp['service']="telegram"
        otp['identifier']=body.chatId
        otp['otp']=str(totp.now())
        body.otp=otp['otp']
        otp['timestamp']=int(datetime.now().timestamp())
        jsonn={}
        jsonn['otp']=body.otp
        jsonn['chatId']=int(body.chatId)
        response=requests.post("http://localhost:3100/send",json=jsonn)
        print(json.loads(response.content.decode('utf-8')))
        res=json.loads(response.content.decode('utf-8'))

        if res['message']=='success':
            if dbOtp==None:
                otpCollection.insert_one(otp)
            else:
                otpCollection.update_one({"_id":ObjectId(dbOtp['_id'])},{"$set":otp})
            return JSONResponse(content={
                "message":"otp sent",
                "status":"success",
                "isError":False
            })
        else:
            JSONResponse(content={
                "message":response.message,
                "status":"failure",
                "isError":True
            })
    except Exception as e:
        return JSONResponse(content={
                "message":str(e),
                "status":"failure",
                "isError":True
            })


@botRoute.post("/verify-telegram-otp")
async def verifyTelegramOtp(otp:Otp):
    try:
        currTimeStamp=int(datetime.now().timestamp())
        dbOtp=otpCollection.find_one({'$and':[{"identifier":otp.identifier},{"service":"telegram"}]})
        print(dbOtp)
        if dbOtp==None:
            return JSONResponse(content={
                "message":"Invalid",
                "status":"failure",
                "isError":False
            }) 
        if dbOtp['otp']!=otp.otp or currTimeStamp-dbOtp['timestamp']>300:
            return JSONResponse(content={
                "message":"Invalid",
                "status":"failure",
                "isError":False
            })
        otpCollection.delete_one({"_id":ObjectId(dbOtp['_id'])})
        return JSONResponse(content={
                "message":"Verified",
                "status":"success",
                "isError":False
            })
    except Exception as e:
        return JSONResponse(content={
                "message":str(e),
                "status":"failute",
                "isError":True
            })