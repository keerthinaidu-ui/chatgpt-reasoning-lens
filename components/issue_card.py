import html
import streamlit as st

def render_issue_card(highlight_data):
    """Renders the contextual explanation card for a selected underline."""
    if not highlight_data:
        return

    sources = highlight_data.get("sources", [])
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
        <div class="issue-label" style="color: #F59E0B; font-weight: 600; margin-bottom: 4px;">Why is this flagged?</div>
        <div class="issue-text" style="margin-bottom: 10px; color: #FFFFFF;">{highlight_data['why_flagged']}</div>
        
        <div class="issue-label" style="color: #7E7F8F; font-weight: 600;">What the claim assumes</div>
        <div class="issue-text" style="margin-bottom: 8px;">{highlight_data['what_assumes']}</div>
        
        <div class="issue-label" style="color: #7E7F8F; font-weight: 600;">What evidence supports it</div>
        <div class="issue-text" style="margin-bottom: 8px;">{highlight_data['evidence_supports']}</div>

        <div class="issue-label" style="color: #7E7F8F; font-weight: 600;">What evidence is missing</div>
        <div class="issue-text" style="margin-bottom: 8px;">{highlight_data['evidence_missing']}</div>

        <div class="issue-label" style="color: #7E7F8F; font-weight: 600;">Why ChatGPT is uncertain</div>
        <div class="issue-text" style="margin-bottom: 8px;">{highlight_data['why_uncertain']}</div>

        <div class="issue-label" style="color: #7E7F8F; font-weight: 600;">What would change the conclusion</div>
        <div class="issue-text" style="margin-bottom: 8px;">{highlight_data['what_could_change']}</div>

        {sources_section_html}
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("❌ Close Explanation", key="close_issue_btn"):
        st.session_state.selected_highlight_id = None
        st.rerun()

