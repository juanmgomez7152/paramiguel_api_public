from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Response
import logging
from app.api.translation.services.translation_service import TranslationService
router = APIRouter(tags=["Translation"])

logger = logging.getLogger(__name__)
translation_service = TranslationService()

@router.post("/upload-picture/")
async def upload_picture(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    response,code = await translation_service.process_image(file)
    return Response(content=response, media_type="application/json",status_code=code)

@router.post("/send-message/")
async def translate_sent_message(request: Request):
    logger.info("Translating message...")
    json_data = await request.json()
    response,code = await translation_service.translate_text(json_data)
    return Response(content=response, media_type="application/json",status_code=code)

@router.post("/turn-text-to-speech/")
async def turn_text_to_speech(request: Request):
    logger.info("Turning text to speech...")
    json_data = await request.json()
    
    response,code = await translation_service.tts(json_data)
    return Response(
            content=response, 
             media_type="audio/mpeg", 
             headers={"Content-Disposition": "attachment; filename=speech.mp3"}, 
             status_code=code)
