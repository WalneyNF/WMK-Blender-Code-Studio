# SPDX-License-Identifier: MIT
"""WMK Architecture Lab v0.1 — casa paramétrica demonstrativa.
Walney Moreira Klein — walneyk@hotmail.com
Blender > Scripting > Open > Run Script.
Arquivo JSON: planta-exemplo.json (ao lado do script), ou altere JSON_PATH.
Não remove objetos existentes. Não é projeto executivo de arquitetura.
"""
import bpy
import json
import math
from pathlib import Path
from datetime import datetime

JSON_PATH = ""  # Ex.: r"D:\Ferramentas\WMK-Blender-Code-Studio\examples\wmk-architecture-lab\planta-exemplo.json"

DEFAULT = {
    "schema":"wmk.architecture.v0.1", "name":"Casa exemplo WMK",
    "unit":"m", "width":10, "depth":8, "height":2.8,
    "wall_thickness":0.18, "slab_thickness":0.16,
    "openings":[
        {"id":"PORTA_ENTRADA","side":"south","offset":1.6,"width":0.95,"height":2.15,"sill":0},
        {"id":"JANELA_SALA","side":"south","offset":5.25,"width":1.8,"height":1.25,"sill":1},
        {"id":"JANELA_FUNDOS","side":"north","offset":5.8,"width":1.65,"height":1.2,"sill":1},
        {"id":"JANELA_LATERAL","side":"east","offset":2.7,"width":1.2,"height":1.15,"sill":1.05}
    ],
    "partitions":[
        {"id":"DIVISA_QUARTO","start":[4.4,0.18],"end":[4.4,7.82]},
        {"id":"DIVISA_BANHEIRO","start":[4.4,3.1],"end":[9.82,3.1]}
    ]
}


def load_spec():
    path = Path(JSON_PATH).expanduser() if JSON_PATH else Path(__file__).with_name("planta-exemplo.json") if "__file__" in globals() else None
    if path and path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    print("[WMK] JSON não encontrado: usando planta padrão embutida no script")
    return DEFAULT


def number(value, name, lo=0.001, hi=10000):
    if isinstance(value, bool) or not isinstance(value, (int,float)):
        raise ValueError(f"{name} precisa ser numérico")
    v=float(value)
    if not math.isfinite(v) or not lo <= v <= hi:
        raise ValueError(f"{name} fora dos limites [{lo}, {hi}]")
    return v


def validate(spec):
    if not isinstance(spec,dict) or spec.get("unit")!="m":
        raise ValueError("A planta precisa ser JSON com unit='m'")
    w=number(spec["width"],"width",1,500)
    d=number(spec["depth"],"depth",1,500)
    h=number(spec["height"],"height",2,30)
    t=number(spec["wall_thickness"],"wall_thickness",0.05,1.0)
    number(spec.get("slab_thickness",.16),"slab_thickness",.05,1.0)
    if min(w,d)<=2*t:
        raise ValueError("Paredes maiores do que o espaço útil")
    by_side={"south":[],"north":[],"east":[],"west":[]}
    for x in spec.get("openings",[]):
        side=x.get("side")
        if side not in by_side:
            raise ValueError("lado inválido em abertura")
        a=number(x["offset"],"offset",0,500)
        z=number(x.get("sill",0),"peitoril",0,30)
        span=number(x["width"],"width abertura",.1,10)
        top=z+number(x["height"],"height abertura",.1,10)
        limit=w if side in ("south","north") else d
        if a+span>=limit or a<=0.001 or top>=h:
            raise ValueError(f"Abertura {x.get('id')} excede a parede ou sua altura")
        by_side[side].append((a,a+span,z,top))
    for side,arr in by_side.items():
        arr.sort()
        if any(a[0]<b[1]-1e-7 for b,a in zip(arr,arr[1:])):
            raise ValueError(f"Aberturas sobrepostas na parede {side}")
    for p in spec.get("partitions",[]):
        pts=(p.get("start"),p.get("end"))
        if any(not isinstance(v,(list,tuple)) or len(v)!=2 for v in pts):
            raise ValueError("Partição necessita start/end com 2 coordenadas")
        coords=[number(z,"coordenada",0,500) for v in pts for z in v]
        if coords[0]>w or coords[2]>w or coords[1]>d or coords[3]>d:
            raise ValueError("Partição além dos limites da casa")
        if math.hypot(coords[2]-coords[0],coords[3]-coords[1]) < .1:
            raise ValueError("Partição muito curta")
    return w,d,h,t,by_side


def mat(name,color,metal=0,rough=.8):
    m=bpy.data.materials.new(name=name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    n=m.node_tree.nodes.get("Principled BSDF")
    if n:
        n.inputs["Base Color"].default_value=(*color,1)
        n.inputs["Metallic"].default_value=metal
        n.inputs["Roughness"].default_value=rough
    return m


def box(name, cx,cy,cz, dx,dy,dz, coll,material,kind,props=None):
    if min(dx,dy,dz)<=0.00001:
        return None
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx,cy,cz))
    ob=bpy.context.object
    ob.name="WMK_ARQ_"+name
    ob.dimensions=(dx,dy,dz)
    # Transformações dimensionais aplicadas para facilitar conferência e GLB.
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for old in tuple(ob.users_collection):
        old.objects.unlink(ob)
    coll.objects.link(ob)
    ob.data.materials.append(material)
    ob["wmk_kind"]=kind
    ob["wmk_width_m"]=round(dx,4)
    ob["wmk_depth_m"]=round(dy,4)
    ob["wmk_height_m"]=round(dz,4)
    for k,v in (props or {}).items():
        ob["wmk_"+k]=v
    return ob


def build():
    spec=load_spec()
    w,d,h,t,by_side=validate(spec)
    name="WMK_ARQUITETURA_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    coll=bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    bpy.context.scene.unit_settings.system="METRIC"
    bpy.context.scene.unit_settings.scale_length=1.0
    bpy.context.scene.unit_settings.length_unit="METERS"
    alv=mat("WMK_ARQ_Alvenaria",(.73,.72,.65))
    piso=mat("WMK_ARQ_Piso",(.45,.43,.39))
    detalhe=mat("WMK_ARQ_Marcacoes",(.18,.5,.75),.05,.55)
    slab=number(spec.get("slab_thickness",.16),"slab_thickness")
    box("Laje_Piso",w/2,d/2,-slab/2,w,d,slab,coll,piso,"floor",{"area_m2":round(w*d,3)})

    # Paredes com aberturas físicas: caixas abaixo/acima e ao lado de vãos.
    # As quatro paredes estão centralizadas sobre as bordas da planta;
    # isso significa dimensões nominais de eixo, não medidas internas úteis.
    count=0
    for side in ("south","north","west","east"):
        length=w if side in ("south","north") else d
        positions={0,length}
        for lo,hi,_,_ in by_side[side]:
            positions.update((lo,hi))
        stops=sorted(positions)
        for i,(lo,hi) in enumerate(zip(stops,stops[1:])):
            if hi-lo<1e-5:
                continue
            # Uma abertura ocupa inteiramente esse intervalo horizontal.
            opening=next(((a,b,sill,top) for a,b,sill,top in by_side[side] if a<=lo+1e-6 and hi<=b+1e-6),None)
            levels=[(0,h)] if opening is None else [(0,opening[2]),(opening[3],h)]
            for j,(bottom,top) in enumerate(levels):
                if top-bottom<1e-5:
                    continue
                mid=(lo+hi)/2
                if side in ("south","north"):
                    x,y=mid,0 if side=="south" else d
                    dx,dy=hi-lo,t
                else:
                    x,y=0 if side=="west" else w,mid
                    dx,dy=t,hi-lo
                count+=1
                box(f"Parede_{side}_{i:02d}_{j}",x,y,(bottom+top)/2,dx,dy,top-bottom,
                    coll,alv,"wall",{"side":side,"segment":i})

    for idx,part in enumerate(spec.get("partitions",[])):
        x1,y1=map(float,part["start"])
        x2,y2=map(float,part["end"])
        length=math.hypot(x2-x1,y2-y1)
        # Uma partição é um cubo orientado pelo segmento start/end.
        ob=box(f"Divisoria_{idx:02d}",(x1+x2)/2,(y1+y2)/2,h/2,
               length,t,h,coll,alv,"partition",{"partition_id":part.get("id",str(idx))})
        ob.rotation_euler.z=math.atan2(y2-y1,x2-x1)

    # Molduras ilustrativas são mantidas distintas e opcionais: cada vão é
    # geometria realmente vazia, não um desenho sobre uma parede sólida.
    for side,entries in by_side.items():
        for i,(a,b,sill,top) in enumerate(entries):
            center=(a+b)/2
            if side in ("north","south"):
                x,y=center,0 if side=="south" else d
                dx,dy=b-a,.025
            else:
                x,y=0 if side=="west" else w,center
                dx,dy=.025,b-a
            # Marcador muito fino apenas no topo: não fecha o vão.
            box(f"Marcacao_Vao_{side}_{i}",x,y,top+.012,dx,dy,.024,
                coll,detalhe,"opening_marker",{"side":side,"offset_m":a,"width_m":b-a})

    doc=bpy.data.texts.new(name+"_DNA.json")
    doc.write(json.dumps(spec,ensure_ascii=False,indent=2))
    print(f"[WMK] Criado {name}: {count} segmentos exteriores, {len(spec.get('partitions',[]))} divisórias.")
    print("[WMK] Veja a coleção no Outliner e o JSON no Text Editor. Medidas em metros.")
    return coll


if __name__=="__main__":
    build()
