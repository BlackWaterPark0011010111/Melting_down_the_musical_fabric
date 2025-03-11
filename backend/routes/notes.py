from fastapi import APIRouter, File, UploadFile, HTTPException
import cv2
import numpy as np
from PIL import Image
import io

router = APIRouter()

def process_image(file: UploadFile):
    image_bytes = file.file.read()

    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("L")
        img_np = np.array(image)

        edges = cv2.Canny(img_np, 100, 200)
        
        return {"message": "Обработка изображения завершена", "edges_detected": bool(np.any(edges))}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Ошибка при обработке изображения: " + str(e))

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Неверный формат файла. Требуется JPEG или PNG.")
    result = process_image(file)
    return result
