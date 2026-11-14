# Conectando o Blender com Codex, VS Code, Cursor e outras IAs

> Este manual é parte do **WMK Blender Code Studio**. Requer o **MCP for Blender** instalado no Blender. Não é necessário instalar o Studio Web para usar o MCP em um cliente de IA.

## 1. Entendendo a arquitetura

```text
Codex / Cursor / VS Code / Claude
      │ cliente MCP (stdio)
      ▼
Servidor Python do MCP for Blender
      │ socket TCP local: 127.0.0.1:9876
      ▼
Add-on MCP dentro do Blender
      │
      ▼
Cena 3D, objetos, materiais e animações
```

O número **9876 não é uma URL HTTP nem um servidor MCP SSE**: é a porta TCP do complemento do Blender. O cliente MCP inicia um **processo Python via `uv`** que conversa com o add-on. Não configure o Cursor apontando diretamente para `http://localhost:9876`.

## 2. Pré-requisitos no Windows

1. Instale [Blender](https://www.blender.org/) e abra-o.
2. Instale [uv](https://docs.astral.sh/uv/), se necessário: `winget install --id=astral-sh.uv -e`.
3. Obtenha o código do MCP, por exemplo em `D:\Ferramentas\mcp-for-blender`.
4. Na pasta do MCP, execute `uv sync --python 3.11` se essa versão do projeto usar Python 3.11; siga também o README original para as versões suportadas.
5. Instale/ative o add-on **MCP for Blender**, conforme o [README original](../README-MCP-ORIGINAL.md).
6. No Blender, pressione **N** na Viewport, selecione **MCP for Blender** e clique em **Start MCP Server** se ele não estiver iniciado.
7. Confirme a porta `9876` e mantenha a conexão limitada ao próprio computador.

> Os caminhos `D:\Ferramentas\...` abaixo são **exemplos**. Substitua-os pela pasta real em que você instalou o fork.

## 3. Codex no VS Code — configuração TOML

Abra o arquivo `%USERPROFILE%\.codex\config.toml` e adicione:

```toml
[mcp_servers.blender]
command = "uv"
args = ["run", "--project", "D:\\Ferramentas\\mcp-for-blender", "--python", "3.11", "mcp-for-blender"]

[mcp_servers.blender.env]
UV_PYTHON_PREFERENCE = "only-managed"
BLENDER_MCP_SAFE_MODE = "1"
BLENDER_HOST = "localhost"
BLENDER_PORT = "9876"
```

Reinicie a sessão do Codex e execute, no terminal em que o comando `codex` esteja disponível:

```powershell
codex mcp list
```

No chat do Codex, peça: **“Use get_scene_info para listar os objetos da cena sem modificar nada.”** Autorize o uso da ferramenta apenas após conferir o comando.

**Nota:** `BLENDER_MCP_SAFE_MODE` depende do código do fork e não é uma sandbox do Python `bpy`. Nunca trate o modo seguro como proteção absoluta.

## 4. Cursor — passo a passo

1. Instale e abra o Cursor.
2. Abra seu projeto.
3. Crie o arquivo `.cursor/mcp.json` no projeto (para configuração local desse projeto), ou `%USERPROFILE%\.cursor\mcp.json` (para usar em todos os projetos).
4. Cole o JSON abaixo:

```json
{
  "mcpServers": {
    "blender": {
      "command": "uv",
      "args": [
        "run",
        "--project",
        "D:\\Ferramentas\\mcp-for-blender",
        "--python",
        "3.11",
        "mcp-for-blender"
      ],
      "env": {
        "UV_PYTHON_PREFERENCE": "only-managed",
        "BLENDER_MCP_SAFE_MODE": "1",
        "BLENDER_HOST": "localhost",
        "BLENDER_PORT": "9876"
      }
    }
  }
}
```

5. Salve o arquivo e reinicie/recarregue o Cursor.
6. Em **Settings → MCP**, verifique o servidor `blender` e suas ferramentas.
7. Abra um chat no modo **Agent** e peça: **“Use o MCP Blender para verificar a cena sem alterá-la.”**
8. Depois de verificar a conexão, faça um teste de criação de cubo em uma cena vazia.

Para projetos de equipe, não inclua segredos nos arquivos de configuração versionados.

Documentação oficial: [Cursor MCP](https://docs.cursor.com/context/model-context-protocol).

## 5. VS Code com GitHub Copilot (diferente do Codex)

**Atenção:** o GitHub Copilot e o Codex têm configurações MCP independentes. O arquivo `config.toml` do Codex não substitui a configuração do Copilot.

Nas versões atuais do VS Code, abra **Chat: Open Customizations → MCP Servers → Add Server**. Para o formato portátil `mcpServers`, um exemplo para a configuração Copilot é:

```json
{
  "mcpServers": {
    "blender": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "--project", "D:\\Ferramentas\\mcp-for-blender", "--python", "3.11", "mcp-for-blender"]
    }
  }
}
```

Se for necessário, inclua também as variáveis de ambiente do exemplo do Cursor. O destino padrão das novas configurações pessoais do Copilot é `~/.copilot/mcp-config.json` (ou `$COPILOT_HOME/mcp-config.json`). O formato antigo `.vscode/mcp.json` usa outra estrutura e está em processo de descontinuação; não copie o JSON diretamente para lá.

Leia [Configuração MCP oficial do VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

## 6. Claude Desktop e outros clientes

Clientes que suportam **MCP por stdio** usam normalmente a mesma estrutura do Cursor:

```json
{
  "mcpServers": {
    "blender": {
      "command": "uv",
      "args": ["run", "--project", "D:\\Ferramentas\\mcp-for-blender", "--python", "3.11", "mcp-for-blender"]
    }
  }
}
```

No Claude Desktop para Windows, confira o arquivo `%APPDATA%\Claude\claude_desktop_config.json`, conforme a versão instalada. Outros clientes podem usar nomes de campos e formatos diferentes; consulte a documentação oficial do respectivo cliente. **Não rode várias cópias concorrentes do servidor MCP na mesma porta sem verificar se o fork suporta isso.**

## 7. Teste de segurança e funcionamento

1. Salve o arquivo `.blend` antes do teste.
2. Abra uma cena nova no Blender.
3. Confirme MCP ativo.
4. No cliente de IA, execute uma ferramenta de **consulta de cena**.
5. Verifique se a ferramenta mostra `Cube`, `Camera` e `Light` na cena inicial, se presentes.
6. Depois faça um teste explícito para criar um cubo `WMK_TESTE_MCP`.
7. Inspecione o resultado na Viewport e no Outliner.

**Nunca comece testando com scripts que apagam objetos ou alteram arquivos.**

## 8. Solução de problemas

| Sintoma | Verificação |
|---|---|
| `uv` não encontrado | Abra novo terminal e execute `uv --version`; ajuste PATH |
| Servidor não conecta | Confirme Blender aberto, add-on ativado e porta 9876 |
| Porta ocupada | Verifique se outro processo está usando `9876` |
| Ferramentas não aparecem | Reinicie o cliente e verifique o caminho de configuração |
| Projeto Python não abre | Execute `uv sync` na pasta correta; confira Python |
| Cursor mostra configuração inválida | Valide o JSON, especialmente barras invertidas `\\` |
| Não funciona fora da máquina | A configuração do exemplo é **somente local**, intencionalmente |
| Erro após atualizar MCP | Verifique compatibilidade entre servidor Python e versão do add-on |

## 9. IA opcional, Studio independente

O **WMK Blender Code Studio** permite aprender scripts `bpy` e gerar modelos sem serviços pagos de IA. Quando um cliente como Codex ou Cursor estiver conectado ao mesmo Blender, ele poderá inspecionar e modificar o modelo com sua autorização. Guarde a versão `.blend`, o prompt, a resposta e o relatório da etapa em seu projeto.

---

**WMK — Walney Moreira Klein — walneyk@hotmail.com**

**MCP original:** © 2025 Siddharth Ahuja e colaboradores; licença MIT preservada.
