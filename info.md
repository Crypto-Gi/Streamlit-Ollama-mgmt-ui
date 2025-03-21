Dashboard App (Streamlit-based)
┌───────────────────────────────────────────────────────────┐
│                                                           │
│  ┌───────────────────┐     ┌───────────────────────┐      │
│  │   Configuration   │     │    API Interaction    │      │
│  │   (User Input)    │───► │    (Ollama Server)    │      │
│  └───────────────────┘     └───────────┬───────────┘      │
│                                        │                  │
│  ┌───────────────────┐                 │                  │
│  │     Dashboard     │<──────────────────┘                │
│  │ (Elegant UI, Dark │                                    │
│  │ Mode, Apple Style)│                                    │
│  └───────────────────┘                                    │
│                                                           │
└───────────────────────────────────────────────────────────┘
                             │
                             │ HTTP Requests
                             ▼
                 Ollama REST API (Remote Host)
┌───────────────────────────────────────────────────────────┐
│                                                           │
│         /api/show, /api/tags, /api/delete, etc.           │
│                                                           │
└───────────────────────────────────────────────────────────┘
(Hosted externally, address provided by user)

---

## Dashboard Architecture

### User Input Configuration Page
- **Ollama Server Configuration:**
  - Input for `Server IP`
  - Input for `Port`
  - Button to test API connectivity
- **Authentication (Optional):**
  - (Future-proof placeholder for API key or authentication tokens if implemented later)

---

### API Interaction Module
- Utilizes `requests` library for API interactions with Ollama REST endpoints.
- Functions wrapped in reusable Streamlit functions with validation scripts.

API Interaction encapsulates all provided endpoints clearly structured into dedicated Python functions:

- `get_model_details(model_name)`
- `list_running_models()`
- `delete_model(model_name)`
- `pull_model(model_name, stream=True)`
- `get_version()`
- `load_model_into_vram(model_name, keep_alive)`
- `remove_model_from_vram(model_name)`

### Elegant Dashboard UI Sections (Apple-like Dark Mode UI)

**Navigation Sidebar:**
- Styled with subtle transparency, Apple-like rounded corners, subtle shadows.
- Navigation links:
  - Overview
  - Model Management
  - Model Interaction
  - Server Status & Settings

### Dashboard Page Layout
- Apple-inspired, minimalist design.
- Soft, rounded corners and shadowed UI components.
- Colors: Deep black, muted greys, soft gradients (blue-grey).
- Typography inspired by Apple’s SF Pro font.

### UI/UX Elements:
- Dark mode toggle button (enabled by default).
- Card-based layout (Streamlit cards with subtle shadow, rounded corners).
- Responsive design for mobile/tablet/desktop.

---

## Detailed Dashboard Sections & Functionality

### 1. Model Overview Dashboard
- Displays all models currently available/running.
- Details: Model name, size, tags, and metadata retrieved via API `/api/tags`.

### 2. Model Management Panel
- **Download New Model**
  - Drop-down selection or search box to choose models .
  - Status indicator (progress bar) for downloading (`POST /api/pull`).
- **Delete Model**
  - Confirmation pop-up before deleting a model (`DELETE /api/delete`).
- **Model Info**
  - Click on model name to fetch detailed metadata (`GET /api/show`).

### 3. Model Memory Management (VRAM Control)
- Buttons to Load or Unload models from VRAM (`POST /api/generate`):
  - Keep-alive timer configuration (`5m`, `10m`, `0` for immediate unload).

### 3. Server Information Card
- Displays current Ollama server version (`GET /api/version`).

### 4. Live Model Status Monitor
- Lists currently loaded models and active sessions (`GET /api/tags`).
- Refresh button for updating the list in real-time.

---

## Complete Streamlit Architecture (Framework Overview)

- **Frontend**: Streamlit App running on user host.
  - Reactively updates based on user inputs and API responses.
  - Real-time visual feedback.

- **Backend API Layer (Python Requests):**
  - Streamlit directly communicates to Ollama REST APIs via user-configured IP and Port.
  - Secure connection handling (TLS/HTTPS if required in the deployment scenario).

---

## Dashboard Tech Stack & Dependencies

- Python
- Streamlit
- Requests (Python library for HTTP)
- JSON manipulation and parsing (native Python)
- Optional (for enhanced aesthetics and interactions):  
  - CSS Injection (`streamlit.components.v1.html`) for advanced styling.
  - Streamlit Theme config (native dark theme customized).

---

## Complete Prompt for App Initialization:

```shell
pip install streamlit requests
