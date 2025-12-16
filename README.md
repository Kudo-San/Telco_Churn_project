
# 📡 Telco Customer Churn Prediction

![Status](https://img.shields.io/badge/Status-Concluído-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)

## 💼 Sobre o Projeto

Este projeto é uma solução completa (End-to-End) desenvolvida para prever a rotatividade de clientes (Churn) em uma empresa de Telecomunicações. 

O objetivo não foi apenas treinar um modelo, mas criar uma **ferramenta de suporte à decisão** que permitisse à equipe de retenção identificar clientes em risco e agir preventivamente, focando no impacto financeiro (ROI).

### 🎯 Resultados Alcançados

* **Recall de 79%:** O modelo é capaz de identificar a grande maioria dos clientes em risco.
* **Aumento de Lucro:** Implementação de threshold otimizado financeiramente, superando a estratégia padrão em **R$ 4.000,00/mês** (simulação em base de teste).
* **App Interativo:** Dashboard para uso da equipe de CS (Customer Success) com recomendações automáticas.

* A TELCON Customer Intelligence utiliza **Machine Learning** para:
- Identificar clientes com alto risco de churn
- Estimar impacto financeiro (MRR e LTV)
- Recomendar ações de retenção ou expansão
- Apoiar gestores com visão clara, visual e orientada a negócio

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Machine Learning:** XGBoost (Gradient Boosting), Scikit-Learn
* **Manipulação de Dados:** Pandas, Numpy
* **Visualização:** Plotly, Matplotlib
* **Deploy/Web App:** Streamlit
* **Persistência:** Joblib
* **UX/UI:** customizado com CSS

---

## 📊 O Dashboard (Streamlit)

O projeto inclui uma interface gráfica onde o usuário pode simular perfis de clientes e receber:
1.  **Probabilidade de Churn** em tempo real.
2.  **Score de Risco** classificado (Seguro vs Crítico).
3.  **Ações Recomendadas** baseadas em regras de negócio (ex: Migração de base, Cross-sell, Upsell).
4.  **Dashboard executivo sem rolagem**
- KPIs estratégicos (Risco, Probabilidade, Receita, LTV)
- Modo Claro / Modo Escuro
- Recomendações automáticas baseadas no score
- Experiência pensada para gestores e times de retenção


![Demo do App](https://via.placeholder.com/800x400?text=Inserir+Print+do+App+Aqui)
*(Nota: Substitua este link pelo print real do seu app)*

---

## 🚀 Como Executar Localmente

1. Clone o repositório:
```bash
git clone [https://github.com/SEU_USUARIO/telco-churn-project.git](https://github.com/SEU_USUARIO/telco-churn-project.git)

