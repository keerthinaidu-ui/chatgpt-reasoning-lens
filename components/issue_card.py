import streamlit as st

def render_issue_card(highlight_data):
    """Renders the contextual explanation card for a selected underline."""
    if not highlight_data:
        return

    st.markdown(f"""
    <div class="issue-card" style="border-left: 4px solid {highlight_data['underline_color']};">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span class="issue-type-badge" style="background-color: {highlight_data['badge_color']};">
                {highlight_data['issue_type']}
            </span>
            <span class="confidence-pill">Confidence: {highlight_data['confidence']}</span>
        </div>
        <div style="font-style: italic; color: #D1D5DB; font-size: 0.9rem; margin-bottom: 14px; padding: 8px 12px; background: rgba(255,255,255,0.05); border-radius: 6px;">
            "{highlight_data['text']}"
        </div>
        <div class="issue-label">Issue</div>
        <div class="issue-text">{highlight_data['issue']}</div>
        
        <div class="issue-label">Why It Matters</div>
        <div class="issue-text">{highlight_data['why_it_matters']}</div>
        
        <div class="issue-label">What to Check</div>
        <div class="issue-text">{highlight_data['what_to_check']}</div>
        
        <div class="issue-label">What Could Change the Conclusion</div>
        <div class="issue-text">{highlight_data['what_could_change']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("❌ Close Explanation", key="close_issue_btn"):
        st.session_state.selected_highlight_id = None
        st.rerun()

