import os
import cv2
import albumentations as A
from utils import clamp_keypoints, prepare_keypoint_dict,create_output_directories, keypoint_yolo

def rotate_augment(DIR_SRC, image_path, SAVE_DIR, rotate_degree):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    image_name = image_path.split('/')[-1]
    image = cv2.imread(f'{DIR_SRC}/images/{image_path}')
    image_height, image_width = image.shape[:2]
    keypoint_dict = prepare_keypoint_dict(txt_path=f'{DIR_SRC}/labels/{image_name[:-4]}.txt', 
                                          image_height=image_height, 
                                          image_width=image_width)
    
    augmentations = A.Compose([
        A.RandomBrightnessContrast(p=0.3),
        A.Affine(rotate=[rotate_degree, rotate_degree], p=1, mode=cv2.BORDER_CONSTANT, fit_output=True),
    ], keypoint_params=A.KeypointParams(format='xy', remove_invisible=True),
        additional_targets={'image': 'image', 'keypoints1': 'keypoints', 'keypoints2': 'keypoints'},
    )

    keypoint_dict['2'] = clamp_keypoints(keypoints=keypoint_dict['2'], 
                                         height=image_height,
                                         width=image_width, 
                                         )
    keypoint_dict['3'] = clamp_keypoints(keypoints=keypoint_dict['3'], 
                                         height=image_height,
                                         width=image_width, 
                                         )
    transformed = augmentations(image=image, 
                                keypoints1=keypoint_dict['2'], 
                                keypoints2 = keypoint_dict['3']
                            )
    
    transformed_image = transformed['image']
    transformed_keypoints1 = transformed['keypoints1']
    transformed_keypoints2 = transformed['keypoints2']

    new_height, new_width = transformed_image.shape[:2]
    
    keypoints1 = keypoint_yolo(transformed_keypoints1, 
                               new_width=new_width, 
                               new_height=new_height)
    keypoints2 = keypoint_yolo(transformed_keypoints2, 
                               new_width=new_width, 
                               new_height=new_height)
    des_keypoint_dict = {'2': keypoints1,
                         '3': keypoints2}

    output_path = create_output_directories(SAVE_DIR, subdir=str(rotate_degree))
    
    save_path = f'{output_path}/images/{image_name[:-4]}_rotate_{rotate_degree}.jpg'
    txt_path = f'{output_path}/labels/{image_name[:-4]}_rotate_{rotate_degree}.txt'
    with open(txt_path, 'w') as f:
        text1 = '2 ' + ' '.join(f'{x} {y}' for x, y in keypoints1)
        text2 = '3 ' + ' '.join(f'{x} {y}' for x, y in keypoints2)
        f.write(text1 + '\n')
        f.write(text2)
    cv2.imwrite(save_path, transformed_image)
    file_name = save_path.split('/')[-1]
    return des_keypoint_dict, new_width, new_height, image_name, file_name, rotate_degree