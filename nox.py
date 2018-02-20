import nox


@nox.session
def lint(session):
    session.interpreter = 'python3.6'
    session.install('flit', 'mypy', 'flake8')
    session.run('flit', 'install')
    session.run('flake8', 'releasetool', 'tests')
    # TODO: run mypy on the tests when there are tests. :)
    session.run('mypy', '--ignore-missing-imports', 'releasetool')
