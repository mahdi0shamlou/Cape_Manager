from fastapi import APIRouter, HTTPException
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

@router.get("/status/{vm_name}")
async def read_vm_details(vm_name: str):
    conn = libvirt.open('qemu:///system')
    if conn is None:
        raise Exception("Failed to open connection to qemu:///system")

    try:
        domain = conn.lookupByName(vm_name)
        vm_info = {
            'name': domain.name(),
            'id': domain.ID(),
            'state': domain.state()[0],
            'info': domain.info(),  # This returns detailed information about the VM
            'xml_desc': domain.XMLDesc()  # This returns the XML description of the VM
        }
    except libvirt.libvirtError as e:
        conn.close()
        raise HTTPException(status_code=404, detail=f"VM with ID {vm_name} not found: {str(e)}")

    conn.close()
    return vm_info
