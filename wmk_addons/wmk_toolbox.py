# SPDX-License-Identifier: MIT
# WMK Blender Toolbox — complemento opcional e independente do MCP for Blender.
# Copyright (c) 2026 Walney Moreira Klein — walneyk@hotmail.com
# Não remove créditos nem substitui o addon do MCP original.
bl_info = {
    "name": "WMK Blender Toolbox",
    "author": "Walney Moreira Klein",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar (N) > WMK",
    "description": "Modelagem procedural e diagnóstico local MCP com interface WMK",
    "category": "3D View",
}

import bpy
import socket
import os
from datetime import datetime
from pathlib import Path
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty, StringProperty


def _local_port_reachable(port: int, timeout: float = 0.3) -> bool:
    """Verifica somente a porta TCP local. Não executa comandos no Blender."""
    try:
        with socket.create_connection(("127.0.0.1", int(port)), timeout=timeout):
            return True
    except (OSError, ValueError):
        return False


def _wmk_collection(scene):
    name = "WMK_TOOLBOX"
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
    if collection.name not in {c.name for c in scene.collection.children}:
        # Colocar na coleção da cena atual, sem desanexar coleções de outras cenas.
        try:
            scene.collection.children.link(collection)
        except RuntimeError:
            pass
    return collection


def _move_to_wmk_collection(obj, collection):
    # Quando possível, só retirar da Collection padrão; preservar vínculos externos.
    if collection not in obj.users_collection:
        collection.objects.link(obj)
    for old in list(obj.users_collection):
        if old != collection and old.name == "Collection":
            old.objects.unlink(obj)


def _wmk_material(name, color, metallic, roughness):
    material = bpy.data.materials.get(name)
    if material is None:
        material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    material.diffuse_color = (*color, 1.0)
    bsdf = material.node_tree.nodes.get("Principled BSDF") if material.node_tree else None
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    return material


class WMK_PG_Settings(bpy.types.PropertyGroup):
    shape: EnumProperty(
        name="Forma",
        items=[
            ("CUBE", "Cubo", "Criar cubo"),
            ("CYLINDER", "Cilindro", "Criar cilindro"),
            ("SPHERE", "Esfera UV", "Criar esfera"),
            ("TORUS", "Toro", "Criar toro"),
            ("CONE", "Cone", "Criar cone"),
        ],
        default="CUBE",
    )
    width: FloatProperty(name="Largura", default=2.0, min=0.05, max=100.0, unit="LENGTH")
    depth: FloatProperty(name="Profundidade", default=2.0, min=0.05, max=100.0, unit="LENGTH")
    height: FloatProperty(name="Altura", default=2.0, min=0.05, max=100.0, unit="LENGTH")
    segments: IntProperty(name="Segmentos", default=32, min=8, max=128)
    bevel: FloatProperty(name="Bevel", default=0.08, min=0.0, max=1.0, unit="LENGTH")
    metallic: FloatProperty(name="Metal", default=0.65, min=0.0, max=1.0)
    roughness: FloatProperty(name="Rugosidade", default=0.35, min=0.0, max=1.0)
    color: EnumProperty(
        name="Cor",
        items=[
            ("CYAN", "Ciano WMK", ""),
            ("PURPLE", "Roxo WMK", ""),
            ("SILVER", "Prata", ""),
            ("ORANGE", "Laranja", ""),
        ],
        default="CYAN",
    )
    mcp_port: IntProperty(name="Porta MCP", default=9876, min=1024, max=65535)
    connection_info: StringProperty(name="Conexão", default="Não testada")
    backup_info: StringProperty(name="Backup", default="Nenhum backup gerado")


_COLORS = {
    "CYAN": (0.01, 0.65, 0.85),
    "PURPLE": (0.35, 0.08, 0.75),
    "SILVER": (0.65, 0.72, 0.79),
    "ORANGE": (0.95, 0.32, 0.05),
}


class WMK_OT_CheckMCP(bpy.types.Operator):
    bl_idname = "wmk.check_mcp"
    bl_label = "Testar conexão MCP"
    bl_description = "Verifica se uma porta local TCP está aberta; não autentica o serviço"
    bl_options = {"REGISTER"}

    def execute(self, context):
        props = context.scene.wmk_toolbox
        if _local_port_reachable(props.mcp_port):
            props.connection_info = f"TCP local aberta: 127.0.0.1:{props.mcp_port}"
            self.report({"INFO"}, props.connection_info)
        else:
            props.connection_info = "Porta inacessível: inicie o MCP no Blender"
            self.report({"WARNING"}, props.connection_info)
        return {"FINISHED"}


class WMK_OT_AddPrimitive(bpy.types.Operator):
    bl_idname = "wmk.add_primitive"
    bl_label = "Criar peça WMK"
    bl_description = "Cria nova malha em coleção própria sem apagar outros objetos"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        p = context.scene.wmk_toolbox
        position = tuple(context.scene.cursor.location)
        try:
            if p.shape == "CUBE":
                bpy.ops.mesh.primitive_cube_add(size=1, location=position)
            elif p.shape == "CYLINDER":
                bpy.ops.mesh.primitive_cylinder_add(vertices=p.segments, radius=0.5, depth=1, location=position)
            elif p.shape == "SPHERE":
                bpy.ops.mesh.primitive_uv_sphere_add(segments=p.segments, ring_count=max(4, p.segments // 2), radius=0.5, location=position)
            elif p.shape == "TORUS":
                bpy.ops.mesh.primitive_torus_add(major_segments=p.segments, minor_segments=max(6, p.segments // 4), location=position)
            else:
                bpy.ops.mesh.primitive_cone_add(vertices=p.segments, radius1=0.5, depth=1, location=position)
            obj = context.object
            obj.name = "WMK_" + p.shape.title()
            # Aplique escalas de forma intuitiva, sem alterar a geometria original de outros objetos.
            obj.dimensions = (p.width, p.depth, p.height)
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            material = _wmk_material("WMK_" + p.color, _COLORS[p.color], p.metallic, p.roughness)
            obj.data.materials.append(material)
            _move_to_wmk_collection(obj, _wmk_collection(context.scene))
            self.report({"INFO"}, f"Peça criada: {obj.name}")
            return {"FINISHED"}
        except Exception as exc:
            self.report({"ERROR"}, f"Erro ao criar peça: {exc}")
            return {"CANCELLED"}


class WMK_OT_AddBevel(bpy.types.Operator):
    bl_idname = "wmk.add_bevel"
    bl_label = "Adicionar Bevel"
    bl_description = "Adiciona modificador não destrutivo ao objeto selecionado"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    def execute(self, context):
        obj = context.active_object
        p = context.scene.wmk_toolbox
        modifier = obj.modifiers.new(name="WMK_Bevel", type="BEVEL")
        modifier.width = p.bevel
        modifier.segments = 3
        self.report({"INFO"}, "Modificador Bevel adicionado (não aplicado)")
        return {"FINISHED"}


class WMK_OT_BackupBlend(bpy.types.Operator):
    bl_idname = "wmk.backup_blend"
    bl_label = "Salvar cópia de segurança"
    bl_description = "Salva uma cópia do .blend em novo arquivo sem sobrescrever o original"
    bl_options = {"REGISTER"}

    def execute(self, context):
        source = bpy.data.filepath
        if not source or not Path(source).is_file():
            self.report({"WARNING"}, "Salve seu arquivo .blend primeiro (Ctrl+Shift+S)")
            return {"CANCELLED"}
        path = Path(source)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        target = path.with_name(path.stem + "_WMK_BACKUP_" + timestamp + ".blend")
        try:
            bpy.ops.wm.save_as_mainfile(filepath=str(target), copy=True)
            context.scene.wmk_toolbox.backup_info = str(target)
            self.report({"INFO"}, "Backup criado: " + target.name)
            return {"FINISHED"}
        except Exception as exc:
            self.report({"ERROR"}, f"Falha no backup: {exc}")
            return {"CANCELLED"}


class WMK_PT_Main(bpy.types.Panel):
    bl_label = "WMK Blender Toolbox"
    bl_idname = "WMK_PT_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "WMK"

    def draw(self, context):
        layout = self.layout
        p = context.scene.wmk_toolbox
        top = layout.box()
        top.label(text="WMK | Blender por Código", icon="MODIFIER")
        top.label(text="Walney Moreira Klein")
        link = layout.box()
        link.label(text="Diagnóstico local", icon="NETWORK_DRIVE")
        link.prop(p, "mcp_port")
        link.operator("wmk.check_mcp", icon="FILE_REFRESH")
        link.label(text=p.connection_info[:76])
        model = layout.box()
        model.label(text="Gerador de primitivas", icon="MESH_CUBE")
        model.prop(p, "shape")
        col = model.column(align=True)
        col.prop(p, "width")
        col.prop(p, "depth")
        col.prop(p, "height")
        model.prop(p, "segments")
        model.prop(p, "color")
        model.prop(p, "metallic")
        model.prop(p, "roughness")
        model.operator("wmk.add_primitive", icon="ADD")
        mod = layout.box()
        mod.label(text="Operações", icon="MOD_BEVEL")
        mod.prop(p, "bevel")
        mod.operator("wmk.add_bevel", icon="MOD_BEVEL")
        safe = layout.box()
        safe.label(text="Proteção do trabalho", icon="FILE_BACKUP")
        safe.operator("wmk.backup_blend", icon="DUPLICATE")
        safe.label(text=p.backup_info[:60])
        layout.separator()
        layout.label(text="walneyk@hotmail.com")


CLASSES = (
    WMK_PG_Settings,
    WMK_OT_CheckMCP,
    WMK_OT_AddPrimitive,
    WMK_OT_AddBevel,
    WMK_OT_BackupBlend,
    WMK_PT_Main,
)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.wmk_toolbox = PointerProperty(type=WMK_PG_Settings)


def unregister():
    if hasattr(bpy.types.Scene, "wmk_toolbox"):
        del bpy.types.Scene.wmk_toolbox
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
