import shlex
import subprocess


def run(sql, args=None):
    if args is None:
        args = []
    return subprocess.run(
        ["echo {} | pgspot {}".format(shlex.quote(sql), " ".join(args))],
        shell=True,
        capture_output=True,
        text=True,
    ).stdout
