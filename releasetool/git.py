import re
import subprocess
from typing import Sequence


def list_tags() -> Sequence[str]:
    subprocess.check_output(
        ['git', 'fetch', '--tags'])
    output = subprocess.check_output(
        ['git', 'tag', '--list', '--sort=-creatordate']).decode('utf-8')
    tags = output.split('\n')

    return tags


def summary_log(
        from_: str, to: str='origin/master', where: str='.') -> Sequence[str]:
    output = subprocess.check_output([
        'git', 'log', '--format=%s', f'{from_}..{to}', where]
    ).decode('utf-8')
    commits = output.strip().split('\n')
    return commits


def checkout_create_branch(
        branch_name: str,
        base: str = 'origin/master') -> None:
    subprocess.check_output([
        'git', 'checkout', '-b', branch_name, base])


def commit(files: Sequence[str], message: str) -> None:
    """Create a release commit."""
    subprocess.check_output([
        'git', 'add'] + list(files))
    subprocess.check_output([
        'git', 'commit', '-m', message])


def push(branch: str, remote: str = 'origin') -> None:
    """Push the release branch to the remote."""
    subprocess.check_output([
        'git', 'push', '-u', remote, branch])


def get_github_repo_name(remote='origin') -> str:
    output = subprocess.check_output(
        ['git', 'remote', 'get-url', remote]).decode('utf-8')
    # TODO: Deal with not matching.
    return re.match(r'(.+)@(.+):(?P<name>.+)\.git', output).group('name')
