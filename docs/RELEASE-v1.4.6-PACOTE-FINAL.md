# WMK Blender Code Studio — Distribuição v1.4.6 (14/11/2026)

**Mantenedor:** Walney Moreira Klein — walneyk@hotmail.com
**Estado:** pacote Web XAMPP gerado e entregue no ChatGPT; publicação no GitHub ainda parcial.

## Conteúdo do ZIP Web

- 37 arquivos, incluindo index.html, assets/app.js, assets/app.css, templates/catalog.json (42 templates), templates/common.py.txt e api/bridge.php.
- Monaco com realce Python; parâmetros com salvamento; escala global; execução direta dos templates e autorização explícita para Python editado via MCP local.
- Experimentos modules/hybrid e modules/architecture, manuais HTML, verificadores, logos WMK e capturas.
- O projeto MCP for Blender original permanece no fork, não é substituído nem está embutido neste ZIP Web.

## Publicação no GitHub

Arquivos publicados no momento: studio/index.html, studio/manual.html, studio/README.md, studio/README-INTEGRACAO.md.

**A pasta studio/ no GitHub ainda não funciona isoladamente:** faltam os arquivos assets/, templates/, api/ e modules/ do pacote local. Este registro não representa uma publicação completa de código.

**O ZIP não foi anexado ao GitHub Releases:** esta integração do GitHub não fornece a operação de publicar binários em Releases. O arquivo entregue nesta conversa precisa ser anexado manualmente ao Release público para downloads fora do ChatGPT.

## Verificações realizadas

- 42 itens no catálogo, IDs únicos.
- node --check em assets/app.js e php -l em api/bridge.php.
- JSON legível, análise sintática dos scripts Python.
- Teste CRC do ZIP e arquivo SHA256SUMS.txt com hashes dos recursos.

**Ainda pendente:** testar os templates visualmente no Blender e testar execução completa MCP no Windows do usuário. O código Python livre não é isolado por sandbox.

## Instalação

1. Faça Backup JSON dos templates e uma cópia da instalação anterior.
2. Extraia o ZIP em C:\xampp\htdocs\WMK-Blender-Code-Studio.
3. Abra http://127.0.0.1/WMK-Blender-Code-Studio/ com Apache ativo.
4. Para execução direta, habilite extension=sockets no PHP do Apache, reinicie-o e ative o MCP original no Blender na porta 9876 local.
5. Não exponha a ponte PHP ou o socket MCP à internet.

## Roadmap

Consulte roadmap.html para Outliner sincronizado, animação, materiais, rig, imagem para 3D e arquitetura avançada.

**Licença:** preserve MIT e créditos do MCP original, especialmente Siddharth Ahuja.