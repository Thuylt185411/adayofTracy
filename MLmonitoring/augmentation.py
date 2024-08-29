import pandas as pd
import cv2
import os
import random
import numpy as np
import albumentations as A
from utils import transform_aug_rotate



ID_BEGIN_SHADOW = 10000

def df_to_csv(df, save_dir, name_csv):
    """
    Lưu DataFrame vào tệp CSV.

    Args:
        df (pd.DataFrame): DataFrame chứa dữ liệu.
        save_dir (str): Đường dẫn thư mục lưu kết quả.
        name_csv (str): Tên tệp CSV.
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    csv_path = os.path.join(save_dir, f'{name_csv}.csv')
    df.to_csv(csv_path, index=False)
    print(f'Đã lưu csv vào {csv_path}')

def aug_folder(DIR_SRC = f'/home/f88/khdl/thuylt15/aug_img_seg/dangkiem_yolo',
                degree: int = 90,
                SAVE_DIR='',
                SAVE_CSV_PATH='',
                aug_func = transform_aug_rotate,
                aug_func_nm = '',
                ):
    deg = degree
    ID_BEGIN_ROTATE = deg*1000
    chunk=0
    print(deg)
    des_id_img_aug = []
    des_segmentation_ar = []
    des_category_id_ar = []
    des_width_ar = []
    des_height_ar = []
    des_file_name_ar = []
    des_file_pth_ar = []
    transform_ar = []
    i = 0
    list_path = os.listdir(f'{DIR_SRC}/images')
    length = len(list_path)
    for path in list_path:
        print(f'Dang xu ly {deg} anh thu {i}/{len(list_path)}')
        file_name = path.split('.')[0]
        print(file_name)
            
        # try:
        if 1==1:
            des_keypoint_dict, des_width, des_height, des_file_name, des_file_path, transform_a = aug_func(
                DIR_SRC=DIR_SRC,
                image_name=file_name,
                rotate_degree=deg,
                SAVE_DIR=SAVE_DIR,
            )
        # except: 
        #     des_keypoint_dict={}
        i+=1

        des_id_img_aug.append(i + ID_BEGIN_ROTATE)
        des_segmentation_ar.append(des_keypoint_dict)
        des_width_ar.append(des_width)
        des_height_ar.append(des_height)
        des_file_name_ar.append(des_file_name)
        des_file_pth_ar.append(des_file_path)
        transform_ar.append(transform_a)

        chunk +=1
        if chunk==100 or i==(length-1):
            df_new = pd.DataFrame({
                'id':des_id_img_aug,
                'segmentation':des_segmentation_ar,
                'new_category_id':des_category_id_ar,
                'width':des_width_ar,
                'height':des_height_ar,
                'file_name':des_file_name_ar,
                'transform':transform_ar,
                'file_path':des_file_pth_ar
            })

            df_to_csv(df=df_new, 
                    save_dir=SAVE_CSV_PATH, 
                    name_csv='img_rotate_'+str(deg)+str(aug_func_nm))
            chunk=0
    return SAVE_CSV_PATH, len(transform_ar)

def add_gaussian_light(DIR_SRC,
                        image_path, 
                        SAVE_DIR, 
                        ):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    image_name = image_path.split('/')[-1]
    img = cv2.imread(f'{DIR_SRC}/images/{image_path}')
    image_width, image_height = img.shape[:2]
    lines = []
    keypoint_dict = {}
    with open(f'{DIR_SRC}/labels/{image_name[:-4]}.txt') as f:
        lines = f.readlines()
    for line in lines:
        point = line.strip().split(' ')
        dict = {}
        if point[0] == '2' or point[0] == '3':
            keypoints = [(int(float(point[i]) * image_width), 
                    int(float(point[i + 1]) * image_height)) 
                    for i in range(1, len(point), 2)]
            dict = {f'{point[0]}':keypoints}
        keypoint_dict.update(dict)
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
        os.makedirs(output_path)
        os.makedirs(f'{output_path}/images')
        os.makedirs(f'{output_path}/labels')
    if os.path.exists(output_path) and not os.path.exists(f'{output_path}/labels'):
        os.makedirs(f'{output_path}/images')
        os.makedirs(f'{output_path}/labels')
    
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
    keypoint_dict = {'2':keypoints1,
                     '3':keypoints2,
                     }
    save_path = f'{output_path}/images/{image_name[:-4]}light.jpg'
    txt_path = f'{output_path}/labels/{image_name[:-4]}light.txt'

    with open(txt_path, 'w') as f:
        text1 = '2'
        for (x,y) in keypoints1:
            text1 = text1 + f' {x} {y}'
        text2 = '3'
        for (x,y) in keypoints2:
            text2 = text2 + f' {x} {y}'
        f.write(text1+'\n')
        f.write(text2)
    cv2.imwrite(save_path, final_result)
    file_name = save_path.split('/')[-1]

    return new_width, new_height, file_name, keypoint_dict, {
        'transform': {
            'light': [light_center_x, light_center_y, light_radius, light_intensity]
        }
    }
def clamp_keypoints(keypoints, width, height):
    clamped_keypoints = []
    for x, y, *rest in keypoints:
        clamped_x = max(0, min(x, width - 1))
        clamped_y = max(0, min(y, height - 1))
        clamped_keypoints.append((clamped_x, clamped_y, *rest))
    return clamped_keypoints


def transform_aug_rotate(DIR_SRC,
                         image_name, 
                         rotate_degree, 
                         SAVE_DIR):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    image = cv2.imread(f'{DIR_SRC}/images/{image_name}.jpg')
    keypoint_dict = {}
    image_height, image_width = image.shape[:2]
    with open(f'{DIR_SRC}/labels/{image_name}.txt') as f:
        lines = f.readlines()
    for line in lines:
        point = line.strip().split(' ')
        dict = {}
        if point[0] == '2' or point[0] == '3':
            keypoints = [(int(float(point[i]) * image_width), 
                    int(float(point[i + 1]) * image_height)) 
                    for i in range(1, len(point), 2)]
            dict = {f'{point[0]}':keypoints}
        keypoint_dict.update(dict)
    print(keypoint_dict)
    print(image_width, image_height)

    augmentations = A.Compose([
                            A.RandomBrightnessContrast(p=0.3),
                            A.Affine(rotate=[rotate_degree, rotate_degree], p=1, mode=cv2.BORDER_CONSTANT, fit_output=True),
    ],  keypoint_params=A.KeypointParams(format='xy', remove_invisible=True),
        additional_targets={'image':'image',
                            'keypoints1': 'keypoints',
                            'keypoints2': 'keypoints'},
    )
    keypoint_dict['2'] = clamp_keypoints(keypoint_dict['2'], image_width, image_height)
    keypoint_dict['3'] = clamp_keypoints(keypoint_dict['3'], image_width, image_height)

    transformed = augmentations(image=image, 
                                keypoints1=keypoint_dict['2'], 
                                keypoints2 = keypoint_dict['3'])
    transformed_image = transformed['image']
    transformed_keypoints1 = transformed['keypoints1']
    transformed_keypoints2 = transformed['keypoints2']
    print(transformed_keypoints1)
    new_height, new_width = transformed_image.shape[:2]
    print(new_height, new_width)
    new_segmentation1 = [coord for point in transformed_keypoints1 for coord in point]
    new_segmentation2 = [coord for point in transformed_keypoints2 for coord in point]
    print(new_segmentation1)
    keypoints1 = [((float(new_segmentation1[i]) / new_width), 
                (float(new_segmentation1[i + 1]) / new_height)) 
            for i in range(0, len(new_segmentation1), 2)]
    keypoints2 = [((float(new_segmentation2[i]) / new_width), 
                (float(new_segmentation2[i + 1]) / new_height)) 
            for i in range(0, len(new_segmentation2), 2)]
    print(keypoints1)
    des_keypoint_dict = {'2':keypoints1,
                         '3':keypoints2
                         }
    
    output_path = f'{SAVE_DIR}/rotate{str(rotate_degree)}'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        os.makedirs(f'{output_path}/images')
        os.makedirs(f'{output_path}/labels')
    if  os.path.exists(output_path) and not os.path.exists(f'{output_path}/images'):  
        os.makedirs(f'{output_path}/images')
        os.makedirs(f'{output_path}/labels')
    save_path = f'{output_path}/images/{image_name[:-4]}_rotate_{rotate_degree}.jpg'
    txt_path = f'{output_path}/labels/{image_name[:-4]}_rotate_{rotate_degree}.txt'
    with open(txt_path, 'w') as f:
        text1 = '2'
        for (x,y) in keypoints1:
            text1 = text1 + f' {x} {y}'
        text2 = '3'
        for (x,y) in keypoints2:
            text2 = text2 + f' {x} {y}'
        f.write(text1)
        f.write('\n')
        f.write(text2)
    print(text1)
    cv2.imwrite(save_path, transformed_image)
    file_name = save_path.split('/')[-1]
    return des_keypoint_dict, new_width, new_height, image_name, file_name, rotate_degree

def aug_folder_non_tf_key(DIR_SRC = f'/home/f88/khdl/thuylt15/aug_img_seg/dangkiem_yolo',
                        SAVE_DIR='',
                        SAVE_CSV_PATH='',
                        aug_func = add_gaussian_light,
                        aug_func_nm = '',
                ):
    ID_BEGIN = 1110000
    des_id_img_aug = []
    des_segmentation_ar = []
    des_category_id_ar = []
    des_width_ar = []
    des_height_ar = []
    des_file_name_ar = []
    transform_ar = []
    i = 0
    list_path = os.listdir(f'{DIR_SRC}/images')
    length = len(list_path)
    chunk = 0
    for path in list_path:
        print(f'Dang xu ly {aug_func} anh thu {i}/{len(list_path)}')
        file_name = path.split('.')[0]
        print(file_name)
        
        if 1==1:
        # try:
            des_width, des_height, des_file_name, des_keypoint_dict, transform_a = aug_func(
                DIR_SRC = DIR_SRC,
                image_path=path,
                SAVE_DIR=SAVE_DIR
            )
            
        # except: 
        #     print('Fail')
        i += 1

        des_id_img_aug.append(i + ID_BEGIN)
        des_segmentation_ar.append(des_keypoint_dict)
        des_width_ar.append(des_width)
        des_height_ar.append(des_height)
        des_file_name_ar.append(des_file_name)
        transform_ar.append(transform_a)

        chunk += 1
        if chunk == 100 or i == (length - 1):
            df_new = pd.DataFrame({
                'id': des_id_img_aug,
                'segmentation': des_segmentation_ar,
                'new_category_id': des_category_id_ar,
                'width': des_width_ar,
                'height': des_height_ar,
                'file_name': des_file_name_ar,
                'transform': transform_ar,
            })

            df_to_csv(df=df_new, save_dir=SAVE_CSV_PATH, name_csv='img_' + str(aug_func_nm))
            chunk = 0
    return SAVE_CSV_PATH, len(transform_ar)

def aug_random(DIR_SRC,image_path, SAVE_DIR):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    image = cv2.imread(f'{DIR_SRC}/images/{image_path}')
    image_height, image_width = image.shape[:2]
    lines = []
    keypoint_dict = {}
    file_name = image_path.split('.')[0]
    with open(f'{DIR_SRC}/labels/{file_name}.txt') as f:
        lines = f.readlines()
    for line in lines:
        point = line.strip().split(' ')
        dict = {}
        if point[0] == '2' or point[0] == '3':
            keypoints = [(int(float(point[i]) * image_width), 
                    int(float(point[i + 1]) * image_height)) 
                    for i in range(1, len(point), 2)]
            dict = {f'{point[0]}':keypoints}
        keypoint_dict.update(dict)

    augmentations = A.Compose([
        A.GaussNoise(),
        A.OneOf([
            A.MotionBlur(p=.2),
            A.MedianBlur(blur_limit=3, p=0.1),
            A.Blur(blur_limit=3, p=0.1),
        ], p=0.2),
        A.OneOf([
            A.OpticalDistortion(p=0.3),
        ], p=0.2),
        A.OneOf([
            A.CLAHE(clip_limit=2),
            A.RandomBrightnessContrast(),
        ], p=0.3),
        A.HueSaturationValue(p=0.3),
    ],  keypoint_params=A.KeypointParams(format='xy', remove_invisible=True),
        additional_targets={'image':'image',
                            'keypoints1': 'keypoints',
                            'keypoints2': 'keypoints'},
    )

    t = random.seed(42)
    keypoint_dict['2'] = clamp_keypoints(keypoint_dict['2'], image_width, image_height)
    keypoint_dict['3'] = clamp_keypoints(keypoint_dict['3'], image_width, image_height)

    transformed = augmentations(image=image, 
                                keypoints1=keypoint_dict['2'], 
                                keypoints2 = keypoint_dict['3']
                            )
    
    transformed_image = transformed['image']
    transformed_keypoints1 = transformed['keypoints1']
    transformed_keypoints2 = transformed['keypoints2']

    new_height, new_width = transformed_image.shape[:2]
    
    new_segmentation1 = [coord for point in transformed_keypoints1 for coord in point]
    new_segmentation2 = [coord for point in transformed_keypoints2 for coord in point]
    keypoints1 = [((float(new_segmentation1[i]) / new_width), 
                (float(new_segmentation1[i + 1]) / new_height)) 
                for i in range(0, len(new_segmentation1), 2)]
    keypoints2 = [((float(new_segmentation2[i]) / new_width), 
                (float(new_segmentation2[i + 1]) / new_height)) 
                for i in range(0, len(new_segmentation2), 2)]
    des_keypoint_dict = {'2':keypoints1,
                         '3':keypoints2
                         }
    output_path = f'{SAVE_DIR}/random_add'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        os.makedirs(f'{output_path}/images')
        os.makedirs(f'{output_path}/labels')
    if  os.path.exists(output_path) and not os.path.exists(f'{output_path}/images'):  
        os.makedirs(f'{output_path}/images')
        os.makedirs(f'{output_path}/labels')
    save_path = f'{output_path}/images/{file_name}random.jpg'
    txt_path = f'{output_path}/labels/{file_name}random.txt'
    with open(txt_path, 'w') as f:
        text1 = '2'
        for (x,y) in keypoints1:
            text1 = text1 + f' {x} {y}'
        text2 = '3'
        for (x,y) in keypoints2:
            text2 = text2 + f' {x} {y}'
        f.write(text1+'\n')
        f.write(text2)

    cv2.imwrite(save_path, transformed_image)
    file_name = save_path.split('/')[-1]
    return new_width, new_height, file_name, des_keypoint_dict, {
        'transform': f'random {t}' }


for deg in range(90,360,90):
    csv_path, len_transform = aug_folder(DIR_SRC = f'/home/f88/khdl/thuylt15/aug_img_seg/dangkiem_yolo',
                                        degree = deg,
                                        SAVE_DIR='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_rotate',
                                        SAVE_CSV_PATH='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_rotate',
                                        aug_func = transform_aug_rotate,
                                        aug_func_nm = 'rotate',
                                        )
    print(f'Đã lưu csv vào {csv_path}')
    print(f'Đã xử lý được {len_transform} ảnh')

for deg in [-10, 10]:
    csv_path, len_transform = aug_folder(DIR_SRC = f'/home/f88/khdl/thuylt15/aug_img_seg/dangkiem_yolo',
                                        degree = deg,
                                        SAVE_DIR='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_rotate',
                                        SAVE_CSV_PATH='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_rotate',
                                        aug_func = transform_aug_rotate,
                                        aug_func_nm = 'rotate',
                                        )
    print(f'Đã lưu csv vào {csv_path}')
    print(f'Đã xử lý được {len_transform} ảnh')

aug_folder_non_tf_key(DIR_SRC = f'/home/f88/khdl/thuylt15/aug_img_seg/dangkiem_yolo',
                    SAVE_DIR='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_addlight',
                    SAVE_CSV_PATH='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_addlight',
                    aug_func = add_gaussian_light,
                    aug_func_nm = 'add_light',)

aug_folder_non_tf_key(DIR_SRC = f'/home/f88/khdl/thuylt15/aug_img_seg/dangkiem_yolo',
                    SAVE_DIR='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_addlight',
                    SAVE_CSV_PATH='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_addlight',
                    aug_func = aug_random,
                    aug_func_nm = 'aug_random',)