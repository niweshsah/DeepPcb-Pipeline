

# Automated Quality Inspection System for PCB Manufacturing

## Project Overview

This repository contains the solution for **Question 2: Automated Quality Inspection System for Manufacturing**. The project implements a computer vision-based quality assurance tool designed to detect, classify, and assess defects on Printed Circuit Boards (PCBs).

Using a fine-tuned YOLOv8 model, the system analyzes images of bare PCBs to identify common manufacturing faults such as open circuits, shorts, mousebites, and spurs. The system automatically localizes these defects, assigns a severity level based on industry standards, and generates annotated visual reports.

## Features

* **Automated Defect Detection:** Utilizes the YOLO architecture for real-time inference on high-resolution PCB images.
* **Multi-Class Classification:** Capable of identifying multiple specific defect types including Open, Short, Mousebite, Spur, Copper, and Pin-hole.
* **Dynamic Severity Assessment:** Implements logic to classify defect severity (CRITICAL, HIGH, MODERATE, LOW) based on the defect type and its relative surface area.
* **Visual Annotation:** Outputs images with color-coded bounding boxes and labels for immediate visual verification.

## Directory Structure

```text
.
├── quality_inspector.py    # Main inspection script
├── environment.yml         # Conda environment configuration file
├── README.md               # Project documentation
├── test_images/            # Source directory for validation images
│   ├── images/             # Raw test images
│   └── labels/             # Ground truth labels
└── results/                # Output directory for annotated images

```

*Note: The model weights file (`best_yolo_pcb.pt`) must be downloaded separately due to file size constraints.*

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/niweshsah/DeepPcb-Pipeline.git
cd DeepPcb-Pipeline

```

### 2. Install Dependencies

```bash
pip install ultralytics opencv-python numpy

```

### 3. Download Model Weights

Because the trained model file exceeds GitHub's standard file size limit (100MB), it is hosted as a Release Asset.

1. Navigate to the [Releases](https://www.google.com/search?q=https://github.com/niweshsah/DeepPcb-Pipeline/releases) page of this repository.
2. Locate the latest release (e.g., `v1.0.0`).
3. Download the `best_yolo_pcb.pt` file.
4. Place the downloaded file directly into the root directory of this project.

## Usage

The `quality_inspector.py` script accepts command-line arguments to specify the model path, input source, and output destination.

### Basic Execution

To run the inspector using the downloaded model and default test image:

```bash
python quality_inspector.py --model ./best_yolo_pcb.pt

```

### Batch Processing

To inspect all images in the test directory:

```bash
python quality_inspector.py --model ./best_yolo_pcb.pt --input ./test_images/images --output ./results

```

### Command Line Arguments

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `--model` | str | `./best_yolo_pcb.pt` | Path to the downloaded YOLO model weights. |
| `--input` | str | `./test_images/images/...` | Path to an image or directory. |
| `--output` | str | `results` | Directory to save annotated results. |
| `--conf` | float | `0.45` | Confidence threshold (0.0 - 1.0). |

## Methodology

### 1. Defect Detection (YOLOv8)

The core detection engine uses the YOLOv8 architecture fine-tuned on the DeepPCB dataset. It identifies distinct visual anomalies including geometric irregularities and connectivity issues.

### 2. Severity Logic

Defect severity is calculated using the following criteria:

* **CRITICAL:** Functional failures such as **Open** circuits or **Short** circuits.
* **HIGH:** Structural defects like **Mousebites** and **Spurs**.
* **MODERATE/LOW:** Cosmetic defects. If a minor defect exceeds 1% of the total image area, it is elevated to Moderate.

### 3. Localization and Annotation

Coordinates for each defect are extracted and rendered as color-coded bounding boxes:

* **Red:** Critical Severity
* **Orange:** High Severity
* **Yellow/Cyan:** Moderate/Low Severity

## Sample Results

**Example Console Output:**

```text
Loading DeepPCB Model: ./best_yolo_pcb.pt...
Model classes detected: {0: 'open', 1: 'short', 2: 'mousebite', 3: 'spur', ...}

--- Inspecting: 00041000_test.jpg ---
Result: FAIL - 2 defects found.
Saved to: results/checked_00041000_test.jpg

```

**Annotated Visual Samples:**
The following images illustrate the system's ability to localize and classify defects:

---

### Would you like me to...

Help you write a `.gitignore` file to ensure the 147MB model file doesn't accidentally get included in your next `git push`?

![Output 1](images/checked_00041000_temp.png)
![Output 2](images/checked_00041000_test.png)
![Output 3](images/checked_00041001_test.png)
![Output 3](images/checked_00041002_temp.png)