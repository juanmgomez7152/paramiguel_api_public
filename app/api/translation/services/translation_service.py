from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Response
import json
import logging
from typing import Dict
from app.api.translation.services.openai_service import OpenAiSession
from app.api.translation.services.image_parser_service import ImageParserSession


logger = logging.getLogger(__name__)

country_to_languageid:  Dict[str, str] ={}
country_to_language: Dict[str, str] ={}
with open("app/resources/countries_supported.json", "r") as f:
    countries = json.load(f)
    for language, data in countries.items():
        for lang_id, country_list in data.items():
            for country in country_list:
                country_to_languageid[country] = lang_id
                country_to_language[country] = language

openai_session = OpenAiSession()
image_parser = ImageParserSession()

class TranslationService:
    async def process_image(self, file):
        logger.debug(f"Processing image '{file.filename}'...")
        try:
            # Read the image bytes
            image_bytes = await file.read()
            
            extracted_text=await image_parser.parse_image(file.filename,image_bytes)
            return json.dumps({"extracted_text": extracted_text}), 200
        except Exception as e:
            logger.error(f"Error parsing image: {e}")
            return json.dumps({"error": "Error parsing image"}), 500
            
        
         

    async def translate_text(self, request:json):
        try:
            message = request["message"]
            country = request["language"]
            #verify is the country is supported:
            if country not in country_to_languageid:
                raise ValueError(f"Country '{country}' not supported")
            retry = request["retry"]
            language_id=country_to_languageid[country]
            language = country_to_language[country]
            answer = await openai_session.get_translation(retry,message,country=country,language_id=language_id,language=language)

            return json.dumps({"answer": answer}), 200
        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
            return json.dumps({"Value Error": str(ve)}), 400
        except Exception as e:
            logger.error(f"Error sending the response: {e}")
            return json.dumps({"Exception Error": "Error translating message"}), 500

    async def tts(self, request:json):
        try:
            message = request["message"]
            country = request["language"]
            mp3 = await openai_session._openai_audio_call(message,country)
            
            # Get the binary content from the OpenAI response
            audio_content = mp3.content
            return audio_content, 200
        except Exception as e:
            logger.error(f"Error turning text to speech: {e}")
            raise HTTPException(status_code=500, detail="Error turning text to speech")
        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
            raise HTTPException(status_code=400, detail=str(ve))