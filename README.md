# pascalgt
AWS Ground Truth形式のアノテーションファイルとPASCAL-VOC形式を相互に変換します。

## usage
```python
from pathlib import Path
from transformer import GT2Pascal

gt2pascal = GT2Pascal()
gt2pascal.run(path_manifest=Path("./output.manifest"), dir_output_xml=Path("../output"))
```

## license


## ref
* https://dev.classmethod.jp/articles/amazon-sagemaker-ground-truth-to-vott/