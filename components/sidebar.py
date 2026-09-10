import streamlit as st
from data.scenarios import SCENARIOS

def render_sidebar():
    """Renders dark sidebar with ChatGPT heading and TRY SCENARIOS section label."""
    with st.sidebar:
        # Force ultra-high specificity CSS directly inside sidebar
        st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
            background-color: #07080A !important;
            border-right: 1px solid #23242A !important;
        }
        
        .sidebar-brand-title-forced {
            font-size: 1.35rem !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
            display: flex !important;
            align-items: center !important;
            gap: 10px !important;
            padding: 12px 0 16px 0 !important;
        }

        /* FORCED ACTIVE SELECTED EXAMPLE ITEM BACKGROUND COLOR: #00A67E */
        section[data-testid="stSidebar"] button[kind="primary"],
        section[data-testid="stSidebar"] button[data-testid="baseButton-primary"],
        section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
            background-color: #00A67E !important;
            background: #00A67E !important;
            border: 1px solid #00A67E !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 8px rgba(0, 166, 126, 0.4) !important;
        }

        section[data-testid="stSidebar"] button[kind="primary"] p,
        section[data-testid="stSidebar"] button[data-testid="baseButton-primary"] p,
        section[data-testid="stSidebar"] button[kind="primary"] span {
            color: #FFFFFF !important;
        }

        section[data-testid="stSidebar"] button[kind="secondary"],
        section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {
            background-color: transparent !important;
            border: 1px solid transparent !important;
            color: #7E7F8F !important;
        }
        </style>
        <div class="sidebar-brand-title-forced">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22.2819 9.8211C21.6881 4.5451 17.0706 0.5 11.5 0.5C5.42487 0.5 0.5 5.42487 0.5 11.5C0.5 17.0706 4.5451 21.6881 9.8211 22.2819C10.3756 22.3442 10.875 21.9056 10.875 21.3482V18.1583C10.875 17.6534 10.5056 17.2248 10.0076 17.1479C6.88339 16.6648 4.5 13.963 4.5 10.75C4.5 7.02208 7.52208 4 11.25 4C14.9779 4 18 7.02208 18 10.75C18 13.963 15.6166 16.6648 12.4924 17.1479C11.9944 17.2248 11.625 17.6534 11.625 18.1583V21.3482C11.625 21.9056 12.1244 22.3442 12.6789 22.2819C17.9549 21.6881 22 17.0706 22 11.5C22 10.932 21.9576 10.372 21.876 9.8229L22.2819 9.8211Z" fill="#00A67E"/>
            </svg>
            <span style="color: #FFFFFF !important; font-weight: 700;">ChatGPT</span>
        </div>
        """, unsafe_allow_html=True)
        
        # New Chat button
        st.markdown("""
        <div class="new-analysis-btn-wrapper">
            <button class="new-analysis-btn">
                <span>➕ New Chat</span>
                <span class="cmd-k">⌘K</span>
            </button>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-label">TRY SCENARIOS</div>', unsafe_allow_html=True)
        
        scenario_items = [
            ("📊 Data Analysis", "📊 Data Analysis", "Campaign ROI & correlation"),
            ("🔎 Market Research", "🔎 Market Research", "Coffee subscription survey"),
            ("💻 Code Generation", "💻 Code Generation", "Average age calculation")
        ]
        
        current_scenario_key = st.session_state.get("selected_scenario", "📊 Data Analysis")
        
        for scenario_key, title, subtitle in scenario_items:
            is_active = (current_scenario_key == scenario_key)
            btn_type = "primary" if is_active else "secondary"
            dot_suffix = "  🟢" if is_active else ""
            
            if st.button(
                f"{title}\n{subtitle}{dot_suffix}",
                key=f"side_nav_{scenario_key}",
                use_container_width=True,
                type=btn_type
            ):
                st.session_state.selected_scenario = scenario_key
                st.session_state.chat_sent = False
                st.session_state.selected_highlight_id = None
                st.session_state.lens_active = True
                st.rerun()

        st.markdown("""
        <div class="sidebar-footer-card">
            <div class="sidebar-footer-title">
                <span>❇️</span> Active Lens Layer
            </div>
            Evaluates calculations, causal claims, hidden assumptions, and claims in real-time.
        </div>
        """, unsafe_allow_html=True)
