from pathlib import Path

from src.transformer import GT2Pascal

path_output_manifest = Path("./example_data/manifest/output.manifest")
sample_dict_json = {"source-ref": "s3://test-ground-truth-object-detection/image1.jpg",
                    "sample-job-clone": {"image_size": [{"width": 1108, "height": 1477, "depth": 3}], "annotations": [
                        {"class_id": 0, "top": 640, "left": 10, "height": 463, "width": 488},
                        {"class_id": 1, "top": 777, "left": 589, "height": 359, "width": 511}]},
                    "sample-job-clone-metadata": {"objects": [{"confidence": 0}, {"confidence": 0}],
                                                  "class-map": {"0": "dog", "1": "cat"},
                                                  "type": "groundtruth/object-detection", "human-annotated": "yes",
                                                  "creation-date": "2021-09-21T12:55:32.782712",
                                                  "job-name": "labeling-job/sample-job-clone"}}

gt2pascal = GT2Pascal()


class TestGT2Pascal:

    def test_read_manifest(self):
        list_json_dict = gt2pascal.read_manifest(path_output_manifest)
        assert len(list_json_dict) == 3

    def test_run(self, tmpdir):
        gt2pascal.run(path_output_manifest, tmpdir)
        assert len(list(Path(tmpdir).iterdir())) == 3

    def test_extract_project_name(self):
        assert gt2pascal.extract_project_name(sample_dict_json) == "sample-job-clone"

    def test_get_source_image_filename(self):
        assert str(gt2pascal.get_source_image_filename(sample_dict_json)) == "image1.jpg"

    def test_transform(self):
        xml = gt2pascal.transform(sample_dict_json, "sample-job-clone")
        assert xml is not None
