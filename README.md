# Pipeline de Previsão de Séries Temporais com Modelos Híbridos

Este repositório contém um pipeline completo e automatizado de Machine Learning para previsão de séries temporais. O projeto foi desenvolvido como um estudo de caso prático, abordando desde a geração de dados sintéticos complexos até a implementação de estratégias de modelagem avançadas, avaliação honesta e detecção de vazamento de dados (data leakage).

## Principais Características

* **Pipeline Automatizado:** Execução de todo o fluxo (ETL, Feature Engineering, Treinamento, Avaliação) com um único comando.
* **Engenharia de Features Avançada:** Criação de features de lag, médias móveis, componentes de data (`dia_da_semana`, `mes`) e índice de tempo para capturar múltiplos padrões.
* **Estratégia de Modelo Híbrido:** Combina a força da **Regressão Linear** para modelar a tendência principal com a capacidade do **Random Forest** de aprender os resíduos (padrões não-lineares e sazonais).
* **Simulação Realista:** O gerador de dados cria uma série temporal com tendência não-linear, múltiplas sazonalidades (anual e semanal), ruído variável, eventos complexos e choques aleatórios, simulando os desafios de um cenário real.
* **Avaliação Honesta:** O pipeline foi cuidadosamente projetado para evitar data leakage, garantindo que a avaliação dos modelos reflita sua verdadeira capacidade preditiva em dados não vistos.
* **Código Modular e Configurável:** O projeto é organizado em módulos com responsabilidades únicas e utiliza um arquivo `config.py` centralizado, facilitando a manutenção e a experimentação.
* **Pronto para Docker:** Inclui um `Dockerfile` e `.dockerignore` para fácil portabilidade e execução em qualquer ambiente.

## Estrutura do Projeto

O repositório está organizado da seguinte forma para garantir a separação de responsabilidades:

projeto_temporal/
├── data/         # Contém os dados brutos e processados gerados pelo pipeline.
├── models/       # Armazena os modelos treinados e serializados (.pkl).
├── reports/      # Salva os artefatos visuais, como gráficos de previsão.
├── src/          # Contém todo o código-fonte do projeto.
│   ├── config.py         # Arquivo central de configurações.
│   ├── etl.py            # Script para extração, transformação e limpeza dos dados.
│   ├── features.py       # Script para engenharia de features.
│   ├── generate_data.py  # Script para gerar os dados brutos.
│   ├── main.py           # Orquestrador principal do pipeline.
│   ├── plot_results.py   # Script para gerar a visualização dos resultados.
│   ├── train.py          # Script para treinamento e avaliação dos modelos.
│   └── utils.py          # Funções de utilidade compartilhadas.
├── .dockerignore   # Especifica arquivos a serem ignorados pelo Docker.
├── .gitignore      # Especifica arquivos a serem ignorados pelo Git.
├── Dockerfile      # Receita para construir a imagem Docker do projeto.
└── requirements.txt# Lista de dependências Python do projeto.


## ⚙️ Como Executar o Projeto

Siga os passos abaixo para configurar e executar o pipeline na sua máquina local.

### Pré-requisitos

* [Python 3.9+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads/)

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/loucop/Temporal-Series-Prediction.git](https://github.com/loucop/Temporal-Series-Prediction.git)
    cd Temporal-Series-Prediction
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # No Windows
    python -m venv venv
    .\venv\Scripts\Activate

    # No macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### Execução

1.  **Gere os Dados Brutos (Primeira vez):**
    Execute o script de geração de dados para criar o arquivo `raw.xlsx`.
    ```bash
    python src/generate_data.py
    ```

2.  **Execute o Pipeline Completo:**
    O `main.py` irá orquestrar todas as etapas, desde a limpeza dos dados até a geração do gráfico final.
    ```bash
    python src/main.py
    ```

    Ao final da execução, os modelos treinados estarão na pasta `models/` e o gráfico de previsão estará em `reports/`.

* **Limitações dos Modelos:** Demonstrou-se na prática a incapacidade de modelos de árvore (Random Forest) de extrapolar tendências e a necessidade de features específicas como o `time_index`.
* **Detecção de Data Leakage:** A busca por um R² realista nos forçou a identificar e corrigir múltiplas formas de vazamento de dados, desde o cálculo da média móvel até o uso de features com conhecimento futuro.
* **Poder dos Modelos Híbridos:** A combinação da Regressão Linear (para a tendência) com o Random Forest (para os resíduos) provou ser uma estratégia robusta e eficaz para lidar com a complexidade da série.
