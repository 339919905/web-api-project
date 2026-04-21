"""
Seed script for the Task Management API.
This script inserts a small set of sample tasks into the database,
which is useful for coursework demos and screenshots.
"""

from datetime import date

from database import Base, SessionLocal, Task, engine


def seed_tasks():
    """Create the database tables and insert sample tasks if none exist."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        existing_count = db.query(Task).count()
        if existing_count > 0:
            print("Seed skipped: tasks already exist in the database.")
            return

        sample_tasks = [
            Task(
                title="Finish backend coursework",
                description="Complete the CRUD API and verify all endpoints.",
                completed=False,
                due_date=date(2026, 4, 30),
            ),
            Task(
                title="Write project report",
                description="Summarize design decisions, testing, and deployment steps.",
                completed=False,
                due_date=date(2026, 5, 2),
            ),
            Task(
                title="Prepare demonstration slides",
                description="Create a short presentation for the coursework review.",
                completed=True,
                due_date=date(2026, 5, 5),
            ),
        ]

        db.add_all(sample_tasks)
        db.commit()
        print("Seed completed: sample tasks inserted successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_tasks()
