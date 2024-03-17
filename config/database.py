from pymongo import MongoClient


client=MongoClient("mongodb+srv://major:major@cluster0.vdj3e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db=client.major

usersCollection=db["users"]

otpCollection=db["otp"]