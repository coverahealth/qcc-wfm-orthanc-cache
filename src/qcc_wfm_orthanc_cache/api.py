from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from covera.loglib import (
    configure_get_logger,
)
from qcc_wfm_orthanc_cache.db import init_db
from qcc_wfm_orthanc_cache.models import CacheRequest
from qcc_wfm_orthanc_cache.orthanc_util import process_studies_multitasking

_logger = configure_get_logger()

app = FastAPI()

# Initialize the database session
@app.on_event("startup")
def on_startup():
    init_db()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/api/load-cache")
async def load_cache(req: CacheRequest):
    try:
        process_studies_multitasking(req.accession_numbers)    
        return {"message": "Studies are added cache queue."}
    except Exception as e:
        _logger.error(f"Error in caching the DICOMs in Orthanc {e}")

@app.post("/api/clear-cache")
async def load_cache():
    try:
        _logger.info(f"Exam clear request received")
        return JSONResponse(content={"message": "Cleared cache successfully!"})
    except Exception as e:
        _logger.error(f"Error in clearing the DICOMs in Orthanc {e}")

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy"})






