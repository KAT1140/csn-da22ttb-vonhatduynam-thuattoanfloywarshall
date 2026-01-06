# 🔗 Mô phỏng Giải thuật Floyd-Warshall

Ứng dụng desktop mô phỏng trực quan giải thuật Floyd-Warshall để tìm đường đi ngắn nhất giữa tất cả các cặp đỉnh trong đồ thị có hướng. Được xây dựng với Python và Tkinter, cung cấp giao diện hiện đại và trải nghiệm học tập tương tác.

## ✨ Tính năng chính

### 🎯 Mô phỏng trực quan
- Hiển thị từng bước thực hiện thuật toán với animation mượt mà
- Giao diện hiện đại với thiết kế flat và màu sắc chuyên nghiệp
- Hỗ trợ cuộn dọc với mouse wheel trên toàn bộ ứng dụng

### 📊 Đồ thị đa dạng
- Hỗ trợ 2-10 đỉnh với các hình dạng tự động: tam giác, vuông, ngũ giác, lục giác
- Tạo đồ thị mẫu ngẫu nhiên với một click
- Hiển thị đỉnh với các hình dạng và màu sắc phân biệt theo vai trò

### 📈 Theo dõi thời gian thực
- Ma trận khoảng cách cập nhật theo từng bước với highlight
- Hiển thị đường đi xa nhất (đường đi ngắn nhất có khoảng cách lớn nhất)
- Nhật ký chi tiết ghi lại toàn bộ quá trình thực hiện

### ⚡ Điều khiển linh hoạt
- Chạy tự động với tốc độ tùy chỉnh
- Chế độ từng bước để phân tích chi tiết
- Tạm dừng và tiếp tục bất kỳ lúc nào
- Reset về trạng thái ban đầu

## 🛠️ Yêu cầu hệ thống

- **Python**: 3.7 trở lên
- **Hệ điều hành**: Windows, macOS, Linux
- **Thư viện Python** (được cài đặt tự động):
  - `tkinter` - Giao diện người dùng (có sẵn trong Python)
  - `numpy` ≥ 1.21.0 - Tính toán ma trận
  - `networkx` ≥ 2.6.0 - Xử lý đồ thị
  - `matplotlib` ≥ 3.5.0 - Vẽ biểu đồ và đồ thị

## 🚀 Cài đặt và chạy

### Phương pháp 1: Cài đặt trực tiếp

```bash
# 1. Clone repository
git clone <repository-url>
cd floyd-warshall-visualization

# 2. Cài đặt dependencies
pip install -r requirements.txt

# 3. Chạy ứng dụng
python floyd_visual.py
```

### Phương pháp 2: Sử dụng môi trường ảo (khuyến nghị)

```bash
# 1. Tạo môi trường ảo
python -m venv .venv

# 2. Kích hoạt môi trường ảo
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Chạy ứng dụng
python floyd_visual.py
```

## 📖 Hướng dẫn sử dụng

### Bước 1: Thiết lập đồ thị
1. **Nhập số đỉnh**: Chọn số đỉnh từ 2-10 và nhấn **"Tạo Ma trận"**
2. **Nhập trọng số**: 
   - Nhập trọng số cho các cạnh trong ma trận kề
   - Sử dụng `999` để biểu thị vô cực (không có cạnh)
   - Đường chéo chính luôn là 0 (khoảng cách từ đỉnh đến chính nó)
3. **Hoặc tạo mẫu**: Nhấn **"🎯 Tạo đồ thị mẫu"** để tạo đồ thị ngẫu nhiên

### Bước 2: Chạy mô phỏng
- **▶ Bắt đầu**: Chạy mô phỏng tự động với tốc độ đã chọn
- **⏸ Tạm dừng**: Dừng tạm thời để quan sát chi tiết
- **⏭ Bước tiếp**: Thực hiện từng bước một để phân tích
- **↻ Đặt lại**: Reset về trạng thái ban đầu
- **Thanh tốc độ**: Điều chỉnh tốc độ mô phỏng (chậm → nhanh)

### Bước 3: Theo dõi kết quả
- **Ma trận hiện tại**: Quan sát ma trận khoảng cách được cập nhật
- **Đồ thị trực quan**: Xem các đỉnh được highlight theo vai trò
- **Cuộn xuống**: Xem chi tiết từng bước với đồ thị nhỏ và giải thích
- **Nhật ký**: Đọc mô tả chi tiết các thao tác được thực hiện

## 🎨 Giao diện người dùng

### Panel trái - Điều khiển chính
- **Thiết lập ma trận**: Nhập số đỉnh và tạo ma trận kề
- **Nút điều khiển**: Bắt đầu, tạm dừng, bước tiếp, đặt lại
- **Thanh tốc độ**: Điều chỉnh tốc độ mô phỏng (100ms - 2000ms)
- **Hướng dẫn nhanh**: Các bước sử dụng cơ bản

### Panel giữa - Mô phỏng trực quan
- **Đồ thị chính**: Hiển thị đồ thị với layout tự động theo số đỉnh
- **Chi tiết các bước**: Cuộn xuống để xem từng bước với:
  - Đồ thị nhỏ với đỉnh được highlight
  - Ma trận trạng thái tại bước đó
  - Giải thích chi tiết phép tính

### Panel phải - Thông tin chi tiết
- **Ma trận khoảng cách**: Hiển thị ma trận hiện tại với highlight
- **Đường đi xa nhất**: Đường đi ngắn nhất có khoảng cách lớn nhất
- **Nhật ký thực hiện**: Log chi tiết từng bước thuật toán

## 🔍 Đặc điểm kỹ thuật

### Thuật toán Floyd-Warshall

Thuật toán sử dụng quy hoạch động với ba vòng lặp lồng nhau:

```python
for k in range(n):      # Đỉnh trung gian
    for i in range(n):  # Đỉnh nguồn
        for j in range(n):  # Đỉnh đích
            if distance[i][k] + distance[k][j] < distance[i][j]:
                distance[i][j] = distance[i][k] + distance[k][j]
```

**Độ phức tạp thuật toán:**
- **Thời gian**: O(V³) - V là số đỉnh
- **Không gian**: O(V²) - Lưu trữ ma trận khoảng cách
- **Ứng dụng**: Tìm đường đi ngắn nhất giữa mọi cặp đỉnh

### Hình dạng đồ thị tự động

| Số đỉnh | Hình dạng | Mô tả |
|---------|-----------|-------|
| 3 | Tam giác đều | Các đỉnh tạo thành tam giác cân |
| 4 | Hình vuông | Bố trí theo 4 góc vuông |
| 5 | Ngũ giác đều | Các đỉnh đều trên đường tròn |
| 6 | Lục giác đều | Bố trí hexagon cân đối |
| 7+ | Spring layout | Thuật toán force-directed |

### Ký hiệu đỉnh trong mô phỏng

| Hình dạng | Màu sắc | Vai trò |
|-----------|---------|---------|
| 🔴 Tròn | Đỏ | Đỉnh trung gian (k) |
| 🟡 Vuông | Vàng | Đỉnh nguồn (i) |
| 🟠 Tam giác | Cam | Đỉnh đích (j) |
| 🟢 Tròn | Xanh lá | Các đỉnh khác |

## 📁 Cấu trúc dự án

```
floyd-warshall-visualization/
├── 📄 floyd_visual.py          # Ứng dụng chính - GUI và logic thuật toán
├── 📄 README.md               # Tài liệu hướng dẫn (file này)
├── 📄 requirements.txt        # Danh sách dependencies
├── 📁 .venv/                  # Môi trường ảo Python (tùy chọn)
└── 📁 __pycache__/           # Cache Python (tự động tạo)
```

## 🛡️ Xử lý lỗi và validation

Ứng dụng có hệ thống kiểm tra và xử lý lỗi toàn diện:

- ✅ **Kiểm tra đầu vào**: Chỉ cho phép 2-10 đỉnh
- ✅ **Validation ma trận**: Kiểm tra giá trị số nguyên hợp lệ (0-999)
- ✅ **Kiểm tra kết nối**: Đảm bảo có ít nhất một cạnh trước khi bắt đầu
- ✅ **Xử lý lỗi hiển thị**: Fallback khi có lỗi vẽ đồ thị
- ✅ **Mouse wheel binding**: Tự động áp dụng cho tất cả widget
- ✅ **Memory management**: Tự động dọn dẹp tài nguyên đồ thị

## 🚀 Tính năng nâng cao

### Đồ thị mẫu thông minh
- Tự động tạo các dạng đồ thị khác nhau mỗi lần nhấn
- Đảm bảo có đường đi giữa các đỉnh để demo hiệu quả
- Tránh tạo đồ thị quá đơn giản hoặc quá phức tạp

### Giao diện responsive
- Tự động điều chỉnh theo kích thước màn hình
- Hỗ trợ fullscreen và windowed mode
- Layout linh hoạt với các panel có thể resize

### Hiển thị thông minh
- Chỉ hiển thị đường đi xa nhất thay vì tất cả đường đi
- Tự động scroll đến vị trí bước đầu tiên khi bắt đầu
- Highlight thông minh các ô ma trận đang được cập nhật

## 🎓 Mục đích giáo dục

Ứng dụng này được thiết kế đặc biệt cho việc học tập và giảng dạy:

- **Sinh viên**: Hiểu rõ cách hoạt động của thuật toán Floyd-Warshall
- **Giảng viên**: Công cụ demo trực quan trong lớp học
- **Tự học**: Khám phá thuật toán với tốc độ phù hợp
- **Nghiên cứu**: Phân tích hiệu suất trên các loại đồ thị khác nhau

## Tác giả

**Võ Nhật Duy Nam**  
Dự án mô phỏng giải thuật Floyd-Warshall.

## Giấy phép

Dự án này được phát hành dưới giấy phép MIT.

---
