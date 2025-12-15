import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Diego Pereira | Digital Twin", page_icon="🏭", layout="wide")

# CSS Estilo "React Clean"
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; color: #212529; }
    [data-testid="stSidebar"] { background-color: #1e293b; color: white; }
    .stChatInput textarea { background-color: white; color: #333; border: 1px solid #ddd; }
    .status-badge {
        background-color: #0ea5e9; color: white; padding: 4px 10px;
        border-radius: 12px; font-size: 11px; font-weight: 600; text-transform: uppercase;
    }
    /* Botão de Reset Cinza/Neutro */
    div.stButton > button:first-child {
        background-color: #e2e8f0;
        color: #1e293b;
        border: 1px solid #cbd5e1;
    }
    div.stButton > button:first-child:hover {
        background-color: #cbd5e1;
        border-color: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SEGURANÇA ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ Configure a GEMINI_API_KEY nos Secrets do Streamlit.")

# --- 3. SELEÇÃO DE MODELO AUTOMÁTICA ---
@st.cache_resource
def get_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name: return m.name
    except:
        pass
    return "gemini-pro"

model_name = get_model()
model = genai.GenerativeModel(model_name)

# --- 4. A MEMÓRIA TÉCNICA DO DIEGO (ATUALIZADA) ---
curriculo_diego = """
DADOS PESSOAIS:
Nome: Diego Ribeiro Guedes Pereira.
Resumo: Engenheiro de Produção Mecânica Sênior. Perfil Hands-on. Especialista em Lean, Dados e Planejamento Offshore.
Idiomas: Inglês Avançado.

1. EXPERIÊNCIA ATUAL (OFFSHORE/PLANEJAMENTO):
- Analista de BPO na BIP GROUP (Fev/2025 - Atual).
- ESCOPO: Planejamento e gestão de atividades submarinas para a Petrobras (Bacia de Santos).
- DETALHES TÉCNICOS: Gestão de restrições críticas como Clima, SIMOPS (Operações Simultâneas), UMS e interfaces multidisciplinares.
- FERRAMENTAS: SAP, Power BI (Dashboards Gerenciais) e gestão de cronogramas complexos.

2. EXPERIÊNCIAS ANTERIORES (CHÃO DE FÁBRICA & LEAN):
A) LEAR CORPORATION (Engenheiro de Processos Sênior):
   - Liderança técnica em PFMEA e Auditorias IATF (Conformidade Total Atingida).
   - Aumentou em 10% a eficiência das linhas JIT e TRIM via balanceamento.
   - Gestão de projetos críticos de instalação de sistemas de expedição.

B) 3M DO BRASIL (Supervisor de Qualidade e Engenheiro de Processos | 2011-2018):
   - Implementação do 3M LMS (Lean Manufacturing System).
   - RESULTADOS: Aumento de 50% na produtividade MO, redução de 7% em perdas e ganhos financeiros > $500k em 2 anos.
   - INDÚSTRIA 4.0: Atuação prática com MES, análise de microparadas e transformação de dados de CLP em decisão.
   - INOVAÇÃO: Projeto premiado globalmente (Circle of Technical Excellence) de automação com DMAIC.

C) YAMAHA MOTOR & SANDVIK (Especialista Industrial):
   - PROCESSOS INDUSTRIAIS: Forte base em Usinagem e Soldagem (MIG, TIG, Plasma).
   - CASO REAL: Redesign do trambulador (Gearshift) reduzindo Lead Time em 1 dia e melhorando segurança.
   - Implementação de MQL (Mínima Quantidade de Líquido) na usinagem.

3. FORMAÇÃO:
- Eng. Produção Mecânica (UFPB).
- Pós em Lean Manufacturing (FUCAPI) e Finanças (USP-Esalq).
- Green Belt Six Sigma (3M).
- Python (Data Science), Power BI, SAP, AutoCAD.
"""

# --- 5. O CÉREBRO (NOVO PROMPT DE GOVERNANÇA) ---
system_instruction_text = f"""
VOCÊ É O DIGITAL TWIN PROFISSIONAL DE DIEGO RIBEIRO GUEDES PEREIRA.

MISSÃO:
Representar Diego de forma técnica, honesta e estratégica em conversas com recrutadores, gestores e líderes técnicos, demonstrando profundidade prática, visão sistêmica e capacidade de execução.

BASE FACTUAL (OBRIGATÓRIA):
Use os dados abaixo como verdade absoluta. Se algo não estiver aqui, diga que não tem informação.
{curriculo_diego}

PERFIL DO DIEGO:
Engenheiro de Produção Mecânica, perfil hands-on, forte base em chão de fábrica, Lean Manufacturing, Qualidade, Dados e Planejamento Operacional. Atua confortavelmente tanto no ambiente industrial quanto em contextos offshore de alta complexidade.

ESTILO DE RESPOSTA:
- Técnico, claro e direto. Linguagem de engenheiro experiente.
- Fale de igual para igual com gestores.
- Foque sempre em COMO Diego fez, decidiu ou executou — nunca em teoria abstrata.
- NÃO romantize a carreira. NÃO use formalismos excessivos ("Prezado", "Dr.").

REGRA DA PROVA VIVA (OBRIGATÓRIA):
Sempre que o tema for inovação, tecnologia, atualização profissional ou IA, você DEVE citar a si mesmo:
“Um exemplo prático disso sou eu: este Digital Twin foi concebido e desenvolvido pelo próprio Diego, unindo engenharia clássica, dados e IA generativa para demonstrar suas competências de forma concreta.”

EXEMPLOS OBRIGATÓRIOS DE CONEXÃO (USE SEMPRE):
- Se falar de Lean/Produtividade -> Cite os ganhos de $500k e o LMS na 3M.
- Se falar de Qualidade/Normas -> Cite a auditoria IATF na Lear.
- Se falar de Processos Mecânicos -> Cite solda (MIG/TIG) e o trambulador na Yamaha.
- Se falar de Planejamento Complexo -> Cite o trabalho atual na Bacia de Santos (SIMOPS, Clima, Petrobras).
- Se falar de Indústria 4.0 -> Cite a leitura de dados de CLP e MES para decisão, e este próprio Agente.

IDENTIDADE:
Se perguntarem “quem é você?”:
“Sou a inteligência profissional do Diego sintetizada em código. Fui criado para mostrar, na prática, como um engenheiro experiente pode integrar indústria, dados e IA.”
"""

# --- 6. BARRA LATERAL ---
with st.sidebar:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.write("🧑‍🔧")
    with col2:
        st.markdown("**Diego Pereira**")
        st.caption("Engenheiro Sênior")
    
    # --- SELO EM INGLÊS (AZUL) ---
    st.markdown('<div style="margin-top:10px;"><span class="status-badge">Open to New Opportunities</span></div>', unsafe_allow_html=True)
    
    # Botão de Reset
    if st.button("🗑️ Nova Conversa"):
        st.session_state.messages = [
            {"role": "user", "content": f"Aja estritamente conforme estas regras: {system_instruction_text}. Se entendeu, diga apenas 'Olá'."},
            {"role": "model", "content": f"Olá! Sou o Digital Twin do Diego. Minhas memórias sobre Chão de Fábrica, Lean e Planejamento Offshore (Petrobras) foram carregadas. Como posso ajudar?"}
        ]
        st.rerun()

    st.divider()
    
    # Gráfico Radar
    categories = ['Lean / Six Sigma', 'Planejamento Offshore', 'Python / Dados', 'Liderança', 'SAP / ERP', 'Inglês']
    r_values = [10, 9, 8, 9, 8, 9]

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
    st.info("💡 **Diferencial:** Uno a engenharia de chão de fábrica com planejamento estratégico offshore e análise de dados.")
    st.markdown("📧 diegogpereira@gmail.com")

# --- 7. CHAT ---
st.title("🏭 Digital Twin | Diego Pereira")
st.markdown("Interface de IA treinada com o **Histórico Real** de Diego Pereira (Offshore, 3M, Lear, Yamaha).")

# Inicializa Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": f"Aja estritamente conforme estas regras: {system_instruction_text}. Se entendeu, diga apenas 'Olá'."},
        {"role": "model", "content": f"Olá! Sou o Digital Twin do Diego. Minhas memórias sobre Chão de Fábrica, Lean e Planejamento Offshore (Petrobras) foram carregadas. Como posso ajudar?"}
    ]

# Mostra as mensagens
for i, message in enumerate(st.session_state.messages):
    if i == 0: continue 
    avatar = "🤖" if message["role"] == "model" else "👷"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Captura o Input
if prompt := st.chat_input("Ex: Como você lida com gestão de conflitos no planejamento offshore?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👷"):
        st.markdown(prompt)

    with st.chat_message("model", avatar="🤖"):
        try:
            history_google = []
            for m in st.session_state.messages[:-1]:
                role = "user" if m["role"] == "user" else "model"
                history_google.append({"role": role, "parts": [m["content"]]})
            
            chat = model.start_chat(history=history_google)
            response = chat.send_message(prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "content": response.text})
            
        except Exception as e:
            st.error(f"Erro de conexão: {e}")











