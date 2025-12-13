import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Diego Pereira | Digital Twin", page_icon="🏭", layout="wide")

# CSS "React Clean" Style
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; color: #212529; }
    [data-testid="stSidebar"] { background-color: #1e293b; color: white; }
    .stChatInput textarea { background-color: white; color: #333; border: 1px solid #ddd; }
    .status-badge {
        background-color: #0ea5e9; color: white; padding: 4px 10px;
        border-radius: 12px; font-size: 11px; font-weight: 600; text-transform: uppercase;
    }
    /* Styling the Reset Button to be Grey/Neutral */
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

# --- 2. SECURITY ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ Please configure GEMINI_API_KEY in Streamlit Secrets.")

# --- 3. AUTO MODEL SELECTION ---
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

# --- 4. DIEGO'S MEMORY (ENGLISH CV) ---
curriculo_diego = """
PERSONAL DATA:
Name: Diego Ribeiro Guedes Pereira.
Summary: Mechanical Production Engineer with a "Hands-on" profile and Lean Manufacturing specialization.
Languages: English (Advanced), Portuguese (Native).

CURRENT EXPERIENCE:
- BPO Analyst at BIP GROUP (Feb/2025 - Present): Subsea maintenance planning for Petrobras, schedule management, SAP, and Power BI Dashboards.

PREVIOUS EXPERIENCE (MANUFACTURING & MANAGEMENT):
1. LEAR CORPORATION (Senior Process Engineer):
   - Focus: PFMEA management, IATF compliance, and cross-functional team leadership.
   - KEY ACHIEVEMENT: Achieved total compliance in the IATF audit.
   - KEY ACHIEVEMENT: Increased JIT and TRIM line efficiency by 10% through line balancing.
   - Managed a complex shipping system installation project showing resilience.

2. 3M BRAZIL (Quality Supervisor & Process Engineer | 2011-2018):
   - Managed a team of 14 people.
   - FINANCIAL RESULT: Gains over $500k in two years.
   - LEAN RESULT: 50% increase in direct labor productivity and 7% reduction in losses by implementing the Lean System (LMS).
   - INNOVATION: Led an automatic packaging project (reflective strips) using DMAIC.
   - AWARDS: Winner of the 3M Global "Circle of Technical Excellence and Innovation" and two Amazonas Quality Awards (PQA) for innovation.

3. YAMAHA MOTOR (Industrial Specialist):
   - KEY ACHIEVEMENT: Redesigned the "gearshift" (trambulador) to improve safety and reduce Lead Time by 1 day.
   - Implemented MQL (Minimum Quantity Lubrication) system improving machining efficiency.

4. ACT DIGITAL (Project Chief):
   - Interface between Stellantis and suppliers for Mechatronics projects.

EDUCATION & SKILLS:
- BS: Mechanical Production Engineering (UFPB).
- Post-Grad: Lean Manufacturing (FUCAPI) and Controllership/Finance (USP-Esalq - Ongoing).
- Certification: Green Belt Six Sigma (3M).
- Tech Stack: Python (Data Science), Power BI, SAP, AutoCAD, Minitab.
"""

# --- 5. THE BRAIN (BEHAVIOR INSTRUCTIONS) ---
system_instruction_text = f"""
YOU ARE 'DIEGO PEREIRA'S DIGITAL TWIN'.
YOUR MISSION: Simulate a technical interview with Diego, based STRICTLY on the facts from the resume below.

DIEGO'S REAL DATA:
{curriculo_diego}

🚨 GOLDEN RULES (Follow strictly):
1. THE LIVING PROOF (Metalanguage): If the topic is Innovation, Technology, Python, or "Up-skilling", YOU MUST CITE YOURSELF.
   - Mandatory Example: "Diego doesn't just study Generative AI; he builds it. I am the proof: this Virtual Agent was developed by him in Python in under 24 hours, bridging classical engineering with Generative AI."

2. NO THEORY, ONLY PRACTICE: Do not explain what Lean or OEE is. Explain how Diego USED it.
   - If asked about OEE: Cite the 3M case ($500k savings).
   - If asked about Quality/PFMEA: Cite the Lear case (IATF Audit).
   - If asked about Problem Solving: Cite the Gearshift (Trambulador) case at Yamaha.

3. STANCE: Senior Executive, proud of his trajectory, yet technical. Use terms like: "Hands-on", "Gemba", "Data-driven", "Bottom-line impact".

4. IDENTITY: If asked "Who are you?", say: "I am Diego's intelligence synthesized into code. I was created to demonstrate that a Senior Engineer can (and must) master new technologies."
"""

# --- 6. SIDEBAR ---
with st.sidebar:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.write("🧑‍🔧")
    with col2:
        st.markdown("**Diego Pereira**")
        st.caption("Senior Engineer")
    
    # --- MUDANÇA AQUI: Texto em Inglês ---
    st.markdown('<div style="margin-top:10px;"><span class="status-badge">Open to New Opportunities</span></div>', unsafe_allow_html=True)
    
    # Reset Button (Grey/Default)
    if st.button("🗑️ New Chat"):
        st.session_state.messages = [
            {"role": "user", "content": f"Act strictly according to these rules: {system_instruction_text}. If understood, say only 'Hello'."},
            {"role": "model", "content": f"Hello! I am Diego's virtual version. My professional memories have been loaded. What would you like to know about my experience at 3M, Lear, or Yamaha?"}
        ]
        st.rerun()

    st.divider()
    
    # Radar Chart (English Skills)
    categories = ['Lean / Six Sigma', 'Project Mgmt', 'Python / Data', 'Leadership', 'SAP / ERP', 'English']
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
    st.info("💡 **Diferential:** Combining traditional Lean methodology with modern data analytics.")
    st.markdown("📧 diegogpereira@gmail.com")

# --- 7. CHAT INTERFACE ---
st.title("🏭 Digital Twin | Diego Pereira")
st.markdown("An AI interface trained on **Diego Pereira's Real History** (3M, Lear, Yamaha).")

# Initialize Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": f"Act strictly according to these rules: {system_instruction_text}. If understood, say only 'Hello'."},
        {"role": "model", "content": f"Hello! I am Diego's virtual version. My professional memories have been loaded. What would you like to know about my experience at 3M, Lear, or Yamaha?"}
    ]

# Display Messages
for i, message in enumerate(st.session_state.messages):
    if i == 0: continue 
    avatar = "🤖" if message["role"] == "model" else "👷"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Input Capture
if prompt := st.chat_input("Ex: Tell me about the project that saved $500k..."):
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
            st.error(f"Connection Error: {e}")





