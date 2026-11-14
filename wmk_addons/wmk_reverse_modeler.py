# SPDX-License-Identifier: MIT
"""WMK Reverse Modeler - Exporta dados de malhas Blender para JSON e gera Python.
Walney Moreira Klein — walneyk@hotmail.com

Uso no Blender: Scripting > Text Editor > Run Script.
Altere OUTPUT_DIR para uma pasta válida. O script lê apenas os objetos MESH
selecionados (ou todas as malhas quando SELECTED_ONLY=False).
Sem operações destrutivas e sem dependências externas.

Limitações: geometria base (sem aplicar modifiers), transformações mundiais,
atribuição de materiais por face e valores PBR básicos. Não serializa:
texturas/nodes completos, rigs, Shape Keys, animações ou constraints.
"""
import bpy
import json
import math
from pathlib import Path

OUTPUT_DIR = str(Path.home() / "WMK-Reverse-Modeler")
SELECTED_ONLY = True
MAX_VERTICES = 300000  # proteção contra saída gigantesca por objeto


def _vector(values):
    return [round(float(x), 7) for x in values]


def _rgba(material):
    if material is None:
        return [0.7, 0.7, 0.7, 1.0]
    return _vector(material.diffuse_color)


def export_meshes():
    objects = (list(bpy.context.selected_objects) if SELECTED_ONLY
               else list(bpy.context.scene.objects))
    result = {"schema": "wmk.mesh_snapshot.v0.1",
              "units": "meters", "source": "Blender", "objects": []}
    for obj in objects:
        if obj.type != "MESH":
            continue
        mesh = obj.data
        if len(mesh.vertices) > MAX_VERTICES:
            raise ValueError(
                f"{obj.name}: {len(mesh.vertices)} vertices, "
                f"acima do limite de {MAX_VERTICES}. "
                "Use uma seleção menor ou aumente conscientemente o limite.")
        vertices = [_vector(v.co) for v in mesh.vertices]
        polygons = [{"vertices": list(p.vertices), "material_index": p.material_index}
                    for p in mesh.polygons]
        materials = [{"name": mat.name if mat else None,
                      "rgba": _rgba(mat)}
                     for mat in mesh.materials]
        entry = {"name": obj.name, "vertices": vertices,
                 "polygons": polygons, "materials": materials,
                 "matrix_world": [_vector(row) for row in obj.matrix_world]}
        result["objects"].append(entry)
    return result


def write_outputs():
    folder = Path(OUTPUT_DIR).expanduser()
    folder.mkdir(parents=True, exist_ok=True)
    payload = export_meshes()
    if not payload["objects"]:
        raise RuntimeError("Nenhuma malha encontrada. Selecione objetos do tipo Mesh.")
    path = folder / "wmk-modelo.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
                    encoding="utf-8")
    generator = folder / "wmk-reconstruir.py"
    generator.write_text(REBUILD_SCRIPT, encoding="utf-8")
    print("[WMK] JSON:", path)
    print("[WMK] Script de reconstrução:", generator)
    print("[WMK] Objetos exportados:", len(payload["objects"]))


REBUILD_SCRIPT = '''# SPDX-License-Identifier: MIT
# WMK Reverse Modeler: reconstrói malhas exportadas como JSON.
# Walney Moreira Klein — walneyk@hotmail.com
# Abra este script no Blender e execute com Alt+P.
# Mantenha wmk-modelo.json na mesma pasta ou defina JSON_FILE.
import bpy
import json
from pathlib import Path
from mathutils import Matrix

JSON_FILE = str(Path(__file__).with_name("wmk-modelo.json")) if "__file__" in globals() else ""

def rebuild():
    if not JSON_FILE:
        raise ValueError("Defina JSON_FILE com o caminho completo do arquivo JSON")
    p = Path(JSON_FILE).expanduser()
    payload = json.loads(p.read_text(encoding="utf-8"))
    if payload.get("schema") != "wmk.mesh_snapshot.v0.1":
        raise ValueError("Schema de snapshot não suportado")
    col = bpy.data.collections.new("WMK_RECONSTRUIDO")
    bpy.context.scene.collection.children.link(col)
    total = 0
    for item in payload["objects"]:
        vertices = item["vertices"]
        faces = [p["vertices"] for p in item["polygons"]]
        mesh = bpy.data.meshes.new(item["name"] + "_MESH")
        mesh.from_pydata(vertices, [], faces)
        mesh.update()
        obj = bpy.data.objects.new(item["name"] + "_REBUILD", mesh)
        col.objects.link(obj)
        obj.matrix_world = Matrix(item["matrix_world"])
        for m in item.get("materials", []):
            rgba = m.get("rgba", [0.7, 0.7, 0.7, 1])
            mat = bpy.data.materials.new(m.get("name") or "WMK_Material")
            mat.diffuse_color = rgba
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = rgba
            mesh.materials.append(mat)
        for idx, info in enumerate(item["polygons"]):
            if mesh.materials:
                mesh.polygons[idx].material_index = min(
                    int(info.get("material_index", 0)), len(mesh.materials)-1)
        total += 1
    print("[WMK] Reconstruidos", total, "objetos na colecao", col.name)

if __name__ == "__main__":
    rebuild()
'''

if __name__ == "__main__":
    write_outputs()
