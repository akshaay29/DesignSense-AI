RULES = {
    "min_wall_thickness": {
        "id":       "DFM-001",
        "title":    "Wall thickness too thin",
        "min_mm":   2.0,
        "severity": "critical",
        "message":  "Wall thickness {val}mm is below minimum {min}mm for injection moulding.",
        "fix":      "Increase wall thickness to at least 2.0mm or add structural ribs.",
    },
    "min_draft_angle": {
        "id":       "DFM-002",
        "title":    "Insufficient draft angle",
        "min_deg":  1.5,
        "severity": "major",
        "message":  "Draft angle {val}° is below recommended minimum {min}° for clean ejection.",
        "fix":      "Increase draft angle to at least 1.5° to prevent part sticking in mould.",
    },
    "min_hole_diameter": {
        "id":       "DFM-003",
        "title":    "Hole diameter too small",
        "min_mm":   2.5,
        "severity": "major",
        "message":  "Hole diameter {val}mm is too small — risk of drill breakage.",
        "fix":      "Increase hole diameter to minimum 2.5mm or use EDM process.",
    },
    "thin_face_area": {
        "id":       "DFM-004",
        "title":    "Face area too small",
        "max_mm2":  40.0,
        "severity": "minor",
        "message":  "Face area {val}mm² is very small — may cause meshing issues.",
        "fix":      "Consider merging with adjacent face or increasing feature size.",
    },
}


def check_rules(faces: list[dict]) -> list[dict]:
    """Run all DFM rules against extracted face data. Returns list of issues."""
    issues = []

    for face in faces:
        idx = face["face_index"]

        # DFM-001 wall thickness
        t = face.get("wall_thickness_mm")
        if t is not None:
            rule = RULES["min_wall_thickness"]
            if t < rule["min_mm"]:
                issues.append({
                    "issue_id":    f"{rule['id']}-F{idx}",
                    "rule_id":     rule["id"],
                    "title":       rule["title"],
                    "face_index":  idx,
                    "severity":    rule["severity"],
                    "description": rule["message"].format(val=t, min=rule["min_mm"]),
                    "fix":         rule["fix"],
                    "value":       t,
                })

        # DFM-002 draft angle
        d = face.get("draft_angle_deg")
        if d is not None:
            rule = RULES["min_draft_angle"]
            if d < rule["min_deg"]:
                issues.append({
                    "issue_id":    f"{rule['id']}-F{idx}",
                    "rule_id":     rule["id"],
                    "title":       rule["title"],
                    "face_index":  idx,
                    "severity":    rule["severity"],
                    "description": rule["message"].format(val=d, min=rule["min_deg"]),
                    "fix":         rule["fix"],
                    "value":       d,
                })

        # DFM-003 hole diameter
        h = face.get("hole_diameter_mm")
        if h is not None:
            rule = RULES["min_hole_diameter"]
            if h < rule["min_mm"]:
                issues.append({
                    "issue_id":    f"{rule['id']}-F{idx}",
                    "rule_id":     rule["id"],
                    "title":       rule["title"],
                    "face_index":  idx,
                    "severity":    rule["severity"],
                    "description": rule["message"].format(val=h, min=rule["min_mm"]),
                    "fix":         rule["fix"],
                    "value":       h,
                })

        # DFM-004 small face area
        a = face.get("area_mm2")
        if a is not None:
            rule = RULES["thin_face_area"]
            if a < rule["max_mm2"]:
                issues.append({
                    "issue_id":    f"{rule['id']}-F{idx}",
                    "rule_id":     rule["id"],
                    "title":       rule["title"],
                    "face_index":  idx,
                    "severity":    rule["severity"],
                    "description": rule["message"].format(val=a),
                    "fix":         rule["fix"],
                    "value":       a,
                })

    return issues