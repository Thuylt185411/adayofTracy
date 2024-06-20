ML monitoring 

ML monitoring được dịch là giám sát ML là một loạt các kỹ thuật được triển khai để đo lường hiệu suất
của model tốt hơn so với các key đo hiệu suất và có thể hiểu được khi nào vấn đề được phát sinh
ở một model học máy.

Một chu trình của 


Monitoring workflow - chu trình giám sát

Một chu trình giám sát truyền thống bao gồm các bước sau

1. Tính toán hiệu suất của mô hình: Ta có thẻ dùng MSE, Accuracy, F1-score

2. Đưa ra cảnh báo dựa vào những thay đổi của data đầu vào - **drifts in the input data**

3. Hậu quả của rất nhiều cảnh báo giả


một chu trình giám sát lý tưởng với ML models là có thể đánh giá hiệu suất trong thời gian thực, thậm chí ???? 

Và việc dùng ML để giám sát đem lại nhiều lợi ích
- Có thể giám sát được hiệu suất kỹ thuật, hiệu suất mô hình
- có thể phân tích được nguyên nhân gốc rễ của vấn đề khi xảy ra sự cố đối với mô hình

Vậy chu trình ML monitoring lý tưởng sẽ bao gồm các bước như thế nào

1. performance monitoring
2. alert
3. root cause analysis
4. issue resolution

Đầu tiên, tại bước performance monitoring là giám sát hiệu suất của mô hình. Việc này bao gồm các bước đó là: Tính toán hiệu suất mô hình dựa vào giá trị dự đoán của mô hình so với ground-truth,Hoặc là ta estimate performance nghĩa là ước lượng hiệu suất khi không có sẵn dữ liệu ground-truth. Ta measuring business impact - đo lường ảnh hưởng của nghiệp vụ ví dụ như các chỉ số KPI điều này cho ta cái nhìn về một mô hình đang thể hiện liên quan đến ????

Khi giám sát hiệu suất, mô hình sẽ đưa ra những cảnh báo, nếu không có cảnh báo lỗi, mô hình vẫn tiếp tục giám sát bình thường. Nếu mô hình đưa ra cảnh báo, mô hình sẽ chuyển qua phân tích nguyên nhân gốc rễ. Nguyên nhân có thể là những biến đổi đồng biến - covariance shift hoặc những biến đổi về bản chất - biến đổi mối quan hệ - concept drift như là biến đổi dữ liệu đầu vào

Cuối cùng là giải quyết vấn đề khi đã biết nguyên nhân gốc rễ. Tùy vào nguyên nhân đến từ biến đổi nào, các giải pháp sẽ khác nhau. Ta có thể retrain -đào tạo lại mô hình khi lỗi hoặc hiệu suất không tốt là do thay đổi dữ liệu như là thêm dữ liệu mới ... Hoặc cải tiến, cơ cấu lại use case, làm lại, xử lý lại mô hình về các đặc trưng hoặc thay đổi mô hình khác do có thể một số đặc trưng không còn phù hợp. Hoặc là thay đổi cơ sở hạ tầng như là nâng cấp thiết bị,...




Tận dụng kiến thức chuyên môn để hiểu được tại sao mô hình lại thất bại