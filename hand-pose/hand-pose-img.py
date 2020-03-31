import cv2 as cv
import numpy as np

protoFile = "model/pose_deploy.prototxt"
weightsFile = "model/pose_iter_102000.caffemodel"

num_points = 22

threshold = 0.1

POSE_PAIRS = [
        [0,1],[1,2],[2,3],[3,4],
        [0,5],[5,6],[6,7],[7,8],
        [0,9],[9,10],[10,11],[11,12],
        [0,13],[13,14],[14,15],[15,16],
        [0,17],[17,18],[18,19],[19,20]
]

frame = cv.imread("input/front-back.jpg")

frame_copy = np.copy(frame)

# Create net from already trained model
net = cv.dnn.readNetFromCaffe(protoFile, weightsFile)

# Get image dimensions
frame_width = frame.shape[1]
frame_height = frame.shape[0]

aspect_ratio = frame_width/frame_height

# Input network image dimensions
in_height = 368
in_width = int(((aspect_ratio * in_height) * 8) // 8)

# Get image BLOB
img_blob = cv.dnn.blobFromImage(
        frame,
        scalefactor=1.0/255,
        size=(in_width, in_height),
        mean=(0,0,0),
        swapRB=False,
        crop=False
)

# Set input for network and make prediction
net.setInput(img_blob)

output = net.forward()

# Draw points
points = []

for i in range(num_points):
    #
    prob_map = output[0, i, :, :]
    prob_map = cv.resize(prob_map, (frame_width, frame_height))

    min_val, prob, min_loc, point = cv.minMaxLoc(prob_map) # finds the global min and max


    if prob > threshold:
        points.append((int(point[0]), int(point[1])))

    else:
        points.append(None)

# Draw skeleton
for pair in POSE_PAIRS:
    start = pair[0]
    end = pair[1]

    if points[start] and points[end]:
        cv.line(
                img=frame_copy,
                pt1=points[start],
                pt2=points[end],
                color=(0, 255, 255),
                thickness=2
        )

        cv.circle(
                img=frame_copy,
                center=points[start],
                radius=8,
                color=(0, 0, 255),
                thickness=-1,
                lineType=cv.FILLED
        )

        cv.circle(
                img=frame_copy,
                center=points[end],
                radius=8,
                color=(0, 0, 255),
                thickness=-1,
                lineType=cv.FILLED
        )



cv.imshow("Skeleton + Keypoints", frame_copy)

cv.waitKey(0)
cv.destroyAllWindows()
