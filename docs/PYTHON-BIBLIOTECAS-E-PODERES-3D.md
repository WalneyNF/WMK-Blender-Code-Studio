# Manual — Ampliando o Blender com Python e bibliotecas

**WMK Blender Code Studio | Desenvolvedor: Walney Moreira Klein — walneyk@hotmail.com**

## Visão geral

O WMK Studio pretende oferecer mais que exemplos de `bpy`: um sistema modular de ferramentas para gerar, analisar e transformar objetos 3D usando bibliotecas Python, com uma interface Web e integração opcional com MCP e IA.

### Python comum × Blender Python × Studio

- **Python** é a linguagem e pode executar cálculos, algoritmos, processamento de dados e bibliotecas externas.
- **`bpy`** é a API do Blender: manipula cenas, objetos, malhas, materiais, nós, animações, arquivos, renders e configurações do aplicativo.
- **`bmesh`** atua em vértices, arestas e faces com uma estrutura de malha editável.
- **`mathutils`** oferece Vector, Matrix, Quaternion e Euler, úteis para articulações e transformações.
- **WMK Studio** pretende encapsular operações comuns em templates e módulos configuráveis, permitindo controlar o Blender via código e interface visual.
- **MCP** é a interface para clientes de IA; não é uma biblioteca de modelagem. O MCP original usa o Python do Blender para executar e consultar operações.

O Blender executa scripts em seu **próprio interpretador Python**, que pode diferir do `python` do Windows. Veja documentação oficial: https://docs.blender.org/api/current/info_overview.html

## Bibliotecas que podemos aproveitar

| Biblioteca | Uso sugerido | Instalação |
|---|---|---|
| `bpy` | Cena, objetos, materiais, animações | Integrada ao Blender |
| `bmesh` | Construção e edição de geometria | Integrada ao Blender |
| `mathutils` | Vetores, matrizes, ângulos e quaternions | Integrada ao Blender |
| `math`, `itertools`, `json` | Matemática, geração procedural, configurações | Biblioteca padrão |
| `numpy` | Cálculos numéricos e geração de grandes matrizes | Verificar disponibilidade no Blender instalado |
| `scipy` | Otimização, interpolação e geometria numérica | Instalação opcional compatível |
| `Pillow` | Texturas e processamento de imagem | Instalação opcional compatível |
| `trimesh` | Análise e reparo básico de malhas | Instalação opcional compatível |
| `networkx` | Grafos, caminhos e estruturas de conectividade | Instalação opcional |
| `shapely` | Geometria e operações 2D antes de extrusão | Instalação opcional compatível |

**Importante:** listar uma biblioteca não significa que ela já está instalada, integrada ao Studio ou permitida pelo modo seguro do MCP.

## Diagnosticar o Python do Blender

No Blender, abra **Scripting → Python Console** e execute:

```python
import sys, importlib.util, bpy
print("Blender:", bpy.app.version_string)
print("Python:", sys.version)
print("Executável Python:", sys.executable)
for nome in ("numpy", "scipy", "PIL", "trimesh", "networkx", "shapely"):
    print(nome, bool(importlib.util.find_spec(nome)))
```

Isso consulta as bibliotecas sem modificar a instalação.

## Exemplo 1 — criar uma ponte procedural

```python
import bpy
from mathutils import Vector

colecao = bpy.data.collections.get("WMK_PONTE")
if colecao is None:
    colecao = bpy.data.collections.new("WMK_PONTE")
    bpy.context.scene.collection.children.link(colecao)

for i in range(7):
    ponto = Vector((i * 2.2, 0, 1.2))
    bpy.ops.mesh.primitive_cube_add(size=1, location=ponto)
    obj = bpy.context.object
    obj.name = f"WMK_Pilar_{i:02d}"
    obj.dimensions = (0.55, 0.55, 2.4)
    for c in tuple(obj.users_collection):
        c.objects.unlink(obj)
    colecao.objects.link(obj)
```

O modelo é simples e não substitui uma análise estrutural: é apenas um exemplo para jogos.

## Exemplo 2 — peça procedural de revolução

```python
import bpy
import bmesh
from math import sin, cos, tau

malha = bpy.data.meshes.new("WMK_Anel_Mesh")
obj = bpy.data.objects.new("WMK_Anel", malha)
bpy.context.scene.collection.objects.link(obj)

bm = bmesh.new()
raio, tubo = 2.0, 0.35
n, m = 32, 12
vertices = []
for i in range(n):
    linha = []
    for j in range(m):
        a, b = tau*i/n, tau*j/m
        linha.append(bm.verts.new(((raio+tubo*cos(b))*cos(a),
                                   (raio+tubo*cos(b))*sin(a),
                                   tubo*sin(b))))
    vertices.append(linha)
bm.verts.ensure_lookup_table()
for i in range(n):
    for j in range(m):
        bm.faces.new((vertices[i][j],vertices[(i+1)%n][j],
                      vertices[(i+1)%n][(j+1)%m],vertices[i][(j+1)%m]))
bm.to_mesh(malha)
bm.free()
malha.update()
```

**Observação:** esse exemplo cria um toro com superfície paramétrica. O template Toro embutido usa um caminho diferente. Pode-se comparar os resultados e a contagem de faces para aprender.

## Instalar bibliotecas externas com segurança

É preferível **não instalar automaticamente** pacotes no Python global do Blender. Para experimentos, utilize um **ambiente virtual externo** e faça um pipeline de arquivos (JSON, GLB, imagens) entre esse processo e o Blender.

Se realmente precisar de uma biblioteca dentro do Blender:
1. Execute o diagnóstico acima, copie o caminho do interpretador de Blender e confirme sua versão Python.
2. Verifique se existe wheel compatível com Python, Windows e arquitetura usados.
3. Faça backup do ambiente e do projeto.
4. Execute instalações somente de fontes e versões confiáveis, por decisão explícita do usuário; nunca por script recebido de IA.
5. Reinicie o Blender e teste `import pacote`.
6. Prefira empacotar dependências como wheels em uma extensão Blender, seguindo as orientações oficiais: https://docs.blender.org/manual/en/5.0/advanced/extensions/addons.html

**Cuidado:** o Python 3.13 instalado no Windows pode não ser a mesma versão usada pelo Blender. O `pip` executado no terminal do Windows não instala necessariamente a biblioteca no Blender.

## Organização em módulos WMK (proposta)

```text
wmk_modules/
  core/           # contratos, parâmetros, execução autorizada, logs
  geometry/       # bpy + bmesh + mathutils
  materials/      # shaders e texturas
  animation/      # keyframes, rig e timelines
  physics/        # colisores e cenas de simulação
  exporters/      # arquivos GLB, FBX, OBJ
  adapters/       # pacotes opcionais (numpy, scipy, pillow)
  ai/             # Groq, Ollama, OpenAI, Gemini (segredos fora do Git)
```

Esses diretórios são uma proposta de arquitetura e **não uma afirmação de que esses módulos já existam**.

## Política de segurança

- Não execute código arbitrário vindo de uma IA automaticamente.
- O `safe_mode.py` do MCP original é **opt-in** e sua política não permite importar automaticamente todas as bibliotecas listadas neste manual. Não desative essa proteção apenas para acomodar um pacote externo.
- Prefira operações explícitas com parâmetros validados, aprovações e backups da cena.
- `bpy` deve ser acessado na thread principal/ambiente apropriado; não manipule cenas livremente em threads de rede.
- Bibliotecas opcionais não podem tornar a instalação básica obrigatoriamente pesada.
- Arquivos grandes e dependências nativas devem ser tratados como módulos opcionais.

## Roadmap técnico

**P1:** diagnosticar módulos e ambiente Python pelo Studio, com resultado legível e orientação de instalação.  
**P1:** ampliar snippets/autocomplete para `bpy`, `bmesh` e `mathutils` no Monaco.  
**P1:** desenvolver operações estruturadas para objetos, materiais e animações, com retorno tipado.  
**P2:** módulo procedural de geometrias e ferramentas paramétricas orientadas por JSON.  
**P2:** geradores de robôs, veículos, trilhos, prédios, terrenos e props low-poly.  
**P2:** `numpy` opcional para computação mais pesada e avaliação de desempenho.  
**P3:** adaptadores isolados `scipy`, `trimesh`, `Pillow`, `networkx` e `shapely`.  
**P3:** validação de assets, exportação para engines e pipeline de render com fila.

## Referências oficiais

- API Python Blender 5.2: https://docs.blender.org/api/5.2/
- API principal: https://docs.blender.org/api/current/
- Python integrado: https://docs.blender.org/api/main/info_overview.html
- Desenvolvimento de complementos: https://developer.blender.org/docs/handbook/extensions/addon_dev_setup/
- Distribuição de dependências: https://docs.blender.org/manual/en/5.0/advanced/extensions/addons.html

**Licenciamento:** preserve a licença MIT e os créditos de Siddharth Ahuja e colaboradores no MCP. As novas contribuições WMK mantêm os créditos Walney Moreira Klein — walneyk@hotmail.com. Bibliotecas externas têm suas próprias licenças.
