import cv2, random, os, time, imutils
import numpy as np
from tensorflow.keras.models import load_model

# Allow GPU growth if TensorFlow is using GPU
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

# Load YOLO network
net = cv2.dnn.readNet("yolov3-custom_7000.weights", "yolov3-custom.cfg")

# Try CUDA, fallback to CPU if not available
try:
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
except:
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Load CNN helmet model
model = load_model('helmet-nonhelmet_cnn.h5')
print('Model loaded!!!')

# Load video
cap = cv2.VideoCapture('testing videos/test2.mp4')
COLORS = [(0, 255, 0), (0, 0, 255)]  # green and red

# Helmet classification function
def helmet_or_nonhelmet(helmet_roi):
    try:
        helmet_roi = cv2.resize(helmet_roi, (224, 224))
        helmet_roi = np.array(helmet_roi, dtype='float32')
        helmet_roi = helmet_roi.reshape(1, 224, 224, 3)
        helmet_roi = helmet_roi / 255.0
        return int(model.predict(helmet_roi)[0][0])
    except Exception as e:
        print(f"Prediction error: {e}")
        return None

# Get YOLO output layers
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Process video
while True:
    ret, img = cap.read()
    if not ret:  # stop when video ends
        break

    # Resize frame to manageable size
    img = imutils.resize(img, height=550)

    # TODO: add YOLO detection + helmet classification here
    # For now, just show the frame
    cv2.imshow("Frame", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()