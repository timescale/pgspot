import pytest
import subprocess

from pathlib import Path
from os.path import splitext, basename


@pytest.mark.parametrize('sql_file', list(Path('testdata').glob("*.sql")))
def test_golden_sql(sql_file, snapshot):
    result = subprocess.run(["python pgspot {}".format(str(sql_file))], shell=True, capture_output=True, text=True)
    output = result.stdout

    snapshot.snapshot_dir = 'testdata/expected'
    snapshot.assert_match(output, "{}.out".format(splitext(basename(sql_file))[0]))
