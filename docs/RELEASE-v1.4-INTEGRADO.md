# WMK Blender Code Studio — Notas da distribuição v1.4 integrada

**Mantenedor:** Walney Moreira Klein — walneyk@hotmail.com  
**Data:** 14/11/2026  
**Modalidade:** pacote Web local para XAMPP, distribuído como ZIP na conversa do ChatGPT (não disponibilizado no GitHub Releases).

## Conteúdo reunido

1. Studio v1.3 Editor Pro como base, preservando Monaco com destaque Python, temas, snippets, modo foco, fonte ajustável e bridge PHP local.
2. Biblioteca de 40 templates `bpy` com validação estática.
3. Revisão do template **Hélice de helicóptero**, corrigindo o cálculo radial das posições das pás e mantendo o controlador `WMK_CTRL_ROTOR`.
4. **WMK Hybrid Modeler** inicial: viewport com Three.js, primitivos, seleção, transformações com sliders, cópia e exportação `.py`. O protótipo incluído no pacote é uma implementação reduzida e independente daquela publicada em `experiments/wmk-hybrid-modeler`.
5. **WMK Architecture Lab**: planta 2D parametrizada em metros, JSON configurável, código Blender para paredes, aberturas, laje e divisórias e manual HTML.
6. Arquivos de arte WMK fornecidos pelo autor, junto de capturas do teste anterior (a captura da hélice antiga demonstra um **problema**, não a validação do código revisado).
7. Testes automatizados estáticos no arquivo `checks/validate_package.py` incluído no ZIP.

## Instalação da versão Web

Extraia em `C:\xampp\htdocs\WMK-Blender-Code-Studio\`. Execute Apache pelo XAMPP e abra `http://127.0.0.1/WMK-Blender-Code-Studio/`.

Para usar a ponte Blender, habilite `extension=sockets` no `php.ini` em uso no Apache, reinicie o serviço e ative o add-on MCP original em `127.0.0.1:9876`.

A distribuição não inclui nem modifica o núcleo MCP original: `addon.py`, `src/`, `pyproject.toml` e `LICENSE` continuam no fork principal e devem ser mantidos.

## Verificações efetuadas

- 40/40 templates com sintaxe Python analisável e referências `P['parâmetro']` existentes no schema de cada template.
- Sintaxe JavaScript principal: `node --check`.
- Ponte PHP: `php -l`.
- Sintaxe Python do gerador de casas: `py_compile`.
- Integridade do arquivo ZIP: `unzip -t`.
- **Não testado:** execução visual dos templates no Blender 5.2, carregamento dos módulos Three.js/Monaco em navegador real e equivalência geométrica dos modelos.
- A abertura no navegador automatizado deste ambiente foi bloqueada; teste no Windows do usuário permanece pendente.

## Continuação do projeto

1. Testar a hélice corrigida e registrar captura da geometria correta.
2. Publicar, caso desejado, o conteúdo do Studio Web em `studio/` no GitHub para não depender do ZIP.
3. Conectar o Outliner real da cena do Blender ao Studio, por operações validadas.
4. Implementar extrusão, vértices, arestas e faces no Hybrid Modeler.
5. Refinar Architecture Lab com portas internas, paredes por pontos, cotas e importação de planta por imagem.
6. Completar tutorial do Apache Lab e preparar GLB para motor de jogos.

**Licenciamento:** preserve o arquivo MIT e todos os créditos do projeto MCP original.