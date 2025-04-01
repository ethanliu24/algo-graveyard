from app.schemas.question import Source, Status
from datetime import datetime, timezone

SOLUTIONS = [
    {
        "id": "s1",
        "summary": "Test",
        "explanation": "test",
        "language": "python",
        "time_complexity": "n!",
        "space_complexity": "n^n",
        "ai_analysis": {
            "time_complexity": "n!",
            "space_complexity": "n^n",
            "feedback": "trash",
        },
        "code": "print(\"hello world\")",
        "created_at": datetime(2011, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
        "last_modified": datetime(2011, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
    },
    {
        "id": "s2",
        "summary": "Test 2",
        "explanation": "test 2",
        "language": "python",
        "time_complexity": "n!",
        "space_complexity": "n^n",
        "ai_analysis": {
            "time_complexity": "n!",
            "space_complexity": "n^n",
            "feedback": "trash",
        },
        "code": "print(\"hello world\")",
        "created_at": datetime(2011, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
        "last_modified": datetime(2011, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
    }
]

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
        "solutions": [SOLUTIONS[0]],
        "created_at": datetime(2011, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
        "last_modified": datetime(2011, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
    },
    {
        "id": "delete_endpoint",
        "source": Source.OTHER.value,
        "link": "",
        "status": Status.UNOPTIMIZED.value,
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
