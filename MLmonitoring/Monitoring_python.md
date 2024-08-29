Monitoring a data pipeline

# Data preparation and performance estimation
Trong chương này, bạn sẽ được giới thiệu về thư viện NannyML và các chức năng cơ bản của nó. Ban đầu, bạn sẽ tìm hiểu quy trình chuẩn bị dữ liệu thô để tạo các bộ tham chiếu và phân tích sẵn sàng cho việc giám sát sản xuất. Như một ví dụ thực tế, bạn sẽ điều tra việc dự đoán số tiền boa khi đi taxi ở New York. Ở cuối chương, bạn cũng sẽ khám phá cách ước tính hiệu suất của mô hình dự đoán tiền boa bằng NannyML.

Trước khi học bạn cần nắm được các kiến thức cơ bản của việc giám sát, chẳng hạn như:
- quy trình gián sát lý tưởng
- những thách thức của mô hình giám sát trong sản xuất - production
- khái niệm về silent model failures, covariate shift, concept drift
- Sáu phương pháp phát hiện covariate shift 
- Các khái niệm lý thuyết đằng sau các phương pháp ước tính hiệu suất CBPE và DLE (CBPE là confidence-based performance estimate, DLE là direct loss estimate)


## What this course will cover?
- Xây dựng một hệ thống giám sát với NannyML
- Thực hành ước tính hiệu suất
- Xác định giá trị tiền tệ của mô hình học máy
- Sử dụng các phương pháp phát hiện sự thay đổi hiệp phương sai khác nhau

## Thách thức của monitoring
1. Không tiếp cận được với ground-truth
2. Những alerts fatigue là việc phải đối mặt với quá nhiều cảnh báo bao gồm cả cảnh báo giả và bỏ lỡ những cảnh báo liên quan

### open-source solution
- evidently
- deepchecks
- nannyML
NannyML cho phép ước tính hiêu suất mô hình ngay cả khi không có ground-truth

## how to use NannyML?
1. Chuẩn bị dữ liệu - nannyML yêu cầu 2 bộ dữ liệu là tập tham chiều reference - test set và tập phân tích analysis - production data. (một cột chứa ground-truth cơ bản)
```(python)
import nannyml
ref, anal, anal_gt = nannyml.load_us_ma_employment_data()
# load bộ data set 
```

? key features of nannyML: nannyML là thư viện mã nguồn mở giúp DS giám sát mô hình của họ khi production. Bạn có nhớ key features của nó là gì k?
1. ước tính và tính toán hiệu suất
2. phát hiện thay đổi đơn biến và đa biến - multivariable and univariate drift detection
3. giám sát chất lượng dữ liệu - data quality monitoring
4. tính toán và ước tính business value
5. measuring operational metrics - đo lường các chỉ số hoạt động -> false

## Data preparation for NannyML
1. Loading the data
```
dataset_path = 'thuy.csv'
data = pd.read_csv(dataset_path)
data.head()

```
2. preprocessing the data
```
# create data partiton
data['partition'] = pd.cut(
                        data['datetime'],
                        bins=[pd.to_datetime('....')],
                        right=False,
                        labels = ['']
)
```
3. splitting the data
```
```

4. Build the model
- train `LGBMRegressor` using `lightgbm` library
- evaluate the model on a test set
- deploy the model

5. creating reference and analysis sets
- reference sets: requires ground truth, use a test set and set a baseline performance
- analysis sets: GT is optional, uses knowledge gained from previous set, created using the most recent input data and model's predictions

## Performance estimate
- CBPE - confidence based performance estimation
- DLE - direct loss estimation

### Direct loss estimation
DLE được sử dụng cho các bài toán hồi quy. Ý tưởng đằng sau của DLE là đào tạo một mô hình External ML để ước tính các giá trị của loss function, đây là sự khác biệt giữa dự đoán của mô hình và giá trị thực tế.

NannyML sử dụng thuật toán LGBM làm mô hình ML external - nó được huấn luyện trên bộ tham chiếu và sau đó được cung cấp bộ phân tích trong trong quá trình production, từ đó thu được ước tính hiệu suất.

nannyML hỗ trợ sáu số liệu hồi quy: MAE, MAPE, MSE, RMSE, MSLE và RMSLE

*code implement*
```
chunk_period='d' - update hàng ngày
estimator = nannyml.DLE(
    ...
)
estimator.fit(ref)
results = estimator.estimate(anal)
```
### confidence based preformance estimation
Phương pháp được sử dụng cho cả bài toán phân loại nhị phân và multiclass. Tận dụng các confidence score - điểm tin cậy của mô hình dự đoán để ước tính tất cả giá trị của confusion matrix. Điều đó cho phép ta ước tính các hiệu suất phân loại khác nhau - classification performance metrics như là acc, roc, auc, f1 score, precision

**code implement**
```
estimator = nannyml.CBDE(
    ...
)
..
results.plot().show()
```

?Specify the algorithm and problem type
Imagine you are a data scientist consultant working for a hotel chain. Your task is to build a model to predict whether the customer will arrive (or not). Many bookings are made months in advance, which means you're dealing with the delayed ground truth issue.
What is the name of the performance estimation algorithm you would use and the problem type you would describe it?
-> CBPE, binary classification

# Monitoring Performance and Business Value
Trong phần này, ta sẽ tìm hiểu về tính toán hiệu suất được sử dụng khi có GT, và tiếp cận một số phương pháp nâng cao để xử lý kết quả bao gồm filtering, plotting, converting chúng thành data frames, chunking and establishing custom thresholds. Cuối cùng ta tính business value của mô hình với dữ liệu hotel booking

## When labels are available
So sánh hiệu suất thực tế và hiệu suất ước tính

GT muộn - delayed GT
```
# Intialize the calculator
calculator = nannyml.PerformanceCalculator(
    y_true='tip_amount',
    y_pred='y_pred',
    chunk_period='d',
  	metrics=['mae'],
    timestamp_column_name='lpep_pickup_datetime',
    problem_type='regression')

# Fit the calculator
calculator.fit(reference)
realized_results = calculator.calculate(analysis)

# Show comparison plot for realized and estimated performance
realized_results.compare(estimated_results).plot().show()
```
?When performance estimation is off
Imagine you're a data scientist at a bank, working on a loan default use case. You receive labels to validate your model and performance estimation algorithm every month. During one particular month, you observe that many customers with well-paid jobs are defaulting more often due to a significant surge in inflation and a corresponding job crisis.
As you compare the estimated and realized performance, you notice a significant disparity between them.
What could be why the performance estimation algorithm is not as effective in this situation?

-> CBPE and DLE algorithms will not work well under the concept drift. Now that you understand the possibilities and limitations of the algorithms let's validate them on our tip prediction model and US Consensus dataset!


## Working with calculated and estimated results

1. how to chunk the data?
3 cách : 
- time-based: daily, weekly, monthly
- size-based: 
- number-based:


2. specifying different chunks
3. initializing custom thresholds
- standard deviation thresholds: manually set lower and upper standard deviation multiplier
- contant thre