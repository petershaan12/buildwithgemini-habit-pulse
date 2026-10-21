import datetime
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-03-e41827d1e1fe"

def seed():
    print(f"Connecting to Firestore for project: {PROJECT_ID}...")
    db = firestore.Client(project=PROJECT_ID)

    # 1. Seed user profile & mascot state
    user_ref = db.collection("users").document("default_user")
    user_ref.set({
        "id": "default_user",
        "display_name": "Hero",
        "xp": 60,
        "level": 1,
        "coins": 25,
        "current_streak": 3,
        "mascot_name": "Sprout",
        "mascot_mood": "happy",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    })
    print("✓ Seeded user profile ('default_user')")

    # 2. Seed initial habits
    habits = [
        {
            "id": "habit_water",
            "name": "Drink 2L Water",
            "category": "Hydration",
            "target": "2 Liters",
            "streak": 3,
            "completed_today": False,
            "xp_reward": 20,
        },
        {
            "id": "habit_walk",
            "name": "Morning 15-min Walk",
            "category": "Fitness",
            "target": "15 mins",
            "streak": 2,
            "completed_today": False,
            "xp_reward": 25,
        },
        {
            "id": "habit_read",
            "name": "Read 10 Pages",
            "category": "Mindfulness",
            "target": "10 pages",
            "streak": 1,
            "completed_today": False,
            "xp_reward": 20,
        },
    ]

    for h in habits:
        db.collection("habits").document(h["id"]).set(h)
        print(f"✓ Seeded habit: {h['name']} ({h['id']})")

    # 3. Seed initial rewards/badges
    rewards = [
        {
            "id": "badge_hydration_hero",
            "title": "Hydration Hero",
            "description": "Logged water for 3 consecutive days!",
            "type": "badge",
            "unlocked": True,
            "xp_required": 50,
        },
        {
            "id": "badge_consistency_king",
            "title": "Consistency Master",
            "description": "Reach a 7-day streak on any habit.",
            "type": "badge",
            "unlocked": False,
            "xp_required": 150,
        }
    ]

    for r in rewards:
        db.collection("rewards").document(r["id"]).set(r)
        print(f"✓ Seeded reward: {r['title']} ({r['id']})")

    print("\nDatabase seeding completed successfully!")

if __name__ == "__main__":
    seed()
