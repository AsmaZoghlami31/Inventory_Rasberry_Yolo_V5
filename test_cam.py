import cv2
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # DirectShow backend
print(cap.isOpened())
if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Test', frame)
        cv2.waitKey(0)
    else:
        print("Failed to grab frame")
    cap.release()
cv2.destroyAllWindows()