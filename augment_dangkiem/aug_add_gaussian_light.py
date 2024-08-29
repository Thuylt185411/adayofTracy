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
    img = cv2.imread(f'{DIR_SRC}/images/{image_path}')
    height, width = img.shape[:2]

    light_center_x = random.randint(200, width - 200)
    light_center_y = random.randint(200, height - 200)
    light_radius = random.randint(150, 300)
    mask_light = np.zeros((height, width), dtype=np.float32)
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
    new_width, new_height, _ = final_result.shape

    output_path = f'{SAVE_DIR}/add_gaussian_light'
    if not os.path.exists(output_path):
        os.makedirs(f'{output_path}/images')
        os.makedirs(f'{output_path}/labels')

    keypoint_dict = {}  # Load keypoints from file
    keypoint_dict['2'] = clamp_keypoints(keypoint_dict['2'], new_width, new_height)
    keypoint_dict['3'] = clamp_keypoints(keypoint_dict['3'], new_width, new_height)
    new_segmentation1 = [coord for point in keypoint_dict['2'] for coord in point]
    new_segmentation2 = [coord for point in keypoint_dict['3'] for coord in point]
    keypoints1 = [((float(new_segmentation1[i]) / new_width), 
                   (float(new_segmentation1[i + 1]) / new_height)) 
                  for i in range(0, len(new_segmentation1), 2)]
    keypoints2 = [((float(new_segmentation2[i]) / new_width), 
                   (float(new_segmentation2[i + 1]) / new_height)) 
                  for i in range(0, len(new_segmentation2), 2)]
    save_path = f'{output_path}/images/{image_name[:-4]}light.jpg'
    txt_path = f'{output_path}/labels/{image_name[:-4]}light.txt'

    with open(txt_path, 'w') as f:
        text1 = '2'
        for x, y in keypoints1:
            text1 += f' {x} {y}'
        text2 = '3'
        for x, y in keypoints2:
            text2 += f' {x} {y}'
        f.write(text1 + '\n')
        f.write(text2)
    cv2.imwrite(save_path, final_result)
    file_name = save_path.split('/')[-1]

    return new_width, new_height, file_name, save_path, {
        'transform': {
            'light': [light_center_x, light_center_y, light_radius, light_intensity]
        }
    }