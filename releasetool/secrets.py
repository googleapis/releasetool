import click
import keyring

_SERVICE = 'com.google.cloud.devrel.releasetool'


def get_password(name):
    return keyring.get_password(_SERVICE, name)


def set_password(name, password):
    """Ensure we have a github username and token."""
    keyring.set_password(_SERVICE, 'github', password)


def ensure_password(name, prompt):
    password = get_password(name)

    if not password:
        password = click.prompt(prompt)
        set_password(name, password)

    return password
