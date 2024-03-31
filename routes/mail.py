from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.database import otpCollection,usersCollection
from models.otp import Otp
from schemas.schemas import individual_serial, list_serial
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyotp
mailRoute=APIRouter()



@mailRoute.post("/sendmail")
async def sendMail(email:str):
    try:
        dbOtp=otpCollection.find_one({'$and':[{"identifier":email},{"service":"email"}]})
        msg=MIMEMultipart('alternative')
        msg['From']="scoretrack@outlook.com"
        msg["To"]=email
        msg['Subject']="OTP From BANK"
        secretKey=pyotp.random_base32()
        totp = pyotp.TOTP(secretKey)
        otp={}
        otp['service']="email"
        otp['identifier']=email
        otp['otp']=str(totp.now())
        otp['timestamp']=int(datetime.now().timestamp())
        html="<html><body>Your otp is <strong>"+otp['otp']+"</strong></body></html>"
        message=MIMEText(html,'html')
        msg.attach(message)
        smtp_server='smtp-mail.outlook.com'
        smtp_port=587
        try:
            server=smtplib.SMTP(smtp_server,smtp_port)
            server.starttls()
            server.login("scoretrack@outlook.com","Nagasai@0602")
            server.sendmail("scoretrack@outlook.com",email,msg.as_string())
        except Exception as e:
            return JSONResponse(content={
                "message":str(e),
                "status":"failure",
                "isError":True
            })
        if dbOtp==None:
            otpCollection.insert_one(otp)
        else:
            otpCollection.update_one({"_id":ObjectId(dbOtp['_id'])},{"$set":otp})
    except Exception as e:
        return JSONResponse(content={
                "message":str(e),
                "status":"failure",
                "isError":True
            })

    return JSONResponse(content={
            "message":"Otp sent successfully",
            "status":"success",
            "isError":False
        })

@mailRoute.post("/verify-email-otp")
async def verifyEmailOtp(otp:Otp):
    try:
        currTimeStamp=int(datetime.now().timestamp())
        dbOtp=otpCollection.find_one({'$and':[{"identifier":otp.identifier},{"service":"email"}]})
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
        usersCollection.update_one({"email":otp.identifier},{"$set":{"isEmailVerified":True}})
        otpCollection.delete_one({"_id":ObjectId(dbOtp['_id'])})
        return JSONResponse(content={
                "message":"OTP Verified",
                "status":"success",
                "isError":False
            })
    except Exception as e:
        return JSONResponse(content={
                "message":str(e),
                "status":"failure",
                "isError":True
            })

@mailRoute.get("/qqq")
async def f():
    print(pyotp.random_base32())
    totp = pyotp.TOTP("base32secret3232",interval=300)
    return totp.now()