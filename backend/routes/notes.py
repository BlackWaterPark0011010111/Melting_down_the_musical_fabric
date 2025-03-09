from fastapi import APIRouter, File, UploadFile
import cv2
import numpy as np
from PIL import Image
import io

router = APIRouter()

def process_image(file: UploadFile):
    image_bytes = file.file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("L")
    img_np = np.array(image)

    edges = cv2.Canny(img_np, 100, 200)
    
    # Тут добавляешь логику для конвертации в табы
    return {"message": "Обработка изображения завершена", "edges_detected": bool(np.any(edges))}

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    result = process_image(file)
    return result
