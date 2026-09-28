import streamlit as st
import ollama

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Friendly AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ==========================================
# CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #dbeafe,
        #fce7f3,
        #ede9fe
    );
    font-family: Arial, sans-serif;
}

/* Main title */
h1 {
    text-align: center;
    color: #7c3aed;
    font-size: 45px;
    font-weight: bold;
}

/* Headers */
h2, h3 {
    color: #6d28d9;
}

/* Text input */
.stTextInput input {
    border: 2px solid #8b5cf6;
    border-radius: 12px;
    padding: 12px;
    background-color: white;
}

/* Select box */
.stSelectbox > div > div {
    border-radius: 12px;
}

/* Buttons */
.stButton > button {
    width: 100%;
    background: linear-gradient(
        90deg,
        #8b5cf6,
        #ec4899
    );
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px;
    font-size: 18px;
    font-weight: bold;
}

/* Button hover */
.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #7c3aed,
        #db2777
    );
    color: white;
}

/* AI response */
.ai-response {
    background-color: white;
    border: 2px solid #c084fc;
    border-radius: 15px;
    padding: 20px;
    margin-top: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
}

/* User message */
.user-message {
    background-color: #ede9fe;
    border-radius: 12px;
    padding: 15px;
    margin-top: 10px;
}

/* Footer */
.footer {
    text-align: center;
    color: #6b7280;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# TITLE
# ==========================================

st.title("🤖 Friendly AI Chatbot")

st.write("### 💬 Ask me anything!")

st.write(
    "A simple AI chatbot powered by Ollama."
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("⚙️ Chatbot Settings")

name = st.sidebar.text_input(
    "Enter your name:"
)

model = st.sidebar.selectbox(
    "Select AI Model:",
    [
        "llama3.2",
        "llama3.1",
        "mistral"
    ]
)

st.sidebar.info(
    "Choose a model that is installed in Ollama."
)


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ==========================================
# DISPLAY CHAT HISTORY
# ==========================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
            👤 <b>{name if name else "You"}:</b>
            <br><br>
            {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="ai-response">
            🤖 <b>AI:</b>
            <br><br>
            {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )


# ==========================================
# QUESTION INPUT
# ==========================================

question = st.text_input(
    "💭 Enter your question:",
    placeholder="Type your question here..."
)


# ==========================================
# ASK AI
# ==========================================

if st.button("🚀 Ask AI"):

    if question.strip() == "":

        st.warning("⚠️ Please enter a question.")

    else:

        # Add user question
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        # Prepare messages for Ollama
        messages = [
            {
                "role": "system",
                "content": """
                You are a friendly and funny AI assistant.

                Explain things in simple language.

                Be helpful and encouraging.

                Give clear answers.
                """
            }
        ]

        messages.extend(
            st.session_state.messages
        )

        try:

            with st.spinner("🤔 AI is thinking..."):

                response = ollama.chat(
                    model=model,
                    messages=messages
                )

            answer = response["message"]["content"]

            # Save AI response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            # Refresh page
            st.rerun()

        except Exception as e:

            st.error(
                "❌ Could not connect to Ollama."
            )

            st.write(
                "Make sure Ollama is running and the selected model is installed."
            )


# ==========================================
# CLEAR CHAT
# ==========================================

if st.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    st.rerun()


# ==========================================
# FOOTER
# ==========================================

st.markdown(
    """
    <div class="footer">
    ✨ Powered by Streamlit + Ollama 🤖
    </div>
    """,
    unsafe_allow_html=True
)