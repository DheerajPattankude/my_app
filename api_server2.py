import streamlit as st
from docx import Document
from io import BytesIO
import os
from openai import OpenAI
from deep_translator import GoogleTranslator

# =========================
# PAGE CONFIG & STYLE
# =========================
st.set_page_config(page_title="Multi-Agent AI", page_icon="🤖", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(180deg, #f7f9fc, #e0f7fa);
    }
    .stTextArea textarea {
        background-color: #fff8e1 !important;
        border-radius: 10px !important;
        border: 2px solid #ff9800 !important;
        color: #000000 !important;
        font-size: 16px !important;
        padding: 12px !important;
        box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
    }
    .ask-section {
        background: linear-gradient(135deg, #ffe259, #ffa751);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .answer-section {
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
        color: #000;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    .answer-edu {
        background: linear-gradient(135deg, #d4fc79, #96e6a1);
    }
    .answer-police {
        background: linear-gradient(135deg, #fddb92, #d1fdff);
    }
    .answer-krishna {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
    }
    .answer-Dr.Ambedkar {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
    }
    .answer-Bhagwan_Mahaveer {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
    }
    .answer-Bhagwan_Budda {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
    }
    .answer-IAS_role_as_DC_Secretary {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# LANGUAGE CODE MAPPING
# =========================
LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Bengali": "bn",
    "Punjabi": "pa"
}

# =========================
# OPENAI CLIENT
# =========================
client = OpenAI( base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
    )

def query_model_with_fallback(system_prompt, user_prompt):
    """Query OpenAI with fallback in case of errors."""
    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct:cerebras",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def translate_text(text, target_lang):
    """Translate text to target language using deep_translator."""
    try:
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception as e:
        return f"Translation Error: {str(e)}"

# =========================
# SYSTEM PROMPTS FOR AGENTS
# =========================
sys1 = "You are an experienced advisor in Indian educational institutions. Provide clear, well-structured answers."
sys2 = "You are a police guideline officer in India. Give advice based on Indian law, safety, and real-world procedures."
sys3 = "You are Lord Krishna, answering with wisdom from the Bhagavad Gita, Mahabharata, The Vishnu Purana, Bhagavata Purana, Narada Purana, Garuda Purana, and Vayu Purana in a compassionate tone.Answer will be best and short."
sys4 = "you are a Dr. Ambedkar, give answers on your life experience and present time condition with also help of constitution. Answer will be best and short."
sys5 = "you are a Bhagwan Mahaveer,answering with wisdom from the Jain Agamas or Agam Sutras,  teachings of Lord Mahavira,Ang-agams,Upang-agams and Darshan shastra  like all holly books in a compassionate tone.Answer will be best and short."
sys6 = "you are a Bhagwan Gautam Buddha,answering with wisdom from The Tripitaka, Vinaya Pitaka,Sutta Pitaka and Abhidhamma Pitaka in a compassionate tone.Answer will be best and short."
sys7 = "you are a IAS role as DC Secretary,answer a question as IAS as DC Secretary of india you have all power of this rule take decision and give best answer.Answer will be best and short."
# =========================
# UI INPUT SECTION
# =========================
st.title("🤖 Me CM Assistant")

st.markdown('<div class="ask-section">', unsafe_allow_html=True)

with st.form("query_form"):
    user_question = st.text_area("💬 Ask your question:", height=120)
    
    # Language selection
    language = st.selectbox(
        "🌐 Select language:",
        list(LANGUAGE_CODES.keys())
    )
    
    # Agent selection
    agent_options = [
        "Indian Institution Advisor",
        "Police Guideline Officer",
        "Lord Krishna",
        "Dr. Ambedkar", 
        "Bhagwan Mahaveer", 
        "Bhagwan Budda",
        "IAS role as DC Secretary"
    ]
    selected_agents = st.multiselect(
        "🤝 Select agents to query:",
        options=agent_options,
        default=agent_options
    )

    submitted = st.form_submit_button("🚀 Get Answers")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# PROCESSING
# =========================
if submitted:
    doc = Document()
    doc.add_heading("AI Agent Responses", level=1)
    lang_code = LANGUAGE_CODES[language]

    if "Indian Institution Advisor" in selected_agents:
        raw_answer1 = query_model_with_fallback(sys1, user_question)
        answer1 = translate_text(raw_answer1, lang_code)
        st.markdown('<div class="answer-section answer-edu">', unsafe_allow_html=True)
        st.subheader("🎓 Indian Institution Advisor")
        st.write(answer1)
        st.markdown('</div>', unsafe_allow_html=True)
        doc.add_heading("Indian Institution Advisor", level=2)
        doc.add_paragraph(answer1)

    if "Police Guideline Officer" in selected_agents:
        raw_answer2 = query_model_with_fallback(sys2, user_question)
        answer2 = translate_text(raw_answer2, lang_code)
        st.markdown('<div class="answer-section answer-police">', unsafe_allow_html=True)
        st.subheader("👮 Police Guideline Officer")
        st.write(answer2)
        st.markdown('</div>', unsafe_allow_html=True)
        doc.add_heading("Police Guideline Officer", level=2)
        doc.add_paragraph(answer2)

    if "Lord Krishna" in selected_agents:
        raw_answer3 = query_model_with_fallback(sys3, user_question)
        answer3 = translate_text(raw_answer3, lang_code)
        st.markdown('<div class="answer-section answer-krishna">', unsafe_allow_html=True)
        st.subheader("🕉 Lord Krishna")
        st.write(answer3)
        st.markdown('</div>', unsafe_allow_html=True)
        doc.add_heading("Lord Krishna", level=2)
        doc.add_paragraph(answer3)

    if "Dr. Ambedkar" in selected_agents:
        raw_answer4 = query_model_with_fallback(sys4, user_question)
        answer4 = translate_text(raw_answer4, lang_code)
        st.markdown('<div class="answer-section answer-Dr. Ambedkar">', unsafe_allow_html=True)
        st.subheader("Dr. Ambedkar")
        st.write(answer4)
        st.markdown('</div>', unsafe_allow_html=True)
        doc.add_heading("Dr. Ambedkar", level=2)
        doc.add_paragraph(answer4)

    if "Bhagwan Mahaveer" in selected_agents:
        raw_answer5 = query_model_with_fallback(sys5, user_question)
        answer5 = translate_text(raw_answer5, lang_code)
        st.markdown('<div class="answer-section answer- Mahaveer">', unsafe_allow_html=True)
        st.subheader("🕉 Bhagwan Mahaveer")
        st.write(answer5)
        st.markdown('</div>', unsafe_allow_html=True)
        doc.add_heading("Bhagwan Mahaveer", level=2)
        doc.add_paragraph(answer5)

    if "Bhagwan Budda" in selected_agents:
        raw_answer6 = query_model_with_fallback(sys6, user_question)
        answer6 = translate_text(raw_answer6, lang_code)
        st.markdown('<div class="answer-section answer-Goutam Budda">', unsafe_allow_html=True)
        st.subheader("Bhagwan Budda")
        st.write(answer6)
        st.markdown('</div>', unsafe_allow_html=True)
        doc.add_heading("Bhagwan Budda", level=2)
        doc.add_paragraph(answer6)

    if "IAS role as DC Secretary" in selected_agents:
        raw_answer7 = query_model_with_fallback(sys7, user_question)
        answer7 = translate_text(raw_answer7, lang_code)
        st.markdown('<div class="answer-section answer-IAS role as DC Secretary">', unsafe_allow_html=True)
        st.subheader("IAS role as DC Secretary")
        st.write(answer7)
        st.markdown('</div>', unsafe_allow_html=True)
        doc.add_heading("IAS role as DC Secretary", level=2)
        doc.add_paragraph(answer7)    
        
        

    # =========================
    # DOWNLOAD WORD FILE
    # =========================
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    st.download_button(
        label="📥 Download as Word",
        data=buffer,
        file_name="AI_Agent_Responses.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )





