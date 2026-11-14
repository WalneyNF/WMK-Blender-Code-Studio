# v1.4.5: salva código integral; escala universal nos 42 templates.

# WMK Blender Code Studio v1.4 — Distribuição integrada para XAMPP

Créditos: Walney Moreira Klein — walneyk@hotmail.com

## O que está incluído

- Studio v1.3 Editor Pro como base, atualizado para v1.4: Monaco Python com temas WMK, painel foco, preferências, snippets e ponte PHP local.
- 41 templates em `templates/catalog.json` (auditoria estática em `docs/AUDITORIA-TEMPLATES.json`).
- **Hélice corrigida**: pás radiais com comprimento controlado, controlador e keyframes.
- `modules/architecture/`: planta métrica 2D com sliders, JSON, gerador bpy para lajes/paredes com aberturas e manual HTML.
- `modules/hybrid/`: protótipo de modelagem Web com viewport Three.js, Outliner, sliders e exportação Python bpy.
- `modules/mesh_parts/`: consulte addon do fork em `wmk_addons/wmk_mesh_parts_lab.py`; integrado por referência e documentação, ainda não foi validado no Blender.

## Iniciar

Copie esta pasta para `C:\xampp\htdocs\WMK-Blender-Code-Studio`, inicie o Apache no XAMPP e abra:

`http://127.0.0.1/WMK-Blender-Code-Studio/`

No menu da versão 1.4, abra os laboratórios novos. Para a ponte PHP, ative `extension=sockets` no php.ini carregado pelo Apache, reinicie o Apache e, no Blender, inicie o addon original MCP na porta 9876 em localhost. Não exponha a ponte à internet.

## Importante

Esta distribuição **não substitui o MCP original** nem embute o repositório upstream. O addon.py, src/, pyproject.toml e LICENSE do MCP permanecem no fork GitHub, separados do pacote Web XAMPP. As novas páginas são protótipos que precisam de testes no Blender 5.2; não representam um CAD/BIM completo. Edição topológica de vértices/arestas/faces e extrusão ainda é planejada.

**Não execute scripts bpy de fontes desconhecidas.** Salve seu `.blend` antes de testar.

## Identidade visual e demonstração real

![WMK Neon](assets/brand/wmk-emblema-neon.png)

![WMK Studio](assets/brand/wmk-estudio-banner.png)

![WMK Blender Code Studio](assets/brand/wmk-3d-banner.png)

### Capturas fornecidas pelo autor

![Editor 1.3 e template de hélice](docs/screenshots/07-editor-helice-studio.png)

![Resultado anterior no Blender que motivou a correção](docs/screenshots/08-blender-helice-antes-da-correcao.png)

**Atenção:** a captura do Blender representa o resultado incorreto da versão anterior, e **não** comprova que a hélice nova foi testada.


## Revisão v1.4.2 — Correções visuais e de navegação

- Os três arquivos de identidade WMK ficam em `assets/brand/`. Duas artes estão visíveis no início do Marketplace; o emblema está na barra lateral.
- Laboratórios aparecem no menu lateral e como cartões no Marketplace, não apenas no rodapé.
- Criado `docs/GUIA-EXECUCAO-BLENDER.html` para corrigir o endereço de ajuda e orientar instalação/execução.
- Monaco mantém a mesma instância ao alternar telas e revalida a linguagem `python` ao retornar ao editor.
- Após instalar, pressione Ctrl+F5 no navegador para limpar cache dos arquivos da versão anterior.

## v1.4.6: executar sem baixar
Abra o Studio, marque as confirmações e clique **Executar no Blender via MCP**. Para Python livre/alterado, a autorização adicional é obrigatória. [Guia](docs/CORRECAO-EXECUCAO-DIRETA-v1.4.6.md).