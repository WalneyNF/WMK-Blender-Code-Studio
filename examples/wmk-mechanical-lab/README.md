# WMK Mechanical Lab — Dobradiça Paramétrica

**Walney Moreira Klein — walneyk@hotmail.com**

Esta demonstração transforma uma dobradiça de porta em um conjunto de **componentes Python `bpy`** totalmente separado no Blender.

## Teste em 5 minutos

1. No GitHub, baixe [dobradica_parametrica.py](./dobradica_parametrica.py).
2. Abra o Blender 4.2 ou posterior, salve uma cópia de sua cena e entre em **Scripting**.
3. Abra o script com **Text Editor → Open** e execute **Alt+P**.
4. Confira a coleção `WMK_DOBRADICA_...` no Outliner. Os elementos principais são `WMK_Chapa_Esquerda`, `WMK_Chapa_Direita`, `WMK_Anel_E_...`, `WMK_Anel_D_...`, `WMK_Pino_Central` e `WMK_CTRL_ABERTURA`.
5. Mova a linha do tempo entre os frames **1 e 50**: a chapa direita gira ao redor do eixo vertical Z.

**O script não apaga a cena e não depende de IA, XAMPP ou MCP.** A execução no Blender do usuário ainda precisa ser verificada visualmente.

## Alterar as medidas

Todos os parâmetros ficam no dicionário `P` no começo do arquivo, com medidas em **metros**:

| Parâmetro | Padrão | Significado |
|---|---:|---|
| `altura` | 0.105 | Altura da dobradiça: 105 mm |
| `largura_cada_chapa` | 0.048 | Largura de cada chapa: 48 mm |
| `espessura_chapa` | 0.003 | Espessura de cada chapa: 3 mm |
| `raio_externo` | 0.007 | Raio externo dos anéis |
| `raio_furo_eixo` | 0.004 | Raio interno de passagem do pino |
| `raio_pino` | 0.0036 | Raio do pino |
| `raio_fu_ro_parafuso` | 0.0028 | Raio dos furos de parafuso |
| `numero_segmentos` | 5 | Anéis intercalados entre as chapas |
| `numero_furos_por_chapa` | 3 | Furos por folha |
| `folga_entre_aneis` | 0.0006 | Folga axial entre anéis |
| `abertura_graus` | 95 | Abertura de demonstração |
| `animar` | True | Habilita keyframes de abertura |

## Como funciona geometricamente?

- Uma **chapa** é um cubo alongado com dimensões em metros.
- Cada **furo de parafuso** é um cilindro temporário orientado na direção Y. Um modificador **Boolean Difference** subtrai esse cilindro da chapa e depois o objeto temporário é removido.
- Cada **anel** é um cilindro com um segundo cilindro subtraído do centro, produzindo um tubo oco.
- Os anéis alternam entre as chapas esquerda e direita. Os anéis da direita acompanham o controlador `WMK_CTRL_ABERTURA`.
- O **pino** é um cilindro independente que atravessa o centro dos anéis.
- A animação gira apenas o controlador, sem precisar mover manualmente cada peça.

### Organização esperada no Outliner

```text
WMK_DOBRADICA_...
├── WMK_Chapa_Esquerda
├── WMK_Chapa_Direita
├── WMK_CTRL_ABERTURA
│   ├── WMK_Chapa_Direita (parent)
│   ├── WMK_Anel_D_02
│   └── WMK_Anel_D_04
├── WMK_Anel_E_01
├── WMK_Anel_E_03
├── WMK_Anel_E_05
├── WMK_Pino_Central
└── WMK_Cabeca_Pino
```

A visualização acima representa relações de **parentesco**, não subcoleções dentro do Blender.

## Como exibir ao vivo no WMK Studio?

A arquitetura recomendada é gerar **dois resultados a partir do mesmo JSON**:

```text
Parâmetros JSON da dobradiça
          │
          ├── Gerador JavaScript/Three.js → preview interativo no navegador
          │
          └── Gerador Python/bpy → geometria nativa no Blender
```

Esse **preview sincronizado da dobradiça ainda não está implementado**; este commit publica o gerador Blender. Usar dois geradores exige testes de equivalência entre booleans, orientação, unidades e materiais. O protótipo de visualização geral está em [WMK Hybrid Modeler](../../experiments/wmk-hybrid-modeler/).

Para executar **Python `bpy` livre** e ver seu resultado real, o Blender precisa atuar como motor de prévia; JavaScript no navegador não interpreta `bpy` automaticamente.

## Limitações e cuidados

A montagem é **didática, não uma dobradiça certificada para fabricação**. O encaixe entre anéis e chapas pode requerer reforço geométrico, tolerâncias físicas, tratamento de normais e inspeção de interferências. Materiais e animação são simplificados. O script ainda não foi executado e inspecionado visualmente no Blender 5.2.3 neste ambiente.

A aplicação de booleanos usa operações no Blender e deve ocorrer no contexto apropriado da thread principal, em uma cena de teste.

## Evoluções

1. Sliders HTML para medidas com preview sincronizado.
2. Suporte a countersink/rebaixo para cabeça dos parafusos.
3. Chanfros e vincos, cilindros com melhor geometria e verificações de interferência.
4. Pivôs mecânicos editáveis, mais animações e exportação GLB.
5. Catálogo de peças: dobradiças, chapas perfuradas, suportes, engrenagens, polias e eixos.

Licença MIT com preservação da autoria e avisos legais originais do MCP for Blender.
