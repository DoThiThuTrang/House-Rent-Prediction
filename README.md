<a id="top"></a>

<!-- Banner -->
<p align="center">
  <a href="https://www.uit.edu.vn/" title="Trường Đại học Công nghệ Thông tin" style="border: none;">
    <img src="https://i.imgur.com/WmMnSRt.png" alt="Trường Đại học Công nghệ Thông tin | University of Information Technology">
  </a>
</p>

<h1 align="center"><b>PHÂN TÍCH DỮ LIỆU<br>(Data Analysis)</b></h>

[![Status](https://img.shields.io/badge/status-done-blue?style=flat-square)](https://github.com/DoThiThuTrang/House-Rent-Prediction)
[![Status](https://img.shields.io/badge/language-python-blue?style=flat-square)](https://github.com/DoThiThuTrang/House-Rent-Prediction)

# [BẢNG MỤC LỤC](#top)
* [Giới thiệu môn học](#giới-thiệu-môn-học)
* [Thông tin đồ án](#thông-tin-đồ-án)
* [Các bước cần thiết](#các-bước-cần-thiết)
  
# [GIỚI THIỆU MÔN HỌC](#top)
* **Tên môn học:** Phân tích dữ liệu - Data Analysis
* **Mã môn học:** IE224
* **Mã lớp:** IE224.O11.CNCL

# [THÔNG TIN ĐỒ ÁN](#top)
* **Đề tài đồ án:** Dự đoán giá thuê nhà tại TP Hồ Chí Minh 
* **Ngôn ngữ lập trình:** Python
* **Mô tả chung:** Dựa vào giá thuê thực tế ứng với các điều kiện của nhà như: diện tích, số phòng ngủ, số nhà vệ sinh, … mô hình sẽ được huấn luyện và khi nhập vào một danh sách các điều kiện mà nhà đang có, mô hình sẽ đưa ra dự đoán giá thuê của căn nhà đó.

# [CÁC BƯỚC CẦN THIẾT](#top)
Thị trường bất động sản thay đổi liên tục và thường xuyên, do đó, chúng tôi sẽ dựa vào dữ liệu thực tế để cho ra kết quả chính xác nhất. Do đó, để xây dựng mô hình này, chúng tôi đã đặt ra 2 vấn đề cần phải giải quyết: dữ liệu và mô hình. 
* Với dữ liệu, chúng tôi đã tiến hành tự thu thập dữ liệu thực tế trên trang **https://batdongsan.com.vn/** – trang web về bất động sản lớn nhất Việt Nam. Dữ liệu thu thập được sẽ được đi qua các bước tiền xử lý, phân tích, … để có thể đưa vào mô hình dự đoán. 
* Với mô hình thực hiện, chúng tôi nhận thấy với bộ dữ liệu có đặc điểm các trường thông tin tương quan với nhau, các thuật toán hồi quy sẽ khá phù hợp. Chúng tôi sẽ sử dụng đa dạng các thuật toán để cho ra được mô hình tốt nhất với bài toán này. 


## 1. Thu thập dữ liệu 
### a. Nguồn dữ liệu: 
**Trang web:** https://batdongsan.com.vn/

Chúng tôi sẽ thu thập thông tin dựa trên trường dữ liệu thông tin mà trang web hiện ra cho người dùng thấy và sử dụng được: 

<img src='./Images/Website structure.png'>

Đồng thời ngoại trừ những trường thông tin hiện sẵn trên web, còn có những trường thông tin ẩn giấu trong cấu trúc trang web:

<img src='./Images/Website structure (2).png'>

### b. Công cụ sử dụng:

Với cấu trúc của trang web như trên, chúng tôi thu thập dữ liệu thông qua các bước sau:
*	**Bước 1:** Thu thập các đường dẫn tới bài đăng chi tiết của mỗi bài đăng, với mỗi loại bất động sản (căn hộ, biệt thự, nhà đất) sẽ lấy 500 đường dẫn. Lưu trữ các đường dẫn bài đăng và loại bất động sản tương ứng của bài đăng.
*	**Bước 2:** Với mỗi bài đăng, dựa vào phân tích cấu trúc trang web ở trên, thu thập các trường thông tin dữ liệu. 
*	**Bước 3:** Với mỗi bài đăng, lưu trữ các trường thông tin đã thu thập. Chuyển sang đường dẫn tiếp theo nếu còn.

Chúng tôi sử dụng thư viện **Selenium** để truy cập các đường dẫn và lấy dữ liệu.
### c. Bộ dữ liệu thu thập được:
Vì dữ liệu của chúng tôi tự thu thập dựa trên các tin được đăng trên mạng, do đó chúng tôi sẽ cần phải đánh giá việc tin được đăng lên có phải là tin ảo hay không. Chúng tôi sẽ chia dữ liệu dựa trên 2 khía cạnh ***thông tin bài đăng*** và ***thông tin bất động sản***. [Chi tiết bộ dữ liệu](./Crawl%20Data/Mô%20tả%20Dataset.docx).
  
Chúng tôi đã xây dựng luồng xử lý phù hợp với bộ dữ liệu này như sau:  
<img src='./Images/Flow chart.png'>

## 2. Tiền xử lý dữ liệu 
* Loại bỏ cột ‘other’: Đây là cột rỗng, chúng tôi sẽ tiến hành loại bỏ.
* Loại bỏ các dòng bị trùng lặp
* Loại bỏ các dòng có cột ‘price’ có giá trị là thỏa thuận
*	Quy đổi giá trị price thành dạng số và có đơn vị là triệu/tháng
*	Tách cột ‘location’ thành các cột project, streets, ward, district

## 3. Phân tích dữ liệu

Một bộ dữ liệu tốt chúng tôi không chỉ xem xét về lượng của nó mà còn xem xét về chất. Do đó, chúng tôi cần phải đánh giá các giá trị của mỗi thuộc tính. 

<img src='./Images/Data analysis.png'>

Chúng tôi xem xét đến độ lệch chuẩn cũng như xem xét đến các giá trị ngoại lai. Để có thể đưa ra cái nhìn tổng quan nhất, chúng tôi sẽ sẽ thăm dò dữ liệu. 

<img src='./Images/Data result.png'>

Ngoài ra, đối với các biến phân loại, chúng tôi sử dụng thêm phương pháp EDA để xác định tầm quan trọng của các biến đó. 

<img src='./Images/Data analysis (2).png'>

Sau khi tiến hành phân tích, chúng tôi giữ lại 11 trường thông tin, các dòng dữ liệu bị trùng lặp cũng đã được loại bỏ. [Chi tiết bộ dữ liệu](./Data/final_data.csv).

## 4. Huấn luyện mô hình 
Có thể thấy, dữ liệu của chúng tôi là bộ dữ liệu có tính tuyến tính khi giá bán cuối cùng phụ thuộc vào các biến độc lập. Vì thế, nhóm chúng tôi lựa chọn thuật toán Hồi quy nhiều tuyến tính cho bài toán này. 

Tuy nhiên, thử nghiệm ban đầu cho ra giá tri không khả quan, đòi hỏi chúng tôi cần phải xử lý thêm cho bô dữ liệu của mình và lựa chọn sử dụng một thuật toán khác cho bài toán này. Với yêu cầu này, chúng tôi đã thử nghiệm thêm các thuật toán khác cũng dùng cho bài toán hồi quy. 

Tất cả các thuật toán chúng tôi sử dụng đều yêu cầu dữ liệu số hóa, vì thế các thuộc tính có tính phân loại sẽ được chúng tôi mã hóa: *‘building_type’*, *‘furniture’*, *‘project_names’*, *‘streets’*, *‘wards’*, *‘districts’* bằng **OneHotEncoder**. 

Kết quả của các mô hình của chúng tôi như sau:

<img src='./Images/Data result (2).png'>

Dựa vào kết quả được tổng hợp trên, chúng tôi đã rút ra được một số kết luận về mô hình như sau: 
*	Các mô hình ensemble như CatBoost, LightGBM, Histogram Gradient Boosting và XGBoost cho thấy hiệu suất tốt.
*	Mô hình SVR với kernel là linear cũng cho kết quả khả quan.
*	Mô hình Linear Regression lại không cho kết quả tốt. Có thể giải thích rằng, với bộ dữ liệu sau khi được mã hóa các biến phân loại lên đến 1519 dòng và 765 cột thì mô hình đơn giản như Linear Regression sẽ không thể nào xử lý đủ tốt. 



