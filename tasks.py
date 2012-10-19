from invoke import task, run


@task
def deploy(target, force=False):
    if target is None:
        raise Exception("Must provide a target")

    opts = []

    if force:
        opts += ["-f"]

    run("git push {opts} {target} master".format(target=target, opts=" ".join(opts)))
