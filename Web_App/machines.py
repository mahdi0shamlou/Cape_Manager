from fastapi import APIRouter, Depends, HTTPException
import libvirt
#----------------------------------- lib that we created
from lib.LibvirtConnectionManager_File import LibvirtConnectionManager
#------------------------------------------------


router_machines = APIRouter()


# Dependency to get the connection manager
def get_libvirt_manager() -> LibvirtConnectionManager:
    return LibvirtConnectionManager()


@router_machines.post("/machines/start/{vm_name}")
async def start_vm(vm_name: str, manager: LibvirtConnectionManager = Depends(get_libvirt_manager)):
    try:
        conn = manager.get_connection()
        domain = conn.lookupByName(vm_name)

        if domain.isActive():
            raise HTTPException(status_code=400, detail=f"VM '{vm_name}' is already running.")

        domain.create()  # Start the VM
        return {"message": f"VM '{vm_name}' has been started successfully."}
    except libvirt.libvirtError as e:
        raise HTTPException(status_code=404, detail=f"VM with name '{vm_name}' not found: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router_machines.post("/machines/stop/{vm_name}")
async def stop_vm(vm_name: str, manager: LibvirtConnectionManager = Depends(get_libvirt_manager)):
    try:
        conn = manager.get_connection()
        domain = conn.lookupByName(vm_name)

        if not domain.isActive():
            raise HTTPException(status_code=400, detail=f"VM '{vm_name}' is not running.")

        domain.shutdown()  # Gracefully shut down the VM
        return {"message": f"VM '{vm_name}' has been shut down successfully."}
    except libvirt.libvirtError as e:
        raise HTTPException(status_code=404, detail=f"VM with name '{vm_name}' not found: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
