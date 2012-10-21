import contextlib
import os
import shutil
import tempfile

from invoke import task, run


@contextlib.contextmanager
def TemporaryDirectory(*args, **kwargs):
    directory = tempfile.mkdtemp(*args, **kwargs)

    try:
        yield directory
    finally:
        shutil.rmtree(directory)


@task
def deploy(target, force=False):
    if target is None:
        raise Exception("Must provide a target")

    opts = []

    if force:
        opts += ["-f"]

    run("git push {opts} {target} master".format(target=target, opts=" ".join(opts)))


@task(aliases=["db.dump"])
def db_dump(db="warehouse", create=True, drop=False):
    url = run("heroku pgbackups:url --app crate-warehouse", hide="out").stdout

    with TemporaryDirectory() as tmp:
        location = os.path.join(tmp, "crate.dump")

        run("curl -o {location} '{url}'".format(url=url, location=location))

        if drop:
            run("dropdb {db}".format(db=db))

        if create:
            run("createdb {db}".format(db=db))

        run("pg_restore --verbose --clean --no-acl --no-owner -d {db} {location}".format(db=db, location=location))
