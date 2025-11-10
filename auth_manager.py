import streamlit as st
import os
from dotenv import load_dotenv
import hashlib

class AuthManager:
    def __init__(self):
        load_dotenv()
        self.users = self._load_users_from_env()
    
    def _load_users_from_env(self):
        """Load users from environment variable"""
        auth_string = os.getenv("AUTH_USERS", "")
        
        if not auth_string:
            st.error("⚠️ No users configured! Please set AUTH_USERS in .env file")
            st.info("Format: AUTH_USERS=username1:password1;username2:password2")
            return {}
        
        users = {}
        user_pairs = auth_string.split(";")
        
        for pair in user_pairs:
            if ":" in pair:
                username, password = pair.strip().split(":", 1)
                users[username.strip()] = password.strip()
        
        return users
    
    def _hash_password(self, password):
        """Hash password for secure comparison"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_credentials(self, username, password):
        """Verify username and password"""
        if username in self.users:
            return self.users[username] == password
        return False
    
    def get_user_count(self):
        """Get number of registered users"""
        return len(self.users)
    
    def render_login_screen(self):
        """Render the login interface"""
        st.markdown("""
        <div style="max-width: 450px; margin: 8rem auto; padding: 3rem; 
                    background: rgba(255,255,255,0.06); backdrop-filter: blur(30px);
                    border: 1px solid rgba(255,255,255,0.12); border-radius: 1.5rem;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
                    animation: slideUp 0.8s ease-out;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                           font-size: 3rem; margin-bottom: 0.5rem;">✨</h1>
                <h1 style="background: linear-gradient(135deg, #a855f7 0%, #ec4899 50%, #f97316 100%);
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                           font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">Perplexity AI</h1>
                <p style="color: #cbd5e1; font-size: 1.05rem;">Sign in to continue</p>
            </div>
        </div>
        
        <style>
            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form", clear_on_submit=False):
                username = st.text_input(
                    "Username", 
                    placeholder="Enter your username",
                    key="login_username"
                )
                password = st.text_input(
                    "Password", 
                    type="password",
                    placeholder="Enter your password",
                    key="login_password"
                )
                submit = st.form_submit_button("🔐 Login", use_container_width=True)
                
                if submit:
                    if self.verify_credentials(username, password):
                        st.session_state["authenticated"] = True
                        st.session_state["current_user"] = username
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                
                # Show user count hint
                st.markdown(f"""
                <div style="text-align: center; margin-top: 1.5rem; padding: 0.75rem;
                            background: rgba(168, 85, 247, 0.1); border-radius: 0.75rem;
                            border: 1px solid rgba(168, 85, 247, 0.2);">
                    <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0;">
                        💡 {self.get_user_count()} registered user(s) available
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    def check_authentication(self):
        """Check if user is authenticated"""
        if "authenticated" not in st.session_state:
            st.session_state["authenticated"] = False
        
        return st.session_state["authenticated"]
    
    def logout(self):
        """Logout current user"""
        st.session_state["authenticated"] = False
        if "current_user" in st.session_state:
            del st.session_state["current_user"]
        st.rerun()
    
    def get_current_user(self):
        """Get currently logged in username"""
        return st.session_state.get("current_user", "Guest")
