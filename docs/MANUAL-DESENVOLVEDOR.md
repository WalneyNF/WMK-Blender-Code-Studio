# Manual do Desenvolvedor — WMK Blender Code Studio + MCP

## Propósito e limites
O repositório hospeda **dois componentes independentes**: o fork do **MCP for Blender** na raiz, e a aplicação **Studio** em `studio/`. O MCP deve permanecer funcional sem XAMPP; o Studio deve permitir estudar e gerar scripts sem MCP. A integração ocorre por um contrato local — não misture as dependências do servidor MCP com as do navegador.

## Arquitetura
```text
Navegador (HTML/CSS/JS + Monaco)
    | POST JSON (somente localhost)
    v
studio/api/bridge.php
    | valida templateId e parâmetros contra catalog.json
    | cria script bpy usando common.py.txt e código autorizado
    v
socket TCP 127.0.0.1:9876
    | JSON: {"type":"execute_code","params":{"code":"..."}}
    v
Add-on MCP dentro do Blender -> bpy -> cena
```

O MCP também disponibiliza um servidor MCP próprio para clientes de IA; **não confunda** as duas interfaces.

## Arquivos relevantes
- `studio/index.html`: estrutura e entradas do editor.
- `studio/assets/app.js`: estado, seleção de templates, parâmetros, editor, histórico e requisições.
- `studio/assets/app.css`: tema, responsividade e painéis.
- `studio/templates/catalog.json`: catálogo de modelos autorizados.
- `studio/templates/common.py.txt`: utilitários compartilhados com geradores Python.
- `studio/api/bridge.php`: validação e comunicação socket local.
- `studio/manual.html`, `docs/MANUAL-USUARIO.md`: instruções para usuários.
- `docs/ROADMAP-WMK.md`, `studio/roadmap.json`: evolução planejada.
- Raiz `src/`, `addon.py`, `pyproject.toml`: componentes do MCP original (preservar).

## Criar um novo template
1. Copie um registro de `studio/templates/catalog.json` para servir de exemplo.
2. Escolha **ID exclusivo e estável**, em minúsculas, com caracteres `a-z0-9_`.
3. Informe título, categoria, nível, resumo, parâmetros com tipo, valor inicial e limites.
4. Gere o código Python usando exclusivamente parâmetros do catálogo; não aceite fragmentos arbitrários de `bpy` enviados pelo navegador.
5. Utilize uma coleção dedicada para objetos criados, nomes previsíveis e scripts idempotentes quando possível.
6. Teste em cena nova, compare a geometria criada com as dimensões solicitadas e documente exemplos.
7. Crie teste automático de sintaxe Python e validação do schema JSON.
8. Adicione o novo item ao catálogo, aula correspondente e changelog.

**Cuidado:** o catálogo é executável pelo backend local. Revisões de templates exigem revisão de código, não apenas conferência do card.

## Testar alterações
```bash
php -l studio/api/bridge.php
node --check studio/assets/app.js
python -m json.tool studio/templates/catalog.json > /dev/null
```

Para rodar o teste `node --check`, Node.js pode ser instalado **somente como ferramenta opcional de desenvolvimento**; o usuário final não precisa dele.

Teste manual mínimo: abrir a página, navegar por categorias, selecionar template, mostrar código, ajustar parâmetros, gerar novamente, copiar, baixar `.py`, testar MCP, executar template autorizado, verificar objeto no Blender, gerar backup JSON e recarregar.

## Segurança
- **Nunca** exponha a ponte PHP ou o socket Blender em uma interface pública.
- Restrinja endereço remoto, Host e Origin, valide método HTTP e tamanho da requisição.
- A ponte deve consultar **somente um catálogo de templates revisados** e aceitar parâmetros tipados com limites.
- Não aceite execução arbitrária de texto do Monaco pelo endpoint público.
- Evite shell, `eval`, `exec`, arquivos externos e escrita fora das pastas autorizadas.
- Faça backup da cena antes de operações destrutivas.
- A conexão TCP envia comandos sequenciais; documente timeouts, respostas incompletas e reconexão.
- Antes de uma distribuição pública estável, acrescente autenticação de sessão/anti-CSRF apropriada e revise possíveis ataques por navegação a localhost.

## Contribuições ao MCP
- Preserve a API de transporte e a compatibilidade com versões anteriores do complemento.
- Inclua testes para novas mensagens e parâmetros.
- Evite mudanças não documentadas na forma de retorno JSON.
- Valide thread safety, limite de tamanho, cancelamento e tratamento de exceções.
- Separe mudanças no MCP de melhorias do Studio em commits e revisões distintas.
- Teste com Blender aberto e várias cenas, inclusive cenas salvas.

## Integração com Codex e Cursor
Cliente MCP -> processo `uv run --project ... mcp-for-blender` -> complemento no Blender. Consulte [manual de IAs](INTEGRACAO-IAS.md) para exemplos atuais e lembre-se de que nomes de menus variam entre clientes/versões. Nunca documente uma conexão como validada sem teste real.

## Bibliotecas Python
O Blender fornece sua distribuição Python. Pacotes externos devem ser compatíveis com ela; preferir bibliotecas puramente Python. Bibliotecas que exigem compilação nativa podem precisar de versões específicas. Não instale dependências automaticamente na máquina de quem usa o Studio. Registre versões, propósito, licença, origem e estratégia de fallback.

## Boas práticas de UX
- Editor simples sempre disponível se Monaco falhar.
- Nunca perder conteúdo editado ao trocar de aba/template.
- Painéis flexíveis com layout JSON versionado.
- Templates com parâmetros, descrição, exemplos e botão de restaurar originais.
- Suporte a importação/exportação de bibliotecas assinadas ou revisadas; scripts de terceiros devem permanecer não executáveis por padrão.
- Acessibilidade, navegação por teclado e mensagens de erro em português.

## Licenciamento e atribuição
O MCP original usa **MIT**, com Copyright (c) 2025 Siddharth Ahuja. **Mantenha o texto e os avisos originais**. Adições WMK devem informar autoria e licença sem substituir o copyright original. Componentes de terceiros podem ter licenças próprias (Monaco, Blender, imagens e assets). Não declare que todo conteúdo externo está automaticamente sob MIT.

## Critérios de aceite para um PR
Código formatado, teste de sintaxe, exemplo manual reproduzível, sem regressão no MCP, sem upload de credenciais ou arquivos .blend privados, documentação pt-BR atualizada, roadmap sincronizado e changelog resumido.

**Mantenedor do Studio:** Walney Moreira Klein — walneyk@hotmail.com.
