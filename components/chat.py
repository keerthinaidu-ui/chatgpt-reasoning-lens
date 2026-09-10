import streamlit as st
import html
from components.issue_card import render_issue_card

def render_chat_area(scenario_data):
    """Renders user message, user data/code, AI response card, Lens toggle, and subtle interactive underlines."""
    
    # Header title
    st.markdown(f"## {scenario_data['title']}")

    # Conversation Scrollable Area
    # 1. User Message Display
    st.markdown('<div class="user-msg-container">', unsafe_allow_html=True)
    st.markdown(f"**User:** {scenario_data['prompt']}")
    
    # Display User Provided Data/Code if present
    if scenario_data.get("user_data"):
        st.markdown("**Provided Data / Code:**")
        if scenario_data["id"] == "code_gen":
            st.code(scenario_data["user_data"], language="python")
        else:
            st.code(scenario_data["user_data"], language="text")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # 2. AI Response Card Container
    st.markdown('<div class="ai-msg-container">', unsafe_allow_html=True)
    
    # Lens Toggle Header
    t_col1, t_col2 = st.columns([3, 1])
    with t_col1:
        st.markdown("#### 🤖 ChatGPT Response")
    with t_col2:
        lens_on = st.toggle(
            "🔎 Reasoning Lens",
            value=st.session_state.get("lens_active", True),
            key="lens_toggle_widget"
        )
        st.session_state.lens_active = lens_on

    st.markdown("<br>", unsafe_allow_html=True)

    highlights = scenario_data["highlights"]
    response_text = scenario_data["response"]

    # When Reasoning Lens is OFF: render clean text with NO highlights or issue details
    if not st.session_state.lens_active:
        if scenario_data["id"] == "code_gen":
            # Split code snippet and text explanation for code scenario
            parts = response_text.split("\n\nThis function")
            st.code(parts[0], language="python")
            if len(parts) > 1:
                st.markdown(f"This function{parts[1]}")
        else:
            st.markdown(response_text)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # When Reasoning Lens is ON:
    # Build annotated HTML with ONLY subtle colored underlines underneath the text/code.
    # No issue labels, no trust scores, no warning badges, no separate lists beside the text.
    
    annotated_html = response_text
    
    # For code scenario, format code vs text nicely while preserving underlines
    for hl in highlights:
        is_active = (st.session_state.get("selected_highlight_id") == hl["id"])
        
        # Subtle colored underline style: transparent background, colored bottom border / text-decoration
        border_style = f"background-color: transparent; border-bottom: 3px dashed {hl['underline_color']}; text-decoration: none;" if not is_active else f"background-color: rgba(255,255,255,0.1); border-bottom: 3px solid {hl['underline_color']}; text-decoration: none;"
        
        # Clickable inline button link via query param or button selector
        hl_markup = f'<span class="hl-underline" style="{border_style} padding: 1px 3px; cursor: pointer; border-radius: 2px;">{html.escape(hl["text"])}</span>'
        
        annotated_html = annotated_html.replace(hl["text"], hl_markup)

    if scenario_data["id"] == "code_gen":
        # Separate the Python function block and narrative text
        lines = annotated_html.split("\n\n")
        st.markdown(f"```python\n{lines[0]}\n```", unsafe_allow_html=True)
        if len(lines) > 1:
            st.markdown(f"<div style='line-height: 1.8; margin-top: 10px;'>{lines[1]}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='line-height: 1.8; margin-top: 10px;'>{annotated_html}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Interactive Underline Selector Controls (Subtle & Contextual)
    st.caption("👇 *Click a phrase below to inspect its Reasoning Lens annotation:*")
    hl_cols = st.columns(len(highlights))
    for idx, hl in enumerate(highlights):
        with hl_cols[idx]:
            is_active = (st.session_state.get("selected_highlight_id") == hl["id"])
            btn_label = f"{'▶ ' if is_active else ''}\"{hl['text'][:20]}...\""
            if st.button(btn_label, key=f"hl_btn_{hl['id']}", use_container_width=True):
                if is_active:
                    st.session_state.selected_highlight_id = None
                else:
                    st.session_state.selected_highlight_id = hl["id"]
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Contextual Explanation Card (Appears directly below AI response inside conversation)
    current_hl_id = st.session_state.get("selected_highlight_id")
    if current_hl_id:
        active_hl_data = next((h for h in highlights if h["id"] == current_hl_id), None)
        if active_hl_data:
            render_issue_card(active_hl_data)

    # 4. Bottom Composer Input Bar (Maintains ChatGPT Layout)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.text_input("Send a message...", value="", placeholder="Send a message to ChatGPT...", disabled=True, key="bottom_composer")

