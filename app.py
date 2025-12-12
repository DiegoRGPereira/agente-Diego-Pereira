import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Diego Pereira | Diagnóstico", page_icon="🔧", layout="wide")

# CSS Básico
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; color: #212529; }
    [data-testid="stSidebar"] { background-color: #1e293b; color: white; }
</style>
""", unsafe_allow_html=True)

# --- SEGURANÇA ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ Configure a GEMINI_API_KEY nos Secrets do Streamlit.")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🔧 Diagnóstico")
    st.write("Use o botão abaixo para ver quais modelos sua chave pode acessar.")
    
    if st.button("Listar Modelos Disponíveis"):
        try:
            st.info("Consultando API do Google...")
            # Lista todos os modelos disponíveis para sua chave
            available_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
            
            if available_models:
                st.success(f"Sucesso! Encontrei {len(available_models)} modelos.")
                st.code("\n".join(available_models))
            else:
                st.warning("A chave conectou, mas nenhum modelo de texto foi encontrado.")
                
        except Exception as e:
            st.error(f"Erro Fatal: {e}")

# --- ÁREA PRINCIPAL ---
st.title("🕵️ Teste de Conexão Google AI")
st.markdown("""
Se você está vendo erros **404 Not Found**, clique no botão na barra lateral.
Ele vai listar os nomes exatos que o Google aceita para a sua conta.
""")

st.divider()

# Teste Rápido de Chat (Tenta usar o primeiro modelo que encontrar)
st.subheader("Teste Automático de Chat")

if st.button("Tentar conectar com qualquer modelo disponível"):
    try:
        # Pega o primeiro modelo da lista automaticamente
        my_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if my_models:
            model_name = my_models[0] # Pega o primeiro da lista
            st.write(f"Tentando usar o modelo: **{model_name}**")
            
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Diga apenas: 'Conexão Funcionando!'")
            st.success(f"Resposta da IA: {response.text}")
        else:
            st.error("Nenhum modelo disponível para teste.")
            
    except Exception as e:
        st.error(f"Erro no teste: {e}")

