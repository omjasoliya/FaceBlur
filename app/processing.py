import json
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
from PIL.ImageFilter import GaussianBlur
import comet_ml
from ultralytics import SAM
from transformers import pipeline

# Initialize SAM model
SAM_version = "mobile_sam.pt"
model = SAM(SAM_version)
comet_ml.init(anonymous=True, project_name="4: OWL-ViT + SAM")
detector = pipeline(
    model= "google/owlvit-base-patch32",
    task="zero-shot-object-detection"
)

# Function to preprocess outputs
def preprocess_outputs(output):
    input_scores = [x["score"] for x in output]
    input_labels = [x["label"] for x in output]
    input_boxes = []
    for i in range(len(output)):
        input_boxes.append([*output[i]["box"].values()])
    input_boxes = [input_boxes]
    return input_scores, input_labels, input_boxes


# add function for img resizing (Up to 1024 Pixels)
def resize_image(raw_image, max_width=1020):
    if raw_image.size[0] > max_width:
        wpercent = max_width / float(raw_image.size[0])
        hsize = int(float(raw_image.size[1]) * wpercent)
        raw_image = raw_image.resize((max_width, hsize), Image.ANTIALIAS)
    return raw_image

# Function to preprocess outputs
def preprocess_outputs(output):
    input_scores = [x["score"] for x in output]
    input_labels = [x["label"] for x in output]
    input_boxes = []
    for i in range(len(output)):
        input_boxes.append([*output[i]["box"].values()])
    input_boxes = [input_boxes]
    return input_scores, input_labels, input_boxes

# Function to process image
def process_image(raw_image):
    max_width=1020
    if raw_image.size[0] > max_width:
        wpercent = max_width / float(raw_image.size[0])
        hsize = int(float(raw_image.size[1]) * wpercent)
        raw_image = raw_image.resize([max_width, hsize])
        # if any error occurs so remove this upper portion till def fun thnkyou !
    try:
        # Perform detection (placeholder, replace with actual detection logic)
        candidate_labels = ["human face"]
        output = detector(raw_image, candidate_labels=candidate_labels)  # Replace 'detector' with actual detection logic
        input_scores, input_labels, input_boxes = preprocess_outputs(output)

        # Predict masks
        result = model.predict(raw_image, bboxes=input_boxes[0], labels=np.repeat(1, len(input_boxes[0])))

        # Apply Gaussian blur and create output image
        blurred_img = raw_image.filter(ImageFilter.GaussianBlur(radius=5))

        # Ensure masks are not empty and check shapes
        masks = result[0].masks.data.cpu().numpy()
        if masks.size == 0:
            raise ValueError("No masks found in the prediction results.")

        total_mask = np.zeros(masks[0].shape)
        for mask in masks:
            total_mask = np.add(total_mask, mask)

        output = np.where(
            np.expand_dims(total_mask != 0, axis=2),
            np.array(blurred_img),
            np.array(raw_image)
        )

        output_image = Image.fromarray(output.astype('uint8'))
        return output_image
    except Exception as e:
        raise ValueError(f"Error processing image: Add Appropriate Images")
