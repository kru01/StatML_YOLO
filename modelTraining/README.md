# YOLO Model Training

Datasets:
-   Source: [Open Images Dataset V7](https://storage.googleapis.com/openimages/web/index.html) and [Animals Detection Images Dataset](https://www.kaggle.com/datasets/antoreepjana/animals-detection-images-dataset).
-   Filtered: [Full dataset for my YOLO project](https://kaggle.com/datasets/276603f6effbe666aef9aa0c1df328ebed65a67af6de779faa4c312d199870a8).
-   The filtered dataset contain both the dataset for YOLOv4 and YOLOv8 model
-   The dataset for YOLOv4 is a subset of [Animals Detection Images Dataset] as our YOLOv4 model label annotation is not in YOLO format.
-   The dataset for YOLOv8 is from [Open Images Dataset V7]

## [Ultralytics' YOLOv8](https://docs.ultralytics.com/models/yolov8/)

-   The actual training was done on [Kaggle](https://www.kaggle.com/anphongtrannguyen).
-   Models should be saved to `../src/static/models`.

## [Tianxiaomo's pytorch-YOLOv4](https://github.com/Tianxiaomo/pytorch-YOLOv4)

-   The [training and model](https://kaggle.com/datasets/85f52bba94f35c7001e174b5a0c70e8199b84330b1a05f5091904f572463302c) were done and hosted on [Kaggle](https://www.kaggle.com/anphongtrannguyen).
-   This won't be implemented in the website, as it would be too convoluted, and the produced models are too large.
