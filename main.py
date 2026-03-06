from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import models
from database import engine, get_db
import os
import shutil
import csv
import zipfile


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Aurviz Audio Pipeline API")


os.makedirs("storage", exist_ok=True)

@app.post("/api/audio/upload")
async def upload_audio(
    device_id: str = Form(...),
    transcription: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    
    device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
    if not device:
        device = models.Device(device_id=device_id, device_model="Unknown")
        db.add(device)
        db.commit()


    file_location = f"storage/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    db_record = models.AudioRecord(
        device_id=device_id,
        file_path=file_location,
        transcription=transcription
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)


    return {
        "status": "success",
        "audio_id": db_record.audio_id
    }



@app.get("/api/device/{device_id}/audio")
def get_device_audio(device_id: str, db: Session = Depends(get_db)):
    records = db.query(models.AudioRecord).filter(models.AudioRecord.device_id == device_id).all()
    
    if not records:
        raise HTTPException(status_code=404, detail="No audio records found for this device")

    result = []
    for r in records:
        result.append({
            "audio_id": r.audio_id,
            "device_id": r.device_id,
            "transcription": r.transcription,
            "audio_url": r.file_path,
            "timestamp": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return result

@app.get("/api/dataset/download")
def download_dataset(db: Session = Depends(get_db)):
    records = db.query(models.AudioRecord).all()
    

    dataset_dir = "dataset"
    os.makedirs(dataset_dir, exist_ok=True)
    csv_path = os.path.join(dataset_dir, "metadata.csv")
    zip_path = "dataset.zip"


    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["audio_file", "transcription", "device_id"])
        
        for r in records:
            filename = os.path.basename(r.file_path)
            writer.writerow([filename, r.transcription, r.device_id])
            
            # Copy audio file to dataset folder if it exists
            if os.path.exists(r.file_path):
                shutil.copy(r.file_path, os.path.join(dataset_dir, filename))


    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(dataset_dir):
            for file in files:
                zipf.write(os.path.join(root, file), file)


    shutil.rmtree(dataset_dir)


    return FileResponse(zip_path, media_type="application/zip", filename="dataset.zip")