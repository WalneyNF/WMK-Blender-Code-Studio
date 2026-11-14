# WMK AI Modeler — Proposta de integração com provedores de IA

**Estado:** projeto de arquitetura/documentação. Não está implementado como endpoint funcional. O MCP original continua utilizável com clientes como Codex e Cursor.

## Objetivo

Oferecer uma IDE de modelagem 3D em que o usuário descreve uma peça, a IA produz um script Python `bpy`, o Studio mostra o código no editor, e **a execução ocorre apenas depois da revisão e confirmação**.

## Duas formas de integrar IA

**A. IA dentro do Studio:** módulo PHP local chama APIs externas (Groq, OpenAI, Gemini) ou serviços locais (Ollama), recebendo respostas em texto/código; o Blender não é exposto na rede. O Studio faz o papel de host e controlador da experiência.

**B. IA por clientes MCP:** Codex, Cursor, Claude e outros clientes conectam o servidor `mcp-for-blender` ao complemento no Blender. A API de IA e a autenticação pertencem ao cliente, conforme sua configuração. Para isso, **não é necessário** que o addon do Blender armazene chaves dos provedores.

A especificação MCP separa hosts/clientes/servidores. O servidor fornece ferramentas; não deve assumir que controla os custos e a credencial do modelo que o usa.

## Adaptadores planejados

| Provedor | Transporte | Autenticação |
|---|---|---|
| Groq | HTTPS, interface de chat compatível com parte da API OpenAI | `GROQ_API_KEY` |
| OpenAI | HTTPS, API oficial | `OPENAI_API_KEY` |
| Gemini | API oficial Google (adaptador independente) | chave Google |
| Ollama | HTTP local em `127.0.0.1:11434` | normalmente sem chave em ambiente local |

Modelos e endpoints devem ser configuráveis e verificados em documentação oficial. Um adaptador não garante paridade de recursos: modelos diferentes podem oferecer limites de contexto, chamadas de ferramentas e formatos diversos.

## Armazenamento de credenciais

1. **Nunca** incluir chaves no HTML, JS, catálogo, backup JSON, URL ou repositório Git.
2. Preferir variáveis de ambiente de processos **locais**, cofre de credenciais do sistema ou arquivos de configuração fora do Web root e fora do Git.
3. No XAMPP, não colocar o segredo em `htdocs`. O PHP deve obter o segredo de uma fonte local segura, não retorná-lo ao navegador.
4. A tela da API deve indicar conectado/desconectado e ocultar o valor completo da chave.
5. Não gravar chaves ou prompts sensíveis em logs.
6. Restringir o servidor PHP a loopback; não oferecer um endpoint de proxy genérico para URLs arbitrárias (SSRF).
7. Validação de Origin/Host, sessão local, proteção contra CSRF, tempo limite e cotas de chamadas são requisitos antes de habilitar execução via navegador.

## Pipeline de geração proposto

```text
Pedido do usuário
  → adaptar prompt ao template e às restrições Blender
  → provedor IA gera explicação + bpy
  → Monaco exibe diff e destaques
  → validador AST / política de operações
  → prévia/inspeção e confirmação explícita
  → backup ou checkpoint
  → envio ao Blender por operação autorizada
  → retorno, captura e registro no DNA do asset
```

O validador AST não é sandbox infalível. Código livre nunca deve ser executado automaticamente após a resposta de IA; preferir inicialmente operações paramétricas allowlisted.

## Interfaces previstas

- Configurações por provedor e modelo; conexão/teste sem divulgar segredo.
- Editor de prompt e presets (casa, espada, robô, veículo, cenário).
- Resultado lado a lado: explicação, código, parâmetros e possíveis riscos.
- Copiar, salvar rascunho, comparar versões e registrar tentativas.
- Orçamento de tokens, limite por requisição, cancelamento e logs sem credenciais.
- Autonomia graduada: somente sugerir, pedir aprovação em cada ação, permitir apenas ações seguras.

## Etapas de implementação

1. Módulo `AIProvider` com resposta padronizada e teste de conexão.
2. Adaptadores Groq e Ollama com prompts de geração de código (sem execução).
3. Integração no Monaco, histórico local e exportação JSON **sem credenciais**.
4. Política de segurança, validação AST e operações de Blender revisadas.
5. Testes de API com respostas simuladas; testes manuais de Blender isolados.
6. Adaptadores OpenAI, Gemini e outros provedores conforme demanda.

## Exemplo de prompt de segurança

> Você é um assistente de modelagem para Blender. Gere apenas um script bpy que crie objetos novos em uma coleção própria, sem apagar objetos existentes, abrir arquivos, executar shell ou acessar a rede. Explique o código em português e descreva os parâmetros, as alterações e os riscos.

**Contribuição:** WMK Blender Code Studio — Walney Moreira Klein — walneyk@hotmail.com.
