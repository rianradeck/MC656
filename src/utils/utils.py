import socket


def ip_address_is_valid(address):
    try:
        socket.inet_aton(address)
    except OSError:
        return False
    else:
        return True


def nickname_is_valid(nickname):
    return (
        4 <= len(nickname)
        and len(nickname) <= 12
        and all(x.islower() or x.isdigit() for x in nickname)
    )
