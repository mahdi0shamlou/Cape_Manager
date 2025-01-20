from fastapi import APIRouter, HTTPException
import requests

router_tasks = APIRouter()


@router_tasks.get("/tasks/list/")
async def get_status_of_list_task():
    """Fetches the list of tasks from the external API and returns the response."""
    url = "http://localhost:8000/apiv2/tasks/list/100"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the parsed JSON response

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")

@router_tasks.get("/tasks/status/{task_id}/")
async def get_status_of_one_task(task_id: int):
    """Fetches the list of tasks from the external API and returns the response."""
    url = f"http://localhost:8000/apiv2/tasks/view/{task_id}/"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the parsed JSON response

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")

@router_tasks.get("/tasks/report/{task_id}/")
async def get_report_of_one_task(task_id: int):
    """Fetches the list of tasks from the external API and returns the response."""
    url = f"http://localhost:8000/apiv2/tasks/get/report/{task_id}/json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the parsed JSON response

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")

@router_tasks.get("/tasks/iocs/{task_id}/")
async def get_iocs_of_one_task(task_id: int):
    """Fetches the list of tasks from the external API and returns the response."""
    url = f"http://localhost:8000/apiv2/tasks/get/iocs/{task_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")