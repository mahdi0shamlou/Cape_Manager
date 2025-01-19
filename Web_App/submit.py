import time

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
import os
import requests
import libvirt
#----------------------------------- lib that we created
from lib.LibvirtConnectionManager_File import LibvirtConnectionManager
#------------------------------------------------


router_submit = APIRouter()


# Dependency to get the connection manager
def get_libvirt_manager() -> LibvirtConnectionManager:
    return LibvirtConnectionManager()


def submit_file(file_path: str, machine_name: str):
    """Uploads a file to the specified API endpoint and returns the task ID and message."""
    url = "http://localhost:8000/apiv2/tasks/create/file/"
    files = {'file': open(file_path, 'rb')}
    data = {'machine': machine_name}

    try:
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()  # Raise an error for bad responses
        response_data = response.json()  # Parse the JSON response

        # Check if there is an error in the response
        if not response_data.get('error'):
            task_id = response_data['data']['task_ids'][0]  # Get the first task ID
            message = response_data['data']['message']  # Get the message
            return task_id, message  # Return task ID and message
        else:
            print("Error in response:", response_data.get('errors'))
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None


@router_submit.post("/submit/")
async def upload_file_route(file: UploadFile = File(...), machine_name: str = Form(...), manager: LibvirtConnectionManager = Depends(get_libvirt_manager)):
    # Save the uploaded file temporarily
    temp_file_path = f"/tmp/{file.filename}"
    """Handles file upload and sends it to the specified API endpoint after starting the VM."""
    try:
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Call the upload_file function
        task_id, message = submit_file(temp_file_path, machine_name)

        if task_id is None:
            raise HTTPException(status_code=500, detail="Failed to upload file.")
        time.sleep(10) # this sleep is necessary
        # Start the virtual machine using LibvirtConnectionManager
        try:
            conn = manager.get_connection()
            domain = conn.lookupByName(machine_name)

            if domain.state()[0] != libvirt.VIR_DOMAIN_RUNNING:
                domain.create()  # Start the VM if it is not running

        except libvirt.libvirtError as e:
            raise HTTPException(status_code=404,
                                detail=f"VM with name '{machine_name}' not found or could not be started: {str(e)}")

        return {"task_id": task_id, "message": message}

    finally:
        # Clean up: remove the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)





