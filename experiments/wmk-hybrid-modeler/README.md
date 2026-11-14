# WMK Hybrid Modeler — Manual de primeiro contato

**Walney Moreira Klein — walneyk@hotmail.com**

Protótipo v0.1 localizado em [index.html](./index.html).

## Qual é a proposta?

Um editor **híbrido**: usar ferramentas visuais típicas de modelagem 3D (viewport, objetos, propriedades e sliders) para gerar **código Python `bpy`** que recria a cena no Blender.

O protótipo usa **Three.js** para desenhar a prévia tridimensional e **Blender `bpy`** para o script gerado. O navegador **não tem acesso direto ao Blender** nesta versão. Nenhum código é enviado automaticamente ao MCP.

## Como iniciar

1. Faça download da pasta `experiments/wmk-hybrid-modeler/` ou clone o fork.
2. Execute `index.html` em um servidor HTTP local. Exemplo usando Python do Windows:
   ```powershell
   cd D:\Ferramentas\WMK-Blender-Code-Studio
   py -3 -m http.server 8177
   ```
3. Abra `http://127.0.0.1:8177/experiments/wmk-hybrid-modeler/`.
4. A primeira abertura necessita **internet** para carregar módulos Three.js do CDN. Não há dependência de IA ou GPU dedicada.
5. Na barra superior, clique `+ Cubo`, `+ Esfera`, `+ Cilindro` ou `+ Toro`.
6. Selecione o objeto no Outliner à esquerda ou clique nele no viewport central.
7. À direita, ajuste posição, rotação, escala, segmentos, cor, metalicidade e rugosidade.
8. Use os modos de manipulação `Mover` / `Girar` / `Escalar` do viewport.
9. Observe o Python gerado no painel inferior. Clique `Exportar bpy.py` para salvar.
10. No Blender, abra **Scripting > Text Editor > Open**, selecione o arquivo `.py` e clique **Run Script** (`Alt+P`). Salve antes uma cópia de seu `.blend`.

## Atalhos

| Atalho | Função |
|---|---|
| G | Mover o objeto |
| R | Girar o objeto |
| S | Escalar o objeto |
| Ctrl + D | Duplicar objeto |
| Delete | Remover objeto |
| Mouse esquerdo | Selecionar objeto |
| Arrastar no vazio | Orbitar câmera |
| Scroll | Zoom |
| Botão direito | Deslocar câmera (pan) |

Atalhos não operam quando o cursor está em um campo de texto.

## Exemplo — prototipar um rotor

1. Crie um **cilindro**: ele será o eixo.
2. Crie um **cubo** e ajuste escala X alta, Y e Z baixas.
3. Duplique a pá, gire 90° no eixo Z.
4. Configure material metálico no eixo e escuro nas pás.
5. Exporte o script `wmk_hybrid_scene.py`.
6. Execute no Blender e confira a coleção `WMK_HYBRID_SCENE`.

**Limite:** o protótipo não atribui parentesco nem animações. O rotor montado visualmente é uma demonstração geométrica, não um rig pronto.

## O que já funciona na v0.1

- Viewport 3D com iluminação, grade, câmera orbital e manipuladores.
- Outliner de objetos do protótipo.
- Primitivas: cubo, esfera, cilindro e toro.
- Seleção, mover, girar, escalar e duplicar.
- Ajustar segmentos e materiais PBR básicos.
- Gerar Python `bpy` de todos os objetos presentes.
- Exportar script `.py` sem executar código externo.

## O que falta

- Seleção direta de **vértices, arestas e faces**, com ferramentas de edição realmente topológica.
- **Extrusão de faces**, inset, loop cut, bevel, mirror e modificadores.
- Hierarquia pai/filho, pivôs, armatures e animações.
- **Monaco** integrado neste protótipo — o painel atual utiliza um campo de texto para exibir o script.
- Salvar/abrir projetos JSON e histórico undo/redo.
- Sincronização bidirecional com a **cena real do Blender** via ponte local validada.
- Testes de equivalência geométrica entre a prévia Three.js e a malha `bpy` do Blender.

## Por que a equivalência exige testes?

Three.js e Blender possuem convenções diferentes, incluindo orientação vertical: o navegador usa Y como eixo superior, enquanto o Blender normalmente utiliza Z. A versão v0.1 reproduz os valores numéricos, mas **a conversão completa de sistema de coordenadas ainda não foi implementada**; a cena exportada pode aparecer orientada diferentemente. Não considere o script exportado equivalente visualmente até validar esse ponto.

## Segurança

O protótipo cria nova coleção no Blender; não apaga a cena existente. Porém, scripts Python possuem poder total dentro do Blender: revise-os antes de executar. O editor de prévia não disponibiliza acesso remoto ou execução via MCP.

## Próximos passos

A versão 0.2 deve ter: conversão Y-up/Z-up; normalização de primitives e testes de equivalência; salvamento JSON; integração com Monaco; e início da edição de faces com extrusão. A 0.3 deverá ter operações estruturadas de leitura/escrita via conexão local, autenticação e aprovação explícita.

Preservar créditos e licença MIT do projeto MCP original.
