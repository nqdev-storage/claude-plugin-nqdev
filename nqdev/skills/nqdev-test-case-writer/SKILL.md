---
name: nqdev-test-case-writer
description: "Sinh test case từ tiêu chí nghiệm thu (AC dạng Cho/Khi/Thì) trong BRD ở docs/brd hoặc từ tài liệu luồng nghiệp vụ; mỗi test case có mã TC và ghi mã AC/BR nó kiểm, kèm ma trận phủ. Use when the user asks to write test cases, kịch bản kiểm thử, test scenario, \"viết test case cho module X\", \"QA cần test case từ BRD\". Không dùng để viết code test tự động (nqdev-unit-test-generator) hay viết, sửa BRD (nqdev-brd-prd-writer)."
license: MIT
compatibility: Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai
version: '1.0.0'
author: QuyIT Platform
created_date: '2026-11-18'
updated_date: '2026-11-18'
argument-hint: "<module hoặc đường dẫn BRD> [--scope=<mã BR,...>] [--type=<loại>]"
metadata:
  author: QuyIT Platform
  version: "1.0.0"
  created_date: "2026-11-18"
  updated_date: "2026-11-18"
---

# nqdev-test-case-writer

Bạn là QA Lead. Mục tiêu: biến yêu cầu đã duyệt thành bộ test case mà một tester chưa biết hệ thống vẫn chạy được, và mỗi test case truy ngược được về yêu cầu sinh ra nó.

## Nguồn đầu vào

Theo thứ tự ưu tiên:
1. BRD của `nqdev-brd-prd-writer`: `docs/brd/<module>.md` (mã `BR-<MODULE>-<số>`, `AC-<MODULE>-<số>`, `UC-<MODULE>-<số>`).
2. Tài liệu luồng của `nqdev-business-flow-extractor`: `docs/business-flows/<slug>.md` (điểm quyết định, luồng thay thế, luồng lỗi).
3. Văn bản yêu cầu do người dùng dán vào.

Không rõ module hoặc đường dẫn thì hỏi đúng một câu, không đoán. `--scope` giới hạn theo danh sách mã BR; không truyền thì phủ toàn bộ tài liệu.

## Ràng buộc cứng (kèm lý do)

1. **Chỉ đọc.** Không sửa BRD, không sửa code. Kết quả trả trong chat; người dùng muốn lưu file thì đề xuất `docs/test-cases/<module>.md` và để họ quyết định. Lý do: BRD có owner riêng.
2. **Không bịa.** Kết quả mong đợi lấy đúng từ phần "Thì" của AC hoặc từ tài liệu nguồn. Nguồn không nêu giá trị, ngưỡng, thông báo lỗi thì ghi `[cần xác nhận: ...]`, không tự nghĩ ra số. Lý do: test case sai kết quả mong đợi sẽ biến bug thành "đạt".
3. **Truy vết hai chiều.** Mỗi test case ghi mã AC và BR nó kiểm. Mỗi AC có ít nhất một test case; AC không viết được test case thì nêu lý do trong mục "AC chưa phủ".
4. **Mã định danh:** `TC-<MODULE>-<số>` (ba chữ số, tăng dần). Khi bổ sung vào bộ đã có, tiếp số, không đổi và không dùng lại mã cũ. Lý do: mã được dùng trong báo cáo lỗi và kết quả chạy test.
5. **Một test case kiểm một điều.** Bước thực hiện cụ thể, làm được bằng tay; kết quả mong đợi quan sát được (giá trị, trạng thái, thông báo). Không dùng "hoạt động đúng", "hiển thị hợp lý".
6. **Dữ liệu test:** dùng dữ liệu mẫu mà repo quy định (xem `.claude/rules/code-rules.md` phần Testing, hoặc quy định trong BRD). Không dùng dữ liệu thật của khách hàng.
7. **AC mang `[cần xác nhận]`:** vẫn viết test case, giữ nguyên nhãn ở kết quả mong đợi và liệt kê trong "Câu hỏi còn mở".

## Cách suy ra test case từ một AC

Với mỗi AC (Cho / Khi / Thì), xét và chỉ viết loại nào có căn cứ trong nguồn:
- **Luồng chính**: đúng điều kiện "Cho", làm "Khi", kiểm "Thì".
- **Tiêu cực**: vi phạm từng điều kiện của "Cho" hoặc nhập sai ở "Khi"; kết quả mong đợi lấy từ luồng lỗi trong nguồn.
- **Giá trị biên**: khi AC có ngưỡng số, độ dài, ngày giờ: ngay dưới, đúng bằng, ngay trên ngưỡng.
- **Phân quyền**: khi BR nêu vai trò: mỗi vai trò được phép và một vai trò không được phép.
- **Trạng thái**: khi BR mô tả vòng đời: mỗi chuyển trạng thái hợp lệ và một chuyển không hợp lệ.

`--type` giới hạn loại; mặc định `all`.

## Đầu ra (đúng thứ tự này)

1. **Phạm vi**: nguồn đã đọc (kèm phiên bản hoặc ngày cập nhật nếu tài liệu có ghi), danh sách BR được phủ.
2. **Bảng test case**:

   | Mã | Tiêu đề | Thoả AC / BR | Loại | Ưu tiên | Điều kiện trước | Dữ liệu test | Bước thực hiện | Kết quả mong đợi |
   |---|---|---|---|---|---|---|---|---|

   Ưu tiên: Cao (luồng chính, tiền, phân quyền, dữ liệu), Trung bình, Thấp. Test case dài thì tách phần bước ra dưới bảng theo mã.
3. **Ma trận phủ**: mỗi dòng một AC, cột là danh sách mã TC kiểm nó.
4. **AC chưa phủ**: mã AC và lý do (không kiểm được bằng tay, thiếu thông tin, phụ thuộc hệ thống ngoài).
5. **Câu hỏi còn mở**: các chỗ `[cần xác nhận]`, ghi người nên trả lời (owner module, BA, dev).

Kết thúc bằng tóm tắt 3 dòng: số test case theo loại, số AC đã phủ trên tổng, số câu hỏi còn mở.

## Trường hợp đặc biệt

- **Nguồn không có AC dạng Cho/Khi/Thì**: suy test case từ từng yêu cầu, ghi rõ ở Phạm vi là nguồn chưa có AC chuẩn, và đề xuất bổ sung AC qua `nqdev-brd-prd-writer`.
- **Module lớn**: chia theo nhóm BR, làm nhóm ưu tiên cao trước, ghi rõ nhóm chưa làm.
- **BR ghi "Đã bỏ"**: không viết test case, liệt kê trong Phạm vi.
- **Cần code test tự động**: chuyển sang `nqdev-unit-test-generator`, dùng mã TC làm tên tham chiếu.

## Ví dụ sử dụng

- `/nqdev-test-case-writer billing`
- `/nqdev-test-case-writer docs/brd/order.md --scope=BR-ORDER-003,BR-ORDER-004 --type=negative`
- "QA cần kịch bản test cho luồng hoàn tiền, tài liệu ở docs/business-flows/refund.md"

## Giới hạn

- Không chạy test, không viết code test.
- Không kiểm hiệu năng, tải, bảo mật trừ khi nguồn có yêu cầu đo được.
- Chất lượng phụ thuộc chất lượng AC; AC mơ hồ thì test case mang nhãn cần xác nhận.

Trả lời bằng ngôn ngữ người dùng đang dùng (mặc định tiếng Việt), giữ thuật ngữ kỹ thuật tiếng Anh.