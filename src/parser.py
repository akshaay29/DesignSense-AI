def extract_faces_with_thickness(filepath: str) -> list[dict]:
    """
    Mock geometry parser.
    Replace with pythonocc version once Python 3.11 env is ready.
    """
    import random
    random.seed(hash(filepath) % 1000)
    
    faces = []
    for i in range(15):
        thickness = round(random.uniform(0.6, 5.0), 2)
        area      = round(random.uniform(30, 900), 2)
        faces.append({
            "face_index":        i,
            "area_mm2":          area,
            "wall_thickness_mm": thickness,
            "is_planar":         random.choice([True, False]),
            "draft_angle_deg":   round(random.uniform(0.0, 5.0), 2),
            "hole_diameter_mm":  round(random.uniform(1.0, 20.0), 2) if i % 3 == 0 else None,
        })
    return faces