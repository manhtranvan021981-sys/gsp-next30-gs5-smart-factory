#!/usr/bin/env python3
"""Fail the deployment if a generated GS5 data package is incomplete."""

from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path


EXPECTED_COLS = [
    "date",
    "month",
    "week",
    "segment",
    "machine",
    "operator",
    "ltt",
    "stat",
    "mat_code",
    "mat_name",
    "process",
    "process_code",
    "line",
    "line_name",
    "unit",
    "shift",
    "qty",
    "ok",
    "ng",
    "ng_rate",
    "allow_qty",
    "allow_rate",
    "over_qty",
    "over_pos",
    "over_rate",
    "downtime",
    "prep_h",
    "nvl_h",
    "machine_h",
    "file_h",
    "reason",
    "capacity",
    "oee",
    "A",
    "P",
    "Q",
    "actual_prod",
    "achv_tech",
    "confidence",
    "flag_count",
    "flags",
    "rag",
    "ltt_req_qty",
    "ltt_allow_ng_qty",
    "converted_qty",
    "setup_std_h",
    "run_std_h",
    "total_std_h",
    "k_lot",
    "job_size_class",
    "oee_weight",
    "oee_lot_adjusted",
    "oee_weight_valid",
    "capa_time_std",
    "capa_actual",
    "capa_rate_std",
    "capa_rate_tech",
]


def read_gzip_json(path: Path):
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        return json.load(stream)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("site/data"))
    parser.add_argument("--plant", default="GS5")
    args = parser.parse_args()
    manifest_path = args.data / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["schema"] == "gs5-static-shards-v1"
    assert manifest["plant"] == args.plant, (
        f"Sai nhà máy: manifest={manifest['plant']}, yêu cầu={args.plant}."
    )
    assert manifest["global"]["accepted_rows"] > 0
    assert manifest["periods"], "Không có phân vùng tháng."
    total = 0
    for period in manifest["periods"]:
        payload = read_gzip_json(args.data / period["file"])
        assert payload["cols"] == EXPECTED_COLS
        assert len(payload["rows"]) == period["rows"]
        assert payload["meta"]["rows"] == period["rows"]
        assert period["rows"] <= 100_000, (
            f"Phân vùng {period['value']} có {period['rows']} dòng; "
            "quá ngưỡng an toàn trình duyệt."
        )
        assert all(len(row) == len(EXPECTED_COLS) for row in payload["rows"])
        total += period["rows"]
    assert total == manifest["global"]["accepted_rows"]
    schedule = read_gzip_json(args.data / manifest["schedule"]["file"])
    assert schedule["meta"]["plant"] == args.plant
    assert len(schedule["rows"]) == manifest["schedule"]["rows"]
    print(
        f"VERIFY OK: {total:,} dòng, {len(manifest['periods'])} phân vùng, "
        f"{len(schedule['rows']):,} dòng lịch hiện hành."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
