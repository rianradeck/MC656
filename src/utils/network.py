import socket


def ip_address_is_valid(address):
    try:
        socket.inet_aton(address)
    except OSError:
        return False
    else:
        return True
