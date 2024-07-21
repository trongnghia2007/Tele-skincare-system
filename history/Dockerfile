# Sử dụng base image Python
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt requirements.txt

# Cài đặt các dependencies từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ nội dung của thư mục hiện tại vào container
COPY . .

# Mở port 5000 để truy cập ứng dụng web
EXPOSE 5000

# Thiết lập lệnh khởi chạy ứng dụng
CMD ["python", "app/app.py"]
