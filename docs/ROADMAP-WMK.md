# Roadmap — MCP for Blender + WMK Blender Code Studio

O objetivo é manter **dois sistemas complementares, gratuitos e de código aberto**, sem quebrar o funcionamento do fork original.

## Princípios

1. **Preservar compatibilidade do MCP** com add-ons, clientes MCP e uso existente.
2. **Separar responsabilidade**: MCP é infraestrutura Python/socket; Studio é UI de modelagem com templates e documentação.
3. **Não depender de IA paga** para criar geometrias procedurais.
4. **Não executar Python arbitrário sem revisão**, principalmente scripts recebidos de terceiros.
5. **Priorizar boas práticas e testes automatizados**, evitando alterações cosméticas que quebrem o fluxo.

## MCP — melhorias a pesquisar e testar

### Curto prazo
- [ ] Criar testes de conexão/reconexão TCP e tratamento de portas em uso.
- [ ] Comparar versões servidor/add-on, emitindo avisos claros em português.
- [ ] Validar mensagens JSON, limites de payload e tempo máximo de operações.
- [ ] Avaliar tratamento de erros de `execute_code` sem vazamento de dados confidenciais.
- [ ] Verificar bloqueio de conexões remotas por padrão e respeito à configuração segura do add-on.

### Médio prazo
- [ ] Expor operações seguras de alto nível: criar primitiva, consultar objeto, aplicar material e modifier.
- [ ] Separar inspeção de cena e mutações com escopos distintos.
- [ ] Testes de compatibilidade com diferentes versões do Blender.
- [ ] Melhorar logs com ID da operação e diagnóstico de falhas.
- [ ] Criar mecanismo de undo/checkpoints de operações previsíveis.

> Essas tarefas são **propostas**. Não indicam defeitos confirmados no MCP atual. Revisar implementação e testes antes de alterar o fork.

## Studio — melhorias planejadas

### Básico
- [ ] Validar visualização de todos os 40 scripts com e sem Monaco.
- [ ] Testar ponte PHP → Blender num Windows real.
- [ ] Melhorar a detecção de Blender desconectado e timeout.
- [ ] Testar scripts em cenas vazias, sem afetar projetos anteriores.

### Intermediário
- [ ] Inspector com painéis móveis, redimensionáveis e layout JSON.
- [ ] Árvore de cena sincronizada com Blender.
- [ ] Galeria de templates com exemplos renderizados reais.
- [ ] Exportação de projetos JSON, scripts Python e documentação Markdown.
- [ ] Coleções por projeto, robô, construção e asset.

### Avançado
- [ ] Geradores compostos de casas, vilas e máquinas.
- [ ] Seeds reprodutíveis e peças paramétricas compatíveis com GLB.
- [ ] Presets para games: colisões, pivôs, escala, LOD e hierarquia.
- [ ] Modo Professor para explicar cada operação `bpy`.
- [ ] Diagnósticos de exportação e validação de modelos 3D.

## Integração de IA

A integração opcional com Codex, Cursor, Copilot e Claude é feita via **MCP**, não diretamente pelo Studio. O manual de configuração está em [INTEGRACAO-IAS.md](INTEGRACAO-IAS.md). Planeja-se incluir presets de prompts, registro de entradas/saídas, guias de segurança e catálogo de operações por ferramenta.

## Critérios para uma Release pública

- A pasta `studio/` precisa estar realmente publicada.
- Os arquivos de template devem existir e seu Python precisa passar na verificação sintática.
- O README deve apontar para arquivos e downloads **que existam**.
- A licença MIT e a atribuição do MCP original precisam ser preservadas.
- Deve existir uma distinção explícita entre recursos testados e experimentais.
- A ponte local deve ser testada de ponta a ponta.

---

WMK Blender Code Studio — Walney Moreira Klein — walneyk@hotmail.com

MCP for Blender — © 2025 Siddharth Ahuja e colaboradores, MIT.
