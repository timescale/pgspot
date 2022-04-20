import subprocess


def run(sql, args):
    return subprocess.run(
        ["echo '{}' | python pgspot {}".format(sql, " ".join(args))],
        shell=True,
        capture_output=True,
        text=True,
    ).stdout
