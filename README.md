# pascalgt
Transform manifest file of AWS Ground Truth and Pascal VOC xml files mutually.

## usage
### install
`pip install pascalgt`

### Pascal VOC to AWS Ground Truth manifest
```python
from pathlib import Path
from pascalgt.transformer import Pascal2GT, GT2Pascal


# transform Pascal VOC xml files into a manifest file of AWS Ground Truth
pascal2gt = Pascal2GT(project_name="test-project", s3_path="s3://test-project/images")
pascal2gt.run(Path("./output.manifest"), Path("./xml/"))
```

### AWS Ground Truth manifest to Pascal VOC
```python
from pathlib import Path
from pascalgt.transformer import Pascal2GT, GT2Pascal


# transform a manifest file of AWS Ground Truth into Pascal VOC xml files
gt2pascal = GT2Pascal()
gt2pascal.run(Path("./output.manifest"), Path("./xml"))
```


## license
The source code is licensed MIT.

## ref
* https://dev.classmethod.jp/articles/amazon-sagemaker-ground-truth-to-vott/