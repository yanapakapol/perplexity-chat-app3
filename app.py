import streamlit as st
from perplexity_backend import PerplexityChat
from auth_manager import AuthManager

# Page configuration
st.set_page_config(
    page_title="Perplexity AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Complete CSS (same as before)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0118 0%, #1a0b2e 50%, #2d1b3d 100%) !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0118 0%, #1a0b2e 50%, #2d1b3d 100%) !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .main {
        background: transparent !important;
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 900px !important;
    }
    
    .main::before {
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 50% 50%, rgba(168, 85, 247, 0.15) 0%, transparent 50%);
        animation: pulse 15s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.1); }
    }
    
    /* Input fields */
    input[type="text"], input[type="password"], textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 0.75rem !important;
        color: #f1f5f9 !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }
    
    input:focus, textarea:focus {
        border-color: rgba(168, 85, 247, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.15) !important;
        background: rgba(255, 255, 255, 0.08) !important;
        outline: none !important;
    }
    
    input::placeholder, textarea::placeholder {
        color: #94a3b8 !important;
    }
    
    label {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    /* All buttons */
    .stButton > button, [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.5) !important;
    }
    
    .stButton > button:hover, [data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 30px rgba(168, 85, 247, 0.7) !important;
    }
    
    [data-testid="stForm"] {
        background: transparent !important;
        border: none !important;
    }
    
    .stAlert {
        border-radius: 0.75rem !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 1.25rem !important;
        padding: 1.5rem !important;
        margin-bottom: 1rem !important;
        transition: all 0.4s ease !important;
    }
    
    .stChatMessage:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(168, 85, 247, 0.4) !important;
        transform: translateX(4px);
        box-shadow: 0 8px 32px rgba(168, 85, 247, 0.2);
    }
    
    [data-testid="stChatMessageContent"], [data-testid="stChatMessageContent"] p {
        color: #f1f5f9 !important;
        font-size: 1rem !important;
        line-height: 1.7 !important;
    }
    
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(30px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 1.5rem !important;
        padding: 0.75rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
    }
    
    .stChatInputContainer:focus-within {
        border-color: rgba(168, 85, 247, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2) !important;
    }
    
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 1rem !important;
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        padding: 1rem 1.25rem !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 0 0 1rem 1rem !important;
        padding: 1.5rem !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 0.75rem !important;
        color: #f1f5f9 !important;
    }
    
    .header-title {
        font-size: 2.75rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 50%, #f97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }
    
    .model-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 1rem;
        padding: 1.25rem;
        margin: 0.75rem 0;
        transition: all 0.3s ease;
    }
    
    .model-card.selected {
        background: rgba(168, 85, 247, 0.15);
        border-color: rgba(168, 85, 247, 0.6);
        box-shadow: 0 8px 30px rgba(168, 85, 247, 0.3);
    }
    
    .tier-badge {
        display: inline-block;
        padding: 0.3rem 0.85rem;
        border-radius: 1rem;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    
    .tier-free {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.25), rgba(59, 130, 246, 0.25));
        color: #67e8f9;
        border: 1px solid rgba(6, 182, 212, 0.4);
    }
    
    .tier-pro {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.25), rgba(249, 115, 22, 0.25));
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    
    .tier-max {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.25), rgba(236, 72, 153, 0.25));
        color: #e879f9;
        border: 1px solid rgba(168, 85, 247, 0.4);
    }
    
    .citation-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 0.75rem;
        padding: 0.85rem 1rem;
        margin: 0.5rem 0;
    }
    
    .citation-number {
        display: inline-block;
        background: linear-gradient(135deg, #a855f7, #ec4899);
        color: white;
        border-radius: 0.5rem;
        padding: 0.3rem 0.65rem;
        font-weight: 700;
        font-size: 0.75rem;
        margin-right: 0.75rem;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 1.25rem;
        padding: 1.75rem;
        transition: all 0.4s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-6px);
        box-shadow: 0 12px 40px rgba(168, 85, 247, 0.25);
    }
    
    .footer-badge {
        background: rgba(168, 85, 247, 0.15);
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 1rem;
        padding: 0.4rem 0.85rem;
        color: #e9d5ff;
        font-size: 0.85rem;
    }
    
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #a855f7, #ec4899);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize authentication
auth = AuthManager()

# Check authentication
if not auth.check_authentication():
    auth.render_login_screen()
    st.stop()

# User is authenticated - show main app
current_user = auth.get_current_user()

# Logout button
col1, col2 = st.columns([8, 1])
with col2:
    if st.button("🚪 Logout"):
        auth.logout()

# Initialize session state
if 'chat' not in st.session_state:
    st.session_state.chat = PerplexityChat()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'model_filter' not in st.session_state:
    st.session_state.model_filter = "all"
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "sonar-reasoning-pro"

# Header
st.markdown(f"<h1 class='header-title'>✨ Welcome, {current_user}!</h1>", unsafe_allow_html=True)
st.markdown("<p class='header-subtitle'>Ask anything. Get intelligent answers with sources.</p>", unsafe_allow_html=True)

# Model Selector
with st.expander("🎯 Choose Your AI Model", expanded=False):
    st.markdown("### Available Models")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("All Models", use_container_width=True):
            st.session_state.model_filter = "all"
    with col2:
        if st.button("Reasoning Only", use_container_width=True):
            st.session_state.model_filter = "reasoning"
    with col3:
        if st.button("By Tier", use_container_width=True):
            st.session_state.model_filter = "tier"
    
    if st.session_state.model_filter == "reasoning":
        available_models = st.session_state.chat.get_reasoning_models()
    elif st.session_state.model_filter == "tier":
        tier = st.selectbox("Select Tier", ["Free", "Pro", "Max"])
        available_models = st.session_state.chat.get_models_by_tier(tier)
    else:
        available_models = st.session_state.chat.available_models
    
    model_options = list(available_models.keys())
    selected_model = st.selectbox(
        "Select Model",
        options=model_options,
        format_func=lambda x: f"{available_models[x]['icon']} {available_models[x]['name']} - {available_models[x]['description']}",
        index=model_options.index(st.session_state.selected_model) if st.session_state.selected_model in model_options else 0,
        key="model_selector"
    )
    
    st.session_state.selected_model = selected_model
    model_info = available_models[selected_model]
    tier_class = f"tier-{model_info['tier'].lower()}"
    
    st.markdown(f"""
    <div class="model-card selected">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
            <span style="font-size: 1.75rem;">{model_info['icon']}</span>
            <div>
                <span style="font-size: 1.15rem; font-weight: 600; color: #f8fafc;">{model_info['name']}</span>
                <span class="tier-badge {tier_class}">{model_info['tier']}</span>
            </div>
        </div>
        <p style="color: #cbd5e1; font-size: 0.95rem;">
            {model_info['description']}
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border: none; height: 1px; background: rgba(255,255,255,0.1); margin: 2rem 0;'>", unsafe_allow_html=True)

# Welcome screen or chat history
if len(st.session_state.chat_history) == 0:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h2 style="font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Ready to Explore?
        </h2>
        <p style="color: #cbd5e1; font-size: 1.05rem;">Ask anything and get intelligent answers</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <span style="font-size: 2.5rem; display: block; margin-bottom: 1rem;">🧠</span>
            <h3 style="color: #f8fafc; font-size: 1.15rem; margin-bottom: 0.5rem;">Advanced Reasoning</h3>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0;">Complex problem-solving with step-by-step analysis</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <span style="font-size: 2.5rem; display: block; margin-bottom: 1rem;">⚡</span>
            <h3 style="color: #f8fafc; font-size: 1.15rem; margin-bottom: 0.5rem;">Lightning Fast</h3>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0;">Get instant responses with real-time processing</p>
        </div>
        """, unsafe_allow_html=True)

# Chat history
for chat in st.session_state.chat_history:
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"<div style='color: #f1f5f9;'>{chat['question']}</div>", unsafe_allow_html=True)
    
    with st.chat_message("assistant", avatar="✨"):
        st.markdown(f"<div style='color: #f1f5f9; line-height: 1.7;'>{chat['answer']}</div>", unsafe_allow_html=True)
        
        if chat["citations"]:
            with st.expander(f"📚 {len(chat['citations'])} Sources"):
                for citation in chat["citations"]:
                    st.markdown(f"""
                    <div class="citation-card">
                        <span class="citation-number">{citation['number']}</span>
                        <strong style="color: #f1f5f9;">{citation['domain']}</strong><br>
                        <a href="{citation['url']}" target="_blank" style="color: #c4b5fd; text-decoration: none;">{citation['url'][:70]}...</a>
                    </div>
                    """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask me anything...")

if user_input:
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"<div style='color: #f1f5f9;'>{user_input}</div>", unsafe_allow_html=True)
    
    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat.ask(user_input, model=st.session_state.selected_model)
            st.markdown(f"<div style='color: #f1f5f9; line-height: 1.7;'>{response['answer']}</div>", unsafe_allow_html=True)
            
            if response["citations"]:
                with st.expander(f"📚 {len(response['citations'])} Sources"):
                    for citation in response["citations"]:
                        st.markdown(f"""
                        <div class="citation-card">
                            <span class="citation-number">{citation['number']}</span>
                            <strong style="color: #f1f5f9;">{citation['domain']}</strong><br>
                            <a href="{citation['url']}" target="_blank" style="color: #c4b5fd; text-decoration: none;">{citation['url'][:70]}...</a>
                        </div>
                        """, unsafe_allow_html=True)
    
    st.session_state.chat_history.append(response)
    st.rerun()

# Footer
st.markdown("<hr style='border: none; height: 1px; background: rgba(255,255,255,0.1); margin: 2rem 0;'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.chat.clear_history()
        st.session_state.chat_history = []
        st.rerun()

with col2:
    st.markdown(f"""
    <div style="text-align: center; padding: 0.75rem;">
        <span class="footer-badge">💬 {len(st.session_state.chat_history)} messages</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="text-align: center; padding: 0.75rem;">
        <span class="footer-badge">{model_info['icon']} {model_info['name']}</span>
    </div>
    """, unsafe_allow_html=True)
