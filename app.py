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
system_instruction_






