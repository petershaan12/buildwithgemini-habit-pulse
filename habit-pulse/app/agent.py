# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from typing import Any, Dict, List
import uuid
import requests
from google import genai
from google.cloud import firestore
from google.cloud import storage
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.code_executors import AgentEngineSandboxCodeExecutor
from google.adk.memory import VertexAiMemoryBankService
from google.adk.models import Gemini
from google.adk.tools import ToolContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from a2ui.core.basic_catalog.v0_8 import BasicCatalog
from a2ui.inference_formats.direct_json import DirectJsonPromptGenerator

from .a2ui_utils import a2ui_callback

MODEL = "gemini-3.8-flash"
IMAGE_MODEL = "gemini-3.1-flash-lite-image"
PROJECT_ID = "qwiklabs-gcp-03-e41827d1e1fe"
LOCATION = "us-east1"
BUCKET_NAME = "habit-pulse-assets-cehhg"
MEMORY_BANK_ID = "7204328939165057024"
AGENT_ENGINE_ID = f"projects/1022414314284/locations/{LOCATION}/reasoningEngines/{MEMORY_BANK_ID}"

# Lazy-loaded clients
_db = None
_storage_client = None
_genai_client = None


def get_db() -> firestore.Client:
    global _db
    if _db is None:
        _db = firestore.Client(project=PROJECT_ID)
    return _db


def get_storage_client() -> storage.Client:
    global _storage_client
    if _storage_client is None:
        _storage_client = storage.Client(project=PROJECT_ID)
    return _storage_client


def get_genai_client() -> genai.Client:
    global _genai_client
    if _genai_client is None:
        _genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    return _genai_client


def list_habits() -> List[Dict[str, Any]]:
    """Retrieves all active habits, their categories, targets, and current streak counts from Firestore.

    Returns:
        A list of dictionaries with habit details.
    """
    db = get_db()
    docs = db.collection("habits").stream()
    habits = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        habits.append(data)
    return habits


def add_habit(name: str, category: str, target: str) -> Dict[str, Any]:
    """Adds a new habit to the user's habit tracker in Firestore.

    Args:
        name: Name of the habit (e.g. 'Daily Meditation').
        category: Category (e.g. 'Mindfulness', 'Fitness', 'Hydration').
        target: Target frequency or quantity (e.g. '10 minutes', '2 Liters').

    Returns:
        A dictionary confirming the newly created habit.
    """
    db = get_db()
    habit_id = f"habit_{name.lower().replace(' ', '_')}"
    habit_data = {
        "id": habit_id,
        "name": name,
        "category": category,
        "target": target,
        "streak": 0,
        "completed_today": False,
        "xp_reward": 20,
    }
    db.collection("habits").document(habit_id).set(habit_data)
    return {"status": "success", "message": f"Habit '{name}' successfully created!", "habit": habit_data}


def log_habit_completion(habit_id: str) -> Dict[str, Any]:
    """Logs completion of a habit for today, updates its streak count, and awards XP.

    Args:
        habit_id: The ID of the habit (e.g. 'habit_water', 'habit_walk', 'habit_read').

    Returns:
        A dictionary confirming habit completion and updated streak.
    """
    db = get_db()
    habit_ref = db.collection("habits").document(habit_id)
    doc = habit_ref.get()
    if not doc.exists:
        return {"status": "error", "message": f"Habit '{habit_id}' not found."}

    data = doc.to_dict()
    new_streak = data.get("streak", 0) + 1
    habit_ref.update({
        "streak": new_streak,
        "completed_today": True,
        "last_completed": datetime.datetime.now(datetime.timezone.utc).isoformat()
    })

    # Update user XP
    user_ref = db.collection("users").document("default_user")
    user_doc = user_ref.get()
    xp_earned = data.get("xp_reward", 20)
    current_xp = 0
    if user_doc.exists:
        user_data = user_doc.to_dict()
        current_xp = user_data.get("xp", 0) + xp_earned
        user_ref.update({
            "xp": current_xp,
            "mascot_mood": "happy"
        })

    return {
        "status": "success",
        "habit_name": data.get("name"),
        "new_streak": new_streak,
        "xp_earned": xp_earned,
        "total_xp": current_xp,
        "mascot_mood": "happy"
    }


def get_user_status() -> Dict[str, Any]:
    """Fetches user profile, current level, XP, coins, and virtual mascot mood from Firestore.

    Returns:
        A dictionary with user profile and mascot status.
    """
    db = get_db()
    user_doc = db.collection("users").document("default_user").get()
    if not user_doc.exists:
        return {"status": "error", "message": "User not found."}
    return user_doc.to_dict()


def get_rewards_and_achievements() -> List[Dict[str, Any]]:
    """Retrieves all available and unlocked achievement badges from Firestore.

    Returns:
        A list of achievement badges and their unlocked status.
    """
    db = get_db()
    docs = db.collection("rewards").stream()
    rewards = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        rewards.append(data)
    return rewards


def get_daily_inspiration_quote() -> Dict[str, str]:
    """Fetches a free real-world motivational quote from the ZenQuotes public API to encourage the user and Sprout.

    Returns:
        A dictionary containing the motivational quote and author.
    """
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list):
                return {
                    "quote": data[0].get("q", "Keep taking small steps every day!"),
                    "author": data[0].get("a", "ZenQuotes")
                }
    except Exception:
        pass
    return {
        "quote": "Small daily habits lead to monumental long-term growth.",
        "author": "HabitPulse Wisdom"
    }


async def generate_item_image(item_description: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Generates an image for a habit milestone, badge, or mascot item using gemini-3.1-flash-lite-image in the global region.
    Saves the image artifact for the Playground UI and uploads it to public Cloud Storage.

    Args:
        item_description: Description of the mascot pose, habit milestone, or achievement badge to generate (e.g. 'A cute 3D clay sprout celebrating with golden stars').
        tool_context: ADK ToolContext to register the artifact in the dev UI / playground.

    Returns:
        A dictionary containing the public GCS image URL and artifact filename.
    """
    genai_client = get_genai_client()
    prompt = f"Cute 3D clay animation style, soft pastel colors, clean lighting, white background: {item_description}"
    
    response = genai_client.models.generate_content(
        model=IMAGE_MODEL,
        contents=prompt,
    )

    image_bytes = None
    mime_type = "image/jpeg"
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                image_bytes = part.inline_data.data
                mime_type = part.inline_data.mime_type or mime_type
                break

    if not image_bytes:
        return {"status": "error", "message": "Failed to generate image bytes."}

    # 1. Save artifact in ADK tool context for the Playground's Artifacts panel
    filename = f"mascot_{uuid.uuid4().hex[:8]}.jpg"
    artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    await tool_context.save_artifact(filename=filename, artifact=artifact_part)

    # 2. Upload bytes to public Cloud Storage bucket
    storage_client = get_storage_client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_string(image_bytes, content_type=mime_type)

    public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

    return {
        "status": "success",
        "filename": filename,
        "public_url": public_url,
        "description": item_description
    }


# WRITE callback: Send session turns to Memory Bank for extraction
async def generate_memories_callback(callback_context: CallbackContext):
    await callback_context.add_session_to_memory()
    return None


# Build A2UI v0.8 System Prompt using Basic Catalog
basic_catalog = BasicCatalog()
a2ui_prompt_gen = DirectJsonPromptGenerator(catalogs=[basic_catalog])

role_desc = (
    "You are HabitPulse, a supportive and cheerful habit-tracking companion. "
    "You help users build healthy habits, check off daily routines, celebrate streaks, "
    "calculate progress trends, and nurture their virtual pet mascot (Sprout). "
    "You remember user preferences, lifestyle routines, goals, and facts across sessions."
)

workflow_desc = "Analyze the request and return structured UI when appropriate."

ui_desc = (
    "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
    "Never nest a Card inside a Card. "
    "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
    "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
    "nothing in adk web). "
    "You may include one Image component, but only when you have a public https "
    "URL for the image (for example the URL an image tool returns after uploading "
    "to a public bucket). Set the Image url to that exact https link, for example "
    "{\"Image\": {\"url\": {\"literalString\": \"https://...\"}}}. Never point an "
    "Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
    "not have a public URL, add a short Text line noting the image instead. "
    "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
    "headings and emphasis. "
    "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
    "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
)

schema_instruction = a2ui_prompt_gen.generate_catalog_instructions()

instruction = f"""{role_desc}

{workflow_desc}

{ui_desc}

{schema_instruction}
"""

# Configure secure sandbox code execution from Agent Engine
sandbox_executor = AgentEngineSandboxCodeExecutor(
    agent_engine_resource_name=AGENT_ENGINE_ID
)

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction,
    tools=[
        PreloadMemoryTool(),
        list_habits,
        add_habit,
        log_habit_completion,
        get_user_status,
        get_rewards_and_achievements,
        get_daily_inspiration_quote,
        generate_item_image,
    ],
    code_executor=sandbox_executor,
    after_model_callback=a2ui_callback,
    after_agent_callback=generate_memories_callback,
)


def memory_service_builder():
    return VertexAiMemoryBankService(
        project=PROJECT_ID,
        location=LOCATION,
        agent_engine_id=MEMORY_BANK_ID,
    )


app = App(
    root_agent=root_agent,
    name="app",
    memory_service_builder=memory_service_builder,
)
