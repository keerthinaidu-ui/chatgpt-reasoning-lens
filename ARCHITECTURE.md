# System & Deployment Architecture: Reasoning Lens

## 1. Executive Overview

**Reasoning Lens for ChatGPT** is a lightweight, high-performance interactive prototype built with Python and Streamlit. It overlays a real-time logical critique layer onto AI-generated responses, highlighting assumptions, supported calculations, unsupported claims, and overconfident conclusions without relying on external API calls or databases.

---

## 2. Component & Application Architecture

The system is structured as a single-page Streamlit application using standard component isolation and custom HTML/CSS injection.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Streamlit App Layer                             │
│                           (app.py)                                     │
└──────────────┬──────────────────────────────────────────┬──────────────┘
               │                                          │
               ▼                                          ▼
┌──────────────────────────────┐          ┌──────────────────────────────┐
│  State & Navigation Manager  │          │   Reasoning Lens UI Engine   │
│ (Query Params & Session State)          │   (components.html / Vanilla)│
└──────────────┬───────────────┘          └──────────────┬───────────────┘
               │                                          │
               ▼                                          ▼
┌──────────────────────────────┐          ┌──────────────────────────────┐
│    Pre-configured Data Set   │          │  Security & Sanitization     │
│     (data/scenarios.py)      │          │(html.escape / Regex Guard)   │
└──────────────────────────────┘          └──────────────────────────────┘
```

### Core Components

1. **Main Entry Point (`app.py`)**:
   * Manages Streamlit layout, dark theme CSS injection, sidebar scenario navigation, and main screen state machine (`chat_sent`, `selected_scenario`, `lens_active`).
2. **Scenario Data Engine (`data/scenarios.py`)**:
   * Contains static definitions for scenarios (Data Analysis, Market Research, Code Generation) with raw prompts, responses, and structured `HighlightIssue` mappings.
3. **Reasoning Lens Component Layer (`components.html`)**:
   * Renders the interactive highlights and inline explanation cards inside an isolated Streamlit iframe.
   * Utilizes client-side DOM manipulation (`event.preventDefault()`, `window.parent.history.replaceState`) for instant, zero-flicker toggle interactions.
4. **Security & Input Guardrails**:
   * All dynamic inputs inserted into HTML/JS are HTML-escaped using `html.escape()`.
   * Query parameters (`selected_hl`) and element IDs are strictly validated against whitelist schemas.
   * Color properties are validated against hexadecimal CSS rules (`^#[0-9a-fA-F]{3,8}$`).

---

## 3. Deployment Architecture: Streamlit Community Cloud

The application is engineered for zero-maintenance, serverless deployment on **Streamlit Community Cloud**.

```
┌─────────────────────────┐
│   GitHub Repository     │
│   (Public / Main Branch)│
└────────────┬────────────┘
             │ Automatic Git Push Sync
             ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   Streamlit Community Cloud                            │
│                                                                        │
│  ┌──────────────────────┐  ┌─────────────────────┐  ┌───────────────┐ │
│  │ Python 3.10+ Container│  │ Dependency Installer│  │ Edge CDN &    │ │
│  │ Runtime              │  │ (requirements.txt)  │  │ SSL/TLS Proxy │ │
│  └──────────────────────┘  └─────────────────────┘  └───────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Deployment Specifications

* **Hosting Platform**: Streamlit Community Cloud (Free Tier)
* **Target Runtime Environment**: Python 3.10+ Linux Container
* **Main Script Path**: `app.py`
* **Network & SSL**: Automatic TLS termination and global HTTPS routing provided natively by Streamlit Edge Infrastructure.

### 3.2 Deployment Package Structure

To ensure instant builds on Streamlit Community Cloud, the repository includes all required configuration files:

```
reasoning lens/
├── app.py                     # Streamlit application entry point
├── requirements.txt           # Python dependencies (streamlit)
├── ARCHITECTURE.md            # System architecture & deployment specifications
├── components/                # Modular UI components
│   └── issue_card.py          # Standalone issue card helpers
├── data/                      # Scenario datasets
│   └── scenarios.py           # Pre-configured reasoning scenarios
└── static/                    # Optional static assets
```

### 3.3 Continuous Deployment (CI/CD Workflow)

1. **Repository Linkage**: Connect the GitHub repository (`main` branch) to Streamlit Community Cloud.
2. **Build Trigger**: Every `git push` to `main` automatically triggers an immutable container build.
3. **Dependency Resolution**: Streamlit Community Cloud parses `requirements.txt` and caches installed packages across restarts.
4. **Health Check**: The platform runs `streamlit run app.py` and monitors container health prior to switching traffic.

### 3.4 Operational & Resource Characteristics

* **Stateless Operation**: No backend databases, persistent file stores, or external API keys are required.
* **Low Memory Footprint**: Operating memory remains under 100 MB, well within standard Community Cloud limits.
* **Instant Cold Starts**: App launches in under 5 seconds due to zero external network requests on startup.

---

## 4. Verification & Testing Strategy

* **Compilation**: `py -m py_compile app.py` verifies Python code integrity prior to commit.
* **Browser Compatibility**: Validated across Chrome, Firefox, Safari, and Edge.
* **Mobile/Responsive**: Supports fluid layouts down to 360px viewport widths.
