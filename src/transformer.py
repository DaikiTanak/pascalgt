import json
from pathlib import Path
from lxml import etree


class Pascal2GT:
    """
    Transform PASCAL-VOC xml files into ground truth
    """
    pass


class GT2Pascal:
    """
    Transform ground truth files into PASCAL-VOC
    """
    def run(self, path_manifest: Path, dir_output_xml: Path) -> None:
        list_json_dict = self.read_manifest(path_manifest)
        project_name = self.extract_project_name(list_json_dict[0])
        for json_dict in list_json_dict:
            xml = self.transform(json_dict, project_name)
            path_source_image = self.get_source_image_filename(json_dict)
            self.save_xml(xml, dir_output_xml / path_source_image.with_suffix(".xml"))
        return

    def read_manifest(self, path_manifest: Path):
        list_json_dict = []
        with open(str(path_manifest), "r") as f:
            list_json_text = f.read().split("\n")

        for json_text in list_json_text:
            if json_text != "":
                json_src = json.loads(json_text)
                list_json_dict.append(json_src)
        return list_json_dict

    def save_xml(self, xml_data: etree.Element, path_save: Path) -> None:
        # xmlファイル出力
        out_xml = etree.tostring(xml_data,
                                 encoding="utf-8",
                                 xml_declaration=True,
                                 pretty_print=True)
        with open(str(path_save), "wb") as f:
            f.write(out_xml)
        return

    def extract_project_name(self, gt_json) -> str:
        return list(gt_json.keys())[1]

    def get_source_image_filename(self, gt_json) -> Path:
        source_ref = gt_json["source-ref"]
        return Path(Path(source_ref).name)

    def transform(self, gt_json, project_name: str) -> etree.Element:
        """
        path_gt_file: .manifest file
        """

        boxlabel_metadata = gt_json[f"{project_name}-metadata"]
        class_mapping = boxlabel_metadata["class-map"]
        assert boxlabel_metadata["type"] == "groundtruth/object-detection"

        boxlabel = gt_json[f"{project_name}"]

        image_size = boxlabel["image_size"][0]
        image_height = image_size["height"]
        image_width = image_size["width"]
        image_depth = image_size["depth"]

        xml_data = etree.Element("annotation")
        etree.SubElement(xml_data, "filename").text = str(self.get_source_image_filename(gt_json))
        size = etree.SubElement(xml_data, "size")
        etree.SubElement(size, "width").text = str(image_width)
        etree.SubElement(size, "height").text = str(image_height)
        etree.SubElement(size, "depth").text = str(image_depth)

        for annotated_bbox in boxlabel["annotations"]:
            class_id = annotated_bbox["class_id"]
            class_name = class_mapping[str(class_id)]
            width = annotated_bbox["width"]
            top = annotated_bbox["top"]
            height = annotated_bbox["height"]
            left = annotated_bbox["left"]

            obj = etree.SubElement(xml_data, "object")
            etree.SubElement(obj, "name").text = class_name
            bndbox = etree.SubElement(obj, "bndbox")
            etree.SubElement(bndbox, "xmin").text = str(left)
            etree.SubElement(bndbox, "ymin").text = str(top)
            etree.SubElement(bndbox, "xmax").text = str(float(left) + float(width))
            etree.SubElement(bndbox, "ymax").text = str(float(top) + float(height))
        return xml_data


if __name__ == "__main__":
    gt2pascal = GT2Pascal()
    gt2pascal.run(Path("../tests/example_data/output.manifest"), Path("../output"))
