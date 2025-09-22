from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Response
import json
import logging
# from app.db.test.test_duckdb_service import insert_user, verify_email_exist, verify_password

router = APIRouter(tags=["Authorization"])
logger = logging.getLogger(__name__)

@router.get("/test")
async def test():
    return {"message":"Authorization test endpoint"}

# @router.post("/sign-in")
# async def sign_in(request: Request):
#     try:
#         data = await request.json()
#         email = data['email']
#         password = data['password']
#         is_email_exist = await verify_email_exist(email)
#         if not is_email_exist:
#             return json.dumps({"error":"email"})
        
#         is_password_corr = await verify_password(email, password)
#         if is_password_corr:
#             return json.dumps({"message":"success"})
#         else:
#             return json.dumps({"error":"password"})
#     except Exception as e:
#         logger.error(f"Error signing in: {e}")
#         return Response(status_code=500)
