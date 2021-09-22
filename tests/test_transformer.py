import pytest
from pathlib import Path

from src.transformer import GT2Pascal

path_output_manifest = Path("./example_data/output.manifest")
gt2pascal = GT2Pascal()


class TestGT2Pascal:

    def test_read_manifest(self):
        list_json_dict = gt2pascal.read_manifest(path_output_manifest)
        assert len(list_json_dict) == 3

    def test_run(self, tmpdir):
        gt2pascal.run(path_output_manifest, tmpdir)
        assert len(list(Path(tmpdir).iterdir())) == 3
