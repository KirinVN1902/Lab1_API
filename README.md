# Lab1_API
# Đồ án 1: Triển khai Web API cho mô hình Tóm tắt văn bản

## 1. Thông tin sinh viên
* **Họ và tên:** Nguyễn Khánh Hoàng
* **MSSV:** 24120055
* **Lớp:** 24CTT3

## 2. Thông tin mô hình Hugging Face
* **Tên mô hình:** Ví dụ: facebook/bart-large-cnn
* **Liên kết mô hình:** https://huggingface.co/facebook/bart-large-cnn
* **Chức năng:** Sử dụng mô hình Transformer để tự động tóm tắt các đoạn văn bản dài thành các ý chính ngắn gọn, tổng quát được nội dung của đoạn văn bản. Hỗ trợ tốt hơn cho các đoạn văn bản Tiếng Anh.

## 3. Hướng dẫn cài đặt thư viện
- Python: 3.8+
- Cài đặt các thư viện trong file requirements.txt: Chạy lệnh sau trên terminal: pip install -r requirements.txt

## 4. Hướng dẫn chạy chương trình
- Phải cài đặt sẵn các thư viện trước.
- Sau đó, chạy lệnh: uvicorn main:app --reload
- Kiểm tra nhanh: Mở trình duyệt và nhập đường link: http://127.0.0.1:8000/docs. 
Khi đó, sẽ được dẫn vào Swagger UI, có thể thử ngay API trên trang đó.

## 5. Hướng dẫn gọi API:
- GET/: Trên terminal, gõ lệnh: curl.exe 127.0.0.1:8000/ hoặc truy cập URL 127.0.0.1:8000/ trên trình duyệt để trả về thông tin cơ bản của API.
- GET /health: Trên terminal, gõ lệnh: curl.exe 127.0.0.1:8000/health hoặc truy cập URL 127.0.0.1:8000/health để kiểm tra trạng thái hoạt động.
- POST /predict:
+ Cách 1: Trên terminal, gõ lệnh:
curl.exe -X POST "127.0.0.1:8000/predict" \ -F "file=@(path_to_document)"
+ Cách 2: Trên terminal, gõ lệnh:
curl.exe -X POST "127.0.0.1:8000/predict" \ -F "text=(paragraph)"
+ Cách 3: Trên trình duyệt, truy cập:
http://127.0.0.1:8000/docs
Chọn POST /predict -> Try it out. Trong phần Request body, tại mục file, chọn Choose File -> Chọn file cần tóm tắt trong máy -> Execute.
+ Cách 4: Trong file test_api.py, dán đoạn văn bản vào mục sample_text rồi gõ dòng lệnh sau trong terminal: py test_api.py
Lưu ý: Nếu chạy bằng cách 1 hoặc cách 3, file được gửi có thể ở định dạng .txt, .docx, .pdf .
## 6. Ví dụ về response:
- GET/: Trả về thông tin cơ bản:
 VD: {"system":"FastAPI + Hugging Face Text Summarization API","description":"Tóm tắt văn bản bằng mô hình AI trên Hugging Face.","main_features":["Nhận file văn bản từ người dùng","Tóm tắt nội dung bằng facebook/bart-large-cnn","Trả kết quả dưới dạng JSON"],"version":"1.0"}
- GET /health: Trả về tình trạng hoạt động
VD: {"status":"ok","uptime_s":7267.957,"model_id":"facebook/bart-large-cnn","model_loaded":true}
- POST /predict: Trả về cấu trúc JSON bao gồm trạng thái xử lý, thông tin dữ liệu...
VD:Status: 200
{
  "status": "ok",
  "input": {
    "source": "text",
    "filename": null,
    "original_chars": 550,
    "used_chars": 550,
    "truncated": false
  },
  "prediction": {
    "summary": "The global COVID-19 pandemic began with an outbreak in Wuhan, China, in December 2019. It spread to other parts of Asia and then worldwide in early 2020. The World Health Organization declared the outbreaka public health emergency of international concern (PHEIC) on 30 January 2020."
  }
}
Đáng chú ý, phần "summary" trong "prediction" sẽ là phần tóm tắt văn bản.



