from app.schemas.question import Source, Status
from datetime import datetime, timezone

QUESTIONS = [
    {
        "id": "q1",
        "source": Source.LEETCODE.value,
        "link": "",
        "status": Status.COMPLETED.value,
        "title": "Test",
        "prompt": "test",
        "test_cases": [],
        "notes": [],
        "hints": [],
        "tags": [],
        "solutions": [],
        "created_at": datetime(2011, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
        "last_modified": datetime(2011, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
    }
]
