# Manual do Usuário — WMK Blender Code Studio

> **Gratuito, em português e baseado em Python.** O Studio é uma interface complementar ao Blender; o MCP for Blender é mantido no mesmo repositório para permitir operações locais ou integração com IAs.

## 1. O que você vai aprender
Você não precisa saber modelar para começar: escolha uma peça, ajuste largura/altura/segmentos no painel, observe o código `bpy` e gere a malha dentro do Blender. Os modelos básicos são procedurais; personagens orgânicos e assets profissionais exigem refinamento posterior.

## 2. Pré-requisitos
- Blender com interface gráfica (recomenda-se usar a versão compatível com o complemento instalado).
- Windows, Linux ou macOS com PHP **8.1+** e extensão `sockets` habilitada, caso queira o botão de execução.
- O complemento MCP for Blender habilitado no Blender, escutando em `127.0.0.1:9876`.
- Navegador atual. O Monaco requer carregamento de recursos da internet, mas o editor de texto simples funciona offline.

**Sem PHP ou MCP:** você ainda pode abrir o Studio para estudar, copiar e baixar os arquivos `.py`, executando-os manualmente no Blender.

## 3. Instalar pelo XAMPP (Windows)
1. Instale o Blender e o XAMPP.
2. Baixe o código do repositório pelo botão **Code → Download ZIP**, ou baixe o pacote do Studio quando houver uma Release publicada.
3. Extraia o projeto em `C:\xampp\htdocs\WMK-Blender-Code-Studio\`.
4. Abra o XAMPP Control Panel e inicie **Apache**.
5. Acesse `http://localhost/WMK-Blender-Code-Studio/studio/`.
6. Se a conexão informar que não existe a extensão sockets, localize o `php.ini` do Apache, habilite `extension=sockets` e reinicie o Apache.
7. Caso apareça versão antiga no navegador, atualize com `Ctrl+Shift+R`.

## 4. Instalar com servidor PHP simples
Abra o terminal na **raiz do repositório**:

```powershell
cd D:\Ferramentas\WMK-Blender-Code-Studio
php -v
php -m | findstr /i sockets
php -S 127.0.0.1:8000
```

Acesse `http://127.0.0.1:8000/studio/`. Não use `php -S 0.0.0.0:8000`: a ponte foi projetada para uso local. O servidor PHP embutido é conveniente para desenvolvimento, não para hospedagem pública.

## 5. Ativar o MCP dentro do Blender
1. Instale e habilite o complemento **MCP for Blender** conforme as instruções do fork em `README-MCP-ORIGINAL.md`.
2. Abra o Blender em modo gráfico e escolha uma **cena de teste vazia**.
3. Na janela 3D, pressione `N` para revelar a barra lateral.
4. Selecione a guia **MCP for Blender**.
5. Verifique se o servidor local está ativo. Se não estiver, clique em **Start MCP Server**.
6. Confirme que a porta exibida é **9876** e que a conexão usa `localhost` / `127.0.0.1`. Nunca abra essa porta para acesso público.
7. No Studio, entre em **Conexão MCP local** e clique em **Testar conexão**. O Studio enviará apenas um comando de observação.

**Dica:** o servidor MCP usado pelo Codex e o socket do complemento são componentes diferentes. O Studio usa uma ponte PHP que conversa diretamente com o socket do complemento. Não precisa manter o Codex aberto para executar templates predefinidos.

## 6. Primeiro teste: um cubo
1. No Blender, faça `File → New → General`. Salve uma cópia do projeto antes de testar.
2. No Studio, abra **Marketplace de templates → Cubo → Abrir editor**.
3. Configure as dimensões e clique em **Regenerar código**.
4. Confirme que o código foi exibido. Se o Monaco estiver em branco, clique em **Editor simples**.
5. Clique em **Testar conexão local**.
6. Marque a caixa que confirma a alteração da cena.
7. Clique em **Executar template autorizado**.
8. Volte ao Blender e confira no **Outliner** e na viewport se o novo objeto foi criado.
9. Repita o procedimento com **Cilindro**, **Toro** e **Engrenagem simples**.

**Não conseguiu conectar?** Confirme Blender aberto, complemento ativo, porta correta, extensão sockets do PHP, Apache executando e ausência de bloqueio por firewall. Consulte o console do navegador (F12) e o log do Apache.

## 7. Entender a interface
- **Marketplace:** pesquisar por categoria, nível, favoritos e abrir templates.
- **Editor & parâmetros:** painel de propriedades, script Python, copiar, baixar e gerar o código.
- **Meus templates:** duplicar e personalizar sem alterar os modelos originais.
- **Projetos & DNA:** associar scripts e configurações a robôs, jogos ou experiências.
- **Aulas:** exercícios progressivos do primeiro cubo à exportação de assets.
- **Conexão:** testar a ponte PHP e consultar mensagens de retorno.

## 8. O que é Python do Blender?
`bpy` é a API que dá acesso à cena e aos objetos do Blender. Por exemplo:

```python
import bpy
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
bpy.context.object.name = "Meu_Primeiro_Cubo"
```

Você também pode executar esse script no próprio Blender: **Scripting → New → colar código → Run Script**. O Python embutido no Blender pode ter versão e bibliotecas diferentes do Python do Windows. Instale extensões sempre na versão correta e de preferência num ambiente separado.

## 9. Modelagem por etapas
**Básico:** cubo, esfera, cilindro, cone, toro, escala e materiais.  
**Intermediário:** modificadores Bevel/Mirror/Array, hierarquia, pivôs e juntas.  
**Avançado:** casas modulares, veículos, robôs, animações e exportação glTF/GLB.

Os templates são exemplos didáticos. Antes de incorporar assets a um jogo, valide materiais, escala, orientação, geometria, rig, animações, limites de polígonos e licença de componentes importados.

## 10. Segurança e backup
- **Salve uma cópia .blend** antes de executar qualquer template.
- A ponte PHP aceita apenas os templates originais e parâmetros validados. Editar livremente o Python no Monaco **não** significa que esse código será executado pelo botão de template.
- Python executado dentro do Blender pode acessar arquivos do computador. Não execute scripts desconhecidos.
- Não hospede a pasta `studio/api` em servidores públicos nem exponha a porta MCP.
- Os projetos do Studio podem usar armazenamento do navegador; exporte o backup JSON antes de limpar os dados do site.

## 11. Usar sem IA e com IA
**Sem IA:** configure templates e envie-os ao Blender pela ponte local.  
**Com IA:** Codex, Cursor e outros clientes MCP podem inspecionar e modelar diretamente pelo MCP, independentemente do Studio. Consulte [Integração com IAs](INTEGRACAO-IAS.md).

## 12. Perguntas frequentes
**O Monaco está em branco:** use **Editor simples**; confira bloqueadores, internet e console do navegador.  
**O botão Executar não funciona:** teste a ponte primeiro; verifique o complemento Blender.  
**Posso editar o script à vontade?** Sim, mas a execução direta de código livre está deliberadamente bloqueada pela ponte por segurança; copie e rode manualmente após revisar.  
**Posso vender modelos gerados?** O código MIT permite uso comercial, mas verifique separadamente licenças de imagens, bibliotecas e assets incorporados.  
**Preciso pagar pela IA?** Não para gerar os templates locais. Modelos de IA externos podem ter custos próprios.

**Projeto WMK — Walney Moreira Klein — walneyk@hotmail.com.** MCP original por Siddharth Ahuja e colaboradores; preserve os avisos de copyright e licença MIT existentes.
