# Análise de Renda Per Capita por CEP no Brasil

## Motivação do Estudo

O Brasil é um dos países com maior desigualdade de renda do mundo. Compreender como essa desigualdade se distribui geograficamente é fundamental para embasar políticas públicas, decisões empresariais e pesquisas acadêmicas. Este estudo utiliza dados de **renda per capita associados a CEPs brasileiros** para explorar padrões regionais de distribuição de renda, identificar disparidades entre estados e regiões, e construir uma base para modelos preditivos de renda a partir de localização geográfica.

A escolha do CEP como unidade de análise permite uma granularidade maior do que análises por município ou estado, revelando heterogeneidades internas que estatísticas agregadas tendem a ocultar.

---

## Perguntas Norteadoras da Análise

### Gráfico 1 — Média e Desvio Padrão da Renda por Região (Barras)
> **Qual a média de renda per capita por região e qual a variabilidade interna de cada uma?**

- Quais regiões concentram as maiores rendas médias?
- A região com maior média também apresenta maior variabilidade?
- Regiões com alto desvio padrão indicam desigualdade interna elevada — quais são elas?

---

### Gráfico 2 — Participação da Renda Média por Região (Pizza)
> **Como se distribui proporcionalmente a renda média entre as regiões brasileiras?**

- Existe uma concentração de renda em poucas regiões?
- A diferença proporcional entre as regiões mais ricas e mais pobres é expressiva?
- Essa distribuição reflete o padrão histórico de desenvolvimento econômico do país?

---

### Gráfico 3 — Desvio Padrão da Renda por Estado em Ordem Decrescente (Linha)
> **Quais estados apresentam maior desigualdade interna de renda?**

- Os estados mais desenvolvidos economicamente são necessariamente os mais desiguais?
- Existe uma correlação entre tamanho do estado e variabilidade da renda?
- Quais estados apresentam renda mais homogênea entre seus CEPs?

---

### Gráfico 4 — Distribuição de Renda por Região sem Outliers (Boxplot)
> **Como se distribui a renda "típica" de cada região, desconsiderando valores extremos?**

- Qual a amplitude interquartil (IQR) de cada região — onde se concentra a maioria da população?
- Existe sobreposição entre as distribuições das regiões, ou elas são claramente separadas?
- A mediana confirma o que a média sugere, ou os outliers distorciam a percepção?

---

### Gráfico 5 — Mapa Geográfico de Renda Per Capita (Scatter por coordenadas)
> **A renda per capita apresenta padrão espacial visível no território brasileiro?**

- É possível identificar visualmente clusters de alta ou baixa renda no mapa?
- As regiões litorâneas ou metropolitanas se destacam em relação ao interior?
- Há gradientes de renda que acompanham eixos geográficos (norte-sul, litoral-sertão)?

---

## Contexto dos Dados

| Campo | Descrição |
|---|---|
| `POSTCODE` | CEP brasileiro (8 dígitos) |
| `LAT` / `LON` | Coordenadas geográficas do centroide do CEP |
| `renda_per_capita` | Renda per capita média dos domicílios do setor censitário associado ao CEP |
| `uf` | Unidade Federativa inferida a partir do intervalo numérico do CEP |
| `regiao` | Região geográfica (Norte, Nordeste, Centro-Oeste, Sudeste, Sul) |

---

## Hipóteses Iniciais

1. **A região Sudeste apresenta a maior renda média**, dada sua concentração industrial e de serviços.
2. **O Norte e Nordeste apresentam os menores valores medianos**, refletindo desigualdade histórica.
3. **Estados como SP e RJ devem ter alto desvio padrão**, pois concentram tanto bolsões de pobreza quanto áreas de altíssima renda.
4. **O mapa deve revelar um gradiente Sul-Norte**, com renda decrescendo em direção ao norte do país.
5. **CEPs com coordenadas próximas a capitais tendem a ter renda mais alta**, refletindo concentração urbana de riqueza.

---

## Próximos Passos

- Treinar um modelo de regressão para **predizer renda per capita** a partir de UF, região e CEP.
- Avaliar o desempenho do modelo com métricas como RMSE e R².
- Explorar features adicionais (densidade demográfica, IDH municipal) para melhorar a predição.
