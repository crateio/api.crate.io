from invoke.task import task
from invoke.run import run

# REALLY HACKY - DON'T JUDGE ME


def _deploy(target, force=False):
    opts = []

    if force:
        opts += ["f"]

    run("git push {opts} {target} master".format(target=target, opts="".join(opts)))


def _call_real(action, *args, **kwargs):
    if args is None:
        args = []

    if kwargs is None:
        kwargs = {}

    g = globals()
    name = "_{action}".format(action=action)

    if name in g:
        g[name](*args, **kwargs)


_actions = set()


@task
def deploy():
    _actions.add("deploy")


@task
def api():
    if not _actions:
        raise Exception("Must call an action prior to selection a target")

    for action in _actions:
        _call_real(action, "api")


@task
def app():
    if not _actions:
        raise Exception("Must call an action prior to selection a target")

    for action in _actions:
        _call_real(action, "app")
