<div align="center">

<img src="assets/mascot.svg" alt="Sprout Mascot" width="110" />

# HabitPulse

### An intelligent habit and wellness companion with a virtual pet mascot, long-term memory, dynamic visual rewards, and live A2UI surfaces.

[![Live Demo](https://img.shields.io/badge/Demo-Live%20on%20Cloud%20Run-brightgreen?style=for-the-badge&logo=googlecloud)](https://habit-pulse-frontend-1022414314284.us-east1.run.app)
[![ADK](https://img.shields.io/badge/ADK-v1.4.0-blue?style=for-the-badge)](https://github.com/google/agent-development-kit)
[![Model](https://img.shields.io/badge/Gemini-3.8%20Flash-orange?style=for-the-badge&logo=google)](https://cloud.google.com/vertex-ai)

**🌐 Live Web Application:** [https://habit-pulse-frontend-1022414314284.us-east1.run.app](https://habit-pulse-frontend-1022414314284.us-east1.run.app)

<br/>

<img src="assets/demo.gif" alt="HabitPulse Interactive Demo" width="85%" style="border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.12);" />

</div>

---

## 📖 Overview

**HabitPulse** transforms daily habit tracking into an engaging, conversational, and rewarding experience. Instead of static spreadsheets or rigid checklists, users nurture and interact with **Sprout**, a cheerful wellness companion that:
- Remembers personal routines and wellness goals across sessions via **Vertex AI Memory Bank**.
- Tracks habit completions, XP gains, and daily streaks in **Cloud Firestore**.
- Generates collectible 3D pastel milestone badges and celebrates achievements via **Gemini Image Gen & Cloud Storage**.
- Dynamically renders interactive **A2UI v0.8 cards** and companion mood states in a responsive web frontend.

---

## 🚀 Key Features & Integrated Services

### 🧠 1. Agent Brain & Cross-Session Memory
- **Model**: `gemini-3.8-flash` powered by the Google Agent Development Kit (ADK).
- **Vertex AI Memory Bank**: Retains personal preferences, wake/sleep schedules, wellness targets, and past conversations across sessions using `PreloadMemoryTool` and automatic post-turn memory callbacks (`generate_memories_callback`).

### 🗄️ 2. Persistent Habit & Progress Tracking (Firestore)
- **Active Habit Management**: Lists habits, daily targets, and categories (`list_habits`, `add_habit`).
- **Streak & XP Calculation**: Idempotent habit completion logs that increment streaks, award XP, and update Sprout's emotional state in real time (`log_habit_completion`).
- **User Profile & Status**: Tracks overall level, accumulated XP, and current companion mood (`get_user_status`).
- **Achievement Showcase**: Retrieves unlocked badges and milestones (`get_rewards_and_achievements`).

### 🎨 3. Mascot & Badge Generation (Nano Banana / Imagen + Cloud Storage)
- **Image Generation**: Uses `gemini-3.1-flash-lite-image` to generate 3D clay pastel-style mascot poses and collectible achievement badges (`generate_item_image`).
- **Google Cloud Storage**: Uploads generated images to a public Cloud Storage bucket for persistent asset delivery and fast inline rendering.

### 🖼️ 4. Rich A2UI v0.8 Interface & Web Dashboard
- **Glassmorphism UI**: High-fidelity dashboard featuring responsive habit suggestions, floating Sprout animations, and native SVG favicon support.
- **A2UI mini-renderer**: Emits structured A2UI surfaces (`Card`, `Column`, `Row`, `Text`, `Image`) directly to frontend clients using `BasicCatalog` and `DirectJsonPromptGenerator`.

### ⚡ 5. Sandboxed Code Execution
- Integrated `AgentEngineSandboxCodeExecutor` for executing dynamic calculations and habit progress trends in a secure cloud environment.

### ☀️ 6. Daily Motivational Wisdom
- Live integration with the ZenQuotes public API (`get_daily_inspiration_quote`) to provide uplifting quotes tailored to current habits.

---

## 🛠️ ADK Function Tools Summary

| Tool Name | Backend Service | Description |
|---|---|---|
| `PreloadMemoryTool` | Vertex AI Memory Bank | Loads relevant long-term memories and user facts into context at session start. |
| `list_habits` | Cloud Firestore | Retrieves all active habits, targets, and streaks. |
| `add_habit` | Cloud Firestore | Creates and configures a new habit entry in Firestore. |
| `log_habit_completion` | Cloud Firestore | Marks a habit completed for today, updates streaks, and awards XP. |
| `get_user_status` | Cloud Firestore | Fetches XP, level, and Sprout's emotional state. |
| `get_rewards_and_achievements` | Cloud Firestore | Lists available and unlocked milestone badges. |
| `generate_item_image` | Gemini Image Gen + GCS | Generates 3D mascot/badge graphics and uploads them to GCS. |
| `get_daily_inspiration_quote` | ZenQuotes API | Fetches daily motivational quotes. |

---

## 🏗️ Architecture & Project Structure

```
.
├── habit-pulse/
│   ├── app/
│   │   ├── agent.py               # Main ADK agent definition, tools, memory, and A2UI setup
│   │   ├── a2ui_utils.py          # A2UI callback and catalog serializer
│   │   ├── fast_api_app.py        # Backend FastAPI server
│   │   └── app_utils/             # A2A and Reasoning Engine adapters
│   ├── frontend/
│   │   ├── Dockerfile             # Container configuration for Cloud Run
│   │   ├── main.py                # A2A FastAPI proxy server
│   │   ├── requirements.txt       # Frontend dependencies
│   │   └── static/
│   │       ├── favicon.svg        # Cute Sprout vector favicon
│   │       ├── mascot.svg         # High-resolution Sprout companion vector asset
│   │       └── index.html         # Web UI with glassmorphism dashboard & A2UI renderer
│   ├── deployment/                # Terraform deployment definitions
│   ├── pyproject.toml             # Python dependencies
│   └── agents-cli-manifest.yaml   # Agent Runtime configuration
├── project_brief.md               # Product design specifications & gamification roadmap
└── README.md                      # Comprehensive project documentation
```

---

## ☁️ Cloud Run Deployment & Live Architecture

The web frontend is deployed to **Google Cloud Run** and acts as a lightweight, secure proxy communicating with the **Vertex AI Reasoning Engine** over the **Agent-to-Agent (A2A)** protocol:

```
[ Browser UI ]
      │ (HTTPS / WebSocket)
      ▼
[ Cloud Run Frontend Proxy ] (FastAPI + ADC Auth)
      │ (A2A Protocol / JSON-RPC)
      ▼
[ Vertex AI Agent Engine ] (Gemini 3.8 Flash + Firestore + Memory Bank)
```

- **Cloud Run URL**: `https://habit-pulse-frontend-1022414314284.us-east1.run.app`
- **Region**: `us-east1`
- **Security**: The browser communicates only with the proxy (no leaked cloud credentials or CORS issues). The proxy authenticates via Application Default Credentials (ADC) with `roles/aiplatform.user`.

---

## 💻 Local Setup & Running Instructions

### Prerequisites
- Python 3.11+
- `uv` package manager (`pip install uv` or via [Astral](https://docs.astral.sh/uv/))
- Google Cloud SDK (`gcloud`) authenticated with Application Default Credentials:
  ```bash
  gcloud auth application-default login
  ```

### 1. Run the Agent Locally (ADK Web Dev UI)
Navigate into the agent directory and launch the ADK development server:
```bash
cd habit-pulse
uv sync
uv run adk web app
```

### 2. Run the Custom Frontend (FastAPI Proxy)
To run the interactive web dashboard locally:
```bash
cd habit-pulse/frontend
pip install -r requirements.txt
export AGENT_ENGINE_RESOURCE_NAME="projects/1022414314284/locations/us-east1/reasoningEngines/7204328939165057024"
export AGENT_DIRECTORY="app"
python main.py
```
Open your web browser and navigate to `http://localhost:8080`.

---

## 📜 License
Distributed under the Apache 2.0 License.
