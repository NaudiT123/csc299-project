"""Task manager core logic: data model, storage, and operations.

Tasks are stored as a JSON array of objects with fields:
  id            : int
  title         : str
  description   : str
  created_at    : ISO 8601 timestamp (UTC)
  due_date      : YYYY-MM-DD or None
  priority      : int (1 high - 5 low)
  status        : 'pending' or 'complete'
  summary       : str (optional AI generated)

OpenAI summarization is optional. Set environment variable OPENAI_API_KEY.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import os
from typing import List, Dict, Optional

try:
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover - openai may not be installed or available
    OpenAI = None  # type: ignore


Task = Dict[str, object]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load(store_path: Path) -> List[Task]:
    if not store_path.exists():
        return []
    try:
        with store_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except Exception:
        return []


def _save(store_path: Path, tasks: List[Task]) -> None:
    with store_path.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def _next_id(tasks: List[Task]) -> int:
    return (max((t["id"] for t in tasks), default=0) + 1)  # type: ignore[arg-type]


def _generate_summary(title: str, description: str) -> str:
    # Graceful fallback if OpenAI unavailable
    if OpenAI is None or not os.getenv("OPENAI_API_KEY"):
        return "(Summary unavailable: OpenAI API key not set)"
    try:
        client = OpenAI()
        prompt = (
            "Summarize the following task concisely (<= 30 words).\n"
            f"Title: {title}\nDescription: {description}"
        )
        # Using chat completion for summarization
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.4,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:  # pragma: no cover
        return f"(Summary error: {e.__class__.__name__})"


def add_task(
    store_path: Path,
    title: str,
    description: str = "",
    due_date: Optional[str] = None,
    priority: int = 3,
    summarize: bool = False,
) -> Task:
    tasks = _load(store_path)
    if priority < 1 or priority > 5:
        priority = 3
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            due_date = None
    task: Task = {
        "id": _next_id(tasks),
        "title": title,
        "description": description,
        "created_at": _now_iso(),
        "due_date": due_date,
        "priority": priority,
        "status": "pending",
        "summary": _generate_summary(title, description) if summarize else "",
    }
    tasks.append(task)
    _save(store_path, tasks)
    return task


def list_tasks(
    store_path: Path,
    filter_mode: str = "all",
    sort_mode: str = "priority",
) -> List[Task]:
    tasks = _load(store_path)
    if filter_mode == "pending":
        tasks = [t for t in tasks if t["status"] == "pending"]
    elif filter_mode == "completed":
        tasks = [t for t in tasks if t["status"] == "complete"]

    def sort_key(t: Task):
        due = t.get("due_date") or "9999-12-31"
        if sort_mode == "due":
            return (due, t["priority"])
        return (t["priority"], due)

    return sorted(tasks, key=sort_key)


def complete_task(store_path: Path, task_id: int) -> bool:
    tasks = _load(store_path)
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "complete"
            _save(store_path, tasks)
            return True
    return False


def delete_task(store_path: Path, task_id: int) -> bool:
    tasks = _load(store_path)
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) != len(tasks):
        _save(store_path, new_tasks)
        return True
    return False


def search_tasks(store_path: Path, query: str) -> List[Task]:
    tasks = _load(store_path)
    q = query.lower()
    # Separate prefix matches from other matches
    prefix_matches = []
    other_matches = []
    
    for t in tasks:
        title_lower = str(t.get("title", "")).lower()
        desc_lower = str(t.get("description", "")).lower()
        summary_lower = str(t.get("summary", "")).lower()
        
        # Check if title starts with query (prioritize these)
        if title_lower.startswith(q):
            prefix_matches.append(t)
        # Check if query appears anywhere in title, description, or summary
        elif q in title_lower or q in desc_lower or q in summary_lower:
            other_matches.append(t)
    
    # Return prefix matches first, then other matches
    return prefix_matches + other_matches


def set_priority(store_path: Path, task_id: int, priority: int) -> bool:
    """Manually set task priority (1-5)."""
    if priority < 1 or priority > 5:
        return False
    tasks = _load(store_path)
    for t in tasks:
        if t["id"] == task_id:
            t["priority"] = priority
            _save(store_path, tasks)
            return True
    return False


def prioritize_task(store_path: Path, task_id: int) -> Optional[int]:
    """Use OpenAI to intelligently determine and set task priority based on content."""
    if OpenAI is None or not os.getenv("OPENAI_API_KEY"):
        return None
    
    tasks = _load(store_path)
    target_task = None
    for t in tasks:
        if t["id"] == task_id:
            target_task = t
            break
    
    if not target_task:
        return None
    
    # Build prompt for AI priority assessment
    prompt = (
        "You are a task prioritization expert. Analyze the following task and assign a priority level "
        "from 1 (highest/most urgent) to 5 (lowest/least urgent).\n\n"
        f"Task Title: {target_task['title']}\n"
        f"Description: {target_task.get('description', 'N/A')}\n"
        f"Due Date: {target_task.get('due_date', 'Not set')}\n\n"
        "Consider:\n"
        "- Urgency (due date proximity)\n"
        "- Importance (impact and consequences)\n"
        "- Dependencies and blocking factors\n"
        "- Complexity and time required\n\n"
        "Respond with ONLY a single number (1-5) and a brief explanation (max 40 words) in this format:\n"
        "Priority: <number>\n"
        "Reason: <explanation>"
    )
    
    try:
        client = OpenAI()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.3,
        )
        content = resp.choices[0].message.content.strip()
        
        # Parse priority from response
        priority = None
        reason = ""
        for line in content.split("\n"):
            if line.startswith("Priority:"):
                try:
                    priority = int(line.split(":")[1].strip())
                    if priority < 1 or priority > 5:
                        priority = 3
                except (ValueError, IndexError):
                    priority = 3
            elif line.startswith("Reason:"):
                reason = line.split(":", 1)[1].strip()
        
        if priority is None:
            priority = 3
        
        # Update the task
        target_task["priority"] = priority
        _save(store_path, tasks)
        
        # Store reason in description if user wants
        print(f"AI Reasoning: {reason}")
        return priority
        
    except Exception as e:
        print(f"(Prioritization error: {e.__class__.__name__})")
        return None


def edit_task(
    store_path: Path,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
) -> bool:
    """Edit an existing task's fields."""
    tasks = _load(store_path)
    for t in tasks:
        if t["id"] == task_id:
            if title is not None:
                t["title"] = title
            if description is not None:
                t["description"] = description
            if due_date is not None:
                if due_date:
                    try:
                        datetime.strptime(due_date, "%Y-%m-%d")
                        t["due_date"] = due_date
                    except ValueError:
                        pass  # Keep existing date if invalid
                else:
                    t["due_date"] = None
            _save(store_path, tasks)
            return True
    return False


def clear_tasks(store_path: Path) -> int:
    """Delete all tasks. Returns count of tasks deleted."""
    tasks = _load(store_path)
    count = len(tasks)
    if count > 0:
        _save(store_path, [])
    return count


def get_overview(store_path: Path) -> Dict[str, int]:
    """Get task statistics overview."""
    tasks = _load(store_path)
    total = len(tasks)
    incomplete = len([t for t in tasks if t["status"] == "pending"])
    
    # Count by priority (only pending tasks)
    pending_tasks = [t for t in tasks if t["status"] == "pending"]
    high_priority = len([t for t in pending_tasks if t["priority"] <= 2])
    
    # Count overdue tasks
    today = datetime.now(timezone.utc).date()
    overdue = 0
    for t in pending_tasks:
        if t.get("due_date"):
            try:
                due = datetime.strptime(t["due_date"], "%Y-%m-%d").date()
                if due < today:
                    overdue += 1
            except ValueError:
                pass
    
    return {
        "total": total,
        "incomplete": incomplete,
        "high_priority": high_priority,
        "overdue": overdue,
    }


def suggest_tasks(store_path: Path, context: str = "") -> List[str]:
    """Use OpenAI to suggest new tasks based on existing tasks and optional context."""
    if OpenAI is None or not os.getenv("OPENAI_API_KEY"):
        return ["(Task suggestions unavailable: OpenAI API key not set)"]
    
    tasks = _load(store_path)
    pending_tasks = [t for t in tasks if t["status"] == "pending"]
    
    # Build context from existing tasks
    task_summary = ""
    if pending_tasks:
        task_summary = "Current pending tasks:\n"
        for t in pending_tasks[:10]:  # Limit to 10 most relevant tasks
            task_summary += f"- {t['title']}"
            if t.get('description'):
                task_summary += f": {t['description']}"
            task_summary += "\n"
    
    prompt = (
        "You are a productivity assistant. Based on the following information, "
        "suggest 3-5 new tasks that would be helpful.\n\n"
    )
    
    if task_summary:
        prompt += task_summary + "\n"
    
    if context:
        prompt += f"Additional context: {context}\n\n"
    
    prompt += (
        "Provide task suggestions as a simple list. "
        "Each suggestion should be concise (one line per task). "
        "Format: just the task title/description, no numbers or bullets."
    )
    
    try:
        client = OpenAI()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7,
        )
        content = resp.choices[0].message.content.strip()
        # Split by newlines and filter empty lines
        suggestions = [line.strip() for line in content.split("\n") if line.strip()]
        # Remove common list prefixes (numbers, bullets, dashes)
        cleaned = []
        for s in suggestions:
            s = s.lstrip("0123456789.-•* ").strip()
            if s:
                cleaned.append(s)
        return cleaned if cleaned else ["No suggestions generated"]
    except Exception as e:
        return [f"(Suggestion error: {e.__class__.__name__})"]


__all__ = [
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task",
    "search_tasks",
    "prioritize_task",
    "set_priority",
    "edit_task",
    "suggest_tasks",
    "clear_tasks",
    "get_overview",
]
