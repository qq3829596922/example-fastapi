# from datetime import datetime,timedelta
# from jose import jwt

# SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM="HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES=30 


# def create_access_token(data:dict):
#     to_encode=data.copy()
#     expire=datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp":expire})
#     print(to_encode)
#     encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
#     print(encoded_jwt)
#     return encoded_jwt



# create_access_token({"user_id":1})
a=({"user_id":1},0)
print(a[0])

