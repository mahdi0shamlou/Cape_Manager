from fastapi import APIRouter, Depends, HTTPException
import libvirt
#----------------------------------- lib that we created
from lib.LibvirtConnectionManager_File import LibvirtConnectionManager
#------------------------------------------------


router_status = APIRouter(tags=["Status Of Kvm Machines"])


# Dependency to get the connection manager
def get_libvirt_manager() -> LibvirtConnectionManager:
    return LibvirtConnectionManager()


@router_status.get("/status/")
async def read_status(manager: LibvirtConnectionManager = Depends(get_libvirt_manager)):
    try:
        conn = manager.get_connection()
        domains = conn.listAllDomains()

        vm_status_list = []
        for domain in domains:
            vm_info = {
                'name': domain.name(),
                'id': domain.ID(),
                'state': domain.state()[0]
            }
            vm_status_list.append(vm_info)

        return vm_status_list
    except libvirt.libvirtError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching VM status: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router_status.get("/status/{vm_name}/")
async def read_vm_details(vm_name: str, manager: LibvirtConnectionManager = Depends(get_libvirt_manager)):
    try:
        conn = manager.get_connection()
        domain = conn.lookupByName(vm_name)

        vm_info = {
            'name': domain.name(),
            'id': domain.ID(),
            'state': domain.state()[0],
            'info': domain.info(),
            'xml_desc': domain.XMLDesc()
        }

        return vm_info
    except libvirt.libvirtError as e:
        raise HTTPException(status_code=404, detail=f"VM with name '{vm_name}' not found: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


