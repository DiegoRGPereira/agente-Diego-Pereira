import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Diego Pereira | Agente Virtual", page_icon="🏭", layout="wide")

# CSS Estilo "React Clean"
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; color: #212529; }
    [data-testid="stSidebar"] { background-color: #1e293b; color: white; }
    .stChatInput textarea { background-color: white; color: #333; border: 1px solid #ddd; }
    .status-badge {
        background-color: #10b981; color: white; padding: 4px 10px;
        border-radius: 12px; font-size: 11px; font-weight: 600; text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SEGURANÇA ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ Configure a GEMINI_API_KEY nos Secrets do Streamlit.")

# --- 3. CÉREBRO (PROMPT INJETADO) ---
# O Gemini Pro antigo não aceita 'system_instruction' direto, então usamos este texto oculto
system_instruction_text = """
VOCÊ É O 'AGENTE VIRTUAL DIEGO PEREIRA'.
IDENTIDADE: Engenheiro de Produção Mecânica, Especialista em Lean (Green Belt) e Dados.
REGRAS DE INTERAÇÃO:
1. Responda como um engenheiro experiente de chão de fábrica (Gemba).
2. MES/OEE: O problema real é o apontamento manual e microparadas. Use OEE para diagnóstico.
3. EXPERIÊNCIA: 3M/Lear/Yamaha (Chão de fábrica). ATUAL: BIP/Petrobras (BPO/Planejamento - não misturar com MES).
4. OBJETIVO: Prove que o Diego une engenharia tradicional com inovação.
CONTATO: diegogpereira@gmail.com
"""

# Usamos o modelo PRO (Texto apenas) que é 100% estável
model = genai.GenerativeModel("gemini-pro")

# --- 4. BARRA LATERAL (PERFIL) ---
with st.sidebar:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.write("🧑‍🔧")
    with col2:
        st.markdown("**Diego Pereira**")
        st.caption("Lean Specialist")
    
    st.markdown('<div style="margin-top:10px;"><span class="status-badge">Open to Work</span></div>', unsafe_allow_html=True)
    st.divider()
    
    # Gráfico Radar
    categories = ['Lean / Six Sigma', 'Gestão de Projetos', 'MES / OEE', 'Python / Dados', 'Liderança', 'SAP']
    r_values = [10, 9, 8, 7, 9, 8]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r_values, theta=categories, fill='toself', name='Diego',
        line_color='#3b82f6', fillcolor='rgba(59, 130, 246, 0.3)'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10], showticklabels=False, linecolor='gray'), bgcolor='rgba(0,0,0,0)'),
        showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=10), margin=dict(l=20, r=20, t=10, b=10), height=250
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info("💡 **Diferencial:** Uno a metodologia Lean tradicional com análise de dados moderna.")
    st.markdown("📧 diegogpereira@gmail.com")

# --- 5. CHAT ---
st.title("🏭 Engenharia 4.0 | Diego Pereira")
st.markdown("Discuta problemas de **Chão de Fábrica, OEE e Lean** com o assistente virtual.")

# Inicializa Histórico com o "Truque da Injeção"
if "messages" not in st.session_state:
    st.session_state.messages = [
        # Mensagem oculta com as regras
        {"role": "user", "content": f"Aja estritamente conforme estas regras: {system_instruction_text}. Se entendeu, diga apenas 'Olá'."},
        {"role": "model", "content": "Olá! Sou a versão virtual do Diego. Vamos discutir estratégias de Lean Manufacturing e eficiência?"}
    ]

# Mostra as mensagens (Pulando a primeira que é a regra oculta)
for i, message in enumerate(st.session_state.messages):
    if i == 0: continue 
    avatar = "🤖" if message["role"] == "model" else "👷"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua dúvida técnica..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👷"):
        st.markdown(prompt)

    with st.chat_message("model", avatar="🤖"):
        try:
            # Envia histórico completo para manter o contexto
            chat = model.start_chat(history=[
                {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} 
                for m in st.session_state.messages[:-1]
            ])
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "content": response.text})
            
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
