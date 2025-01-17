from concurrent.futures import ThreadPoolExecutor
from string import Template
from typing import List
from fastapi import HTTPException
from qcc_wfm_orthanc_cache.db import log_status
import requests
from qcc_wfm_orthanc_cache.config import settings
import httpx
from covera.loglib import (
    configure_get_logger,
)

from fastapi.concurrency import run_in_threadpool

_logger = configure_get_logger()

query_template: Template = Template('''{
    "Level": "Study",
    "Query": {
        "AccessionNumber": "${accession_number}"
    },
    "Expand": true
}''')


class OrthancRequestException(
    requests.exceptions.RequestException
):
    pass

def _study_exists(accession_number:str):
    data = query_template.substitute(accession_number=accession_number)
    if study_found := _orthanc_request(
            method='POST',
            url=settings.download_url + settings.find_endpoint,
            data=data
        ):
            return study_found
    else:
        return False
    
def download_study(accession_number: str):
    log_status(accession_number, 'downloading')
    
    try:
        download_content = []
        if study_list:= _study_exists(accession_number):
            for study in study_list:
                study_content = _download_study_by_id(study['ID'])
                if study_content:
                    download_content.append(study_content)
            log_status(accession_number, 'downloaded')
            return download_content
        else:
            log_status(accession_number, 'FAILED', 'Accession not found in the Orthanc')
            return None
    except httpx.HTTPStatusError as e:
        log_status(accession_number, 'failed', f"Error downloading study: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=f"Error downloading study {accession_number}")

def _download_study_by_id(study_id: str):
    return _orthanc_request(
        method='GET',
        url= f"{settings.download_url}/studies/{study_id}/archive",
        response_content=True
    )
    
    

def upload_study(dicom_data: bytes, accession_number: str):
    log_status(accession_number, 'uploading')
    
    try:
        respones = _orthanc_request(
            method= 'POST',
            url= settings.upload_url + settings.instances_endpoint,
            data=dicom_data[0],
            headers={"Content-Type": "application/dicom"}
        )

        # Successfully uploaded, now log the status
        log_status(accession_number, 'uploaded')
    except httpx.HTTPStatusError as e:
        log_status(accession_number, 'failed', f"Error uploading study: {e}")
        raise HTTPException(status_code=e.response.status_code, detail="Error uploading study")
    except Exception as ex:
        log_status(accession_number, 'failed', f"Error uploading study: {e}")

def _orthanc_request(method: str, url: str, response_content=False, headers=None, data=None) -> dict:
    try:        
        with requests.Session() as session:
            response = session.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                auth=(settings.username, settings.password),
                verify=False
            )
            response.raise_for_status()
            return response.json() if not response_content else response.content
    except requests.exceptions.RequestException as err:
        # if orthanc is down we raise OrthancRequestException
        # which can be used for unique handling
        if err.response and err.response.status_code >= 500:
            raise OrthancRequestException(err)
        else:
            raise

def process_studies_multitasking(accession_numbers: List[str]):
    
    with ThreadPoolExecutor(max_workers=settings.max_workers) as executor:
        # Download studies concurrently
        dicom_data_list = list(
            executor.map(download_study, accession_numbers)
        )
        
        # Upload studies concurrently
        for dicom_data, accession_number in zip(dicom_data_list, accession_numbers):
            executor.submit(upload_study, dicom_data, accession_number)

