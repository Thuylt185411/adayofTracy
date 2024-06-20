Monitoring a data pipeline

# Data preparation and performance estimation
Trong chương này, bạn sẽ được giới thiệu về thư viện NannyML và các chức năng cơ bản của nó. Ban đầu, bạn sẽ tìm hiểu quy trình chuẩn bị dữ liệu thô để tạo các bộ tham chiếu và phân tích sẵn sàng cho việc giám sát sản xuất. Như một ví dụ thực tế, bạn sẽ điều tra việc dự đoán số tiền boa khi đi taxi ở New York. Ở cuối chương, bạn cũng sẽ khám phá cách ước tính hiệu suất của mô hình dự đoán tiền boa bằng NannyML.

Trước khi học bạn cần nắm được các kiến thức cơ bản của việc giám sát, chẳng hạn như:
- quy trình gián sát lý tưởng
- những thách thức của mô hình giám sát trong sản xuất - production
- khái niệm về silent model failures, covariate shift, concept drift
- Sáu phương pháp phát hiện covariate shift 
- Các khái niệm lý thuyết đằng sau các phương pháp ước tính hiệu suất CBPE và DLE (CBPE là confidence-based performance estimate, DLE là direct loss estimate)


## NannyML là gì?
