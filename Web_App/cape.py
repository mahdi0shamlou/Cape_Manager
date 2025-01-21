from fastapi import APIRouter, HTTPException
import subprocess
import re

# Create an instance of APIRouter
router_cape = APIRouter(tags=["Managing Cape Service"])


@router_cape.get("/cape/status/")
async def status_cape():
    try:
        # Run 'systemctl status cape' command
        result = subprocess.run(
            ["systemctl", "status", "cape"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        # Extract relevant information using regex
        active_match = re.search(r'Active:\s+(.*)', result.stdout)
        loaded_match = re.search(r'Loaded:\s+(.*)', result.stdout)
        pid_match = re.search(r'Main PID:\s+(\d+)', result.stdout)

        # Prepare response data
        response_data = {
            "status": "success",
            "active": active_match.group(1) if active_match else "N/A",
            "loaded": loaded_match.group(1) if loaded_match else "N/A",
            "main_pid": pid_match.group(1) if pid_match else "N/A"
        }

        return response_data

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error getting status: {e.stderr}")


@router_cape.post("/cape/restart/")
async def restart_cape():
    try:
        # Run 'systemctl restart cape' command
        result = subprocess.run(
            ["systemctl", "restart", "cape"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return {"status": "success", "message": "Cape service restarted successfully."}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error restarting service: {e.stderr}")
