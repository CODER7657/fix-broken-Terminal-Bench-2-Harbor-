import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")

def compute_expected_from_log(log_path: Path) -> dict:
    """Independently recompute expected report values from the access log."""
    paths = Counter()
    ips = set()
    total = 0

    with open(log_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            match = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if match:
                paths[match.group(1)] += 1

    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0],
    }

def test_report_exists_and_is_valid_json():
    """Verifies instruction.md criterion 1:
    /app/report.json exists and contains valid JSON.
    """
    assert REPORT_PATH.exists(), "report.json does not exist at /app/report.json"
    raw = REPORT_PATH.read_text()
    try:
        json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"report.json is not valid JSON: {exc}") from exc

def test_total_requests_matches_log():
    """Verifies instruction.md criterion 2:
    total_requests exactly matches the count of non-empty lines in access.log.
    """
    report = json.loads(REPORT_PATH.read_text())
    expected = compute_expected_from_log(LOG_PATH)
    assert report.get("total_requests") == expected["total_requests"], (
        f"total_requests mismatch: expected {expected['total_requests']}, "
        f"got {report.get('total_requests')}"
    )

def test_unique_ips_matches_log():
    """Verifies instruction.md criterion 3:
    unique_ips exactly matches the number of distinct first-token IP
    addresses across non-empty log lines.
    """
    report = json.loads(REPORT_PATH.read_text())
    expected = compute_expected_from_log(LOG_PATH)
    assert report.get("unique_ips") == expected["unique_ips"], (
        f"unique_ips mismatch: expected {expected['unique_ips']}, "
        f"got {report.get('unique_ips')}"
    )

def test_top_path_matches_log():
    """Verifies instruction.md criterion 4:
    top_path exactly matches the most common request path found via the
    HTTP method/path pattern.
    """
    report = json.loads(REPORT_PATH.read_text())
    expected = compute_expected_from_log(LOG_PATH)
    assert report.get("top_path") == expected["top_path"], (
        f"top_path mismatch: expected {expected['top_path']!r}, "
        f"got {report.get('top_path')!r}"
    )
