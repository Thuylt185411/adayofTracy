import os
import cv2
import albumentations as A
from utils import clamp_keypoints, prepare_keypoint_dict,create_output_directories, keypoint_yolo
import random
import numpy as np

def add_gaussian_light(DIR_SRC, image_path, SAVE_DIR):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    image_name = image_path.split('/')[-1]
    print(f'{DIR_SRC}/images/{image_path}')
    img = cv2.imread(f'{DIR_SRC}/images/{image_path}')
    image_height, image_width = img.shape[:2]
    if image_width <= 400 or image_height <= 400:
        img = cv2.resize(img, (image_height*5, image_width*5))
        image_height, image_width = img.shape[:2]
    keypoint_dict = prepare_keypoint_dict(txt_path=f'{DIR_SRC}/labels/{image_name[:-4]}.txt', 
                                          image_height=image_height, 
                                          image_width=image_width)

    light_center_x = random.randint(200, image_width - 200)
    light_center_y = random.randint(200, image_height - 200)
    light_radius = random.randint(150, 300)  
    mask_light = np.zeros((image_height, image_width), dtype=np.float32)
    cv2.circle(mask_light, (light_center_x, light_center_y), light_radius, 255, -1)
    blurred_mask_light = cv2.GaussianBlur(mask_light, (0, 0), sigmaX=light_radius * 2)  
    
    blurred_mask_light = blurred_mask_light / blurred_mask_light.max()

    light_intensity = random.uniform(0.5, 1.0)  
    light_effect = np.zeros_like(img, dtype=np.float32)
    
    for i in range(3):  
        channel = img[:, :, i].astype(np.float32) / 255.0
        light_channel = blurred_mask_light * light_intensity
        light_effect[:, :, i] = channel + light_channel

    final_result = np.clip(light_effect * 255.0, 0, 255).astype(np.uint8)
    

    output_path = f'{SAVE_DIR}/add_gaussian_light'
    if not os.path.exists(output_path):
        os.makedirs(f'{output_path}/images')
        os.makedirs(f'{output_path}/labels')

    output_path = create_output_directories(SAVE_DIR, subdir='add_gaussian_light')
    
    new_height, new_width, _ = final_result.shape
    keypoint_dict['2'] = clamp_keypoints(keypoints=keypoint_dict['2'], 
                                         height=new_height,
                                         width=new_width, 
                                         )
    keypoint_dict['3'] = clamp_keypoints(keypoints=keypoint_dict['3'], 
                                         height=new_height,
                                         width=new_width, 
                                         )
    keypoints1 = keypoint_yolo(keypoint_dict['2'], 
                               new_width=new_width, 
                               new_height=new_height)
    keypoints2 = keypoint_yolo(keypoint_dict['3'], 
                               new_width=new_width, 
                               new_height=new_height)

    save_path = f'{output_path}/images/{image_name[:-4]}light.jpg'
    txt_path = f'{output_path}/labels/{image_name[:-4]}light.txt'

    #luu keypoint và ảnh
    with open(txt_path, 'w') as f:
        text1 = '2 ' + ' '.join(f'{x} {y}' for x, y in keypoints1)
        text2 = '3 ' + ' '.join(f'{x} {y}' for x, y in keypoints2)
        f.write(text1 + '\n')
        f.write(text2)
    cv2.imwrite(save_path, final_result)
    file_name = save_path.split('/')[-1]

    return new_width, new_height, file_name, save_path, {
        'transform': {
            'light': [light_center_x, light_center_y, light_radius, light_intensity]
        }
    }