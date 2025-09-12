# Dashboard de Análise de Risco de Crédito

Este projeto é um Dashboard interativo construído com Streamlit para analisar dados de risco de crédito de clientes.

## 📜 Descrição

O dashboard permite a visualização de clientes por faixa etária, risco, e outras métricas importantes. Os dados foram tratados e analisados no notebook que se encontra na pasta `/notebooks`.

## 🚀 Como Executar o Projeto Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/douglasbelizario/Dashboard-de-Analise-de-Risco-de-Credito.git
   ```
2. Navegue até a pasta do projeto:
   ```bash
   cd Credit
   ```
3. Ative o ambiente virtual (Se necessário):
   ```bash
   # Windows
   .\.venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Rode o aplicativo Streamlit:
   ```bash
   streamlit run app.py
   ```

## 📂 Estrutura do Projeto
- **/notebooks/Dashboard_credito_risco.ipynb**: Notebook com toda a análise exploratória e o processo de limpeza e tratamento dos dados.
- **/dados/**: Contém os datasets brutos e tratados.
- **app.py**: O script principal que executa a aplicação Streamlit.
- **requirements.txt**: Lista de dependências do projeto.

## 🔗 Link para o App Online
*(https://dashboardriscocredito.streamlit.app/)*
