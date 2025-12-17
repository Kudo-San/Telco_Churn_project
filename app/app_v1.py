# Import das bibliotecas
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Para rodar o código --> streamlit run app_v1.py

#--------------------------------------------------------------------------------------------------------------------------
#                                             CONFIGURAÇÃO DA PÁGINA
#--------------------------------------------------------------------------------------------------------------------------

st.set_page_config(
    page_title="TELCON CHURN PREDICTOR",
    page_icon="🔮",
    layout="centered"
)

#-------------------------------------------------------------------------------------------------------------------------
#                                              CARREGANDO O MODELO
#-------------------------------------------------------------------------------------------------------------------------

@st.cache_resource # Isso faz o streamlit carregar só uma vez, para ser mais rápido
def carregar_arquivo():
    modelo = joblib.load('modelo_xgboost.pkl')
    colunas = joblib.load('feature_modelo.pkl')
    return modelo, colunas

try: 
    model, feature_names = carregar_arquivo()
except FileNotFoundError:
    st.error("Erro: Arquivos do modelo não encontrados. Rode o notebook de treino primeiro!")
    st.stop()

#------------------------------------------------------------------------------------------------------------------------
#                                               INTERFACE VISUAL
#------------------------------------------------------------------------------------------------------------------------

st.title("🔮 Previsão de Churn - Telco")
st.markdown("Preencha os dados do cliente para calcular a probabilidade de cancelamento.")

st.sidebar.header("Perfil do Cliente")

# Impute dos usuários (Focando nas variáveis principais)
# 1. Dados Contratuais
contract = st.sidebar.selectbox("Tipo de Contrato", ['Month-to-month', 'One year', 'Two year'])
internet_service = st.sidebar.selectbox("Tipo de Internet", ['Fiber optic', 'DSL', 'No'])
payment_method = st.sidebar.selectbox("Método de Pagamento", ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])

# 2. Dados Númericos
tenure =st.sidebar.slider("Tempo de Casa (Meses)", 0, 72, 12)
monthly_charges = st.sidebar.number_input("Mensalidade ($)", min_value=0.0, max_value=150.0, value=70.0)
total_charges = st.sidebar.number_input("Total Pago até Hoje ($)", min_value=0.0, value=monthly_charges * tenure)

# 3. Outros (Simplificado para o app não ficar gigante, coloquei defaults ou inputs simples)
dependents = st.sidebar.checkbox("Possui Dependentes?", value=False)
paperless = st.sidebar.checkbox("Fatura Digital (Paperless)?", value=True)

#------------------------------------------------------------------------------------------------------------------------
#                       PROCESSAMENTO (Transformar inputs no formato que o modelo entenda)
#------------------------------------------------------------------------------------------------------------------------

# 1. Criar DataFrame com os dados brutos (igual ao CSV original)
# Vou garantir que as colunas categóricas tenham os valores originais 'Yes'/'No' se usarmos get_dummies
input_dict = {
    'tenure': tenure,
    'MonthlyCharges': monthly_charges,
    'TotalCharges': total_charges,
    'Contract': contract,
    'InternetService': internet_service,
    'PaymentMethod': payment_method,
    'Dependents': 'Yes' if dependents else 'No',
    'PaperlessBilling': 'Yes' if paperless else 'No',

    # Para simplificar este exemplo, vamos assumir 'No' para as outras colunas que não colocamos no input
    'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No', 'PhoneService': 'Yes', 
    'MultipleLines': 'No', 'OnlineSecurity': 'No', 'OnlineBackup': 'No', 
    'DeviceProtection': 'No', 'TechSupport': 'No', 'StreamingTV': 'No', 'StreamingMovies': 'No'
}

input_df = pd.DataFrame([input_dict])

# 2. FEATURE ENGINEERING (A mesma lógica do Notebook V3.0)
# Criando a variável de interação Fibra + Mensal
input_df['Interaction_Fiber_Month'] = input_df.apply(
    lambda x: 1 if x['InternetService'] == 'Fiber optic' and x['Contract'] == 'Month-to-month' else 0, 
    axis=1
)

# 3. Encoding (Transformar texto em números)
# O get_dummies vai criar colunas. O problema é: se o input for só "DSL", 
# ele não vai criar a coluna "InternetService_Fiber optic".
input_df_encoded = pd.get_dummies(input_df)

# 4. ALINHAMENTO DE COLUNAS
# O modelo espera EXATAMENTE as colunas do treino. O reindex cria as que faltam (com 0) e remove extras.
input_df_final = input_df_encoded.reindex(columns=feature_names, fill_value=0)

# --- PREVISÃO ---
if st.button("Calcular Risco de Churn"):
    # Probabilidade
    probabilidade = model.predict_proba(input_df_final)[0][1]
    
    # Threshold Otimizado (que descobrimos no notebook)
    threshold_otimo = 0.52 
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Probabilidade de Saída", f"{probabilidade:.1%}")
    
    with col2:
        if probabilidade >= threshold_otimo:
            st.error("🚨 ALTO RISCO")
            st.write("**Ação Recomendada:** Oferecer desconto agressivo ou plano fidelidade imediatamente.")
        else:
            st.success("✅ CLIENTE SEGURO")
            st.write("**Ação Recomendada:** Manter relacionamento padrão.")

    # Mostrar gráfico de probabilidade
    st.progress(int(probabilidade * 100))
    
    # Debug (Opcional - para você ver o que está entrando no modelo)
    with st.expander("Ver dados processados (Debug)"):
        st.write(input_df_final)
    