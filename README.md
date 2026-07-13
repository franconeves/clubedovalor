# 📈 Analisador Quantitativo B3 - Fórmula Mágica

Este projeto é um script automatizado em Python que realiza uma varredura de dados em tempo real na Bolsa de Valores brasileira (B3). Ele aplica uma versão adaptada da **Fórmula Mágica de Joel Greenblatt**, cruzando indicadores de preço (múltiplos operacionais) com indicadores de eficiência (rentabilidade).

## 🛠️ Tecnologias Utilizadas
* **Python 3.x**
* **Pandas**: Manipulação, saneamento e ordenação de dados.
* **YFinance (Yahoo Finance API)**: Extração de cotações e múltiplos financeiros em tempo real.
* **OpenPyXL**: Mecanismo de exportação de dados para planilhas `.xlsx`.

## 📂 Estrutura do Repositório
* `/exports`: Armazena os relatórios gerados automaticamente com carimbo de data.
* `geminiMain.py`: Script principal de execução.
* `requirements.txt`: Lista de dependências de bibliotecas.
* `METODOLOGIA.md`: Detalhamento teórico dos filtros.
* `CHECKLIST_MANUAL.md`: Guia para análise humana pré-compra.

## 🚀 Como Executar o Projeto

1. Abra o seu terminal (Git Bash) e navegue até a pasta do projeto:
   ```bash
   cd /c/Componentes/clubedovalor