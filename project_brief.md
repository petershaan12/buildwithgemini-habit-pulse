# My agent: HabitPulse (with Virtual Companion & Gamification)

**One-liner:** A playful, engaging habit and wellness companion that combines Tamagotchi-style virtual pet care and Duolingo-style gamification with Google ADK, Vertex AI, Firestore, and Nano Banana image generation.

---

## 🎯 Product Overview

HabitPulse transforms daily habit tracking into an interactive, rewarding experience. Users nurture a charming 3D-style virtual pet mascot whose moods, animations, and growth directly reflect real daily habit check-ins and streaks.

---

## 🐾 1. Virtual Pet Mascot ("Sprout / Boba")

- **Visual Style:** Original, soft pastel palette, rounded organic shapes, expressive eyes, and high-fidelity 3D clay/chibi aesthetic generated via Nano Banana (`gemini-3.1-flash-lite-image` / Imagen 3).
- **Consistent Identity:** A persistent character prompt descriptor ensures visual consistency across expressions and poses.
- **Mascot States & Triggers:**
  - `idle`: Default resting state when habits are pending.
  - `happy`: Triggered when a habit is checked off.
  - `celebrating`: Triggered on streak milestones or level-ups.
  - `sleepy`: Evening reminder or low activity.
  - `cheering`: Midday check-in encouragement.
  - `sad`: Broken streak or overdue daily habits.
  - `level-up`: Milestone evolution or accessory unlock.
- **Frontend Animation:** Lightweight CSS/JS micro-animations (bobbing, floating, bouncing, blinking, waving) applied to transparent/clean mascot art assets. Mascot reacts to actual user events, never random.

---

## 🎮 2. Gamification & Progression System

- **XP & Leveling:**
  - Completing a habit grants base XP (+20 XP).
  - Milestone level-ups for user and mascot.
- **Coins & Streaks:**
  - Consecutive day streaks award bonus Coins (+10 coins/day streak).
- **Achievements & Collectibles:**
  - Unlockable achievement badges (e.g., "7-Day Hydration Hero", "Early Bird", "Consistency King").
  - Mascot accessories and cosmetic unlocks at specific level tiers.
- **Anti-Cheat / Idempotency:**
  - Idempotent logging prevents duplicate XP or rewards for the same habit on the same calendar day.
- **Delight & Feedback:**
  - Animated confetti showers, floating XP counters, star bursts, and celebratory modal popups.

---

## 🎨 3. Nano Banana & Cloud Storage Integration

- **Model:** Google Nano Banana (`gemini-3.1-flash-lite-image` or Vertex AI image generation API).
- **Asset Types:**
  - Static mascot expression assets (`idle.png`, `happy.png`, `celebrating.png`).
  - Collectible achievement badge artwork.
  - Personalized milestone celebration reward cards.
- **Storage & Caching:**
  - Generated assets are uploaded to a Google Cloud Storage (GCS) bucket and served via public/signed URLs.
  - Mascot assets are cached and reused; generation is reserved for new badges or unique milestone cards to optimize latency and quota.

---

## 🔧 4. ADK Agent Function Tools

1. `create_habit(name: str, frequency: str, category: str, target_count: int)`: Creates a new tracked habit in Firestore.
2. `get_habits(user_id: str)`: Fetches active daily habits with today's completion status.
3. `log_habit(user_id: str, habit_id: str, date: str)`: Idempotently marks a habit complete, calculates XP/coins, and checks for streaks.
4. `get_streaks(user_id: str)`: Retrieves current and best streak counts across all habits.
5. `get_rewards(user_id: str)`: Lists earned and available achievements, badges, and cosmetic items.
6. `claim_reward(user_id: str, reward_id: str)`: Claims an unlocked reward or unlocks an accessory.
7. `get_mascot_state(user_id: str)`: Computes current mascot mood, level, and active animation trigger based on today's progress.
8. `generate_reward_card(user_id: str, milestone_title: str)`: Prompts Nano Banana to produce an achievement badge/card and stores it in GCS.

---

## 🌐 5. Frontend & UI Architecture

- **Layout:** Mobile-first, responsive, playful dashboard.
- **Mascot Stage:** Prominently displays the animated companion with reactive mood states and interactive tap gestures.
- **Daily Checklist:** Interactive habit checklist with instant check-off feedback and streak counters.
- **Gamification Header:** Level badge, animated XP progress bar, coin counter, and streak flame.
- **Reward Inventory & Gallery:** Visual showcase of earned badges, celebration cards, and unlocked mascot gear.
- **A2UI Integration:** Rich cards and tables in conversational agent interfaces where supported, supplemented by custom HTML5/CSS/Tailwind components for advanced game animations and confetti.

---

## 🗄️ 6. Data Architecture

### Firestore Collections:
- **`users`**: `{ id, display_name, xp, level, coins, current_streak, created_at }`
- **`habits`**: `{ id, user_id, name, category, frequency, target_count, created_at, active }`
- **`habit_logs`**: `{ id, habit_id, user_id, date, completed, xp_earned }` (unique constraint per habit + date)
- **`rewards`**: `{ id, title, description, badge_image_url, xp_threshold, type }`
- **`user_rewards`**: `{ id, user_id, reward_id, unlocked_at, claimed }`
- **`mascot_progress`**: `{ user_id, mood, active_accessory, evolution_stage }`

### Memory & State:
- **Agent Platform Memory Bank:** Retains user personal preferences, sleep/wake schedule, motivation triggers, and conversational context across sessions.

---

## 📋 7. Workshop Scope & Implementation Roadmap

### 🚀 Phase 1: MVP (Prioritized for Workshop)
1. **Mascot Foundation:** 1 original mascot character with 3 key states (`idle`, `happy`, `celebrating`).
2. **Habit Lifecycle:** `create_habit`, `get_habits`, and idempotent `log_habit` daily check-ins.
3. **Core Progression:** Base XP calculation, streak incrementing, and mood updates in Firestore.
4. **Nano Banana Asset:** 1 generated collectible achievement badge stored in GCS.
5. **Interactive UI:** Clean, animated mobile-first frontend with reactive mascot state and checklist.

### 🌟 Phase 2: Stretch Goals
- Additional mascot expressions (`sleepy`, `sad`, `cheering`).
- Coin economy and cosmetic accessories/wardrobe shop.
- Dynamic milestone card generation on demand using Nano Banana.
- Code Sandbox integration for weekly habit adherence analysis and trend charts.
