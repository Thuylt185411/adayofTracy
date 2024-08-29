import os

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

def clamp_keypoints(keypoints, width, height):
    clamped_keypoints = []
    for x, y, *rest in keypoints:
        clamped_x = max(0, min(x, width - 1))
        clamped_y = max(0, min(y, height - 1))
        clamped_keypoints.append((clamped_x, clamped_y, *rest))
    return clamped_keypoints

def prepare_keypoint_dict(txt_path, image_width, image_height):
    keypoint_dict = {}
    with open(txt_path) as f:
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
    return keypoint_dict

def keypoint_yolo(transformed_keypoints, new_width, new_height):
    """
    Tính toán keypoints từ transformed_keypoints.

    Args:
        transformed_keypoints (list): Danh sách các điểm đã biến đổi.
        new_width (int): Chiều rộng mới của ảnh.
        new_height (int): Chiều cao mới của ảnh.

    Returns:
        list: Danh sách các keypoints đã chuẩn hóa.
    """
    keypoints = [((float(x) / new_width), (float(y) / new_height)) for x, y in transformed_keypoints]
    return keypoints

def create_output_directories(SAVE_DIR, subdir='random_add'):
    output_path = f'{SAVE_DIR}/{subdir}'
    os.makedirs(f'{output_path}/images', exist_ok=True)
    os.makedirs(f'{output_path}/labels', exist_ok=True)
    return output_path

    