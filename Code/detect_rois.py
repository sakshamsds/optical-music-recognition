# Import necessary libraries
from ultralytics import YOLO
import cv2

pre_trained = YOLO("./runs/detect/train/weights/best.pt")
results = pre_trained.predict('./test/images', save=True, save_txt=True, save_conf=True, conf=0.307, save_crop=True)
# at conf=0.307, we get our highest F1 score

# Load the test image
img = cv2.imread('./test/images/finding-you-1.png')

# Get the classes 
class_dict = {
    0: 'half',
    1: 'quarter',
    2: 'whole'
}
classes = results[0].boxes.cls.cpu().numpy()

# Get bounding box tensor sorted by Y coordinate
bbox_tensor = results[0].boxes.xyxy
bbox_tensor = bbox_tensor[bbox_tensor[:, 1].argsort()]
min_box_height = min(results[0].boxes.xywh[:, 3]).item()     # 69

# Group bounding boxes by Y coordinate
groups = []
current_group = []
for i in range(len(bbox_tensor)):
    if i == 0:
        current_group.append(bbox_tensor[i])
    else:
        if bbox_tensor[i][1] - bbox_tensor[i-1][1] < min_box_height:
            current_group.append(bbox_tensor[i])
        else:
            groups.append(current_group)
            current_group = [bbox_tensor[i]]
    
# Add last group to groups list
groups.append(current_group)

# Sort each group by X min coordinate
for group_idx, group in enumerate(groups):
    group.sort(key=lambda bbox: bbox[0])
    
    # Iterate over the bounding boxes in the group and save them
    for bbox_idx, bbox in enumerate(group):
        
        # Get the coordinates of the bounding box
        x1, y1, x2, y2 = bbox.tolist()

        # Get ROI and save it
        roi = img[int(y1):int(y2), int(x1):int(x2)]
        
        label = class_dict[classes[bbox_idx]]
        cv2.imwrite('./results/group_{}_bbox_{}_{}.png'.format(group_idx+1, bbox_idx+1, label), roi)