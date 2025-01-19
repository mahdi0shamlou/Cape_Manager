import libvirt


class LibvirtConnectionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LibvirtConnectionManager, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def get_connection(self):
        if self.connection is None:
            self.connection = libvirt.open('qemu:///system')
            if self.connection is None:
                raise Exception("Failed to open connection to qemu:///system")
        return self.connection

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None