# Demonstração real — WMK Blender Code Studio → Blender

Esta demonstração foi realizada pelo mantenedor do projeto no Windows, com **WMK Blender Code Studio**, **XAMPP/PHP com sockets habilitado**, **Blender 5.2.3 LTS** e o complemento **MCP for Blender**.

**Evidência observável:** o template **Toro** foi selecionado no Studio; o editor exibiu um script Python de 72 linhas; a interface retornou `"executed": true` e uma mensagem de execução do template; o Blender mostrou um objeto `WMK_Toro` selecionado, na coleção `WMK_LAB_toro`, com material roxo. As capturas não demonstram que os outros 39 templates tenham sido testados, nem que scripts arbitrários do Monaco possam ser executados pela ponte.

## As seis capturas

| Ordem | Arquivo a publicar em `docs/screenshots/` | O que demonstra |
|---|---|---|
| 01 | `01-blender-cena-inicial.jpg` | Cena inicial do Blender antes da criação do objeto |
| 02 | `02-marketplace.jpg` | Interface Web e marketplace de templates |
| 03 | `03-biblioteca-templates.jpg` | Cards e categorias da biblioteca de modelos |
| 04 | `04-editor-toro.jpg` | Template Toro, parâmetros e Python gerado |
| 05 | `05-envio-mcp.jpg` | Resposta da aplicação após envio do template |
| 06 | `06-toro-no-blender.jpg` | `WMK_Toro` criado e selecionado no Blender |

As capturas são de uma sessão real de teste. O Blender estava aberto em modo gráfico e o Studio foi executado localmente.

> **Publicação das imagens:** o material foi preparado como pacote ZIP separado. Os links visuais abaixo devem ser ativados quando os seis arquivos forem efetivamente enviados para `docs/screenshots/` no repositório.

## Passo a passo para reproduzir

1. Inicie o **Blender** e abra uma cena de testes. Salve uma cópia se houver trabalho importante.
2. No Viewport, pressione `N`, abra a guia **MCP for Blender** e confirme o servidor escutando em `localhost:9876`.
3. No XAMPP, em **Apache → Config → PHP (php.ini)**, confirme `extension=sockets` (sem o `;` no início). Reinicie o Apache caso tenha alterado.
4. Acesse a instalação local do WMK Blender Code Studio pelo Apache/PHP.
5. No Marketplace, escolha **Toro**, clique **Abrir editor** e confira o código Python e parâmetros. No editor simples, o realce visual é limitado; o Monaco permite destacar tokens Python.
6. Clique **Testar conexão local**. Se necessário, revise a porta ou os logs.
7. Marque a confirmação **Confirmo que a execução altera a cena aberta**.
8. Clique **Executar template autorizado**.
9. Confira a mensagem de resposta no Studio e o objeto `WMK_Toro` no **Outliner** e na vista 3D do Blender.
10. Faça uma segunda execução variando os raios para testar a parametrização, preservando os arquivos de referência.

## Diagnóstico

| Sintoma | Verificação |
|---|---|
| `Extensão PHP sockets não ativada` | Editar `php.ini`: habilitar `extension=sockets`, reiniciar Apache |
| Falha na porta 9876 | Blender aberto, add-on habilitado, servidor MCP iniciado, endereço localhost |
| Código não aparece | Usar **Editor simples**; verificar scripts/CDN do Monaco e cache |
| “Executado” mas nada visível | Abrir Outliner; conferir coleções `WMK_LAB_*`, enquadrar objeto com Numpad `.`, checar visibilidade |
| Template altera projeto | Salvar cópia `.blend` e usar cena vazia para testes |

## Próximas comprovações

- Teste automatizado e visual dos **40 templates**.
- Teste de reconexão após fechar e reabrir o Blender.
- Teste de compatibilidade com Windows/XAMPP e PHP integrado.
- Teste de materiais, pivôs e exportação glTF/GLB.
- Teste de memória, execução sequencial e cancelamento seguro.

**Licença e atribuição:** o Studio é iniciativa WMK de Walney Moreira Klein; o MCP original pertence aos respectivos autores e colaboradores e mantém seus avisos MIT. Estas capturas foram fornecidas pelo mantenedor como demonstração técnica.
