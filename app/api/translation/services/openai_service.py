from langdetect import detect
from app.api.translation.services.nested_ttl_cache import NestedTTLCache
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging
from typing import Dict

logger = logging.getLogger(__name__)

load_dotenv()
model_name = "gpt-4o"
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")
system_messages: Dict[str, str] = {}
with open("app/resources/translation_system_message.txt") as f:
    origin_system_message = f.read()   
    
class OpenAiSession:
    def __init__(self):
        self.nested_cache = NestedTTLCache(maxsize=100, ttl=300)
        self.nested_audio_cache = NestedTTLCache(maxsize=100, ttl=300)
    
    async def _openai_audio_call(self, message,country):
        try:
            """
                This function is used to convert the text to audio using OpenAI's TTS API.
                The nested_audio_cache is used to store the audio files for the country and language.
                but sometimes the openai API fails to return the full audio file, so more debugging is needed.
            """
            mp3 = client.audio.speech.create(
                model="tts-1",
                voice='ash',
                input=message,
            )
            self.nested_audio_cache[country][message]=mp3
            return mp3
        except Exception as e:
            logger.error("Error making connection to OpenAI: ", e)
    
    async def _openai_call(self, messages, model_name=model_name):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0
            )
    
            answer = response.choices[0].message.content
            return answer
        except Exception as e:
            logger.error("Error making connection to OpenAI: ", e)
            
    async def _stream_openai_call(self, messages, model_name=model_name):
        try:
            response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0,
            stream=True
            )
        
            for chunk in response:
                yield chunk.choices[0].delta.content
    
        except Exception as e:
            logger.error("Error making connection to OpenAI: ", e)

    async def get_translation(self,retry:bool, message:str, country:str, language_id:str, language:str):

        try:
            if message in self.nested_cache[country] and not retry:# Cache hit for the country languge and message
                logger.info(f"MESSAGE Cache hit")
                return self.nested_cache[country][message]
            elif message in self.nested_cache[country]:
                logger.info("Retrying the same call")
            if country not in system_messages: # Cache miss for the country language system message
                system_message = origin_system_message.replace("{Country}", country).replace("{Language}", language)
                system_messages[country] = system_message
                
            query = f"""
            Translate the input_message.
            Input_message: {message}
            """
            payload = [{"role": "assistant", "content": system_messages[country]},
            {"role": "user", "content": query}]
            language_detected = detect(message)
            if language_detected == language_id:
                answer =  "El mensaje ya está en español, no es necesario traducirlo."
            else:
                answer = await self._openai_call(payload)
                
            self.nested_cache[country][message]=answer
            
            return answer
        except Exception as e:
            logger.error(f"Error detecting language: {e}")
            return "Lenguaje no detectado."      
        
    async def stream_message(self,message:str):
            payload = [{"role": "system", "content": self.system_message},
                        {"role": "user", "content": message}]
            try:
                return self.stream_openai_call(payload)
            except Exception as e:
                logger.error(f"STREAM: Error detecting language: {e}")
                return "Lenguaje no detectado."
