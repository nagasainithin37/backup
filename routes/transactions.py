from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.database import usersCollection,transactionCollection
from models.transaction import Transaction
from schemas.schemas import individual_serial, list_serial
transactionRoute=APIRouter()

@transactionRoute.post("/transaction")
async def completeTransaction(accountno:str):
    try:
        user=usersCollection.find_one({"accountno":accountno})
        if user==None:
            return JSONResponse(content={
            "message":"Account not found",
            "status":"failure",
            "isError":False
            })
        transactionObj={}
        transactionObj['accountno']=user['accountno']
        transactionObj['timestamp']=int(datetime.now().timestamp())
        print("Helo ")
        transactionCollection.insert_one(transactionObj)
        print(transactionObj)
        return JSONResponse(content={
            "message":"Transaction completed",
            "status":"success",
            "isError":False,
            "payload":individual_serial(transactionObj)
        })
    except Exception as e:
        return JSONResponse(content={
            "message":str(e),
            "status":"failure",
            "isError":True
        })

@transactionRoute.get("/transaction")
async def completeTransaction(accountno:str):
    try:
        user=usersCollection.find_one({"accountno":accountno})
        if user==None:
            return JSONResponse(content={
            "message":"Account not found",
            "status":"failure",
            "isError":False
            })
        transList=transactionCollection.find({"accountno":user['accountno']}).sort("timestamp", 1)
        return JSONResponse(content={
            "message":"Transaction completed",
            "status":"success",
            "isError":False,
            "payload":list_serial(transList)
        })
    except Exception as e:
        return JSONResponse(content={
            "message":str(e),
            "status":"failure",
            "isError":True
        })