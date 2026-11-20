# Changelog — nqdev-unit-test-generator

Định dạng theo [Keep a Changelog](https://keepachangelog.com/), phiên bản theo Semantic Versioning.

## [1.0.0] — 2026-11-18

### Added
- Đưa skill vào plugin `nqdev`; chuẩn hoá frontmatter theo quy ước skill của repo (license, compatibility, version, author, ngày tạo/cập nhật, khối `metadata`, `argument-hint`).
- `disable-model-invocation: true` và `agents/openai.yaml` (`allow_implicit_invocation: false`): skill ghi file test nên chỉ chạy khi người dùng gọi rõ.
