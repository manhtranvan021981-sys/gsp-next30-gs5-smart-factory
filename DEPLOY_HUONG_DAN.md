# Hướng dẫn triển khai GitHub Pages – GS5

## 1. Đưa bộ mã lên repository

Upload toàn bộ nội dung **bên trong** gói này vào thư mục gốc của repository:

- `.github/workflows/update-dashboard.yml`
- `scripts/process_excel.py`
- `scripts/verify_build.py`
- `index.html`
- `README.md`
- `requirements.txt`
- `.gitignore`

Không upload file Excel.

## 2. Bật GitHub Pages

Mở:

`Settings` → `Pages` → `Build and deployment` → `Source`

Chọn:

`GitHub Actions`

## 3. Cho phép workflow chạy

Mở:

`Actions`

Nếu GitHub hiển thị nút xác nhận workflow, bấm:

`I understand my workflows, go ahead and enable them`

## 4. Chạy lần đầu

Mở:

`Actions` → `Cập nhật dashboard GS5` → `Run workflow` → `Run workflow`

Lần đầu sẽ tải và xử lý file Excel 148 MB nên lâu hơn các lần sau. Chỉ coi là thành công khi tất cả bước đều xanh, đặc biệt:

- `Xử lý Excel thành dữ liệu theo tháng`
- `Kiểm tra dữ liệu trước khi phát hành`
- `Phát hành dashboard`

## 5. Mở dashboard

Sau khi workflow xanh, đường dẫn dự kiến:

`https://manhtranvan021981-sys.github.io/gsp-next30-gs5-smart-factory/`

## 6. Quyền file Excel

Đổi quyền Google Drive từ `Anyone – Editor` thành:

`Anyone with the link – Viewer`

Nếu chuyển file sang `Restricted`, workflow công khai này sẽ không tải được nếu chưa bổ sung cơ chế xác thực.

## 7. Kiểm tra vận hành

- Trạng thái đầu trang phải ghi đúng `GS5`.
- Nguồn phải là `P3_Tong_Hop_LTT_2507.xlsx`.
- Dữ liệu mặc định là tháng mới nhất.
- Có thể chuyển từng tháng; dashboard không nạp cả 279 nghìn dòng cùng lúc.
- `Action tuần này` phải báo chưa cấu hình nguồn GS5, không được hiện công việc GS6.
- Khi Excel không đổi, workflow dùng cache và không xử lý lại.
