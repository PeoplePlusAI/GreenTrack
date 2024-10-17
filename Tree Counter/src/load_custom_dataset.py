import os
import cv2 
import numpy as np
from matplotlib import pyplot as plt 
from matplotlib.patches import Rectangle

def convert_yolo_bbox_info(img_w, img_h,x,y,w,h):
    box = np.zeros(4)
    dw = 1./img_w
    dh = 1./img_h
    x = x/dw
    w = w/dw
    y = y/dh
    h = h/dh
    
    # top left corner of rect
    box[0] = x-(w/2.0)
    box[1] = y-(h/2.0)
    
    # bottom right corner of rect
    box[2] = x+(w/2.0)
    box[3] = y+(h/2.0)

    return box.round().astype(int)

def load_yolo_one_file(labels_file_path, img_size):
    bboxes = []
    txt_file = open(labels_file_path, "r")
    
    # Read labels from text file
    lines = txt_file.read().splitlines()
    for line in lines:
        value = line.split()
        x, y, w, h = list(map(float, value[1:]))
        bb = convert_yolo_bbox_info(img_size[1], img_size[0], x, y, w, h)
        bboxes.append(bb)
    
    return bboxes
    
def load_yolo_dataset():
    labels_path = './data/dataset/train/labels/'
    imgs_path = './data/dataset/train/images/'
    # Get yolo txt file list
    labels_file_list = []
    for file in os.listdir(labels_path):
        if file.endswith(".txt"):
            labels_file_list.append(file)
        
    bboxes_data = dict()
    
    for label_file_name in labels_file_list:
        img_file_name = label_file_name.rstrip(".txt") + ".jpg"
        img_file_path = imgs_path + img_file_name
        img = cv2.imread(img_file_path)
        
        bboxes = load_yolo_one_file(labels_path+label_file_name, img.shape[:2])
        
        bboxes_data[label_file_name] = bboxes
    
    return bboxes_data

def visualize_one_file(label_file_path, img_file_path):
    img = cv2.imread(img_file_path)
    
    bboxes = load_yolo_one_file(label_file_path, img.shape[:2])
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    # Plot the original image on the first subplot
    axes[0].imshow(img)
    axes[0].set_title('Original image')
    axes[0].axis('off')  # Hide axes
    
    # Plot the cropped color image on the second subplot
    bbox = bboxes[0]
    cropped_img = img[bbox[1]:bbox[3], bbox[0]:bbox[2],:]
    axes[1].imshow(cropped_img)
    axes[1].set_title('Cropped color image')
    axes[1].axis('off')  # Hide axes
    
    # Plot the cropped color image on the second subplot
    cropped_img = cv2.resize(cropped_img,(32,32))
    cropped_img = cv2.cvtColor(cropped_img, cv2.COLOR_RGB2GRAY)
    
    axes[2].imshow(cropped_img, cmap='gray')
    axes[2].set_title('Cropped gray resized image')
    axes[2].axis('off')  # Hide axes
    
    # plt.imshow(img)
    # bbox = bboxes[0]
    # plt.gca().add_patch(Rectangle((bbox[0],bbox[1]),bbox[2]-bbox[0],bbox[3]-bbox[1],
    #                               edgecolor='red',
    #                               facecolor='none',
    #                               lw=4))
    # img = img[bbox[1]:bbox[3], bbox[0]:bbox[2],:]
    
    plt.show()
    #return bboxes
    
    
if __name__ == '__main__':
    label_file_path = './data/dataset/train/labels/landscape3.txt'
    img_file_path = './data/dataset/train/images/landscape3.jpg'
    visualize_one_file(label_file_path, img_file_path)
    #print(len(bboxes))