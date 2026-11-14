# SPDX-License-Identifier: MIT
"""WMK Dobradiça Paramétrica v0.1 — exemplo de peças mecânicas por bpy.
Walney Moreira Klein — walneyk@hotmail.com

Blender 4.2+; executar em Scripting > Text Editor > Run Script (Alt+P).
Medidas em METROS. A peça é educacional: não é projeto de fabricação.
A cada execução cria nova coleção e NÃO apaga modelos existentes.
"""
import bpy
import math
import json
from datetime import datetime
from mathutils import Vector

P = {
    "nome": "WMK_DOBRADICA",
    "altura": 0.105,             # 105 mm
    "largura_cada_chapa": 0.048, # 48 mm
    "espessura_chapa": 0.003,    # 3 mm
    "raio_externo": 0.007,       # raio dos anéis
    "raio_furo_eixo": 0.004,     # folga interna
    "raio_pino": 0.0036,
    "raio_fu_ro_parafuso": 0.0028,
    "numero_segmentos": 5,      # ímpar: 3 anéis na esquerda, 2 na direita
    "numero_furos_por_chapa": 3,
    "folga_entre_aneis": 0.0006,
    "abertura_graus": 95,
    "animar": True
}
assert P["numero_segmentos"] in (3,5,7,9), "Use 3, 5, 7 ou 9 segmentos"
assert 0 < P["raio_pino"] < P["raio_furo_eixo"] < P["raio_externo"]
assert P["espessura_chapa"] > 0

bpy.context.scene.unit_settings.system="METRIC"
bpy.context.scene.unit_settings.scale_length=1.0
col=bpy.data.collections.new(P["nome"]+"_"+datetime.now().strftime("%H%M%S_%f"))
bpy.context.scene.collection.children.link(col)

def material(name,rgb,metal=0.6,rough=.35):
    mat=bpy.data.materials.new(name)
    mat.diffuse_color=(*rgb,1)
    mat.use_nodes=True
    n=mat.node_tree.nodes.get("Principled BSDF")
    if n:
        n.inputs["Base Color"].default_value=(*rgb,1)
        n.inputs["Metallic"].default_value=metal
        n.inputs["Roughness"].default_value=rough
    return mat

steel=material("WMK_Dobradiça_Aço",(.47,.53,.58))
dark=material("WMK_Dobradiça_Pino",(.13,.16,.2),.8,.25)
leftmat=material("WMK_Dobradiça_Esquerda",(.38,.62,.70))
rightmat=material("WMK_Dobradiça_Direita",(.64,.54,.40))

def move_to_collection(obj):
    for original in tuple(obj.users_collection):
        original.objects.unlink(obj)
    col.objects.link(obj)
    return obj

def cube(name,location,dimensions,mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj=move_to_collection(bpy.context.object)
    obj.name=name
    obj.dimensions=dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    obj["wmk_component"]="chapa"
    return obj

def cylinder(name,location,radius,depth,mat=None,along_y=False):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=radius, depth=depth,location=location)
    obj=move_to_collection(bpy.context.object)
    obj.name=name
    if along_y:
        obj.rotation_euler.x=math.pi/2
    if mat:
        obj.data.materials.append(mat)
    return obj

def subtract(target,cutter,label):
    """Booleano EXATO. Remove só o objeto temporário criado pelo script."""
    mod=target.modifiers.new(label,"BOOLEAN")
    mod.operation="DIFFERENCE"
    mod.solver="EXACT"
    mod.object=cutter
    # Contexto explícito para aplicar modificador somente no alvo.
    if bpy.context.mode!="OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    target.select_set(True)
    bpy.context.view_layer.objects.active=target
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
    finally:
        if cutter.name in bpy.data.objects:
            bpy.data.objects.remove(cutter,do_unlink=True)

def set_parent_preserve_world(obj,par):
    world=obj.matrix_world.copy()
    obj.parent=par
    obj.matrix_world=world

H=P["altura"]
W=P["largura_cada_chapa"]
T=P["espessura_chapa"]
R=P["raio_externo"]
inner=P["raio_furo_eixo"]
gap=P["folga_entre_aneis"]
count=P["numero_segmentos"]
slot=H/count
left=cube("WMK_Chapa_Esquerda",(-W/2,0,0),(W,T,H),leftmat)
right=cube("WMK_Chapa_Direita",(W/2,0,0),(W,T,H),rightmat)

# Fura cada chapa: cilindro horizontal (Y), atravessando sua espessura.
# Para uso industrial as distâncias dos furos devem seguir normas/catálogos.
for side,obj in (("E",left),("D",right)):
    x=(-W*.58 if side=="E" else W*.58)
    for i in range(P["numero_furos_por_chapa"]):
        z=(-.3+(i/max(1,P["numero_furos_por_chapa"]-1))*.6)*H
        cutter=cylinder("WMK_TEMP_Furo", (x,0,z),
                        P["raio_fu_ro_parafuso"], T*4,along_y=True)
        subtract(obj,cutter,"WMK_Perfurar_Chapa")

# Controlador da chapa direita: abre ao redor do eixo central Z.
pivot=bpy.data.objects.new("WMK_CTRL_ABERTURA",None)
pivot.empty_display_type="PLAIN_AXES"
pivot.empty_display_size=0.025
col.objects.link(pivot)
pivot.location=(0,0,0)
set_parent_preserve_world(right,pivot)

# Tubos ocos intercalados: são malhas independentes das chapas para
# documentar a montagem; não simula solda ou união topológica.
for i in range(count):
    side="E" if i%2==0 else "D"
    length=slot-gap
    z=-H/2+slot*(i+.5)
    barrel=cylinder(f"WMK_Anel_{side}_{i+1:02d}",(0,0,z),R,length,
                    leftmat if side=="E" else rightmat)
    cutter=cylinder("WMK_TEMP_Furo_Eixo",(0,0,z),inner,length+.003)
    subtract(barrel,cutter,"WMK_Furar_Anel")
    barrel["wmk_component"]="anel"
    barrel["wmk_side"]=side
    if side=="D":
        set_parent_preserve_world(barrel,pivot)

pin=cylinder("WMK_Pino_Central",(0,0,0),P["raio_pino"],H+.003,dark)
pin["wmk_component"]="pino"
# Cabeça opcional na parte superior, independente da chapa.
head=cylinder("WMK_Cabeca_Pino",(0,0,H/2+.002),R*.78,.003,dark)

# Bordas levemente arredondadas, depois dos booleanos.
for obj in (left,right):
    bevel=obj.modifiers.new("WMK_Acabamento_Bevel","BEVEL")
    bevel.width=min(.0006,T*.16)
    bevel.segments=2
    obj.modifiers.new("WMK_Normais","WEIGHTED_NORMAL")

if P["animar"]:
    pivot.rotation_mode="XYZ"
    pivot.rotation_euler.z=0
    pivot.keyframe_insert(data_path="rotation_euler",frame=1,index=2)
    pivot.rotation_euler.z=math.radians(P["abertura_graus"])
    pivot.keyframe_insert(data_path="rotation_euler",frame=50,index=2)
    # Volta a fechada no frame 100 para visualizar ciclo.
    pivot.rotation_euler.z=0
    pivot.keyframe_insert(data_path="rotation_euler",frame=100,index=2)
    bpy.context.scene.frame_end=max(bpy.context.scene.frame_end,100)
    bpy.context.scene.frame_set(1)

text=bpy.data.texts.new("WMK_DOBRADICA_DNA.json")
text.write(json.dumps(P,ensure_ascii=False,indent=2))
print(f"[WMK] Dobradiça criada: {col.name} | {count} anéis | "
      f"{P['numero_furos_por_chapa']} furos por chapa")
