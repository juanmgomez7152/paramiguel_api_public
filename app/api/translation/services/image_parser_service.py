import logging
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from io import BytesIO
from typing import Optional
import base64
from cachetools import TTLCache
import os
import ocrspace

executor = ThreadPoolExecutor()
logger = logging.getLogger(__name__)
ocr_space_api_key = os.getenv("OCR_SPACE_API_KEY")
ocr_api = ocrspace.API(api_key=ocr_space_api_key)

class ImageParserSession:   
    cache = TTLCache(maxsize=100, ttl=300)
    def __init__(self):
        pass

    def _get_image_format(self, image_bytes: bytes) -> str:
        """Detect image format from bytes"""
        try:
            with Image.open(BytesIO(image_bytes)) as img:
                return img.format.lower()
        except:
            return 'jpeg'  # Default fallback

    async def parse_image(self, filename: str, image_bytes: bytes) -> Optional[str]:
        if filename in self.cache:
            return self.cache[filename]
        
        try:
            # Convert image bytes to base64
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            # Detect image format for proper MIME type
            image_format = self._get_image_format(image_bytes)
            
            # Format for OCR.space (must include data URI scheme)
            base64_with_data_uri = f"data:image/{image_format};base64,{base64_image}"
            
            response = ocr_api.ocr_base64(base64_with_data_uri)
            self.cache[filename]=response
            return response
                        
        except Exception as e:
            logger.error(f"Error parsing image using OCR.space: {str(e)}")
            return "Problema al leer la imagen"