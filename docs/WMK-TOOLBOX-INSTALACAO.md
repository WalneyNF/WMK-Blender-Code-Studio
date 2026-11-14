# WMK Blender Toolbox v0.1 — instalação e primeiros testes

Este complemento gratuito adiciona uma aba **WMK** à barra lateral do Blender e funciona independentemente do MCP original. É um protótipo ainda não validado na máquina do mantenedor.

## Instalação

1. Abra [wmk_toolbox.py](../wmk_addons/wmk_toolbox.py), clique em **Raw** e salve o arquivo com esse nome.
2. Abra o Blender 5.2.3 LTS, escolha **Edit → Preferences → Add-ons**.
3. Utilize a opção **Install from Disk** (o posicionamento do comando depende da versão do Blender).
4. Selecione `wmk_toolbox.py` e habilite o complemento **WMK Blender Toolbox**.
5. Na Viewport 3D pressione **N**, abra a aba **WMK**.

## Exercício 1 — criar peça

Abra uma cena nova e salve uma cópia do projeto. Na aba WMK selecione **Cubo**, dimensões 2 × 2 × 2, material **Ciano WMK** e clique em **Criar peça WMK**. Confira no Outliner a coleção `WMK_TOOLBOX` e o novo objeto. Repita com **Toro** e **Cilindro**. Para desfazer, use **Ctrl+Z**.

## Exercício 2 — modificador Bevel

Selecione uma peça de malha, ajuste o valor Bevel e clique **Adicionar Bevel**. Confira na aba de modificadores que foi criado `WMK_Bevel` sem aplicação destrutiva.

## Exercício 3 — conexão MCP

Abra o complemento MCP for Blender original, inicie seu servidor no Blender e confirme a porta **9876**. Na aba WMK, clique **Testar conexão MCP**. O resultado verifica somente se existe um listener TCP em `127.0.0.1:9876`; **não autentica o serviço nem executa um script**.

## Exercício 4 — backup

Salve o arquivo `.blend`. Clique **Salvar cópia de segurança** e confira o arquivo `_WMK_BACKUP_*.blend` ao lado do original. Se o projeto ainda não estiver salvo, o painel solicitará salvar primeiro. Não execute experimentos em seu projeto principal.

## Limitações da versão 0.1

- Sem sincronização bidirecional Studio ↔ Blender.
- Sem execução de código livre ou conexão com provedores de IA.
- O diagnóstico de porta não é verificação de identidade/autorização.
- Os templates do Studio e a aba WMK são duas interfaces independentes.
- A compatibilidade precisa ser validada em Blender 5.2.3 e em outras versões suportadas.
- Não altera `src/`, `addon.py`, `pyproject.toml` ou outros arquivos do MCP original.

## Próximos passos

Diagnóstico mais rico, árvore de objetos, transformação e materiais parametrizados, snapshots de cena, exportação GLB e vínculo com o histórico do WMK Studio.

**Créditos:** Walney Moreira Klein — walneyk@hotmail.com. O complemento MCP original permanece sob MIT e atribuição de Siddharth Ahuja e colaboradores.
