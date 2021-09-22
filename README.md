# pascalgt
AWS Ground Truth形式のアノテーションファイルとPASCAL-VOC形式を相互に変換します。

## usage
```python
from transformer import GT2Pascal
gt2pascal_transformer = GT2Pascal()
gt2pascal_transformer.transform("/tmp/annotation_001.json")
```

## license


## ref
* https://dev.classmethod.jp/articles/amazon-sagemaker-ground-truth-to-vott/