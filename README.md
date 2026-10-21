<div align="center">

# 🌱 HabitPulse

### An intelligent habit and wellness companion with a virtual pet mascot, long-term memory, and dynamic visual rewards.

Built with **Google ADK**, **Gemini 3.8 Flash**, **Vertex AI Memory Bank**, **Firestore**, **Cloud Storage**, and **A2UI**.

</div>

---

## 📖 Overview

**HabitPulse** transforms daily habit tracking into an engaging, conversational, and rewarding experience. Instead of static checklists, users interact with **Sprout**, a cheerful wellness companion that remembers personal routines across sessions, tracks habit completions and streaks in Firestore, celebrates milestones with generated 3D badges uploaded to Cloud Storage, and returns rich A2UI cards.

---

## 🚀 Key Features & Integrated Services

### 🧠 1. Agent Brain & Cross-Session Memory
- **Model**: `gemini-3.8-flash` via the Google Agent Development Kit (ADK).
- **Vertex AI Memory Bank**: Retains user preferences, wake/sleep habits, wellness goals, and historical context across multiple sessions using `PreloadMemoryTool` and automatic post-turn memory callbacks (`generate_memories_callback`).

### 🗄️ 2. Persistent Habit & Progress Tracking (Firestore)
- **Active Habit Tracking**: Lists active habits, daily targets, and categories (`list_habits`, `add_habit`).
- **Streak & XP Calculation**: Idempotent habit completion logs that increment streaks, award XP, and update the virtual mascot’s mood in real-time (`log_habit_completion`).
- **User Profile & Status**: Tracks overall level, accumulated XP, and current companion emotional state (`get_user_status`).
- **Achievement Showcase**: Retrieves unlocked badges and milestones (`get_rewards_and_achievements`).

### 🎨 3. Mascot & Badge Generation (Nano Banana / Imagen + Cloud Storage)
- **Image Generation**: Uses `gemini-3.1-flash-lite-image` to generate 3D clay pastel-style mascot poses and collectible achievement badges (`generate_item_image`).
- **Google Cloud Storage**: Uploads generated images to a public Cloud Storage bucket for persistent asset delivery and fast inline rendering.

### 🖼️ 4. Rich A2UI v0.8 Interface
- Emits structured A2UI surfaces (`Card`, `Column`, `Row`, `Text`, `Image`) directly to frontend clients using `BasicCatalog` and `DirectJsonPromptGenerator` with custom streaming callbacks.

### ⚡ 5. Sandboxed Code Execution
- Integrated `AgentEngineSandboxCodeExecutor` for executing dynamic calculations and habit progress trends in a secure cloud environment.

### ☀️ 6. Daily Motivational Wisdom
- Live integration with the ZenQuotes public API (`get_daily_inspiration_quote`) to provide uplifting quotes tailored to current habits.

---

## 🛠️ ADK Function Tools Summary

| Tool Name | Service / Backend | Description |
|---|---|---|
| `PreloadMemoryTool` | Vertex AI Memory Bank | Loads relevant long-term memories and user facts into context at session start. |
| `list_habits` | Cloud Firestore | Retrieves all active habits, targets, and streaks. |
| `add_habit` | Cloud Firestore | Creates and configures a new habit entry in Firestore. |
| `log_habit_completion` | Cloud Firestore | Marks a habit completed for today, updates streaks, and awards XP. |
| `get_user_status` | Cloud Firestore | Fetches XP, level, and Sprout's emotional state. |
| `get_rewards_and_achievements` | Cloud Firestore | Lists available and unlocked milestone badges. |
| `generate_item_image` | Gemini Image Gen + Cloud Storage | Generates 3D mascot/badge graphics and uploads them to GCS. |
| `get_daily_inspiration_quote` | ZenQuotes API | Fetches daily motivational quotes. |

---

## 🔮 Roadmap (Planned, Not Yet Implemented)

- [ ] **Coin Economy & Accessory Wardrobe**: Virtual coin shop to equip accessories and cosmetics on Sprout.
- [ ] **Multi-stage Mascot Evolution**: Visual progression stages as cumulative XP reaches high tiers.
- [ ] **Automated Push Reminders**: Scheduled Cloud Run / Cloud Scheduler cron reminders for daily routines.

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
│   │   ├── main.py                # A2A FastAPI proxy server
│   │   ├── requirements.txt       # Frontend dependencies
│   │   └── static/
│   │       └── index.html         # Web UI with glassmorphism dashboard & A2UI renderer
│   ├── deployment/                # Terraform deployment definitions
│   ├── pyproject.toml             # Python dependencies
│   └── agents-cli-manifest.yaml   # Agent Runtime configuration
├── project_brief.md               # Original project brief & design specs
└── README.md                      # Project documentation
```

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
To run the interactive web dashboard:
```bash
cd habit-pulse/frontend
pip install -r requirements.txt
export AGENT_ENGINE_RESOURCE_NAME="projects/<PROJECT_ID>/locations/<LOCATION>/reasoningEngines/<REASONING_ENGINE_ID>"
export AGENT_DIRECTORY="app"
python main.py
```
Open your web browser and navigate to the local address output by the server (typically `127.0.0.1:8080`).

---

## 📜 License
Distributed under the Apache 2.0 License.
