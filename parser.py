# load STEP file using pythonocc and extract all faces with wall thickness
# load STEP file using pythonocc and extract all faces with wall thickness
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_SHELL
from OCC.Core.TopoDS import topods_Face, topods_Edge
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Plane
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.Bnd import Bnd_Box
import math


def load_step(filepath: str):
    """Load a STEP file and return the shape."""
    reader = STEPControl_Reader()
    status = reader.ReadFile(filepath)
    if status != 1:
        raise ValueError(f"Failed to read STEP file: {filepath}")
    reader.TransferRoots()
    shape = reader.OneShape()
    return shape


def get_all_faces(shape):
    """Return a list of all faces in the shape."""
    faces = []
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    while explorer.More():
        face = topods_Face(explorer.Current())
        faces.append(face)
        explorer.Next()
    return faces


def estimate_wall_thickness(face) -> float:
    """
    Estimate wall thickness for a planar face using bounding box depth.
    For a proper thickness measurement you would ray-cast to the opposite face —
    this gives a fast approximation sufficient for DFM rule checking.
    """
    bbox = Bnd_Box()
    brepbndlib_Add(face, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()

    dx = xmax - xmin
    dy = ymax - ymin
    dz = zmax - zmin

    # thickness is the smallest dimension of the bounding box
    thickness = min(dx, dy, dz)
    return round(thickness, 4)


def get_face_area(face) -> float:
    """Return surface area of a face in mm²."""
    props = GProp_GProps()
    brepgprop_SurfaceProperties(face, props)
    return round(props.Mass(), 4)


def is_planar(face) -> bool:
    """Check if a face is planar."""
    adaptor = BRepAdaptor_Surface(face)
    return adaptor.GetType() == GeomAbs_Plane


def extract_faces_with_thickness(filepath: str) -> list[dict]:
    """
    Main function: load STEP file, extract all faces,
    return list of dicts with face index, area, thickness, and planarity.
    """
    shape = load_step(filepath)

    # mesh the shape first — needed for accurate geometry queries
    mesh = BRepMesh_IncrementalMesh(shape, 0.1)
    mesh.Perform()

    faces = get_all_faces(shape)
    results = []

    for i, face in enumerate(faces):
        try:
            thickness = estimate_wall_thickness(face)
            area = get_face_area(face)
            planar = is_planar(face)

            results.append({
                "face_index": i,
                "area_mm2": area,
                "wall_thickness_mm": thickness,
                "is_planar": planar,
            })
        except Exception as e:
            results.append({
                "face_index": i,
                "error": str(e)
            })

    return results


if __name__ == "__main__":
    import json
    import sys

    filepath = sys.argv[1] if len(sys.argv) > 1 else "sample.step"
    faces = extract_faces_with_thickness(filepath)

    print(json.dumps(faces, indent=2))