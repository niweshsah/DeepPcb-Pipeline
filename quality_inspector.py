import cv2
import sys
import argparse
import numpy as np
from pathlib import Path
from ultralytics import YOLO

# --- DEFAULT PATHS ---
DEFAULT_MODEL = "./best_yolo_pcb.pt"
DEFAULT_INPUT = "./test_images/images/00041001_test.jpg"

class DeepPCBInspector:
    def __init__(self, model_path: str, conf_threshold: float = 0.45):
        self.conf_threshold = conf_threshold
        try:
            print(f"Loading DeepPCB Model: {model_path}...")
            self.model = YOLO(model_path)
            if hasattr(self.model, 'names'):
                print(f"Model classes detected: {self.model.names}")
        except Exception as e:
            print(f"CRITICAL ERROR: Failed to load model at {model_path}. \n{e}")
            sys.exit(1)

    def calculate_severity(self, label: str, box_area: float, img_area: float) -> str:
        label = label.lower()
        if label in ['open', 'short']:
            return "CRITICAL"
        if label in ['mousebite', 'spur']:
            return "HIGH"
        
        relative_size = (box_area / img_area) * 100
        return "MODERATE" if relative_size > 1.0 else "LOW"

    def analyze_image(self, image_path: Path, output_dir: Path):
        """Run inference on a single Deep PCB image."""
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"Error: Could not read image {image_path.name}")
            return

        img_h, img_w, _ = img.shape
        img_area = img_h * img_w
        
        print(f"\n--- Inspecting: {image_path.name} ---")
        results = self.model(img, conf=self.conf_threshold, verbose=False)[0]
        
        detections = len(results.boxes)
        
        if detections == 0:
            print("Result: PASS")
            self._annotate_pass(img)
        else:
            print(f"Result: FAIL - {detections} defects found.")
            for i, box in enumerate(results.boxes):
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                severity = self.calculate_severity(label, (x2-x1)*(y2-y1), img_area)
                self._draw_annotation(img, label, severity, x1, y1, x2, y2)

        output_path = output_dir / f"checked_{image_path.name}"
        cv2.imwrite(str(output_path), img)
        print(f"Saved to: {output_path}")

    def _draw_annotation(self, img, label, severity, x1, y1, x2, y2):
        colors = {"CRITICAL": (0, 0, 255), "HIGH": (0, 165, 255), "MODERATE": (0, 255, 255), "LOW": (0, 255, 255)}
        color = colors.get(severity, (0, 255, 0))
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        label_text = f"{label.upper()} [{severity}]"
        (w, h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - 20), (x1 + w, y1), color, -1)
        cv2.putText(img, label_text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)

    def _annotate_pass(self, img):
        cv2.putText(img, "QA: PASS", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

def main():
    parser = argparse.ArgumentParser(description="DeepPCB Automated Defect Inspection Tool")
    
    # Arguments with defaults
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, 
                        help=f"Path to YOLO model (Default: {DEFAULT_MODEL})")
    parser.add_argument("--input", type=str, default=DEFAULT_INPUT, 
                        help=f"Path to image or directory (Default: {DEFAULT_INPUT})")
    parser.add_argument("--output", type=str, default="results", 
                        help="Directory to save output images (Default: results)")
    parser.add_argument("--conf", type=float, default=0.45, 
                        help="Confidence threshold (Default: 0.45)")

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    inspector = DeepPCBInspector(args.model, args.conf)

    if input_path.is_file():
        inspector.analyze_image(input_path, output_dir)
    elif input_path.is_dir():
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
        images = [f for f in input_path.iterdir() if f.suffix.lower() in valid_extensions]
        if not images:
            print(f"No valid images found in {input_path}")
            return
        print(f"Found {len(images)} images. Processing...")
        for img_p in images:
            inspector.analyze_image(img_p, output_dir)
    else:
        print(f"Error: Path {args.input} does not exist.")

if __name__ == "__main__":
    main()