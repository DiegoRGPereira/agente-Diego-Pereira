import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go

# --- 1. CONFIGURAÇÃO DA PÁGINA (Visual Dark & Profissional) ---
st.set_page_config(page_title="Diego Pereira | Agente Virtual", page_icon="🏭", layout="wide")

# CSS para forçar o estilo escuro e ajustar detalhes
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .stChatInput textarea { background-color: #262730; color: white; }
    .status-badge {
        background-color: #28a745; color: white; padding: 5px 12px;
        border-radius: 15px; font-size: 12px; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. CONFIGURAÇÃO DA IA (SEGURANÇA) ---
# O sistema vai buscar a senha (API Key) nos segredos do servidor, não no código exposto
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Configuração pendente: Adicione a API Key nos 'Secrets' do Streamlit.")

# --- 3. O CÉREBRO (PROMPT DO SISTEMA) ---
system_instruction = """
ROLE: Você é o 'Agente Virtual Diego Pereira', avatar profissional do Engenheiro Diego Pereira.
IDENTIDADE: Especialista em Lean Manufacturing (Green Belt), focado em eficiência e dados.
TOM DE VOZ: Técnico, 'Hands-on', direto e analítico. Não use corporativês vazio.

BASE DE CONHECIMENTO & REGRAS:
1. LEAN vs TECH:
   - Você sabe que o maior problema do MES não é o software, é o APONTAMENTO MANUAL errado e as MICROPARADAS não registradas.
   - Defende o uso de OEE para diagnóstico real, não para bater meta (bonificação).
   - Usa Python/Minitab para limpar dados e achar a verdade (Data Reliability).

2. HISTÓRICO PROFISSIONAL:
   - 3M/Lear/Yamaha: Experiência sólida de chão de fábrica, Kaizen, Redução de Scrap, DMAIC.
   - ATUAL (BIP/Petrobras): Foco em BPO e Planejamento de Manutenções Submarinas. (ATENÇÃO: Não misture a função atual com OEE/MES. São fases diferentes).

3. GATILHOS DE VENDA:
   - Se perguntarem 'Por que um agente?': Responda 'Sou a prova de conceito de que o Diego une a engenharia tradicional com a inovação tecnológica na prática.'
   - Se o assunto for contratação/salário: 'Sou apenas o protótipo técnico. Sugiro conversar com o Diego real para esses detalhes.'

CONTATO: diegogpereira@gmail.com
"""

# Configuração do Modelo Gemini 1.5
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# --- 4. BARRA LATERAL (SEU PERFIL VISUAL) ---
with st.sidebar:
    st.title("Diego Pereira")
    st.caption("Engenheiro de Produção | Lean Specialist")
    st.markdown('<span class="status-badge">Open to Work</span>', unsafe_allow_html=True)
    st.divider()
    
    # Gráfico de Radar (Suas Competências Reais)
    categories = ['Lean / Six Sigma', 'Gestão de Projetos', 'MES / OEE', 'Python / Dados', 'Liderança', 'SAP']
    r_values = [10, 9, 8, 7, 9, 8] # Notas ajustadas conforme seu perfil

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r_values, theta=categories, fill='toself', name='Diego Pereira',
        line_color='#4facfe', fillcolor='rgba(79, 172, 254, 0.3)'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10], showticklabels=False, linecolor='gray'), bgcolor='rgba(0,0,0,0)'),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'), margin=dict(l=20, r=20, t=20, b=20), height=300
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("**Foco:** Confiabilidade de Dados no Chão de Fábrica")
    st.markdown("📧 diegogpereira@gmail.com")
    st.markdown("[🔗 LinkedIn Perfil](https://www.linkedin.com/in/diego-ribeiro-guedes-pereira/)")

# --- 5. ÁREA DE CHAT ---
st.title("💬 Chat com Engenheiro Virtual")
st.markdown("Treinado com a experiência real de **Diego Pereira** para discutir **Lean, OEE e Eficiência**.")

# Inicializa o histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "content": "Olá! Sou o assistente virtual do Diego. Fui treinado para discutir como resolver problemas reais de produção usando Lean e Dados. Como posso ajudar?"}
    ]

# Mostra as mensagens na tela
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "model" else "👷"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Captura a pergunta do usuário
if prompt := st.chat_input("Ex: Como tratar a falta de apontamento no MES?"):
    # Mostra a pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👷"):
        st.markdown(prompt)

    # Gera a resposta da IA
    try:
        chat = model.start_chat(history=[
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
            for m in st.session_state.messages[:-1]
        ])
        response = chat.send_message(prompt)
        
        # Mostra a resposta
        with st.chat_message("model", avatar="🤖"):
            st.markdown(response.text)
        
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        st.error(f"Erro de conexão. Verifique a API Key. Detalhe: {e}")