# Ativar PHP Sockets e executar modelos no Blender

**Para quem usa XAMPP ou PHP comum.** A aplicação Web funciona mesmo sem a extensão `sockets`, mas o botão **Executar template** precisa dela para conversar com o complemento MCP do Blender.

## XAMPP — resolver “Extensão PHP sockets não ativada”
1. Abra **XAMPP Control Panel**.
2. Clique em **Stop** no Apache, se estiver iniciado.
3. Na linha do Apache clique em **Config → PHP (php.ini)**.
4. Pressione **Ctrl+F** e procure `sockets`.
5. Se encontrar `;extension=sockets`, remova **apenas o ponto e vírgula** para ficar `extension=sockets`.
6. Salve o arquivo e inicie o Apache novamente.
7. Atualize o Studio com **Ctrl+Shift+R** e clique em **Conexão MCP local → Testar conexão**.

**Se a linha não existir:** verifique qual versão do PHP/XAMPP você possui e se a extensão está disponível. Não baixe DLLs de fontes não oficiais. O Apache pode usar um `php.ini` diferente do PHP no terminal.

### Verificação
Crie temporariamente `C:\xampp\htdocs\wmk_teste_php.php`:

```php
<?php
header('Content-Type: text/plain; charset=utf-8');
echo 'PHP: ', PHP_VERSION, PHP_EOL;
echo 'sockets: ', extension_loaded('sockets') ? 'ATIVA' : 'INATIVA', PHP_EOL;
echo 'socket_create: ', function_exists('socket_create') ? 'SIM' : 'NAO', PHP_EOL;
```

Abra `http://localhost/wmk_teste_php.php`. Esperado: **sockets: ATIVA** e **socket_create: SIM**. Depois, **apague o arquivo de diagnóstico**.

## PHP comum (sem XAMPP)
No terminal execute `php --ini` para identificar a configuração, `php -m` para listar as extensões e `php -S 127.0.0.1:8000` na raiz do repositório para servir o Studio em `http://127.0.0.1:8000/studio/`. Habilite sockets no `php.ini` correto e reinicie o servidor. O PHP CLI e o Apache podem usar arquivos distintos.

## Teste de ponta a ponta
1. Abra o **Blender** e crie uma cena nova com **File → New → General**.
2. Na viewport 3D pressione **N** e abra a aba **MCP for Blender**.
3. Clique em **Start MCP Server**, caso não esteja ativo.
4. Confirme que a porta configurada é `9876` em `localhost`.
5. Abra o WMK Studio pelo XAMPP/PHP local, entre em **Conexão MCP local** e clique **Testar conexão**.
6. Na galeria escolha o template **Cubo**, abra **Editor & parâmetros**, revise o código Python gerado e marque a confirmação.
7. Clique **Executar template autorizado**; o objeto deve aparecer na cena e no **Outliner** do Blender.

**O Blender precisa estar aberto.** Para executar um `.py` manualmente, use a aba **Scripting → New → Run Script**. Para os templates enviados pelo Studio não é necessário abrir Scripting.

## Editor Monaco
O editor utiliza o idioma Python para destacar palavras-chave, strings, números e comentários. Na versão local v1.2, estão previstos temas, seleção de fonte, tamanho, minimapa e quebra de linha. O Monaco carrega por CDN; se não abrir, use o **Editor simples** e mantenha os scripts acessíveis.

## Segurança
- Use Studio, ponte PHP e socket MCP **somente em localhost**.
- Salve uma cópia do `.blend` antes dos testes.
- A ponte executa apenas templates embutidos com parâmetros validados; código livre editado no Monaco não é executado automaticamente.
- **Não publique** a pasta `studio/api/` em hospedagem Web aberta.

Créditos: **Walney Moreira Klein — walneyk@hotmail.com**. O MCP original é de Siddharth Ahuja e colaboradores, sob licença MIT.
