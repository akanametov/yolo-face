import torch

from ultralytics import YOLO


def test_model_init():
    model = YOLO.new("yolov8n.yaml")
    model.info()
    try:
        YOLO()
    except Exception:
        print("Successfully caught constructor assert!")
    raise Exception("constructor error didn't occur")


def test_model_forward():
    model = YOLO.new("yolov8n.yaml")
    img = torch.rand(512 * 512 * 3).view(1, 3, 512, 512)
    model.forward(img)
    model(img)


def test_model_info():
    model = YOLO.new("yolov8n.yaml")
    model.info()
    model = model.load("best.pt")
    model.info(verbose=True)


def test_model_fuse():
    model = YOLO.new("yolov8n.yaml")
    model.fuse()
    model.load("best.pt")
    model.fuse()


def test_visualize_preds():
    model = YOLO.load("best.pt")
    model.predict(source="ultralytics/assets")


def test_val():
    model = YOLO.load("best.pt")
    model.val(data="coco128.yaml", imgsz=32)


def test_model_resume():
    model = YOLO.new("yolov8n.yaml")
    model.train(epochs=1, imgsz=32, data="coco128.yaml")
    try:
        model.resume(task="detect")
    except AssertionError:
        print("Successfully caught resume assert!")


def test_model_train_pretrained():
    model = YOLO.load("best.pt")
    model.train(data="coco128.yaml", epochs=1, imgsz=32)
    model = model.new("yolov8n.yaml")
    model.train(data="coco128.yaml", epochs=1, imgsz=32)
    img = torch.rand(512 * 512 * 3).view(1, 3, 512, 512)
    model(img)


def test_exports():
    """
                       Format     Argument           Suffix    CPU    GPU
    0                 PyTorch            -              .pt   True   True
    1             TorchScript  torchscript     .torchscript   True   True
    2                    ONNX         onnx            .onnx   True   True
    3                OpenVINO     openvino  _openvino_model   True  False
    4                TensorRT       engine          .engine  False   True
    5                  CoreML       coreml         .mlmodel   True  False
    6   TensorFlow SavedModel  saved_model     _saved_model   True   True
    7     TensorFlow GraphDef           pb              .pb   True   True
    8         TensorFlow Lite       tflite          .tflite   True  False
    9     TensorFlow Edge TPU      edgetpu  _edgetpu.tflite  False  False
    10          TensorFlow.js         tfjs       _web_model  False  False
    11           PaddlePaddle       paddle    _paddle_model   True   True
    """
    from ultralytics import YOLO
    from ultralytics.yolo.engine.exporter import export_formats

    print(export_formats())

    model = YOLO.new("yolov8n.yaml")
    model.export(format='torchscript')
    model.export(format='onnx')
    model.export(format='openvino')
    model.export(format='coreml')
    model.export(format='paddle')


def test():
    test_model_forward()
    test_model_info()
    test_model_fuse()
    test_visualize_preds()
    test_val()
    test_model_resume()
    test_model_train_pretrained()


if __name__ == "__main__":
    test()