import keyring

_SERVICE = 'codes.thea.releasetool'


def get_password(name):
    return keyring.get_password(_SERVICE, name)


def set_password(name, password):
    """Ensure we have a github username and token."""
    keyring.set_password(_SERVICE, 'github', password)
