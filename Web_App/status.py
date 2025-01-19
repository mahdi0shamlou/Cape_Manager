from fastapi import APIRouter
import libvirt

router = APIRouter()

@router.get("/status/")
async def read_status():
    conn = libvirt.open('qemu:///system')
    if conn is None:
        raise Exception("Failed to open connection to qemu:///system")
    domains = conn.listAllDomains()

    vm_status_list = []

    for domain in domains:
        vm_info = {
            'name': domain.name(),
            'id': domain.ID(),
            'state': domain.state()[0]  # state returns a tuple (state, reason)
        }
        vm_status_list.append(vm_info)

    conn.close()
    return vm_status_list
