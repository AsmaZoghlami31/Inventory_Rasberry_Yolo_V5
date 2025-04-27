import cv2
import os

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Couldn’t open webcam.")
    exit()

save_dir = r"C:\Users\zoghl\Projects\YOLO\yolov5\dataset\images\train"
os.makedirs(save_dir, exist_ok=True)
# Find the highest existing number
existing_files = [f for f in os.listdir(save_dir) if f.startswith('img_') and f.endswith('.jpg')]
count = max([int(f.split('_')[1].split('.jpg')[0]) for f in existing_files] + [0]) + 1 if existing_files else 0

print("Press 's' to save, 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture.")
        break
    cv2.imshow('Capture', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        filename = f"{save_dir}\\img_{count}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")
        count += 1
    elif key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
print(f"Captured {count} images.")