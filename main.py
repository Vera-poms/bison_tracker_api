from rtsp_bison_tracker_2 import StreamManager, HLSManager
from fastapi import FastAPI, HTTPException, status
from db import statistics
import os
from utils import replace_mongo_id


app = FastAPI(title="BisonGuard Real-time Detection")

stream = StreamManager(os.getenv("SOURCE"), apply_model=True)


@app.get("/")
def home():
    return {"message": "This is the Bisons real time detection page"}



@app.get("/streaming")
def is_streaming():
    return {"streamimg": stream.start_stream()}
    

@app.post("/stats")
def add_stats():
    if (stream.stats["total_detections"] == 0) or (stream.stats["max_bison_in_frame"] == 0):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No detections made")

    statistics.insert_one({
        "total_frames": stream.stats["total_frames"],
        "total_detections": stream.stats["total_detections"],
        "max_bison_in_frame": stream.stats["max_bison_in_frame"],
        "avg_confidence": stream.stats["avg_confidence"],
        "fps": stream.stats["fps"]
    })
    return {"message": "Statistics saved"}

@app.get("/stats")
def get_stats():
    stats = statistics.find().to_list()
    return {"stats": list(map(replace_mongo_id, stats))}
