import supervision as sv

from inference import get_model

MODEL_ID = "structuralelements/8"

class StructuralElementsClassifier:
    def __init__(self, model_id=MODEL_ID, confidence=0.2):
        self.model = self.get_model(model_id)
        self.confidence = confidence
        self.bounding_box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()

    def get_model(self, model_id):
        # load a pre-trained yolov8n model
        return get_model(model_id=model_id)

    def detect_elements(self, image):
        # run inference on our chosen image, image can be a url, a numpy array, a PIL image, etc.
        results = self.model.infer(image, confidence=self.confidence)[0]

        # load the results into the supervision Detections api
        detections = sv.Detections.from_inference(results)

        # extract labels from the detections
        labels = [
            f"{class_name}"
            for class_name, confidence
            in zip(detections['class_name'], detections.confidence)
        ]

        # annotate the image with our inference results
        annotated_image = self.bounding_box_annotator.annotate(
            scene=image, detections=detections)
        annotated_image = self.label_annotator.annotate(
            scene=annotated_image, detections=detections, labels=labels)

        return annotated_image