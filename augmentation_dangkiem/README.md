Chắc chắn rồi! Dưới đây là phiên bản tiếng Việt của tệp `README.md`:

### README.md

# Augmentation Dangkiem

Thư mục này chứa các hàm tăng cường hình ảnh khác nhau được sử dụng cho việc tăng cường dữ liệu trong các dự án học máy. Các tăng cường bao gồm thêm hiệu ứng ánh sáng Gaussian, xoay hình ảnh và áp dụng các tăng cường ngẫu nhiên.

## Nội dung

- `aug_add_gaussian_light.py`: Chứa hàm `add_gaussian_light` để thêm hiệu ứng ánh sáng Gaussian vào hình ảnh.
- `aug_rotate_augment.py`: Chứa hàm `rotate_augment`để xoay hình ảnh theo một góc độ xác định.
- `aug_random.py`: Chứa hàm `aug_random`để áp dụng các tăng cường ngẫu nhiên vào hình ảnh.

## Các hàm

### add_gaussian_light

Thêm hiệu ứng ánh sáng Gaussian vào hình ảnh.

**Cách sử dụng:**

```python
from augmentation_dangkiem.aug_add_gaussian_light import add_gaussian_light

DIR_SRC = '/path/to/source/directory'
image_path = 'example_image.jpg'
SAVE_DIR = '/path/to/save/directory'

new_width, new_height, file_name, save_path, transform_info = add_gaussian_light(DIR_SRC, image_path, SAVE_DIR)
```

**Tham số:**

- `DIR_SRC`(str): Thư mục nguồn chứa các hình ảnh.
- `image_path` (str): Đường dẫn đến tệp hình ảnh.
- `SAVE_DIR` (str): Thư mục để lưu các hình ảnh đã được tăng cường.

**Trả về:**

- `new_width` (int): Chiều rộng của hình ảnh đã được tăng cường.
- `new_height` (int): Chiều cao của hình ảnh đã được tăng cường.
- `file_name` (str): Tên của tệp hình ảnh đã được lưu.
- `save_path` (str): Đường dẫn đến tệp hình ảnh đã được lưu.
- `transform_info` (dict): Thông tin về các biến đổi đã áp dụng.

### rotate_augment

Xoay hình ảnh theo một góc độ xác định.

**Cách sử dụng:**

```python
from augmentation_dangkiem.aug_rotate_augment import rotate_augment

DIR_SRC = '/path/to/source/directory'
image_path = 'example_image.jpg'
SAVE_DIR = '/path/to/save/directory'
degree = 90

new_width, new_height, file_name, des_keypoint_dict, transform_info = rotate_augment(DIR_SRC, image_path, SAVE_DIR, degree)
```

**Tham số:**

- `DIR_SRC`(str): Thư mục nguồn chứa các hình ảnh.
- `image_path` (str): Đường dẫn đến tệp hình ảnh.
- `SAVE_DIR` (str): Thư mục để lưu các hình ảnh đã được tăng cường.
- `degree`(int): Góc độ để xoay hình ảnh.

**Trả về:**

- `new_width` (int): Chiều rộng của hình ảnh đã được tăng cường.
- `new_height` (int): Chiều cao của hình ảnh đã được tăng cường.
- `file_name` (str): Tên của tệp hình ảnh đã được lưu.
- `des_keypoint_dict` (dict): Từ điển các điểm chính sau khi biến đổi.
- `transform_info` (dict): Thông tin về các biến đổi đã áp dụng.

### aug_random

Áp dụng các tăng cường ngẫu nhiên vào hình ảnh.

**Cách sử dụng:**

```python
from aug_random import aug_random

DIR_SRC = '/path/to/source/directory'
image_path = 'example_image.jpg'
SAVE_DIR = '/path/to/save/directory'

new_width, new_height, file_name, des_keypoint_dict, transform_info = aug_random(DIR_SRC, image_path, SAVE_DIR)
```

**Tham số:**

- `DIR_SRC`(str): Thư mục nguồn chứa các hình ảnh.
- `image_path` (str): Đường dẫn đến tệp hình ảnh.
- `SAVE_DIR` (str): Thư mục để lưu các hình ảnh đã được tăng cường.

**Trả về:**

- `new_width` (int): Chiều rộng của hình ảnh đã được tăng cường.
- `new_height` (int): Chiều cao của hình ảnh đã được tăng cường.
- `file_name` (str): Tên của tệp hình ảnh đã được lưu.
- `des_keypoint_dict` (dict): Từ điển các điểm chính sau khi biến đổi.
- `transform_info` (dict): Thông tin về các biến đổi đã áp dụng.

## Ví dụ sử dụng

Ví dụ sau đây minh họa cách sử dụng hàm `aug_folder` để áp dụng các tăng cường khác nhau cho một thư mục chứa các hình ảnh:

```python
from utils import aug_folder
from augmentation_dangkiem.aug_add_gaussian_light import add_gaussian_light
from augmentation_dangkiem.aug_rotate_augment import rotate_augment
from aug_random import aug_random

# Xoay hình ảnh theo các góc 90, 180 và 270 độ
for deg in range(90, 360, 90):
    csv_path, len_transform = aug_folder(
        DIR_SRC='/path/to/source/directory',
        degree=deg,
        SAVE_DIR='/path/to/save/directory',
        SAVE_CSV_PATH='/path/to/save/csv',
        aug_func=rotate_augment,
        aug_func_nm='rotate',
    )
    print(f'Saved CSV to {csv_path}')
    print(f'Processed {len_transform} images')

# Xoay hình ảnh theo các góc -10 và 10 độ
for deg in [-10, 10]:
    csv_path, len_transform = aug_folder(
        DIR_SRC='/path/to/source/directory',
        degree=deg,
        SAVE_DIR='/path/to/save/directory',
        SAVE_CSV_PATH='/path/to/save/csv',
        aug_func=rotate_augment,
        aug_func_nm='rotate',
    )
    print(f'Saved CSV to {csv_path}')
    print(f'Processed {len_transform} images')

# Thêm hiệu ứng ánh sáng Gaussian vào hình ảnh
aug_folder(
    DIR_SRC='/path/to/source/directory',
    SAVE_DIR='/path/to/save/directory',
    SAVE_CSV_PATH='/path/to/save/csv',
    aug_func=add_gaussian_light,
    aug_func_nm='add_light'
)

# Áp dụng các tăng cường ngẫu nhiên vào hình ảnh
aug_folder(
    DIR_SRC='/path/to/source/directory',
    SAVE_DIR='/path/to/save/directory',
    SAVE_CSV_PATH='/path/to/save/csv',
    aug_func=aug_random,
    aug_func_nm='aug_random'
)
```
