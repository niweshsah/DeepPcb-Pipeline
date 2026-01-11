

# Automated Quality Inspection System for PCB Manufacturing

## Project Overview

This repository contains the solution for **Question 2: Automated Quality Inspection System for Manufacturing**. The project implements a computer vision-based quality assurance tool designed to detect, classify, and assess defects on Printed Circuit Boards (PCBs).

Using a fine-tuned YOLOv8 model, the system analyzes images of bare PCBs to identify common manufacturing faults such as open circuits, shorts, mousebites, and spurs. The system automatically localizes these defects, assigns a severity level based on industry standards, and generates annotated visual reports.

## Features

* **Automated Defect Detection:** Utilizes the YOLO (You Only Look Once) architecture for real-time inference on high-resolution PCB images.
* **Multi-Class Classification:** Capable of identifying multiple specific defect types including Open, Short, Mousebite, Spur, Copper, and Pin-hole.
* **Dynamic Severity Assessment:** Implements logic to classify defect severity (CRITICAL, HIGH, MODERATE, LOW) based on the defect type and its relative surface area.
* **Visual Annotation:** Outputs images with color-coded bounding boxes and labels for immediate visual verification by QA engineers.
* **Batch Processing:** Supports processing individual image files or entire directories of test samples.

## Directory Structure

```text
folder/
├── best_yolo_pcb.pt        # Fine-tuned YOLO weights for PCB defect detection
├── environment.yml         # Conda environment configuration file
├── quality_inspector.py    # Main inspection script
├── README.md               # Project documentation
├── test_images/            # Source directory for validation images
│   ├── images/             # Raw test images
│   └── labels/             # Ground truth labels (if applicable)
└── results/                # Output directory for annotated images (generated at runtime)

```

## Installation

### Prerequisites

* Python 3.8 or higher
* Ultralytics (YOLOv8)
* OpenCV
* NumPy

### Setup

It is recommended to use a virtual environment. You can install the required dependencies using the provided `environment.yml` or via pip:

```bash
pip install ultralytics opencv-python numpy

```

## Usage

The `quality_inspector.py` script serves as the main entry point. It accepts command-line arguments to specify the model path, input source, and output destination.

### Basic Execution

To run the inspector on the default test image defined in the script:

```bash
python quality_inspector.py

```

### Batch Processing

To inspect a directory of images (e.g., the provided `test_images/images` folder) and save results to a `results` folder:

```bash
python quality_inspector.py --input ./test_images/images --output ./results

```

### Custom Model or Confidence Threshold

To use a specific model weight or adjust the detection sensitivity:

```bash
python quality_inspector.py --model ./best_yolo_pcb.pt --conf 0.5

```

### Command Line Arguments

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `--model` | str | `./best_yolo_pcb.pt` | Path to the trained YOLO model weights. |
| `--input` | str | `./test_images/images/...` | Path to a single image or a directory of images. |
| `--output` | str | `results` | Directory where processed images will be saved. |
| `--conf` | float | `0.45` | Confidence threshold for defect detection (0.0 - 1.0). |

## Methodology

### 1. Defect Detection (YOLOv8)

The core detection engine is based on the Ultralytics YOLOv8 architecture. The model `best_yolo_pcb.pt` has been trained on the DeepPCB dataset to recognize distinct visual anomalies on circuit boards.

### 2. Severity Logic

The system goes beyond simple detection by calculating a severity score. This is defined in the `calculate_severity` method within the `DeepPCBInspector` class:

* **CRITICAL:** Applied to functional failures such as **Open** circuits (broken connections) and **Short** circuits (unintended connections).
* **HIGH:** Applied to structural defects like **Mousebites** and **Spurs** that may degrade signal integrity.
* **MODERATE/LOW:** Applied to other cosmetic or minor defects. If a minor defect exceeds 1% of the total image area, it is elevated to Moderate; otherwise, it remains Low.

### 3. Localization and Annotation

For every detected defect, the system extracts the bounding box coordinates . These coordinates are used to draw color-coded rectangles on the output image:

* **Red:** Critical Severity
* **Orange:** High Severity
* **Yellow/Cyan:** Moderate/Low Severity

## Results

Upon execution, the script reports the number of defects found per image in the console and saves the annotated images to the specified output directory.

**Example Console Output:**

```text
Loading DeepPCB Model: ./best_yolo_pcb.pt...
Model classes detected: {0: 'open', 1: 'short', 2: 'mousebite', 3: 'spur', ...}

--- Inspecting: 00041000_test.jpg ---
Result: FAIL - 2 defects found.
Saved to: results/checked_00041000_test.jpg

```

**Example Visual Output:**
The resulting images will contain bounding boxes clearly labeling the defect type (e.g., "OPEN [CRITICAL]") and its precise location on the PCB.

![Output 1](images/checked_00041000_temp.png)
![Output 2](images/checked_00041000_test.png)
![Output 3](images/checked_00041001_test.png)
![Output 3](images/checked_00041002_temp.png)