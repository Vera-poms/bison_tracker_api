from rtsp_bison_tracker_2 import StreamManager, HLSManager
from fastapi import FastAPI, HTTPException, status
from db import statistics
import os


app = FastAPI(title="BisonGuard Real-time Detection")

stream = StreamManager(os.getenv("SOURCE"), apply_model=True)
# hls = HLSManager()


@app.get("/")
def home():
    return {"message": "This is the Bisons real time detection page"}



@app.get("/streaming")
def is_streaming():
    return {"streamimg": stream.start_stream()}
    

@app.get("/stats")
def get_stats():
    
    # while True:
    bison_frame = statistics.find_one({"filter": statistics["max_bison_in_frame"]})
    print(bison_frame)
        
    if (stream.stats["total_detections"] == 0) or (stream.stats["max_bison_in_frame"] == 0):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No detections made")
    # elif stream.stats["max_bison_in_frame"] == bison_frame:
    #     raise HTTPException(status.HTTP_409_CONFLICT, "Already saved")
    
    statistics.insert_one({
        "total_frames": stream.stats["total_frames"],
        # "start_time": hls.start["start_time"],
        "total_detections": stream.stats["total_detections"],
        "max_bison_in_frame": stream.stats["max_bison_in_frame"],
        "avg_confidence": stream.stats["avg_confidence"],
        "fps": stream.stats["fps"]
    })
    return {"message": "Statistics saved"}
