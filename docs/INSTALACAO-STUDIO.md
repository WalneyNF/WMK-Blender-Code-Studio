# Instalação do WMK Blender Code Studio — XAMPP ou PHP local

**Público-alvo:** iniciantes em Blender que conhecem programação ou desejam começar com Python.

## Antes de começar

Este repositório guarda o **MCP for Blender original** na raiz. O Studio Web fica separado na pasta `studio/` quando distribuído e publicado. Não substitua a raiz do MCP por uma pasta Web.

**Requisitos para o Studio:** Windows, Linux ou macOS com PHP 8.1+; navegador moderno. XAMPP é uma alternativa prática no Windows. Blender e o complemento MCP são necessários **somente** para criar objetos diretamente pelo botão de execução; o editor e o estudo dos scripts podem ser usados sem Blender conectado.

## A. Instalação pelo XAMPP no Windows

1. Instale o [XAMPP](https://www.apachefriends.org/).
2. Confirme que o PHP do XAMPP está disponível e tem pelo menos a versão 8.1.
3. Extraia o **pacote completo da aplicação Web**, que deverá conter `index.html`, `assets/`, `templates/` e `api/`.
4. Copie a pasta completa para `C:\xampp\htdocs\WMK-Blender-Code-Studio\`.
5. Abra **XAMPP Control Panel** e clique em **Start** ao lado de Apache.
6. No navegador, acesse `http://localhost/WMK-Blender-Code-Studio/`.
7. Se aparecer uma versão antiga da interface, pressione `Ctrl + Shift + R`.
8. Escolha **Cubo**, abra **Editor & parâmetros** e confirme que existe código Python com `import bpy`.

**Se o Studio estiver dentro do clone deste repositório em `studio/`**, o endereço será `http://localhost/WMK-Blender-Code-Studio/studio/` e você deve copiar a pasta raiz inteira para `htdocs` ou configurar o document root apropriadamente.

### Diagnóstico básico de PHP

Crie temporariamente um arquivo `phpinfo.php` com o conteúdo `<?php echo PHP_VERSION; ?>` na pasta servida, abra-o no navegador e **apague-o logo em seguida**. Se você enxergar o código PHP sem execução, o servidor não está configurado para PHP.

## B. Instalação por servidor PHP integrado

Abra PowerShell ou Terminal dentro da pasta da aplicação:

```powershell
php -v
php -S 127.0.0.1:8000
```

Abra `http://127.0.0.1:8000/`. Deixe o terminal aberto enquanto estiver usando o Studio.

> O servidor integrado é somente para desenvolvimento local. **Não o exponha publicamente.**

## C. Conectar ao Blender MCP

1. Instale o Blender.
2. Instale e ative o add-on do [MCP original](../README-MCP-ORIGINAL.md).
3. Abra a cena de teste e **salve o arquivo .blend**.
4. Na Viewport, pressione **N**; abra a aba MCP e inicie o servidor.
5. Confirme que está escutando localmente em `127.0.0.1:9876`.
6. Abra o Studio na **mesma máquina**, entre no painel **Conexão** e consulte o estado.
7. Somente depois selecione um template **embutido** e clique em executar. Aceite a confirmação e confira a nova peça no Outliner.

A versão v1.x da ponte usa comunicação com a porta local do add-on; essa integração precisa ser validada na máquina de cada usuário. Ela não depende de Codex ou outra IA.

## D. Testar sem qualquer integração

Abra o Blender → **Scripting** → **New** e execute:

```python
import bpy

bpy.ops.mesh.primitive_uv_sphere_add(
    segments=24,
    ring_count=12,
    radius=1.0,
    location=(0, 0, 1.0),
)
bpy.context.object.name = "WMK_Teste_Esfera"
```

Confira se o objeto `WMK_Teste_Esfera` aparece no Outliner.

## E. Códigos do Monaco em branco

- Verifique se você abriu a aba Editor antes de esperar a renderização completa do Monaco.
- Atualize com `Ctrl + Shift + R`.
- Teste o **editor simples** como fallback.
- Confira no console se o CDN do Monaco foi bloqueado pelo navegador, firewall ou extensão.
- Confira se `templates/catalog.json` e os arquivos de geração retornam **200**, não **404**.
- Não trate `window.monaco` como prova de que `monaco.editor.create` já está carregado.
- Os scripts embutidos podem estar carregados nos dados mesmo quando a visualização Monaco está vazia.

## F. Dados e backup

Alguns cadastros e templates pessoais são armazenados no navegador. **Limpar os dados do navegador pode apagá-los.** Exporte cópias JSON e mantenha arquivos `.blend` separados, com nomes e versões claras.

## G. Instalação pública e segurança

O Studio é uma ferramenta **local de desenvolvimento**. Não disponibilize uma API PHP aberta que execute Python arbitrário no Blender. A execução segura requer validação rigorosa de operações e parâmetros, controles de origem, confirmação e isolamento de rede.

Para hospedar apenas o guia e a demonstração visual, use um site estático **sem** a ponte PHP e sem execução remota.

---

WMK Blender Code Studio — Walney Moreira Klein — walneyk@hotmail.com

MCP for Blender original — © 2025 Siddharth Ahuja, sob MIT.
