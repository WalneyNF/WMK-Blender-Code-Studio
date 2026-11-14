# SPDX-License-Identifier: MIT
# WMK Mesh Parts Lab v0.1 — (c) 2026 Walney Moreira Klein
# Importação e separação inicial de modelos GLB; independente do MCP original.
bl_info = {
    "name": "WMK Mesh Parts Lab",
    "author": "Walney Moreira Klein — walneyk@hotmail.com",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "3D View > Sidebar (N) > WMK Parts",
    "description": "Importar GLB e inspecionar/separar peças por malha, ilhas ou materiais",
    "category": "3D View",
}
import bpy
import json
from datetime import datetime
from bpy.props import PointerProperty, StringProperty, EnumProperty, BoolProperty
from mathutils import Vector


class WMKPartsSettings(bpy.types.PropertyGroup):
    filepath: StringProperty(name="GLB/GLTF", subtype="FILE_PATH", default="")
    collection_name: StringProperty(name="Coleção de trabalho", default="")
    split_mode: EnumProperty(name="Separar por", items=[
        ("OBJECTS", "Objetos existentes", "Importar sem alterar topologia"),
        ("LOOSE", "Ilhas desconectadas", "Separar malha por componentes sem vértices compartilhados"),
        ("MATERIAL", "Materiais", "Separar faces pelos slots de material"),
    ], default="LOOSE")
    make_copy: BoolProperty(name="Preservar original", default=True,
        description="Duplicar os objetos selecionados antes de fazer separação")


def _target_collection(context):
    name = context.scene.wmk_parts.collection_name.strip()
    return bpy.data.collections.get(name) if name else None


class WMK_OT_Import(bpy.types.Operator):
    bl_idname = "wmkparts.import_glb"
    bl_label = "Importar GLB/GLTF"
    bl_description = "Importa o arquivo para uma coleção de trabalho"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.wmk_parts
        path = bpy.path.abspath(props.filepath)
        if not path.lower().endswith((".glb", ".gltf")):
            self.report({"ERROR"}, "Selecione um arquivo .glb ou .gltf")
            return {"CANCELLED"}
        import os
        if not os.path.isfile(path):
            self.report({"ERROR"}, "Arquivo não encontrado")
            return {"CANCELLED"}
        old = set(bpy.data.objects)
        try:
            bpy.ops.import_scene.gltf(filepath=path)
            imported = [o for o in bpy.data.objects if o not in old]
            if not imported:
                self.report({"WARNING"}, "Importação sem novos objetos")
                return {"CANCELLED"}
            col = bpy.data.collections.new("WMK_IMPORT_" + datetime.now().strftime("%H%M%S"))
            context.scene.collection.children.link(col)
            for obj in imported:
                if col not in obj.users_collection:
                    col.objects.link(obj)
            props.collection_name = col.name
            self.report({"INFO"}, f"Importados {len(imported)} objetos; coleção {col.name}")
            return {"FINISHED"}
        except Exception as exc:
            self.report({"ERROR"}, f"Falha ao importar: {exc}")
            return {"CANCELLED"}


class WMK_OT_Inspect(bpy.types.Operator):
    bl_idname = "wmkparts.inspect"
    bl_label = "Inspecionar malhas"
    bl_description = "Gera relatório JSON sem modificar nenhum objeto"
    bl_options = {"REGISTER"}

    def execute(self, context):
        col = _target_collection(context)
        if col is None:
            self.report({"ERROR"}, "Importe GLB primeiro ou informe uma coleção válida")
            return {"CANCELLED"}
        entries = []
        for obj in col.all_objects:
            item = {
                "name": obj.name,
                "type": obj.type,
                "parent": obj.parent.name if obj.parent else None,
                "dimensions": [round(float(x), 4) for x in obj.dimensions],
                "location": [round(float(x), 4) for x in obj.location],
            }
            if obj.type == "MESH":
                item.update(vertices=len(obj.data.vertices), faces=len(obj.data.polygons),
                            materials=[m.name if m else None for m in obj.data.materials])
            entries.append(item)
        report = {"schema": 1, "collection": col.name, "objects": entries}
        txt = bpy.data.texts.get("WMK_Parts_Report.json") or bpy.data.texts.new("WMK_Parts_Report.json")
        txt.clear()
        txt.write(json.dumps(report, ensure_ascii=False, indent=2))
        self.report({"INFO"}, f"Relatório: Text Editor > {txt.name} ({len(entries)} objetos)")
        return {"FINISHED"}


class WMK_OT_Split(bpy.types.Operator):
    bl_idname = "wmkparts.split"
    bl_label = "Separar peças"
    bl_description = "Separa malhas por ilhas ou material; não identifica peças semanticamente"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.wmk_parts
        col = _target_collection(context)
        if col is None:
            self.report({"ERROR"}, "Selecione uma coleção de trabalho")
            return {"CANCELLED"}
        if context.mode != "OBJECT":
            self.report({"WARNING"}, "Volte ao Object Mode antes de separar")
            return {"CANCELLED"}
        meshes = [o for o in col.objects if o.type == "MESH"]
        if not meshes:
            self.report({"WARNING"}, "Nenhuma malha encontrada na coleção")
            return {"CANCELLED"}
        if props.split_mode == "OBJECTS":
            self.report({"INFO"}, f"O arquivo já possui {len(meshes)} objetos de malha")
            return {"FINISHED"}
        # A cópia é feita por objeto e malha para preservar o arquivo importado.
        work_col = col
        if props.make_copy:
            work_col = bpy.data.collections.new("WMK_PARTES_" + datetime.now().strftime("%H%M%S"))
            context.scene.collection.children.link(work_col)
            copied = []
            for original in meshes:
                obj = original.copy()
                obj.data = original.data.copy()
                work_col.objects.link(obj)
                obj.name = "WMK_PECA_" + original.name
                # Parentesco original copiado, mas transformações mundiais são mantidas.
                obj.matrix_world = original.matrix_world.copy()
                copied.append(obj)
            meshes = copied
            props.collection_name = work_col.name
        before = set(bpy.data.objects)
        try:
            for obj in meshes:
                bpy.ops.object.select_all(action="DESELECT")
                obj.select_set(True)
                context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_all(action="SELECT")
                bpy.ops.mesh.separate(type="LOOSE" if props.split_mode == "LOOSE" else "MATERIAL")
                bpy.ops.object.mode_set(mode="OBJECT")
            generated = [o for o in bpy.data.objects if o not in before]
            self.report({"INFO"}, f"Separação concluída. {len(generated)} objetos adicionais; confira o Outliner")
            return {"FINISHED"}
        except Exception as exc:
            if context.mode != "OBJECT":
                try:
                    bpy.ops.object.mode_set(mode="OBJECT")
                except Exception:
                    pass
            self.report({"ERROR"}, f"Falha ao separar: {exc}")
            return {"CANCELLED"}


class WMK_PT_Parts(bpy.types.Panel):
    bl_label = "WMK Mesh Parts Lab"
    bl_idname = "WMK_PT_parts"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "WMK Parts"

    def draw(self, context):
        p = context.scene.wmk_parts
        layout = self.layout
        layout.label(text="Walney Moreira Klein", icon="MESH_DATA")
        layout.prop(p, "filepath")
        layout.operator("wmkparts.import_glb", icon="IMPORT")
        layout.separator()
        layout.prop(p, "collection_name")
        layout.operator("wmkparts.inspect", icon="TEXT")
        layout.separator()
        layout.prop(p, "split_mode")
        layout.prop(p, "make_copy")
        layout.operator("wmkparts.split", icon="MOD_EXPLODE")
        layout.separator()
        layout.label(text="Separação geométrica, não por função")
        layout.label(text="Pivôs e rig requerem revisão")


_CLASSES = (WMKPartsSettings, WMK_OT_Import, WMK_OT_Inspect, WMK_OT_Split, WMK_PT_Parts)


def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.wmk_parts = PointerProperty(type=WMKPartsSettings)


def unregister():
    if hasattr(bpy.types.Scene, "wmk_parts"):
        del bpy.types.Scene.wmk_parts
    for cls in reversed(_CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
