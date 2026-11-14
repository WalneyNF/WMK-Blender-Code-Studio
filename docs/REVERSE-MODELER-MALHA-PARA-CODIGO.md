# WMK Reverse Modeler — modelo Blender para JSON e código Python

**Walney Moreira Klein — walneyk@hotmail.com**

O objetivo é fazer o caminho inverso de modelagem: consultar uma malha existente no Blender, salvar seus dados numéricos e gerar um script Python que a reconstrua. O exemplo educacional foi publicado em [wmk_reverse_modeler.py](../wmk_addons/wmk_reverse_modeler.py).

## Primeiro teste

1. No Blender, salve uma cópia de seu `.blend`.
2. Selecione **uma malha** no Outliner.
3. Na aba **Scripting**, abra `wmk_addons/wmk_reverse_modeler.py`.
4. Ajuste `OUTPUT_DIR`, se necessário.
5. Execute com **Alt+P**.
6. O Blender gravará `wmk-modelo.json` com vértices, faces, materiais simples e matriz mundial, e `wmk-reconstruir.py`.
7. No script `wmk-reconstruir.py`, configure `JSON_FILE` explicitamente se o caminho automático não funcionar ao executá-lo no Text Editor. Execute e compare os objetos da coleção `WMK_RECONSTRUIDO`.

**Teste indispensável:** compare vértices, faces, materiais, posição, escala, orientação e tamanho de saída. O script é um protótipo e ainda não foi testado no Blender 5.2.

## Qual é a diferença entre exportar malha e produzir Python procedural?

O snapshot registra as coordenadas dos vértices, faces, índices de material e matriz do objeto; o script reconstruído usa `mesh.from_pydata(vertices, [], faces)`. Isso é **reconstituição por dados**, não a inferência de que a peça é uma hélice, engrenagem ou carroceria. Essa interpretação precisa de algoritmos específicos e, se desejado, IA.

Os arquivos JSON podem ser muito grandes. Para ativos maiores é melhor salvar os arquivos GLB/binários e gerar código de **operações**, não duplicar milhares de coordenadas no código.

## Como separar a malha importada do Meshy?

Já existe [WMK Mesh Parts Lab](../wmk_addons/wmk_mesh_parts_lab.py), com importação de GLB, relatório e separação inicial:

- `OBJECTS`: inspecionar objetos preexistentes;
- `LOOSE`: dividir por partes sem vértices compartilhados;
- `MATERIAL`: dividir por materiais.

Esses métodos dependem da topologia e materiais da origem. Eles **não** sabem automaticamente o que é rotor, tanque, torre, roda, hélice ou braço. Um único objeto com a malha soldada precisará de seleção por faces, algoritmos de segmentação ou reconstrução de componentes.

Fluxo recomendado: **importar GLB → duplicar a malha original → separar o que for possível → nomear e corrigir pivôs → exportar snapshot JSON → ajustar funções Python → preparar animação/GLB para jogos.**

## O que ainda não é preservado no snapshot v0.1?

- Nodes de shader, imagens/UVs e texturas;
- normais customizadas, atributos extras, shape keys e pesos;
- modificadores avaliados e geometria gerada por Geometry Nodes;
- rigs, ossos, constraints e animações;
- estruturas completas de coleções, pais, filhos e instâncias.

Esses itens exigem exportadores especializados e testes de ida e volta. GLB permanece a opção indicada para preservar grande parte dos dados de malha, material e rig compatíveis com o formato.

## Segurança

O exportador publicado **não apaga objetos da cena**. No entanto, Python executado no Blender possui acesso a arquivos e recursos locais: inspecione scripts antes de executar. A reconstrução cria uma coleção nova. Faça backups antes de testes.

## Evolução sugerida

1. Exportação completa com UVs, múltiplos materiais, hierarquias e transformação correta.
2. Aba `Cena → Código` no Studio com consultas pela ponte local, sem serializar geometria gigante pelo socket.
3. Seleção de faces, separação por proximidade e delimitação manual.
4. Reconhecimento assistido de peças mecânicas e edição de pivôs.
5. Geração procedural simplificada com detecção de cilindros, simetrias, padrões e encaixes.
6. Testes de equivalência ida/volta em robôs, helicópteros, veículos e cenas arquitetônicas.
