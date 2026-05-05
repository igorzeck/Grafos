# README

Repositório de pesquia de cidades similares por meio de Grafos utilizando a biblioteca `Igraph` e dados do `IBGE`, `UNDP` e `Koppen`.

## Dicionário de dados

Para o o arquivo `municipio_brasil` em `csv` e `xlsx`.
**IBGE**:
- `municipio_id`: Id do município.
- `municipio_nome`: Nome do município.
- `pib_per_capita`: Pib per capita.
- `populacao`: População em mil habitantes.

**UNDP**:
- `idhm`: Índice de desenvolvimento humano (valores de 0 - 1000).

**KOPPEN**:
- `altitude`: Altitude do município.
- `temperatura_anual`: Temperatura anual do município (ºC - 2013).
- `chuva_anual`: Quantidade de chuva anual (mm - 2013)

## Fontes
IBGE:
https://cidades.ibge.gov.br
IDHM:
https://www.undp.org/pt/brazil/idhm-municipios-2010
Climáticos (KOPPEN):
https://koppenbrasil.github.io/
https://forest-gis.com/classificacao-climatica-de-koppen-geiger-em-shapefile/
https://web.archive.org/web/20190114043011/http://ipef.br/geodatabase/repository/651da1d8va615cz1ad1da8s4rq8146a1dsa2132c1zn1/Koppen_Brazil_2013.rar
