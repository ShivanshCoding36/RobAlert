print("Started")
import cv2
print("Library Imported")
import numpy as np
print("Library Imported")
from alerting import alertFunc
print("Library Imported")
from ArduinoAlert import SendCommandToArduino
print("Library Imported")
import time
print("Library Imported")
# Load Yolo

net = cv2.dnn.readNet("yolov3_training_2000.weights", "yolov3_testing.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
classes = ["Weapon"]
print("Model Loaded")


cap = cv2.VideoCapture(0)
print("Starting Loop")
startedTime = time.time() - 1800
while True:
    _, img = cap.read()
    height, width, channels = img.shape
    # width = 512
    # height = 512

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    
    layer_names = net.getLayerNames()

    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    outs = net.forward(output_layers)

    # Showing information on the screen
    class_ids = []
    confidences = []
    boxes = []
    if outs:
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    print(class_ids)
    if indexes == 0: 
        cTime = time.time() - startedTime
        if cTime >= 1800:
            print("weapon detected in frame")
            alertFunc(["Weapon",str(time.time())])
            SendCommandToArduino('w')
            fName = f"WeaponAt{time.time()}.png"
            cv2.imwrite(fName,img)
            startedTime = time.time()
        
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 3)

    # frame = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    cv2.imshow("Image", img)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()
