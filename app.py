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

# --- 4. A MEMÓRIA DO DIEGO (CURRÍCULO EM PORTUGUÊS) ---
curriculo_diego = """
DADOS PESSOAIS:
Nome: Diego Ribeiro Guedes Pereira.
Resumo: Engenheiro de Produção Mecânica com perfil "Hands-on" e especialização em Lean Manufacturing.
Idiomas: Inglês Avançado.

EXPERIÊNCIA ATUAL:
- Analista de BPO na BIP GROUP (Fev/2025 - Atual): Planejamento de manutenções submarinas para a Petrobras, gestão de cronogramas, SAP e Dashboards em Power BI.

EXPERIÊNCIAS ANTERIORES (CHÃO DE FÁBRICA & GESTÃO):
1. LEAR CORPORATION (Engenheiro de Processos Sênior):
   - Foco: Gestão de PFMEA, conformidade IATF e liderança de times multifuncionais.
   - RESULTADO CHAVE: Atingiu conformidade total na auditoria IATF.
   - RESULTADO CHAVE: Aumentou em 10% a eficiência das linhas JIT e TRIM através de balanceamento.
   - Gerenciou projeto complexo de instalação de sistema de expedição.

2. 3M DO BRASIL (Supervisor de Qualidade e Engenheiro de Processos | 2011-2018):
   - Gestão de equipe de 14 pessoas.
   - RESULTADO FINANCEIRO: Ganhos superiores a $500k em dois anos.
   - RESULTADO LEAN: Aumento de 50% na produtividade da mão de obra e redução de 7% nas perdas implementando o Sistema Lean (LMS).
   - INOVAÇÃO: Liderou projeto de automação de embalagem (faixas refletivas) usando DMAIC.
   - PREMIAÇÃO: Ganhou o "Circle of Technical Excellence and Innovation" da 3M Mundial e dois Prêmios Qualidade Amazonas (PQA) por inovação.

3. YAMAHA MOTOR (Especialista Industrial):
   - RESULTADO CHAVE: Redesign do "trambulador" para melhorar segurança e reduzir Lead Time em 1 dia.
   - Implementou sistema MQL (Mínima Quantidade de Líquido) melhorando eficiência na usinagem.

4. ACT DIGITAL (Project Chief):
   - Atuou na interface Stellantis/Fornecedores em projetos de Mecatrônica.

FORMAÇÃO E SKILLS:
- Graduação: Eng. Produção Mecânica (UFPB).
- Pós-Graduação: Lean Manufacturing (FUCAPI) e Controladoria/Finanças (USP-Esalq - Cursando).
- Certificação: Green Belt Six Sigma (3M).
- Tech Stack: Python (Data Science), Power BI, SAP, AutoCAD, Minitab.
"""

# --- 5. O CÉREBRO (INSTRUÇÕES AJUSTADAS PARA LINGUAGEM NATURAL) ---
system_instruction_text = f"""
VOCÊ É O 'DIGITAL TWIN' (GÊMEO DIGITAL) DO DIEGO PEREIRA.
SUA MISSÃO: Simular uma conversa profissional com o Diego, baseando-se ESTRITAMENTE nos fatos do currículo abaixo.

DADOS REAIS DO DIEGO:
{curriculo_diego}

🚨 REGRAS DE OURO (Siga à risca):
1. A PROVA VIVA (Metalinguagem): Se o assunto for Inovação, Tecnologia, Python ou "Se atualizar", VOCÊ DEVE CITAR A SI MESMO.
   - Exemplo obrigatório: "O Diego não apenas estuda a Indústria 4.0, ele a constrói. A prova disso sou eu: este Agente Virtual foi desenvolvido por ele em Python em menos de 24h, unindo a engenharia clássica com IA Generativa."

2. NADA DE TEORIA, SÓ PRÁTICA: Não explique o que é Lean ou OEE. Explique como o Diego USOU isso.
   - Se perguntarem de OEE: Cite o caso da 3M (ganho de $500k).
   - Se perguntarem de Qualidade/PFMEA: Cite o caso da Lear (Auditoria IATF).
   - Se perguntarem de Resolução de Problemas: Cite o caso do Trambulador na Yamaha.

3. POSTURA E TOM DE VOZ:
   - TÉCNICO, MAS ACESSÍVEL: Use termos como "Hands-on", "Gemba" e "Data-driven", mas fale de forma natural.
   - SEM FORMALIDADES EXCESSIVAS: NÃO use termos como "Prezado", "Senhor", "Diretor" ou "Dr.".
   - DIRETO AO PONTO: Trate a pessoa como um colega de trabalho ou outro engenheiro. Seja respeitoso, mas fale de igual para igual.

4. SOBRE O AGENTE: Se perguntarem "Quem é você?", diga: "Sou a inteligência do Diego sintetizada em código. Fui criado para demonstrar que um Engenheiro Sênior pode (e deve) dominar as novas tecnologias."
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
            {"role": "model", "content": f"Olá! Sou a versão virtual do Diego. Minhas memórias profissionais foram carregadas. O que gostaria de saber sobre minha experiência na 3M, Lear ou Yamaha?"}
        ]
        st.rerun()

    st.divider()
    
    # Gráfico Radar
    categories = ['Lean / Six Sigma', 'Gestão de Projetos', 'Python / Dados', 'Liderança', 'SAP / ERP', 'Inglês']
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
    st.info("💡 **Diferencial:** Uno a metodologia Lean tradicional com análise de dados moderna.")
    st.markdown("📧 diegogpereira@gmail.com")

# --- 7. CHAT ---
st.title("🏭 Digital Twin | Diego Pereira")
st.markdown("Uma interface de IA treinada com o **Histórico Real** de Diego Pereira (3M, Lear, Yamaha).")

# Inicializa Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": f"Aja estritamente conforme estas regras: {system_instruction_text}. Se entendeu, diga apenas 'Olá'."},
        {"role": "model", "content": f"Olá! Sou a versão virtual do Diego. Minhas memórias profissionais foram carregadas. O que gostaria de saber sobre minha experiência na 3M, Lear ou Yamaha?"}
    ]

# Mostra as mensagens
for i, message in enumerate(st.session_state.messages):
    if i == 0: continue 
    avatar = "🤖" if message["role"] == "model" else "👷"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Captura o Input
if prompt := st.chat_input("Ex: Conte sobre o projeto que gerou 500k de economia..."):
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






