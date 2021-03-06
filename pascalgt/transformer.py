import datetime
import json
from pathlib import Path
from lxml import etree
from typing import List, Optional


class Pascal2GT:
    """
    Transform PASCAL-VOC xml files into ground truth
    """

    def __init__(self, project_name: str, s3_path: str):
        self.project_name = project_name
        self.s3_path = s3_path  # s3 key of the directory including images

    def run(self, path_target_manifest: str, path_source_xml_dir: str) -> None:
        path_target_manifest = Path(path_target_manifest)
        path_source_xml_dir = Path(path_source_xml_dir)

        list_xml = []
        for path_file in path_source_xml_dir.iterdir():
            if path_file.suffix == ".xml":
                xml = self.read_pascal_xml(path_file)
                list_xml.append(xml)
        output_manifest_text = self.aggregate_xml(list_xml)
        with open(str(path_target_manifest), mode='w') as f:
            f.write(output_manifest_text)
        return

    def read_pascal_xml(self, path_xml: Path) -> etree.Element:
        assert path_xml.exists()
        xml = etree.parse(str(path_xml))
        return xml

    def aggregate_xml(self, list_xml: List[etree.Element]) -> str:
        """
        aggregate list of xml structure objects into one output.manifest text.
        """
        outputText = ""
        list_output_json_dict = []
        class_name2class_id_mapping = {}

        for xml in list_xml:
            output_dict = {}

            filename = xml.find("filename").text
            size_object = xml.find("size")

            text_image_height = size_object.find("height").text
            text_image_width = size_object.find("width").text

            image_height = int(float(text_image_height) if "." in text_image_height else text_image_height)
            image_width = int(float(text_image_width) if "." in text_image_width else text_image_width)
            image_depth = int(size_object.find("depth").text)

            output_dict["source-ref"] = f"{self.s3_path}/{filename}"
            output_dict[self.project_name] = {"image_size": [{"width": image_width,
                                                              "height": image_height,
                                                              "depth": image_depth}],
                                              "annotations": []}
            output_dict[f"{self.project_name}-metadata"] = {"objects": [],
                                                            "class-map": {},
                                                            "type": "groundtruth/object-detection",
                                                            "human-annotated": "yes",
                                                            "creation-date": datetime.datetime.now().isoformat(
                                                                timespec='microseconds'),
                                                            "job-name": f"labeling-job/{self.project_name}"}

            objects = xml.findall("object")

            for annotated_object in objects:
                class_name = annotated_object.find("name").text
                if class_name2class_id_mapping.get(class_name) is None:
                    class_name2class_id_mapping[class_name] = len(class_name2class_id_mapping)

                class_id = class_name2class_id_mapping[class_name]

                bbox_object = annotated_object.find("bndbox")

                text_x1 = bbox_object.find("xmin").text
                text_x2 = bbox_object.find("xmax").text
                text_y1 = bbox_object.find("ymin").text
                text_y2 = bbox_object.find("ymax").text

                x1 = int(float(text_x1) if "." in text_x1 else text_x1)
                x2 = int(float(text_x2) if "." in text_x2 else text_x2)
                y1 = int(float(text_y1) if "." in text_y1 else text_y1)
                y2 = int(float(text_y2) if "." in text_y2 else text_y2)

                bbox_width = x2 - x1
                bbox_height = y2 - y1

                output_dict[self.project_name]["annotations"].append(
                    {
                        "class_id": class_id,
                        "top": y1,
                        "left": x1,
                        "height": bbox_height,
                        "width": bbox_width,
                    }
                )
                output_dict[f"{self.project_name}-metadata"]["objects"].append({"confidence": 0})

            list_output_json_dict.append(output_dict)

        for output_dict in list_output_json_dict:
            output_dict[f"{self.project_name}-metadata"]["class-map"] = {str(class_id): str(class_name) for (class_name, class_id) in class_name2class_id_mapping.items()}
            outputText += json.dumps(output_dict, separators=(",", ":")) + "\n"
        return outputText


class GT2Pascal:
    """
    Transform ground truth files into PASCAL-VOC
    """

    def run(self, path_source_manifest: str, path_target_xml_dir: str, project_name: Optional[str] = None) -> None:
        path_source_manifest = Path(path_source_manifest)
        path_target_xml_dir = Path(path_target_xml_dir)

        list_json_dict = self.read_manifest(path_source_manifest)
        project_name = project_name if (project_name is not None and isinstance(project_name, str)) else self.extract_project_name(list_json_dict[0])
        for json_dict in list_json_dict:
            xml = self.transform(json_dict, project_name)
            path_source_image = self.get_source_image_filename(json_dict)
            self.save_xml(xml, path_target_xml_dir / path_source_image.with_suffix(".xml"))
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
        # xml??????????????????
        out_xml = etree.tostring(
            xml_data,
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
        Params:
        - gt_json: python dict instance with ground truth annotations
        - project_name: A project name for SageMaker Ground Truth.

        Return: etree.Element instance to express annotations
        """
        try:
            boxlabel = gt_json[f"{project_name}"]
            boxlabel_metadata = gt_json[f"{project_name}-metadata"]
            class_mapping = boxlabel_metadata["class-map"]
        except KeyError:
            raise ValueError("No valid annotations")

        assert boxlabel_metadata["type"] == "groundtruth/object-detection"

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
            etree.SubElement(bndbox, "xmax").text = str(int(left) + int(width))
            etree.SubElement(bndbox, "ymax").text = str(int(top) + int(height))
        return xml_data
