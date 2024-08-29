from utils import aug_folder
from augmentation_dangkiem.aug_add_gaussian_light import add_gaussian_light
from augmentation_dangkiem.aug_rotate_augment import rotate_augment
from aug_random import aug_random

for deg in range(90, 360, 90):
    csv_path, len_transform = aug_folder(
        DIR_SRC='/home/f88/khdl/thuylt15/aug_img_seg/dangkiem_yolo',
        degree=deg,
        SAVE_DIR='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_rotate',
        SAVE_CSV_PATH='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_rotate',
        aug_func=rotate_augment,
        aug_func_nm='rotate',
    )
    print(f'Đã lưu csv vào {csv_path}')
    print(f'Đã xử lý được {len_transform} ảnh')

for deg in [-10, 10]:
    csv_path, len_transform = aug_folder(
        DIR_SRC='/home/f88/khdl/thuylt15/aug_img_seg/dangkiem_yolo',
        degree=deg,
        SAVE_DIR='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_rotate',
        SAVE_CSV_PATH='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_rotate',
        aug_func=rotate_augment,
        aug_func_nm='rotate',
    )
    print(f'Đã lưu csv vào {csv_path}')
    print(f'Đã xử lý được {len_transform} ảnh')

aug_folder(
    DIR_SRC='/home/f88/khdl/thuylt15/aug_img_seg/dangkiem_yolo',
    SAVE_DIR='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_addlight',
    SAVE_CSV_PATH='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_addlight',
    aug_func=add_gaussian_light,
    aug_func_nm='add_light'
)

aug_folder(
    DIR_SRC='/home/f88/khdl/thuylt15/aug_img_seg/dangkiem_yolo',
    SAVE_DIR='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_addlight',
    SAVE_CSV_PATH='/home/f88/khdl/thuylt15/aug_img_seg/data_dangkiem_addlight',
    aug_func=aug_random,
    aug_func_nm='aug_random'
)