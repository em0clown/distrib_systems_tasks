import csv
import json
from pathlib import Path
from coursekit.variant import repo_root

REQUIRED_KEYS = {
    "group", "student_id", "week", "resource", "singular",
    "extra_field", "service", "gateway", "grpc", "graphql", "k8s", "project_code"
}


def test_roster_contains_groups_531_and_532():
    roster_path = repo_root() / "students" / "roster.csv"
    assert roster_path.exists(), f"Roster file not found: {roster_path}"
    with roster_path.open() as f:
        rows = list(csv.DictReader(f))

    by_group = {}
    for row in rows:
        by_group.setdefault(row["group"], []).append(row)

    assert "531" in by_group, "Group 531 must be present in students/roster.csv"
    assert "532" in by_group, "Group 532 must be present in students/roster.csv"
    assert len(by_group["531"]) == 30, f"Expected 30 students in group 531, found {len(by_group['531'])}"
    assert len(by_group["532"]) == 30, f"Expected 30 students in group 532, found {len(by_group['532'])}"


def test_variants_exist_and_valid_for_groups():
    variants_dir = repo_root() / "variants"

    for group in ["531", "532"]:
        for i in range(1, 31):
            sid = f"s{str(i).zfill(2)}"
            for w in range(1, 18):
                week = str(w).zfill(2)
                p = variants_dir / group / sid / f"week-{week}.json"
                assert p.exists(), f"Variant file missing: {p}"
                data = json.loads(p.read_text())
                assert data["group"] == group
                assert data["student_id"] == sid
                assert data["week"] == week
                assert REQUIRED_KEYS.issubset(data.keys())
