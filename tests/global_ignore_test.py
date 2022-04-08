import subprocess


def test_global_ignore():
    result = subprocess.run(["echo 'CREATE TABLE IF NOT EXISTS foo();' | python pgspot"], shell=True, capture_output=True, text=True)
    output = result.stdout

    print("output: {}".format(output))

    assert "PS012" in output
    assert "PS017" in output

    result = subprocess.run(["echo 'CREATE TABLE IF NOT EXISTS foo();' | python pgspot --ignore PS012"], shell=True, capture_output=True, text=True)
    output = result.stdout

    print("output: {}".format(output))

    assert "PS012" not in output
    assert "PS017" in output
