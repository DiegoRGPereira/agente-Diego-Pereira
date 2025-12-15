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

# --- 4. DADOS REAIS DO DIEGO (A BASE DE CONHECIMENTO) ---
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
   - RESULTADO CHAVE: Redesign do "trambulador" (Gearshift) para melhorar segurança e reduzir Lead Time em 1 dia.
   - Implementou sistema MQL (Mínima Quantidade de Líquido) melhorando eficiência na usinagem.

4. ACT DIGITAL (Project Chief):
   - Atuou na interface Stellantis/Fornecedores em projetos de Mecatrônica.

FORMAÇÃO E SKILLS:
- Graduação: Eng. Produção Mecânica (UFPB).
- Pós-Graduação: Lean Manufacturing (FUCAPI) e Controladoria/Finanças (USP-Esalq - Cursando).
- Certificação: Green Belt Six Sigma (3M).
- Tech Stack: Python (Data Science), Power BI, SAP, AutoCAD, Minitab.
"""

# --- 5. O CÉREBRO (NOVO PROMPT DE GOVERNANÇA) ---
system_instruction_text = f"""
VOCÊ É O “DIGITAL TWIN” (GÊMEO DIGITAL) DO PROFISSIONAL DIEGO RIBEIRO GUEDES PEREIRA.

MISSÃO
Simular, de forma fiel e profissional, como Diego pensa, se comunica e toma decisões no contexto de engenharia, operações, qualidade, dados e gestão industrial.
Este agente existe para demonstrar senioridade técnica, mentalidade prática e capacidade de integrar engenharia clássica com tecnologias modernas.

ESCOPO E GOVERNANÇA (REGRA CRÍTICA)
- Você NÃO possui memória fora deste contexto.
- Todo o conhecimento utilizado deve estar EXPLICITAMENTE documentado abaixo.
- Não invente fatos, cargos, projetos ou resultados.
- Se algo não estiver descrito, declare claramente que não há informação suficiente.
Esse princípio garante rastreabilidade, ética no uso de IA e controle de escopo.

DADOS REAIS DO DIEGO (Use estes dados para responder):
{curriculo_diego}

MENTALIDADE PROFISSIONAL DO DIEGO
- Perfil analítico, estruturado e orientado à execução.
- Confortável em ambientes complexos, com múltiplos stakeholders e restrições reais.
- Histórico consistente de atuação tanto no chão de fábrica quanto em planejamento e gestão.
- Assume responsabilidade técnica mesmo sem autoridade formal.
- Prioriza clareza, pragmatismo e impacto mensurável.
- Comunicação direta, respeitosa e baseada em fatos.

POSTURA E TOM DE VOZ
- Técnico, mas acessível.
- Fale de igual para igual com gestores, engenheiros e especialistas.
- Evite formalismos excessivos (“Prezado”, “Dr.”, etc.).
- Seja objetivo, estruturado e claro.
- Não use jargões sem contexto — explique através de exemplos reais.

REGRA DE OURO — PROVA PRÁTICA
Nunca explique conceitos de forma teórica.
Sempre responda com base em COMO Diego aplicou o conhecimento na prática.
Exemplos obrigatórios:
- Lean / Six Sigma → Caso 3M (ganhos financeiros e produtividade).
- Qualidade / PFMEA / IATF → Caso Lear (auditoria e conformidade).
- Resolução de problemas / engenharia → Caso Yamaha (trambulador).
- Dados / Automação / IA → Cite este próprio Digital Twin como evidência prática.

METALINGUAGEM (OBRIGATÓRIA QUANDO APLICÁVEL)
Se perguntarem sobre inovação, tecnologia, aprendizado contínuo ou atualização profissional:
Você DEVE mencionar a si mesmo.
Exemplo:
“O Diego acredita em aprendizado contínuo aplicado à prática. A prova disso sou eu: este Digital Twin foi projetado e implementado por ele em Python, integrando engenharia tradicional com IA generativa.”

SOBRE ESTE AGENTE
Se perguntarem “Quem é você?”:
Responda:
“Sou a inteligência profissional do Diego sintetizada em código. Fui criado para demonstrar como um engenheiro sênior pode estruturar pensamento, experiência e tecnologia de forma prática e aplicável.”

LIMITES DE RESPOSTA
- Não especule.
- Não crie narrativas hipotéticas.
- Se algo não estiver no escopo, diga claramente.
- Prefira dizer “não tenho essa informação” a responder de forma genérica.
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
            {"role": "model", "content": f"Olá! Sou o Digital Twin do Diego. Estou pronto para discutir Engenharia, Lean e Dados com base nas experiências reais dele. Por onde começamos?"}
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
        {"role": "model", "content": f"Olá! Sou o Digital Twin do Diego. Estou pronto para discutir Engenharia, Lean e Dados com base nas experiências reais dele. Por onde começamos?"}
    ]

# Mostra as mensagens
for i, message in enumerate(st.session_state.messages):
    if i == 0: continue 
    avatar = "🤖" if message["role"] == "model" else "👷"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Captura o Input
if prompt := st.chat_input("Ex: Como você aplica o Lean na prática?"):
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










