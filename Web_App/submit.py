import time
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
import os
import requests
import libvirt
import re
from datetime import datetime, timedelta
# Import your custom connection manager
from lib.LibvirtConnectionManager_File import LibvirtConnectionManager

router_submit = APIRouter(tags=["Submit Task To cape"])


# Dependency to get the connection manager
def get_libvirt_manager() -> LibvirtConnectionManager:
    return LibvirtConnectionManager()

def get_last_shutdown_time(machine_name: str) -> datetime:
    """Fetches the last shutdown time of the specified VM from logs."""
    log_file_path = "/var/log/libvirt/qemu/{}.log".format(machine_name)

    if not os.path.exists(log_file_path):
        # If the log file does not exist, return a very old date
        return datetime.min

    with open(log_file_path, 'r') as log_file:
        for line in reversed(log_file.readlines()):
            # Look for shutdown messages in the log lines
            if "shutting down" in line.lower():
                # Use regex to extract timestamp from the log line
                match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                if match:
                    # Convert string timestamp to datetime object
                    return datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')

    # If no shutdown message is found, return a very old date
    return datetime.min


def submit_file(file_path: str, machine_name: str):
    """Uploads a file to the specified API endpoint and returns the task ID and message."""
    url = "http://localhost:8000/apiv2/tasks/create/file/"
    files = {'file': open(file_path, 'rb')}
    data = {'machine': machine_name}

    try:
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        response_data = response.json()

        if not response_data.get('error'):
            task_id = response_data['data']['task_ids'][0]
            message = response_data['data']['message']
            return task_id, message
        else:
            print("Error in response:", response_data.get('errors'))
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None


@router_submit.post("/submit/")
async def upload_file_route(file: UploadFile = File(...), machine_name: str = Form(...), manager: LibvirtConnectionManager = Depends(get_libvirt_manager)):
    temp_file_path = f"/tmp/{file.filename}"

    try:
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Check VM state and last shutdown time
        conn = manager.get_connection()
        domain = conn.lookupByName(machine_name)

        # Get VM state and last shutdown time
        state, reason = domain.state()

        if state == libvirt.VIR_DOMAIN_SHUTOFF:
            # Check if the VM has been off for more than 10 minutes
            last_shutdown_time = datetime.now() - timedelta(minutes=2)
            # Assuming you have a way to retrieve the last shutdown time;
            # this could be a timestamp stored in your database or logs.
            # For demonstration purposes, let's assume it's fetched here.
            last_shutdown_time_from_db = get_last_shutdown_time(machine_name)

            # If the VM has been off for more than 10 minutes
            if last_shutdown_time_from_db < last_shutdown_time:
                task_id, message = submit_file(temp_file_path, machine_name)
                if task_id is None:
                    raise HTTPException(status_code=500, detail="Failed to upload file.")

                # Wait for some time before starting the VM
                #time.sleep(15)
                #domain.create()  # Start the VM after uploading the file
                return {"task_id": task_id, "message": message}
            else:
                return {"Time_shouted": last_shutdown_time_from_db, "Time_last_mines": last_shutdown_time}

        elif state == libvirt.VIR_DOMAIN_RUNNING:
            raise HTTPException(status_code=400, detail=f"VM '{machine_name}' is already running.")

    except libvirt.libvirtError as e:
        raise HTTPException(status_code=404, detail=f"VM with name '{machine_name}' not found or could not be started: {str(e)}")

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
