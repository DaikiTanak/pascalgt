# pascalgt
Transform manifest file of AWS Ground Truth and Pascal VOC xml files mutually.

## usage
### install
`pip install pascalgt`

### Pascal VOC to AWS Ground Truth manifest
```python
from pascalgt.transformer import Pascal2GT

# transform Pascal VOC xml files into a manifest file of AWS Ground Truth
pascal2gt = Pascal2GT(project_name="test-project", s3_path="s3://test-project/images")
pascal2gt.run(path_target_manifest="./output.manifest", path_source_xml_dir="./xml/")
```

### AWS Ground Truth manifest to Pascal VOC
```python
from pascalgt.transformer import GT2Pascal

# transform a manifest file of AWS Ground Truth into Pascal VOC xml files
gt2pascal = GT2Pascal()
gt2pascal.run(path_source_manifest="./output.manifest", path_target_xml_dir="./xml")
```

## license
The source code is licensed MIT.
