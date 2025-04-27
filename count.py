import torch
import cv2
from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_boxes
from utils.torch_utils import select_device

# Load model
weights = 'yolov5s.pt'
img_size = 640
conf_thres = 0.25
iou_thres = 0.45
known_conf_thres = 0.5
device = select_device('')
model = attempt_load(weights, device=device)
stride = int(model.stride.max())
model.eval()

classes = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
    'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
    'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
    'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
    'hair drier', 'toothbrush'
]

def count_objects(source='0'):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Fixed indentation
    while True:
        ret, img = cap.read()
        if not ret:
            print("Camera failed")
            break
        img_orig = img.copy()
        img = cv2.resize(img, (img_size, img_size))
        img = img[:, :, ::-1].copy()
        img = torch.from_numpy(img).to(device).float() / 255.0
        img = img.permute(2, 0, 1).unsqueeze(0)

        pred = model(img)[0]
        pred = non_max_suppression(pred, conf_thres, iou_thres)

        counts = {'person': 0, 'cell phone': 0, 'unknown': 0}
        if pred[0] is not None:
            det = pred[0]
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img_orig.shape).round()
            for *xyxy, conf, cls in det:
                label = classes[int(cls)]
                conf_score = conf.item()
                if label in ['person', 'cell phone'] and conf_score >= known_conf_thres:
                    counts[label] += 1
                elif conf_score < known_conf_thres and conf_score >= conf_thres:
                    counts['unknown'] += 1
                    label = 'unknown'
                x1, y1, x2, y2 = map(int, xyxy)
                cv2.rectangle(img_orig, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img_orig, f'{label} {conf_score:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        y = 30
        for item, count in counts.items():
            cv2.putText(img_orig, f'{item}: {count}', (10, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            y += 30
        print(counts)

        cv2.imshow('Object Counter', img_orig)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    count_objects()