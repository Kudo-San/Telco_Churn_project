# Import das bibliotecas
import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import requests
from streamlit_lottie import st_lottie

# Para rodar o código --> streamlit run app.py

#--------------------------------------------------------------------------------------------------------------------------
#                                                         CONFIGURAÇÃO DA PÁGINA
#--------------------------------------------------------------------------------------------------------------------------

st.set_page_config(
    page_title="Telco Analytics",
    page_icon="📡",
    layout="wide"
)

#--------------------------------------------------------------------------------------------------------------------------
#                                                            TEMA CLARO FIXO
#--------------------------------------------------------------------------------------------------------------------------

bg_color = "#F0F2F6"
card_bg = "#FFFFFF"
text_color = "#111827"
subtext_color = "#4B5563"
sidebar_bg = "#FFFFFF"
border_color = "#D1D5DB"

#--------------------------------------------------------------------------------------------------------------------------
#                                                           CSS PERSONALIZADO
#--------------------------------------------------------------------------------------------------------------------------

st.markdown(f"""
<style>
    .stApp {{ background-color: {bg_color}; }}
    section[data-testid="stSidebar"] {{ background-color: {sidebar_bg}; border-right: 1px solid {border_color}; }}
    h1, h2, h3, h4, h5, p, li {{ color: {text_color} !important; }}
    
    /* TRUQUE PARA ALINHAMENTO */
    [data-testid="column"] {{
        display: flex;
        flex-direction: column; 
    }}
    
    .metric-card {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        text-align: center;
        flex: 1; 
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 400px; /* Aumenta o tamanho dos cards */
    }}
    
    /* TIPOGRAFIA */
    .metric-card h3 {{ 
        color: {subtext_color} !important; 
        font-size: 14px; 
        font-weight: 600; 
        text-transform: uppercase; 
        letter-spacing: 0.05em; 
        margin-bottom: 12px; 
    }}
    .metric-card h2 {{ 
        color: {text_color} !important; 
        font-size: 42px; /* Aumentei um pouco para acompanhar o card maior */
        font-weight: 800; 
        margin: 0;
        line-height: 1.2;
    }}
    .metric-card p {{ 
        font-size: 14px; 
        color: {subtext_color} !important; 
        margin-top: 4px;
        font-weight: 500;
    }}
    
    /* TAGS */
    .tag-container {{
        margin-top: 20px; /* Mais espaço pois o card é alto */
        display: flex;
        gap: 8px;
        justify-content: center;
        flex-wrap: wrap;
    }}
    .tag {{ 
        padding: 6px 12px; 
        border-radius: 9999px;
        font-size: 12px; 
        font-weight: 600; 
        white-space: nowrap;
    }}
    .tag-blue {{ background-color: #DBEAFE; color: #1E40AF; }}
    .tag-gray {{ background-color: #F3F4F6; color: #374151; }}
    .tag-purple {{ background-color: #F3E8FF; color: #6B21A8; }}
    .tag-green {{ background-color: #DCFCE7; color: #166534; }}

    /* BOTÃO */
    div.stButton > button {{
        background-color: #0068C9 !important; 
        color: white !important; 
        border-radius: 8px; 
        height: 56px; 
        width: 100%;
        border: none !important; 
        font-weight: 700; 
        font-size: 16px; 
        box-shadow: 0 4px 6px -1px rgba(0, 104, 201, 0.4);
        transition: all 0.2s;
    }}
    div.stButton > button:hover {{ 
        background-color: #0053A0 !important; 
        transform: translateY(-2px);
    }}
    
    /* FOOTER */
    .footer {{ 
        position: fixed; left: 0; bottom: 0; width: 100%; 
        background-color: {sidebar_bg}; color: {subtext_color}; 
        text-align: center; padding: 12px; font-size: 12px; 
        border-top: 1px solid {border_color}; z-index: 999; 
    }}
</style>
""", unsafe_allow_html=True)

#--------------------------------------------------------------------------------------------------------------------------
#                                                                 FUNÇÕES
#--------------------------------------------------------------------------------------------------------------------------

@st.cache_resource      # Isso faz o streamlit carregar só uma vez, para ser mais rápido
def carregar_arquivos():
    try:
        modelo = joblib.load('modelo_xgboost.pkl')
        colunas = joblib.load('feature_modelo.pkl')
        return modelo, colunas
    except: return None, None

def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

def plot_gauge(probabilidade, threshold):
    cor_barra = "#EF4444" if probabilidade >= threshold else "#10B981"
    tick_color = "#374151"
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = probabilidade * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Probabilidade de Churn", 'font': {'size': 24, 'color': tick_color}},
        number = {'suffix': "%", 'font': {'size': 50, 'color': cor_barra, 'family': "Arial Black"}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': tick_color},
            'bar': {'color': cor_barra},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': tick_color,
            'steps': [{'range': [0, 100], 'color': "rgba(209, 213, 219, 0.3)"}],
            'threshold': {'line': {'color': tick_color, 'width': 4}, 'thickness': 0.75, 'value': threshold * 100}
        }
    ))
    # Ajuste de altura do gráfico para acompanhar os cards de 400px
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={'color': tick_color}, margin=dict(l=30, r=30, t=40, b=30), height=450)
    return fig

#--------------------------------------------------------------------------------------------------------------------------
#                                                            CARREGAR MODELO
#--------------------------------------------------------------------------------------------------------------------------

model, feature_names = carregar_arquivos()
if not model:
    st.error("⚠️ Erro ao importar: Modelos não encontrados.")
    st.stop()

# --- HEADER ---
col_logo, col_header = st.columns([1, 6])
with col_logo:
    lottie_icon = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_tloqefla.json")
    if lottie_icon: st_lottie(lottie_icon, height=70, key="logo")
with col_header:
    st.markdown("# Telco Analytics Solutions")
    st.markdown("##### Sistema de Retenção Inteligente")
st.markdown("---")

# --- SIDEBAR ---
st.sidebar.markdown("### 👤 Perfil do Cliente")
with st.sidebar.form("form_cliente"):
    contract = st.selectbox("Contrato", ['Month-to-month', 'One year', 'Two year'])
    internet_service = st.selectbox("Internet", ['Fiber optic', 'DSL', 'No'])
    payment_method = st.selectbox("Pagamento", ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])
    st.markdown("---")
    tenure = st.slider("Tempo de Casa (Meses)", 0, 72, 12)
    monthly_charges = st.number_input("Fatura Mensal ($)", 0.0, 150.0, 70.0)
    total_charges = st.number_input("LTV (Total Pago)", 0.0, value=monthly_charges*tenure)
    st.markdown("---")
    c1, c2 = st.columns(2)
    dependents = c1.checkbox("Possui Dependentes") 
    paperless = c2.checkbox("Fatura Digital")
    st.write("")
    submit = st.form_submit_button("CALCULAR RISCO")

#--------------------------------------------------------------------------------------------------------------------------
#                                                             DASHBOARD
#--------------------------------------------------------------------------------------------------------------------------

if submit:
    # 1. PROCESSAMENTO
    input_df = pd.DataFrame([{
        'tenure': tenure, 'MonthlyCharges': monthly_charges, 'TotalCharges': total_charges,
        'Contract': contract, 'InternetService': internet_service, 'PaymentMethod': payment_method,
        'Dependents': 'Yes' if dependents else 'No', 'PaperlessBilling': 'Yes' if paperless else 'No',
        'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No', 'PhoneService': 'Yes', 
        'MultipleLines': 'No', 'OnlineSecurity': 'No', 'OnlineBackup': 'No', 
        'DeviceProtection': 'No', 'TechSupport': 'No', 'StreamingTV': 'No', 'StreamingMovies': 'No'
    }])
    input_df['Interaction_Fiber_Month'] = input_df.apply(lambda x: 1 if x['InternetService'] == 'Fiber optic' and x['Contract'] == 'Month-to-month' else 0, axis=1)
    input_df = pd.get_dummies(input_df).reindex(columns=feature_names, fill_value=0)
    prob = model.predict_proba(input_df)[0][1]
    threshold = 0.52

    # 2. LÓGICA DA AÇÂO
    if internet_service == "No":
        produto_label = "Linha Fixa ☎️"
        produto_class = "tag-green"
    else:
        produto_label = f"Internet {internet_service}"
        produto_class = "tag-blue"

    if prob >= threshold:
        status_text, status_class = "CRÍTICO", "color: #EF4444;"
        rec_title, rec_desc, rec_bg, rec_border = "📞 AÇÃO: LIGAR PARA O CLIENTE", "Alto risco de Churn. Oferecer desconto de 15% ou isenção de 1 mensalidade.", "#FEF2F2", "#FCA5A5"
    else:
        status_text, status_class = "SEGURO", "color: #10B981;"
        if internet_service == "No":
            rec_title = "🎯 AÇÃO: CROSS-SELL" 
            rec_desc = "Cliente só tem telefone. Oportunidade de oferecer ( Combo Fibra + TV )."
            rec_bg, rec_border = "#F0FDF4", "#86EFAC"
        else:
            rec_title = "📈 AÇÃO: UPSELL"
            rec_desc = "Cliente estável. Oferecer pacote de TV Premium ou aumentar velocidade."
            rec_bg, rec_border = "#F0F9FF", "#BAE6FD"

    pagamento_icon = "💳" if "automatic" in payment_method else "📝"
    pagamento_label = payment_method.replace(" (automatic)", "")
    fatura_label = "Digital 📱" if paperless else "Correio 📬"
    fatura_class = "tag-blue" if paperless else "tag-gray"

    # --- LAYOUT MASTER ---
    col_left, col_right = st.columns([2, 1]) # Ajuste da proporção para 2:1 para dar espaço aos cards grandes

    with col_left:
        # Linha de Cards
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Risco Calculado</h3>
                <h2 style="{status_class}">{status_text}</h2>
                <p>Score: {prob:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Financeiro</h3>
                <h2>$ {monthly_charges:.0f}</h2>
                <p>LTV: $ {total_charges:,.0f}</p>
                <div class="tag-container">
                    <span class="tag tag-purple">{pagamento_icon} {pagamento_label}</span>
                    <span class="tag {fatura_class}">{fatura_label}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Produto Ativo</h3>
                <h2>{produto_label}</h2>
                <p>{tenure} meses de casa</p>
                <div class="tag-container">
                    <span class="tag {produto_class}">{contract}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Espaçamento
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

        # Banner de Ação
        st.markdown(f"""
        <div style="background-color: {rec_bg}; border: 1px solid {rec_border}; padding: 20px; border-radius: 12px; display: flex; align-items: center;">
            <div style="flex: 1;">
                <h4 style="margin: 0; color: {text_color}; font-size: 18px; font-weight: 700;">{rec_title}</h4>
                <p style="margin: 4px 0 0 0; color: {subtext_color}; font-size: 15px;">{rec_desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        fig = plot_gauge(prob, threshold)
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👈 Utilize o menu lateral para iniciar a análise.")

# --- FOOTER ---
st.markdown(f"""<div class="footer">Desenvolvido por <b>Marcelo Kudo</b> | Powered by Machine Learning XGBoost</div>""", unsafe_allow_html=True)