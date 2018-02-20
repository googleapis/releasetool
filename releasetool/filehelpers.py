import os
import re
import subprocess
import tempfile
from typing import Optional


def open_editor(filename: str, return_contents: bool = False) -> Optional[str]:
    editor = os.environ.get('EDITOR', 'nano')
    subprocess.check_call([editor, filename])

    if return_contents:
        with open(filename, 'r') as fh:
            return fh.read()
    else:
        return None


def open_editor_with_content(
        filename: str,
        contents: str,
        return_contents: bool = False) -> Optional[str]:

    with open(filename, 'w') as fh:
        fh.write(contents)

    return open_editor(filename, return_contents=return_contents)


def open_editor_with_tempfile(contents: str, suffix: str = '.txt') -> str:
    handle, filename = tempfile.mkstemp(suffix)
    os.close(handle)

    content = open_editor_with_content(
        filename, contents, return_contents=True)

    os.remove(filename)

    return content


def insert_before(
        filename: str,
        new_content: str,
        expr: str,
        separator: str = '\n') -> None:
    with open(filename, 'r+') as fh:
        if not new_content.endswith(separator):
            new_content += separator

        content = fh.read()
        match = re.search(expr, content, re.MULTILINE)
        position = match.start()

        output = content[:position] + new_content + content[position:]

        fh.seek(0)
        fh.write(output)


def replace(filename: str, expr: str, replacement: str) -> None:
    with open(filename, 'r+') as fh:
        content = fh.read()

        content = re.sub(expr, replacement, content)

        fh.seek(0)
        fh.write(content)
        fh.truncate()
