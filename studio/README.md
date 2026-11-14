# WMK Blender Code Studio v1.4.5 — Correção de Salvamento e Escala

**Walney Moreira Klein — walneyk@hotmail.com**

**NOVO:** o botão Salvar template preserva o Python inteiro e os parâmetros; cópias dos modelos originais não apagam edições. Os **42 templates** incluem agora parâmetro **Escala global**, aplicado tanto ao script Python baixado quanto à operação autorizada pelo MCP local.

Leia [o guia da correção](docs/CORRECAO-SALVAR-E-ESCALA-v1.4.5.md) antes de atualizar, e use **Backup JSON** da instalação antiga.

---

<div align="center">

# WMK Blender Code Studio
**Modele em 3D com código • Python • Blender • Templates procedurais**

[Manual completo](manual.html) · [Catálogo](docs/catalogo.html) · [Guia da comunidade](docs/GUIA-COMUNIDADE.md)
</div>

**Modelagem 3D via código Python, com templates e integração local ao Blender.**

Projeto educacional em português do Brasil para desenvolvedores que querem criar modelos 3D sem depender exclusivamente da interface manual do Blender. Desenvolvido como um **Studio complementar** ao [Blender](https://www.blender.org/) e ao projeto [MCP for Blender](https://github.com/ahujasid/mcp-for-blender).

> **Atenção ao repositório:** este repositório foi renomeado a partir de um fork do **MCP for Blender**. O Studio é um componente novo e separado. Preserve o código, a licença MIT e os créditos do projeto MCP original. O Studio **não substitui** o add-on MCP nem o servidor Python existente.

## Recursos da versão 1.1

- **41 templates procedurais** em 9 categorias: geometria, operações, mecânica, construções, robôs, personagens, armas cenográficas, veículos e cenários.
- **Editor Monaco** de Python por CDN, com editor simples alternativo quando indisponível.
- Parâmetros editáveis por template, geração de código `bpy` e download de `.py`.
- Biblioteca pessoal: duplicar templates, criar novos, pesquisar e favoritar.
- **Projetos & DNA**: cadastrar projetos e guardar scripts/parametrizações em histórico exportável.
- **Ponte PHP para o Blender MCP** via `127.0.0.1:9876`, com execução limitada aos templates embutidos e parâmetros validados.
- Manual HTML completo, catálogo e exercícios progressivos em português.

## Instalação rápida (Windows + XAMPP)

1. Instale o Blender e XAMPP com PHP 8.1 ou superior.
2. **Instalação pelo ZIP desta conversa:** extraia a pasta `WMK-Blender-Code-Studio` em `C:\xampp\htdocs\`. **Publicação neste repositório:** o conteúdo do pacote pode ser colocado em uma pasta `studio/`, preservando o código original do fork MCP.
3. Inicie o Apache e abra **http://localhost/WMK-Blender-Code-Studio/**. Se você instalou a partir de um clone do GitHub e manteve os arquivos em `studio/`, use **http://localhost/WMK-Blender-Code-Studio/studio/**.
4. Para executar no Blender: abra o programa, habilite o add-on MCP, confirme a conexão local na porta `9876` e teste na seção **Conexão**.
5. Comece com o template **Cubo** e experimente modificações numa cena vazia.

**Sem MCP:** a aplicação continua útil para gerar, estudar, copiar e baixar scripts `.py`, que você executa no Blender em **Scripting → Run Script**.

## Estrutura sugerida do repositório

```text
WMK-Blender-Code-Studio/
├── README.md                 ← documentação principal
├── LICENSE                   ← manter licença original do fork
├── src/                      ← código do MCP existente, não sobrescrever
├── addon.py                  ← add-on do MCP, quando presente
└── studio/                   ← nova aplicação Web
    ├── index.html
    ├── manual.html
    ├── api/bridge.php
    ├── assets/app.css
    ├── assets/app.js
    ├── templates/catalog.json
    ├── templates/common.py.txt
    └── docs/catalogo.html
```

## Segurança

- Use somente no próprio computador, servindo a aplicação via `localhost`.
- **O código Python personalizado do Monaco não é executado pela ponte PHP**: apenas templates originais autorizados com argumentos validados.
- Os templates embutidos executam Python dentro do Blender e **modificam a cena aberta**. Confirme antes, salve seu `.blend` e faça backups.
- Não publique `studio/api/` como serviço remoto nem abra a porta `9876` para a rede.
- Os dados pessoais de projetos/templates são guardados localmente no navegador; exporte backups JSON regularmente.

## Aprenda Python para Blender

No aplicativo, abra [Manual HTML](studio/manual.html). O material apresenta a API `bpy`, transformações, materiais, modificadores, animações, uso de bibliotecas Python, scripts e exercícios do básico ao avançado. Veja também o [Catálogo de 41 templates](studio/docs/catalogo.html).

Exemplo inicial:

```python
import bpy
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
bpy.context.object.name = "WMK_Primeiro_Cubo"
```

## Escopo e limitações

Esta é uma **versão inicial para testes**. Os templates geram geometria procedural simplificada: não prometem modelos orgânicos cinematográficos, rig automático de produção ou assets otimizados para todos os jogos. O editor Monaco exige internet (CDN) neste pacote. Ainda é necessário verificar a conexão MCP e executar os templates no seu ambiente Windows/Blender. O fork MCP permanece separado.

## Créditos

**WMK Blender Code Studio:** Walney Moreira Klein — walneyk@hotmail.com.

**MCP for Blender:** projeto original de [ahujasid/mcp-for-blender](https://github.com/ahujasid/mcp-for-blender) e respectivos colaboradores, sob seus avisos de licença. **Blender:** Blender Foundation e comunidade. Monaco Editor: Microsoft, conforme seus próprios termos. O Studio não é produto oficial da Blender Foundation, Microsoft ou MCP for Blender.

## Contribuições

Contribuições de templates, traduções, melhorias de UX, testes e correções são bem-vindas. Abra uma issue com passos para reproduzir problemas. Ao adicionar templates, documente parâmetros, dependências, versão do Blender testada, exemplo de resultado e licença dos assets utilizados.


## Identidade visual WMK

| Arquivo | Uso |
|---|---|

Créditos do Studio: **Walney Moreira Klein — walneyk@hotmail.com**. Preserve os créditos/licenças originais do MCP e do Blender.

## Nota sobre a execução do Python

O Editor Monaco é um ambiente para estudar e editar scripts. O botão MCP executa **somente templates embutidos e parâmetros permitidos** usando o catálogo no servidor PHP; não executa automaticamente o conteúdo livre do Monaco. Para testar alterações pessoais, utilize o `.py` baixado no Blender → Scripting, depois de revisar o código.


## v1.3 — IDE Python Pro

Nova interface de código: três temas WMK adicionais (Neon Hacker, Ocean e Amber), fonte ajustável, modo foco que ocupa a tela, zoom A+/A-, atalhos, sugestões contextualizadas de Python, snippets de rig mecânico, textura procedural, rotor, exportação GLB e inspeção de cena. Preferências persistidas no navegador. O Monaco precisa de internet para carregar seu CDN; em modo offline o editor simples continua disponível.

**Atenção:** código livre no editor não é executado pela ponte PHP. Os templates autorizados mantêm a política de execução original. Teste o Python livre em Blender > Scripting e salve uma cópia do `.blend`.

## Atualização v1.4.4 — Dobradiça paramétrica

O Marketplace agora oferece **42 templates**, incluindo **Dobradiça de porta paramétrica**, na categoria Mecânica. Confira o [manual](docs/DOBRADICA-TEMPLATE.md). Auditoria de sintaxe e parâmetros concluída; execução visual no Blender pendente.