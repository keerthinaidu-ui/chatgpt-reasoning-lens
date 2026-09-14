import streamlit as st
import streamlit.components.v1 as components
import os
import html
import re
from data.scenarios import SCENARIOS
from components.issue_card import render_issue_card

# 1. Page Configuration
st.set_page_config(
    page_title="ChatGPT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Direct Forced High-Priority CSS Overrides
st.markdown("""
<style>
/* Base Dark Theme Overrides */
html, body, [class*="css"], .stApp {
    background-color: #0B0C0E !important;
    color: #ECECF1 !important;
}

.main .block-container {
    max-width: 760px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 120px !important;
}

/* Sidebar Dark & Forced Styling */
section[data-testid="stSidebar"] {
    background-color: #07080A !important;
    border-right: 1px solid #23242A !important;
}

.sidebar-header-box-forced {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    padding: 10px 0 16px 0 !important;
}

.sidebar-brand-title-forced {
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
}

.sidebar-section-label-forced {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.8px !important;
    color: #7E7F8F !important;
    text-transform: uppercase !important;
    margin: 20px 0 10px 0 !important;
}

/* FORCED ACTIVE SELECTED ITEM BACKGROUND COLOR: #00A67E */
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

section[data-testid="stSidebar"] button[kind="primary"] *,
section[data-testid="stSidebar"] button[data-testid="baseButton-primary"] * {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] button[kind="secondary"],
section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {
    background-color: transparent !important;
    border: 1px solid transparent !important;
    color: #7E7F8F !important;
}

/* Composer Card Container */
.composer-card-container {
    background-color: #15161A !important;
    border: 1px solid #23242A !important;
    border-radius: 16px !important;
    padding: 14px 16px 10px 16px !important;
    margin-top: 10px !important;
    margin-bottom: 12px !important;
    position: relative !important;
}

.composer-card-container div[data-testid="stTextArea"] textarea {
    background-color: transparent !important;
    border: none !important;
    color: #ECECF1 !important;
    font-size: 0.92rem !important;
    padding: 4px 0 !important;
    box-shadow: none !important;
}

/* FORCED GREEN (#00A67E) FILLED SQUARE SEND BUTTON WITH WHITE (#FFFFFF) HORIZONTAL ARROW */
button[key="chatgpt_send_btn"],
button[key="bottom_send_btn"],
div[data-testid="stColumn"] button[key="chatgpt_send_btn"],
div[data-testid="stColumn"] button[key="bottom_send_btn"],
div.stButton > button[key="chatgpt_send_btn"],
div.stButton > button[key="bottom_send_btn"] {
    background-color: #00A67E !important;
    background: #00A67E !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    width: 38px !important;
    height: 38px !important;
    min-width: 38px !important;
    max-width: 38px !important;
    padding: 0 !important;
    border: none !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    box-shadow: 0 2px 8px rgba(0, 166, 126, 0.4) !important;
}

button[key="chatgpt_send_btn"] *,
button[key="bottom_send_btn"] *,
div[data-testid="stColumn"] button[key="chatgpt_send_btn"] *,
div[data-testid="stColumn"] button[key="bottom_send_btn"] * {
    background-color: transparent !important;
    background: transparent !important;
    color: #FFFFFF !important;
    font-size: 1.2rem !important;
    font-weight: bold !important;
}

button[key="chatgpt_send_btn"]:hover,
button[key="bottom_send_btn"]:hover {
    background-color: #008F6C !important;
    background: #008F6C !important;
}

/* Top Toggle Pill */
.top-toggle-container {
    background: #15161A !important;
    border: 1px solid #23242A !important;
    padding: 4px 14px !important;
    border-radius: 20px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
}

/* Embedded Table Styling inside Prompt Box */
.prompt-table-box {
    background: #111215;
    border: 1px solid #22232B;
    border-radius: 8px;
    padding: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    margin-top: 12px;
}

.prompt-table-box table {
    width: 100%;
    border-collapse: collapse;
}

.prompt-table-box th, .prompt-table-box td {
    padding: 8px 12px;
    text-align: left;
    border-bottom: 1px solid #1C1D24;
}

.prompt-table-box th {
    color: #7E7F8F;
    font-size: 0.75rem;
    text-transform: uppercase;
}

.lens-highlight-clickable {
    transition: background-color 0.15s ease;
}

.lens-highlight-clickable:hover {
    background-color: rgba(255, 255, 255, 0.1) !important;
}

#lens-cards-wrapper {
    contain: content;
}

/* Main Page Scenario Cards */
div[data-testid="stColumn"] button[key^="main_scen_"] {
    background-color: #15161A !important;
    border: 1px solid #23242A !important;
    border-radius: 12px !important;
    padding: 16px 14px !important;
    color: #ECECF1 !important;
    min-height: 95px !important;
    height: 100% !important;
    text-align: left !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
    align-items: flex-start !important;
    transition: all 0.2s ease !important;
    white-space: pre-wrap !important;
}

div[data-testid="stColumn"] button[key^="main_scen_"]:hover {
    border-color: #00A67E !important;
    background-color: #1C1D24 !important;
    box-shadow: 0 4px 14px rgba(0, 166, 126, 0.2) !important;
}

div[data-testid="stColumn"] button[key^="main_scen_"] * {
    text-align: left !important;
}

/* Plus Icon Buttons inside Composer Bar */
button[key="bar_plus_btn"],
button[key="bottom_plus_btn"],
div[data-testid="stColumn"] button[key="bar_plus_btn"],
div[data-testid="stColumn"] button[key="bottom_plus_btn"] {
    background: transparent !important;
    border: none !important;
    color: #7E7F8F !important;
    font-size: 1.2rem !important;
    font-weight: bold !important;
    padding: 0 !important;
    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    box-shadow: none !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
}

button[key="bar_plus_btn"] *,
button[key="bottom_plus_btn"] * {
    color: #7E7F8F !important;
    font-size: 1.2rem !important;
}

button[key="bar_plus_btn"]:hover,
button[key="bottom_plus_btn"]:hover {
    background: #1F2026 !important;
    border-radius: 50% !important;
}

button[key="bar_plus_btn"]:hover *,
button[key="bottom_plus_btn"]:hover * {
    color: #ECECF1 !important;
}
</style>
""", unsafe_allow_html=True)

def reset_to_new_chat():
    st.session_state.chat_sent = False
    st.session_state.composer_text = ""
    st.session_state["initial_composer_field"] = ""
    st.session_state["bottom_composer_field"] = ""
    st.session_state.selected_highlight_id = None
    if "selected_hl" in st.query_params:
        try:
            st.query_params.clear()
        except Exception:
            pass

# 3. Initialize Base Session State
if "chat_sent" not in st.session_state:
    st.session_state.chat_sent = False

if "selected_scenario" not in st.session_state or st.session_state.selected_scenario not in SCENARIOS:
    st.session_state.selected_scenario = list(SCENARIOS.keys())[0]

if "last_loaded_scenario" not in st.session_state:
    st.session_state.last_loaded_scenario = st.session_state.selected_scenario

if "composer_text" not in st.session_state:
    st.session_state.composer_text = ""

if "last_sent_prompt" not in st.session_state:
    st.session_state.last_sent_prompt = ""

if "lens_active" not in st.session_state:
    st.session_state.lens_active = False

if "selected_highlight_id" not in st.session_state:
    st.session_state.selected_highlight_id = None

# Handle URL query params ONLY if already viewing a response
valid_hl_ids = {f"{s['id']}_{hl['id']}" for s in SCENARIOS.values() for hl in s.get("highlights", [])}
if "selected_hl" in st.query_params:
    if not st.session_state.chat_sent:
        try:
            st.query_params.clear()
        except Exception:
            pass
        st.session_state.selected_highlight_id = None
    else:
        hl_param = st.query_params["selected_hl"]
        if hl_param in valid_hl_ids:
            st.session_state.selected_highlight_id = hl_param
            if hl_param.startswith("market_research_"):
                st.session_state.selected_scenario = "🔎 Market Research"
            elif hl_param.startswith("code_gen_"):
                st.session_state.selected_scenario = "💻 Code Generation"
            elif hl_param.startswith("data_analysis_"):
                st.session_state.selected_scenario = "📊 Data Analysis"
        else:
            st.session_state.selected_highlight_id = None

# 4. DIRECT SIDEBAR RENDERING
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header-box-forced">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M22.2819 9.8211C21.6881 4.5451 17.0706 0.5 11.5 0.5C5.42487 0.5 0.5 5.42487 0.5 11.5C0.5 17.0706 4.5451 21.6881 9.8211 22.2819C10.3756 22.3442 10.875 21.9056 10.875 21.3482V18.1583C10.875 17.6534 10.5056 17.2248 10.0076 17.1479C6.88339 16.6648 4.5 13.963 4.5 10.75C4.5 7.02208 7.52208 4 11.25 4C14.9779 4 18 7.02208 18 10.75C18 13.963 15.6166 16.6648 12.4924 17.1479C11.9944 17.2248 11.625 17.6534 11.625 18.1583V21.3482C11.625 21.9056 12.1244 22.3442 12.6789 22.2819C17.9549 21.6881 22 17.0706 22 11.5C22 10.932 21.9576 10.372 21.876 9.8229L22.2819 9.8211Z" fill="#00A67E"/>
        </svg>
        <span class="sidebar-brand-title-forced">ChatGPT</span>
    </div>
    """, unsafe_allow_html=True)

    st.button("➕ New Chat", key="new_chat_btn", use_container_width=True, on_click=reset_to_new_chat)


    st.markdown('<div class="sidebar-section-label-forced">TRY SCENARIOS</div>', unsafe_allow_html=True)

    scenario_items = [
        ("📊 Data Analysis", "📊 Data Analysis", "Campaign ROI & correlation"),
        ("🔎 Market Research", "🔎 Market Research", "Coffee subscription survey"),
        ("💻 Code Generation", "💻 Code Generation", "Average age calculation")
    ]

    current_scenario_key = st.session_state.selected_scenario

    for scenario_key, title, subtitle in scenario_items:
        is_active = (st.session_state.selected_scenario == scenario_key)
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
            st.session_state.lens_active = False
            
            scen_data = SCENARIOS[scenario_key]
            prompt_val = scen_data["prompt"]
            if scen_data.get("user_data"):
                prompt_val += "\n\nData:\n" + scen_data["user_data"]
            
            st.session_state.composer_text = prompt_val
            st.session_state["initial_composer_field"] = prompt_val
            st.session_state.last_loaded_scenario = scenario_key
            
            if "selected_hl" in st.query_params:
                st.query_params.clear()
            st.rerun()

    st.markdown("""
    <div style="background: #15161A; border: 1px solid #23242A; border-radius: 10px; padding: 14px; margin-top: 50px; font-size: 0.78rem; color: #7E7F8F; line-height: 1.5;">
        <div style="color: #00A67E; font-weight: 600; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
            <span>❇️</span> Active Lens Layer
        </div>
        Evaluates calculations, causal claims, hidden assumptions, and claims in real-time.
    </div>
    """, unsafe_allow_html=True)

scenario_data = SCENARIOS[st.session_state.selected_scenario]

# 5. Main Screen Rendering
if not st.session_state.chat_sent:
    # --- INITIAL SCREEN VIEW (ChatGPT Homescreen) ---
    st.markdown("""
    <div class="center-hero" style="text-align: center; padding-top: 30px; padding-bottom: 20px;">
        <div class="hero-icon-circle" style="width: 56px; height: 56px; background: #15161A; border: 1px solid #23242A; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 14px;">
            <svg width="34" height="34" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22.2819 9.8211C21.6881 4.5451 17.0706 0.5 11.5 0.5C5.42487 0.5 0.5 5.42487 0.5 11.5C0.5 17.0706 4.5451 21.6881 9.8211 22.2819C10.3756 22.3442 10.875 21.9056 10.875 21.3482V18.1583C10.875 17.6534 10.5056 17.2248 10.0076 17.1479C6.88339 16.6648 4.5 13.963 4.5 10.75C4.5 7.02208 7.52208 4 11.25 4C14.9779 4 18 7.02208 18 10.75C18 13.963 15.6166 16.6648 12.4924 17.1479C11.9944 17.2248 11.625 17.6534 11.625 18.1583V21.3482C11.625 21.9056 12.1244 22.3442 12.6789 22.2819C17.9549 21.6881 22 17.0706 22 11.5C22 10.932 21.9576 10.372 21.876 9.8229L22.2819 9.8211Z" fill="#00A67E"/>
            </svg>
        </div>
        <div class="hero-main-title" style="font-size: 1.8rem; font-weight: 700; margin-top: 10px; margin-bottom: 24px; color: #FFFFFF;">What's on your mind? Pick any scenario</div>
    </div>
    """, unsafe_allow_html=True)

    # Scenario Cards Grid (3 cards)
    scen_col1, scen_col2, scen_col3 = st.columns(3)
    
    def populate_scenario(scen_key):
        st.session_state.selected_scenario = scen_key
        st.session_state.chat_sent = False
        st.session_state.selected_highlight_id = None
        st.session_state.lens_active = False
        
        scen_info = SCENARIOS[scen_key]
        prompt_str = scen_info["prompt"]
        if scen_info.get("user_data"):
            prompt_str += "\n\nData:\n" + scen_info["user_data"]
            
        st.session_state.composer_text = prompt_str
        st.session_state["initial_composer_field"] = prompt_str
        st.rerun()

    with scen_col1:
        if st.button("📊 Data Analysis\n\nCampaign ROI & correlation", key="main_scen_data_analysis", use_container_width=True):
            populate_scenario("📊 Data Analysis")

    with scen_col2:
        if st.button("🔎 Market Research\n\nCoffee subscription survey", key="main_scen_market_research", use_container_width=True):
            populate_scenario("🔎 Market Research")

    with scen_col3:
        if st.button("💻 Code Generation\n\nAverage age calculation", key="main_scen_code_gen", use_container_width=True):
            populate_scenario("💻 Code Generation")

    # Spacing before type bar at bottom of screen
    st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)

    # ChatGPT Typing Bar Container
    st.markdown('<div class="composer-card-container">', unsafe_allow_html=True)
    
    composer_text = st.text_area(
        "Composer",
        value=st.session_state.get("composer_text", ""),
        placeholder="Ask anything or pick a scenario above...",
        height=100,
        key="initial_composer_field",
        label_visibility="collapsed"
    )
    st.session_state.composer_text = composer_text

    # Bottom Toolbar inside typing bar
    bar_c1, bar_c2, bar_c3 = st.columns([1, 8, 2.2])
    with bar_c1:
        st.button("➕", key="bar_plus_btn", help="New Chat", on_click=reset_to_new_chat)
    with bar_c3:
        col_mic, col_send = st.columns([1, 1])
        with col_mic:
            st.markdown('<div style="padding-top: 6px; text-align: right;"><span style="font-size: 1.2rem; color: #7E7F8F; cursor: pointer;" title="Voice mode">🎙️</span></div>', unsafe_allow_html=True)
        with col_send:
            if st.button("➔", key="chatgpt_send_btn"):
                user_txt = st.session_state.get("composer_text", "").strip()
                if not user_txt:
                    scen = SCENARIOS[st.session_state.selected_scenario]
                    user_txt = scen["prompt"]
                    if scen.get("user_data"):
                        user_txt += "\n\nData:\n" + scen["user_data"]
                st.session_state.chat_sent = True
                st.session_state.last_sent_prompt = user_txt
                st.session_state.composer_text = ""
                st.session_state.selected_highlight_id = None
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; color: #565869; font-size: 0.78rem; margin-top: 16px;">
        ChatGPT can make mistakes. Reasoning Lens highlights underlying logical consistency.
    </div>
    """, unsafe_allow_html=True)


else:
    # --- CONVERSATION / ANALYSIS RESPONSE VIEW ---
    top_col1, top_col2 = st.columns([4, 2])
    with top_col2:
        st.markdown('<div class="top-toggle-container">', unsafe_allow_html=True)
        lens_on = st.toggle(
            "● Reasoning Lens ON" if st.session_state.get("lens_active", False) else "Reasoning Lens OFF",
            value=st.session_state.get("lens_active", False),
            key="top_lens_toggle"
        )
        st.session_state.lens_active = lens_on
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"### {scenario_data['title']}")

    # User message box with clean table representation for data
    st.markdown('<div style="background: #15161A; border: 1px solid #23242A; border-radius: 12px; padding: 20px; margin-bottom: 12px;">', unsafe_allow_html=True)
    st.markdown(f"**User Prompt:** {scenario_data['prompt']}")
    
    if scenario_data.get("user_data"):
        if scenario_data["id"] == "code_gen":
            st.code(scenario_data["user_data"], language="python")
        elif scenario_data["id"] == "data_analysis":
            st.markdown("""
            <div class="prompt-table-box">
                <div style="color: #7E7F8F; font-size: 0.75rem; margin-bottom: 8px;">Embedded Data:</div>
                <table>
                    <thead>
                        <tr>
                            <th>Month</th>
                            <th>Sales</th>
                            <th>Advertising Spend</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>January</td><td>1,000</td><td>$5,000</td></tr>
                        <tr><td>February</td><td>1,100</td><td>$5,500</td></tr>
                        <tr><td>March</td><td>1,250</td><td>$8,000</td></tr>
                        <tr><td>April</td><td><span style="color: #00A67E; font-weight: bold;">1,300</span></td><td><span style="color: #F59E0B; font-weight: bold;">$10,000</span></td></tr>
                    </tbody>
                </table>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # AI Response card
    st.markdown('<div style="background: #15161A; border: 1px solid #23242A; border-left: 3px solid #00A67E; border-radius: 12px; padding: 20px; margin-bottom: 20px;">', unsafe_allow_html=True)
    st.markdown("#### 🤖 ChatGPT Response")

    highlights = scenario_data["highlights"]
    response_text = scenario_data["response"]
    scen_id = scenario_data["id"]

    # Check if a highlight card was selected via query params and preserve response view
    if "selected_hl" in st.query_params:
        hl_param = st.query_params["selected_hl"]
        if hl_param in valid_hl_ids:
            st.session_state.selected_highlight_id = hl_param
            st.session_state.chat_sent = True
        else:
            st.session_state.selected_highlight_id = None

    # Render AI response and client-side toggleable explanation cards together inside components.html
    if st.session_state.lens_active:
        cards_html = ""
        safe_scen_id = re.sub(r'[^a-zA-Z0-9_-]', '', str(scen_id))

        for hl in highlights:
            safe_hl_id = re.sub(r'[^a-zA-Z0-9_-]', '', str(hl["id"]))
            unique_id = f"{safe_scen_id}_{safe_hl_id}"
            is_active_card = (st.session_state.get("selected_highlight_id") == unique_id)
            display_style = "block" if is_active_card else "none"

            badge_color = hl["badge_color"] if re.match(r'^#[0-9a-fA-F]{3,8}$', str(hl["badge_color"])) else "#00A67E"
            underline_color = hl["underline_color"] if re.match(r'^#[0-9a-fA-F]{3,8}$', str(hl["underline_color"])) else "#00A67E"

            hl_issue_type = html.escape(str(hl["issue_type"]))
            hl_confidence = html.escape(str(hl["confidence"]))
            hl_why_flagged = html.escape(str(hl["why_flagged"]))
            hl_what_assumes = html.escape(str(hl["what_assumes"]))
            hl_evidence_supports = html.escape(str(hl["evidence_supports"]))
            hl_evidence_missing = html.escape(str(hl["evidence_missing"]))
            hl_why_uncertain = html.escape(str(hl["why_uncertain"]))
            hl_what_could_change = html.escape(str(hl["what_could_change"]))

            sources = hl.get("sources", [])
            if sources:
                source_items_html = ""
                for s in sources:
                    s_title = html.escape(str(s["title"]))
                    s_url = html.escape(str(s["url"]), quote=True)
                    s_domain = html.escape(str(s["domain"]))
                    source_items_html += (
                        f'<li style="margin-bottom: 4px;">'
                        f'<a href="{s_url}" target="_blank" rel="noopener noreferrer" style="color: #60A5FA; text-decoration: underline; font-weight: 500;">{s_title}</a> '
                        f'<span style="color: #9CA3AF; font-size: 0.78rem;">({s_domain})</span>'
                        f'</li>'
                    )
                sources_section_html = (
                    f'<div style="font-size: 0.83rem; margin-top: 10px; padding-top: 10px; border-top: 1px solid #2D2E3A; line-height: 1.5;">'
                    f'<b style="color: #10B981; display: block; margin-bottom: 4px;">🔗 Verified Sources & Citations:</b>'
                    f'<ul style="margin: 0 0 0 18px; padding: 0; color: #D1D5DB;">{source_items_html}</ul>'
                    f'</div>'
                )
            else:
                sources_section_html = (
                    f'<div style="font-size: 0.83rem; color: #7E7F8F; margin-top: 10px; padding-top: 10px; border-top: 1px solid #2D2E3A; line-height: 1.5;">'
                    f'<b style="color: #7E7F8F;">🔗 Sources & Evidence:</b> No external primary source required; evaluated directly against internal prompt data / code logic.'
                    f'</div>'
                )

            card_html = (
                f'<div id="card-{unique_id}" class="reasoning-lens-explanation-card" '
                f'style="display: {display_style}; background: #1C1D24; border: 1.5px solid {underline_color}; '
                f'border-radius: 10px; padding: 16px 20px; margin-top: 10px; margin-bottom: 18px; box-shadow: 0 4px 16px rgba(0,0,0,0.6);">'
                f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">'
                f'<span style="background-color: {badge_color}; color: #111827; font-size: 0.75rem; font-weight: 700; padding: 4px 12px; border-radius: 12px; text-transform: uppercase; letter-spacing: 0.5px;">{hl_issue_type}</span>'
                f'<span style="font-size: 0.8rem; color: #7E7F8F;">Confidence: <b style="color: #ECECF1;">{hl_confidence}</b></span>'
                f'</div>'
                f'<div style="font-weight: 600; font-size: 0.95rem; color: #FFFFFF; margin-bottom: 10px;"><b style="color: #F59E0B;">Why is this flagged?</b><br>{hl_why_flagged}</div>'
                f'<div style="font-size: 0.85rem; color: #D1D5DB; margin-bottom: 6px; line-height: 1.5;"><b style="color: #7E7F8F;">What the claim assumes:</b> {hl_what_assumes}</div>'
                f'<div style="font-size: 0.85rem; color: #D1D5DB; margin-bottom: 6px; line-height: 1.5;"><b style="color: #7E7F8F;">What evidence supports it:</b> {hl_evidence_supports}</div>'
                f'<div style="font-size: 0.85rem; color: #D1D5DB; margin-bottom: 6px; line-height: 1.5;"><b style="color: #7E7F8F;">What evidence is missing:</b> {hl_evidence_missing}</div>'
                f'<div style="font-size: 0.85rem; color: #D1D5DB; margin-bottom: 6px; line-height: 1.5;"><b style="color: #7E7F8F;">Why ChatGPT is uncertain:</b> {hl_why_uncertain}</div>'
                f'<div style="font-size: 0.85rem; color: #D1D5DB; margin-bottom: 6px; line-height: 1.5;"><b style="color: #7E7F8F;">What would change the conclusion:</b> {hl_what_could_change}</div>'
                f'{sources_section_html}'
                f'</div>'
            )
            cards_html += card_html

        sorted_highlights = sorted(enumerate(highlights), key=lambda x: len(x[1]["text"]), reverse=True)
        placeholder_map = {}
        escaped_response_text = html.escape(response_text)
        annotated_html = escaped_response_text

        for idx, hl in sorted_highlights:
            ph = f"___HL_PH_{idx}___"
            escaped_hl_text = html.escape(hl["text"])
            placeholder_map[ph] = (hl, escaped_hl_text)
            annotated_html = annotated_html.replace(escaped_hl_text, ph)

        for ph, (hl, escaped_hl_text) in placeholder_map.items():
            safe_hl_id = re.sub(r'[^a-zA-Z0-9_-]', '', str(hl["id"]))
            unique_id = f"{safe_scen_id}_{safe_hl_id}"
            underline_color = hl["underline_color"] if re.match(r'^#[0-9a-fA-F]{3,8}$', str(hl["underline_color"])) else "#00A67E"
            border_style = f"border-bottom: 3px dashed {underline_color};"
            js_toggle = (
                f"event.preventDefault(); "
                f"var target = document.getElementById('card-{unique_id}'); "
                f"var wrapper = document.getElementById('lens-cards-wrapper'); "
                f"if (target) {{ "
                f"  var isVis = (target.style.display === 'block'); "
                f"  if (wrapper) {{ "
                f"    var cards = wrapper.querySelectorAll('.reasoning-lens-explanation-card'); "
                f"    for (var i = 0; i < cards.length; i++) {{ cards[i].style.display = 'none'; }} "
                f"  }} "
                f"  target.style.display = isVis ? 'none' : 'block'; "
                f"  if (!isVis && target.scrollIntoView) {{ target.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }}); }} "
                f"  var newUrl = isVis ? window.parent.location.pathname : window.parent.location.pathname + '?selected_hl={unique_id}'; "
                f"  try {{ window.parent.history.replaceState(null, '', newUrl); }} catch(e) {{}} "
                f"}}"
            )
            escaped_js_toggle = html.escape(js_toggle, quote=True)
            hl_span = f'<a href="javascript:void(0);" onclick="{escaped_js_toggle}" class="lens-highlight-clickable" style="text-decoration: none; color: inherit; {border_style} padding: 1px 4px; border-radius: 2px; cursor: pointer; display: inline;" title="Click to reveal explanation">{escaped_hl_text}</a>'
            annotated_html = annotated_html.replace(ph, hl_span)

        component_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background-color: transparent;
                    color: #ECECF1;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                }}
                .lens-highlight-clickable:hover {{
                    background-color: rgba(255, 255, 255, 0.1) !important;
                }}
            </style>
        </head>
        <body>
            <div id="lens-cards-wrapper">{cards_html}</div>
            <div style="margin-top: 10px; line-height: 1.7; font-size: 0.95rem; color: #ECECF1; white-space: pre-wrap;">{annotated_html}</div>
        </body>
        </html>
        """
        components.html(component_html, height=450, scrolling=True)
    else:
        if scenario_data["id"] == "code_gen":
            parts = response_text.split("\n\nThis function")
            st.code(parts[0], language="python")
            if len(parts) > 1:
                st.markdown(f"This function{parts[1]}")
        else:
            st.markdown(response_text)

    st.markdown('</div>', unsafe_allow_html=True)

    # Bottom Composer Container in Response View (Empty after sending)
    st.markdown('<div class="composer-card-container">', unsafe_allow_html=True)
    if "bottom_composer_field" not in st.session_state:
        st.session_state["bottom_composer_field"] = ""
    
    composer_text = st.text_area(
        "Composer",
        value=st.session_state.get("bottom_composer_field", ""),
        height=100,
        key="bottom_composer_field",
        label_visibility="collapsed"
    )
    st.session_state.composer_text = composer_text

    r_col1, r_col2, r_col3 = st.columns([1, 8, 2.2])
    with r_col1:
        st.button("➕", key="bottom_plus_btn", help="New Chat", on_click=reset_to_new_chat)
    with r_col3:
        r_col_mic, r_col_send = st.columns([1, 1])
        with r_col_mic:
            st.markdown('<div style="padding-top: 6px; text-align: right;"><span style="font-size: 1.2rem; color: #7E7F8F; cursor: pointer;">🎙️</span></div>', unsafe_allow_html=True)
        with r_col_send:
            if st.button("➔", key="bottom_send_btn"):
                st.session_state.chat_sent = True
                st.session_state.last_sent_prompt = st.session_state.composer_text
                st.session_state.composer_text = ""
                st.session_state["bottom_composer_field"] = ""
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; color: #565869; font-size: 0.75rem; margin-top: 8px;">
        ChatGPT can make mistakes. Reasoning Lens highlights underlying logical consistency.
    </div>
    """, unsafe_allow_html=True)
