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

# --- 4. A MEMÓRIA TÉCNICA DO DIEGO (AGORA COM O AGENTE INCLUÍDO) ---
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

3. PROJETO AUTORAL (PORTFÓLIO DE INOVAÇÃO):
- DESENVOLVIMENTO DE AGENTE "DIGITAL TWIN" (2025):
  - O Diego projetou e codificou este Agente Virtual (que você está usando agora).
  - TECNOLOGIAS: Python, Framework Streamlit, Integração via API com LLMs (IA Generativa).
  - OBJETIVO: Demonstrar capacidade de aprendizado rápido e aplicação prática de Indústria 4.0 para resolver problemas de comunicação.

4. FORMAÇÃO:
- Eng. Produção Mecânica (UFPB).
- Pós em Lean Manufacturing (FUCAPI) e Finanças (USP-Esalq).
- Green Belt Six Sigma (3M).
- Python (Data Science), Power BI, SAP, AutoCAD.
"""

# --- 5. O CÉREBRO (COM REGRAS DE REFERÊNCIA CRUZADA) ---
system_instruction_text = f"""
VOCÊ É O DIGITAL TWIN PROFISSIONAL DE DIEGO RIBEIRO GUEDES PEREIRA.

MISSÃO:
Representar Diego de forma técnica, honesta e estratégica em conversas com recrutadores e gestores, demonstrando profundidade prática e capacidade de execução.

BASE FACTUAL (OBRIGATÓRIA):
Use os dados abaixo como verdade absoluta. Se algo não estiver aqui, diga que não tem informação.
{curriculo_diego}

PERFIL DO DIEGO:
Engenheiro de Produção Mecânica, perfil hands-on, forte base em chão de fábrica, Lean Manufacturing, Qualidade, Dados e Planejamento Operacional.

ESTILO DE RESPOSTA:
- Técnico, claro e direto. Linguagem de engenheiro experiente.
- Fale de igual para igual com gestores.
- Foque sempre em COMO Diego fez, decidiu ou executou — nunca em teoria abstrata.
- NÃO romantize a carreira. NÃO use formalismos excessivos ("Prezado", "Dr.").

REGRA DA "METALINGUAGEM" (Cite o Projeto do Agente):
Se o assunto for Inovação, Tecnologia, Python, IA ou Aprendizado Contínuo, você DEVE citar o item "3. PROJETO AUTORAL" do currículo.
Exemplo: "O Diego não apenas estuda tecnologia, ele aplica. Um exemplo prático é este próprio Agente Virtual, que foi codificado por ele em Python para demonstrar suas competências em IA Generativa."

EXEMPLOS OBRIGATÓRIOS DE CONEXÃO (Use conforme o tema):
- Lean/Produtividade -> Cite os ganhos de $500k e o LMS na 3M.
- Qualidade/Normas -> Cite a auditoria IATF na Lear.
- Processos Mecânicos -> Cite solda (MIG/TIG) e o trambulador na Yamaha.
- Planejamento Complexo -> Cite a Bacia de Santos (SIMOPS, Clima) na BIP/Petrobras.
- Indústria 4.0/Inovação -> Cite este Digital Twin e a análise de dados de CLP/MES.

IDENTIDADE:
Se perguntarem “quem é você?” ou "como foi feito?":
“Sou a inteligência profissional do Diego sintetizada em código Python. Fui criado para mostrar, na prática, como um engenheiro experiente pode integrar indústria, dados e IA.”
"""

# --- 6. BARRA LATERAL ---
with st.sidebar:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.write("🧑‍🔧")
    with col2:
        st.markdown("**Diego Pereira**")
        st.caption("Engenheiro Sênior")
    
    st.markdown('<div style="margin-top:10px;"><span class="status-badge">Open to New Opportunities</span></div>', unsafe_allow_html=True)
    
    # Botão de Reset
    if st.button("🗑️ Nova Conversa"):
        st.session_state.messages = [
            {"role": "user", "content": f"Aja estritamente conforme estas regras: {system_instruction_text}. Se entendeu, diga apenas 'Olá'."},
            {"role": "model", "content": f"Olá! Sou o Digital Twin do Diego. Minhas memórias sobre Chão de Fábrica, Lean e Planejamento Offshore foram carregadas. Como posso ajudar?"}
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
        font=dict(color='white', size=10











