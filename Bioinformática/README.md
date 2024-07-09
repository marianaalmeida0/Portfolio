# Bioinformática23/24

Trabalho Realizado no âmbito da Unidade Curricular de Bioinformática no ano letivo 2023/2024 pelo Grupo 3:

PG53958	Jorge Martins;

PG54061	Mariana Ribeiro;

PG54062	Mariana Almeida;

PG54170	Raquel Lima.

## Informações do Dataset:

Dataset 10: GDS5473

https://www.ncbi.nlm.nih.gov/sites/GDSbrowser?acc=GDS5473

Ficheiro de dados: “gds5473.csv” (48107 linhas – genes X 48 colunas - amostras)

Ficheiro de metadados: “meta-gds5473.csv” – 48 linhas (amostras) X 4 colunas – variáveis

## Breve Descrição: 
Análise de biópsias musculares esqueléticas recolhidas em 1,5; 4; 10 e 24 horas após a refeição em homens jovens e saudáveis submetidos a um jejum de 24 horas. Os resultados fornecem uma compreensão sobre os mecanismos moleculares subjacentes à adaptação metabólica ao jejum em seres humanos saudáveis, tendo como objetivo, neste trabalho,estabelecer uma relação entre a expressão gênica e o tempo de jejum.
O dataset apresenta uma coleção de genes, cerca de 48107 de 48 amostras. Cada amostra é caracterizada no metadaset com base em 4 variáveis: amostra (sample), individuo (individual), tempo (time) e descrição (description).  

## Metodologia:
### Etapa 1:
Carregamento do conjunto de dados e análise dos dados e metadados. Descrição e caraterização dos dados
atribuídos de acordo com a literatura existente. Descrição sucinta das caraterísticas dos dados e metadados
disponíveis e os passos de pré-processamento efetuados ( Transposição no conjunto de dados do dataste; Tratamento de Missing Values e Remoção de colunas nos metadados).
Gráficos exploratórios iniciais das principais características dos dados e meta-dados.

### Etapa 2:
Utilização de técnicas de redução de dimensionalidade adequadas. Aplicação de  métodos
de clustering. Análise dos resultados obtidos.

### Etapa 3:
Previsão do comportamento dos dados, utilizando três modelos/ algoritmos de Aprendizagem
Máquina ( KNN, Decision Tree e Naive Bayes). Análise dos mesmos tendo em conta diferentes
métricas de erro, nomeadamente Accuracy, Precision e Recall. Processo de otimização dos modelos selecionados, utilizando 2 métodos de partição de dados diferentes (Hold-out sample e Cross- Validation). Análise do melhor modelo obtido.

## Literatura Consultada:

Wijngaarden MA, Bakker LE, van der Zon GC, et al. Regulation of skeletal muscle energy/nutrient-sensing pathways during metabolic adaptation to fasting in healthy humans. Am J Physiol Endocrinol Metab. 2014;307(10):E885-E895. doi:10.1152/ajpendo.00215.2014




