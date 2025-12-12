import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
from PIL import Image

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Diego Pereira | Agente Virtual", page_icon="🏭", layout="wide")

# CSS para visual limpo e profissional (Estilo React/Moderno)
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; color: #212529; } /* Fundo claro profissional */
    [data-testid="stSidebar"] { background-color: #1e293b; color: white; }
    .stChatInput textarea { background-color: white; color: #333; border: 1px solid #ccc; }
    .css-1d391kg { padding-top: 1rem; }
    .status-badge {
        background-color: #10b981; color: white; padding: 4px 10px;
        border-radius: 12px; font-size: 11px; font-weight: 600; text-transform: uppercase;
    }
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- 2. SEGURANÇA & API ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ Configure a GEMINI_API_KEY nos Secrets do Streamlit.")

# --- 3. CÉREBRO DA IA (PROMPT) ---
system_instruction = """
VOCÊ É O 'AGENTE VIRTUAL DIEGO PEREIRA'.
IDENTIDADE: Engenheiro de Produção Mecânica, Especialista em Lean (Green Belt) e Dados.
REGRAS TÉCNICAS:
1. ANÁLISE VISUAL: Se receber uma imagem, analise como um engenheiro de chão de fábrica (procure falhas, desperdícios ou dados em gráficos).
2. MES/OEE: O problema real é o apontamento manual e microparadas. Use OEE para diagnóstico.
3. EXPERIÊNCIA: 3M/Lear/Yamaha (Chão de fábrica). ATUAL: BIP/Petrobras (BPO/Planejamento).
4. OBJETIVO: Prove que o Diego une engenharia tradicional com inovação.
CONTATO: diegogpereira@gmail.com
"""

# Usando o modelo Flash que é rápido e aceita imagens
model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=system_instruction)

# --- 4. BARRA LATERAL (PERFIL) ---
with st.sidebar:
    # Cabeçalho do Perfil
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("🧑‍🔧", unsafe_allow_html=True) # Pode trocar por st.image se tiver
    with col2:
        st.markdown("**Diego Pereira**")
        st.caption("Lean Specialist")
    
    st.markdown('<div style="margin-top:10px;"><span class="status-badge">Open to Work</span></div>', unsafe_allow_html=True)
    st.divider()
    
    # Gráfico Radar
    st.markdown("### Competências")
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
    
    st.info("💡 **Diferencial:** Uno a metodologia Lean tradicional com análise de dados moderna (Python/IA).")
    st.markdown("📧 diegogpereira@gmail.com")

# --- 5. ÁREA DE CHAT ---
st.title("🏭 Engenharia 4.0 | Diego Pereira")
st.markdown("Discuta problemas de **Chão de Fábrica, OEE e Lean** ou envie uma imagem para análise.")

# Inicializar Histórico
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "content": "Olá! Sou a versão virtual do Diego. Posso analisar seus processos ou discutir estratégias de Lean Manufacturing. Como posso ajudar?"}
    ]

# Mostrar Mensagens Antigas
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "model" else "👷"
    with st.chat_message(message["role"], avatar=avatar):
        # Se tiver imagem na mensagem, mostra
        if "image" in message:
            st.image(message["image"], width=200)
        st.markdown(message["content"])

# --- 6. ÁREA DE INPUT (TEXTO + IMAGEM) ---
# Upload de arquivo
uploaded_file = st.file_uploader("📎 Anexar imagem (Gráfico, Peça, Tabela)", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if prompt := st.chat_input("Digite sua dúvida técnica..."):
    # 1. Preparar conteúdo do usuário
    user_content = [prompt]
    image_data = None
    
    # Se tiver imagem, processa
    if uploaded_file:
        image_data = Image.open(uploaded_file)
        user_content.append(image_data)
        st.session_state.messages.append({"role": "user", "content": prompt, "image": image_data})
        with st.chat_message("user", avatar="👷"):
            st.image(image_data, width=200)
            st.markdown(prompt)
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👷"):
            st.markdown(prompt)

    # 2. Gerar Resposta (Streaming)
    with st.chat_message("model", avatar="🤖"):
        try:
            # Se tiver imagem, usa generate_content (sem histórico por enquanto para simplificar)
            if image_data:
                response = model.generate_content(user_content, stream=True)
            else:
                # Se for só texto, usa chat history
                chat = model.start_chat(history=[
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} 
                    for m in st.session_state.messages if "image" not in m
                ])
                response = chat.send_message(prompt, stream=True)
            
            # Efeito de digitar na tela
            full_response = st.write_stream(response)
            
            # Salvar resposta no histórico
            st.session_state.messages.append({"role": "model", "content": full_response})
            
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
