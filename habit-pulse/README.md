<div align="center">

# 🌱 HabitPulse

### An intelligent habit and wellness companion with a virtual pet mascot, long-term memory, dynamic visual rewards, and live A2UI surfaces.

[![Live Demo](https://img.shields.io/badge/Demo-Live%20on%20Cloud%20Run-brightgreen?style=for-the-badge&logo=googlecloud)](https://habit-pulse-frontend-1022414314284.us-east1.run.app)
[![ADK](https://img.shields.io/badge/ADK-v1.4.0-blue?style=for-the-badge)](https://github.com/google/agent-development-kit)
[![Model](https://img.shields.io/badge/Gemini-3.8%20Flash-orange?style=for-the-badge&logo=google)](https://cloud.google.com/vertex-ai)

**🌐 Live Service URL:** [https://habit-pulse-frontend-1022414314284.us-east1.run.app](https://habit-pulse-frontend-1022414314284.us-east1.run.app)

<br/>

<img src="../assets/demo.gif" alt="HabitPulse Interactive Demo" width="85%" style="border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.12);" />

</div>

---

## 📖 Overview

**HabitPulse** transforms daily habit tracking into an engaging, conversational, and rewarding experience. Users interact with **Sprout**, a cheerful wellness companion that remembers personal routines across sessions, tracks habit completions and streaks in Firestore, celebrates milestones with generated 3D badges uploaded to Cloud Storage, and returns rich A2UI cards.

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

## ☁️ Cloud Run Deployment

The web frontend is deployed to **Google Cloud Run**:
- **Service**: `habit-pulse-frontend`
- **Region**: `us-east1`
- **Live Endpoint**: [https://habit-pulse-frontend-1022414314284.us-east1.run.app](https://habit-pulse-frontend-1022414314284.us-east1.run.app)
- **Backend Reason Engine Resource**: `projects/1022414314284/locations/us-east1/reasoningEngines/7204328939165057024`

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
uv sync
uv run adk web app
```

### 2. Run the Custom Frontend (FastAPI Proxy)
To run the interactive web dashboard:
```bash
cd frontend
pip install -r requirements.txt
export AGENT_ENGINE_RESOURCE_NAME="projects/1022414314284/locations/us-east1/reasoningEngines/7204328939165057024"
export AGENT_DIRECTORY="app"
python main.py
```
Open your web browser and navigate to `http://localhost:8080`.

---

## 📜 License
Distributed under the Apache 2.0 License.
