import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="SolarBot | Electro Solaire", page_icon="☀️", layout="centered")

st.markdown("""
<style>
.stApp { background: linear-gradient(180deg,#f1fff4 0%,#ffffff 65%); }
[data-testid="stChatMessage"] { border: 1px solid #d7eadb; border-radius: 16px; }
h1 { color:#176b3a; }
</style>
""", unsafe_allow_html=True)

st.title("☀️ SolarBot")
st.caption("Votre assistant intelligent de l’énergie solaire | Electro Solaire")
st.write("Bonjour ! Je suis SolarBot 🌱 Posez-moi vos questions sur l’énergie solaire, les panneaux photovoltaïques et les économies d’électricité.")

# Configure the API key in Streamlit Secrets as OPENAI_API_KEY
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Posez votre question sur l’énergie solaire…")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        with st.chat_message("assistant"):
            with st.spinner("SolarBot réfléchit…"):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role":"system","content":(
                            "Tu es SolarBot, assistant pédagogique du site Electro Solaire. "
                            "Réponds clairement et simplement en français ou dans la langue utilisée par le visiteur. "
                            "Tu es spécialisé dans l'énergie solaire, les panneaux photovoltaïques, "
                            "l'environnement et les économies d'énergie. Ne prétends pas connaître des prix "
                            "ou des données locales non vérifiés."
                        )},
                        *st.session_state.messages
                    ]
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
        st.session_state.messages.append({"role":"assistant","content":answer})
    except Exception:
        st.error("Configuration nécessaire : ajoutez OPENAI_API_KEY dans les secrets de Streamlit, puis relancez l’application.")
