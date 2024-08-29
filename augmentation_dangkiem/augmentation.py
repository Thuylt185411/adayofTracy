import os
import pandas as pd
from utils import df_to_csv


def aug_folder(DIR_SRC, SAVE_DIR, 
               SAVE_CSV_PATH, aug_func, 
               aug_func_nm, degree=None):
    """
    Thực hiện các phép biến đổi và lưu kết quả vào tệp CSV.

    Args:
        DIR_SRC (str): Đường dẫn thư mục nguồn.
        SAVE_DIR (str): Đường dẫn thư mục lưu kết quả.
        SAVE_CSV_PATH (str): Đường dẫn tệp CSV.
        aug_func (function): Hàm biến đổi.
        aug_func_nm (str): Tên hàm biến đổi.
        degree (int, optional): Góc xoay. Mặc định là None.

    Returns:
        tuple: Đường dẫn tệp CSV và số lượng ảnh đã xử lý.
    """
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
        print(f'Dang xu ly {aug_func_nm} anh thu {i}/{len(list_path)}')
        file_name = path.split('.')[0]
        print(file_name)
        i+=1
        try:
            des_width, des_height, des_file_name, des_keypoint_dict, transform_a = aug_func(
                DIR_SRC=DIR_SRC,
                image_path=path,
                SAVE_DIR=SAVE_DIR
            )
        except Exception as e:
            print(f'Fail: {e}')
            continue

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

        break
    return SAVE_CSV_PATH, len(transform_ar)