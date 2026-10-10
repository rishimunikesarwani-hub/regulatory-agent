"""Network guard for Python test workers. Not an operating-system sandbox."""
import ipaddress
import sys

installed = False


def loopback(host):
    if host == "localhost":
        return True
    try:
        address = ipaddress.ip_address(host)
        return address.is_loopback or bool(getattr(address, "ipv4_mapped", None) and address.ipv4_mapped.is_loopback)
    except ValueError:
        return False


def install():
    global installed
    if installed:
        return

    def guard(event, args):
        if event in {"socket.connect", "socket.sendto"}:
            address = args[1]
            if not isinstance(address, tuple) or not loopback(address[0]):
                raise PermissionError("External network disabled in local checks")
        elif event in {"socket.getaddrinfo", "socket.gethostbyname", "socket.gethostbyaddr"}:
            if not loopback(args[0]):
                raise PermissionError("External DNS disabled in local checks")

    sys.addaudithook(guard)
    installed = True
