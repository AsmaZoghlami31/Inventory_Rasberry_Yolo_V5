@echo off
setlocal enabledelayedexpansion

echo Merging images to train...
cd C:\Users\zoghl\Projects\YOLO\yolov5\datasets\coco\filtered_images
set count=61
for /L %%i in (1,1,39) do (
    for /F "tokens=1" %%j in ('dir /b *.jpg') do (
        copy "%%j" "C:\Users\zoghl\Projects\YOLO\yolov5\dataset\images\train\img_!count!.jpg"
        del "%%j"
        set /a count+=1
        goto :next_train
    )
    :next_train
)

echo Merging images to val...
cd C:\Users\zoghl\Projects\YOLO\yolov5\datasets\coco\filtered_images
set count=100
for /L %%i in (1,1,10) do (
    for /F "tokens=1" %%j in ('dir /b *.jpg') do (
        copy "%%j" "C:\Users\zoghl\Projects\YOLO\yolov5\dataset\images\val\img_!count!.jpg"
        del "%%j"
        set /a count+=1
        goto :next_val
    )
    :next_val
)

echo Merging labels to train...
cd C:\Users\zoghl\Projects\YOLO\yolov5\datasets\coco\filtered_labels
set count=61
for /L %%i in (1,1,39) do (
    for /F "tokens=1" %%j in ('dir /b *.txt') do (
        copy "%%j" "C:\Users\zoghl\Projects\YOLO\yolov5\dataset\labels\train\img_!count!.txt"
        del "%%j"
        set /a count+=1
        goto :next_train_label
    )
    :next_train_label
)

echo Merging labels to val...
cd C:\Users\zoghl\Projects\YOLO\yolov5\datasets\coco\filtered_labels
set count=100
for /L %%i in (1,1,10) do (
    for /F "tokens=1" %%j in ('dir /b *.txt') do (
        copy "%%j" "C:\Users\zoghl\Projects\YOLO\yolov5\dataset\labels\val\img_!count!.txt"
        del "%%j"
        set /a count+=1
        goto :next_val_label
    )
    :next_val_label
)

echo Merge complete!
endlocal
pause