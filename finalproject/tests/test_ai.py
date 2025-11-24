"""Unit tests for task_manager.py AI functions using mocks."""

import pytest
from pathlib import Path
import tempfile
from unittest.mock import patch, MagicMock
import os

from task_manager import add_task, prioritize_task, suggest_tasks


@pytest.fixture
def temp_store():
    """Create a temporary tasks.json file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_path = Path(f.name)
    yield temp_path
    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing without real API calls."""
    with patch('task_manager.OpenAI') as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        yield mock_client


class TestSummarizeTask:
    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_summarize_generates_summary(self, mock_openai_class, temp_store):
        """Verify summarize flag triggers AI summary generation."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Mock the response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Complete quarterly financial report by end of month"
        mock_client.chat.completions.create.return_value = mock_response
        
        task = add_task(
            temp_store,
            title="Write report",
            description="Quarterly financial analysis",
            summarize=True
        )
        
        assert task["summary"] == "Complete quarterly financial report by end of month"
        mock_client.chat.completions.create.assert_called_once()

    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_summarize_uses_correct_model(self, mock_openai_class, temp_store):
        """Verify summarize uses gpt-4o-mini model."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test summary"
        mock_client.chat.completions.create.return_value = mock_response
        
        add_task(temp_store, title="Test", description="Description", summarize=True)
        
        call_args = mock_client.chat.completions.create.call_args
        assert call_args.kwargs['model'] == 'gpt-4o-mini'

    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_summarize_includes_title_and_description(self, mock_openai_class, temp_store):
        """Verify summarize prompt includes title and description."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Summary"
        mock_client.chat.completions.create.return_value = mock_response
        
        add_task(
            temp_store,
            title="Project Setup",
            description="Initialize repository and dependencies",
            summarize=True
        )
        
        call_args = mock_client.chat.completions.create.call_args
        prompt = call_args.kwargs['messages'][0]['content']
        assert "Project Setup" in prompt
        assert "Initialize repository and dependencies" in prompt

    @patch.dict(os.environ, {}, clear=True)
    def test_summarize_without_api_key(self, temp_store):
        """Verify summarize fails gracefully without API key."""
        task = add_task(
            temp_store,
            title="Test",
            description="Description",
            summarize=True
        )
        
        assert "(Summary unavailable: OpenAI API key not set)" in task["summary"]

    @patch('task_manager.OpenAI', None)
    def test_summarize_without_openai_package(self, temp_store):
        """Verify summarize fails gracefully without openai package."""
        task = add_task(
            temp_store,
            title="Test",
            description="Description",
            summarize=True
        )
        
        assert "(Summary unavailable: OpenAI API key not set)" in task["summary"]

    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_summarize_handles_api_error(self, mock_openai_class, temp_store):
        """Verify summarize handles API errors gracefully."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        task = add_task(temp_store, title="Test", description="Desc", summarize=True)
        
        assert "(Summary error:" in task["summary"]


class TestPrioritizeTask:
    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_prioritize_sets_priority(self, mock_openai_class, temp_store):
        """Verify prioritize_task sets priority based on AI response."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Priority: 1\nReason: Urgent deadline approaching"
        mock_client.chat.completions.create.return_value = mock_response
        
        task = add_task(temp_store, title="Critical Bug Fix", priority=3)
        priority = prioritize_task(temp_store, task["id"])
        
        assert priority == 1

    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_prioritize_uses_correct_model(self, mock_openai_class, temp_store):
        """Verify prioritize uses gpt-4o-mini model."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Priority: 2\nReason: Important task"
        mock_client.chat.completions.create.return_value = mock_response
        
        task = add_task(temp_store, title="Test Task")
        prioritize_task(temp_store, task["id"])
        
        call_args = mock_client.chat.completions.create.call_args
        assert call_args.kwargs['model'] == 'gpt-4o-mini'

    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_prioritize_includes_task_context(self, mock_openai_class, temp_store):
        """Verify prioritize includes task details in prompt."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Priority: 2\nReason: Moderate urgency"
        mock_client.chat.completions.create.return_value = mock_response
        
        task = add_task(
            temp_store,
            title="Submit Report",
            description="Quarterly analysis",
            due_date="2025-11-30"
        )
        prioritize_task(temp_store, task["id"])
        
        call_args = mock_client.chat.completions.create.call_args
        prompt = call_args.kwargs['messages'][0]['content']
        assert "Submit Report" in prompt
        assert "Quarterly analysis" in prompt
        assert "2025-11-30" in prompt

    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_prioritize_defaults_to_3_on_invalid_response(self, mock_openai_class, temp_store):
        """Verify prioritize defaults to 3 if AI returns invalid priority."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Priority: invalid\nReason: Something"
        mock_client.chat.completions.create.return_value = mock_response
        
        task = add_task(temp_store, title="Task")
        priority = prioritize_task(temp_store, task["id"])
        
        assert priority == 3

    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_prioritize_clamps_out_of_range_priority(self, mock_openai_class, temp_store):
        """Verify prioritize clamps priority to 1-5 range."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Priority: 10\nReason: Very important"
        mock_client.chat.completions.create.return_value = mock_response
        
        task = add_task(temp_store, title="Task")
        priority = prioritize_task(temp_store, task["id"])
        
        assert priority == 3  # Should default to 3

    @patch.dict(os.environ, {}, clear=True)
    def test_prioritize_without_api_key(self, temp_store):
        """Verify prioritize returns None without API key."""
        task = add_task(temp_store, title="Test")
        priority = prioritize_task(temp_store, task["id"])
        
        assert priority is None

    def test_prioritize_nonexistent_task(self, temp_store):
        """Verify prioritize returns None for nonexistent task."""
        priority = prioritize_task(temp_store, 999)
        assert priority is None

    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_prioritize_handles_api_error(self, mock_openai_class, temp_store, capsys):
        """Verify prioritize handles API errors gracefully."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = RuntimeError("API Error")
        
        task = add_task(temp_store, title="Test")
        priority = prioritize_task(temp_store, task["id"])
        
        assert priority is None
        captured = capsys.readouterr()
        assert "(Prioritization error:" in captured.out


class TestSuggestTasks:
    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_suggest_returns_list(self, mock_openai_class, temp_store):
        """Verify suggest_tasks returns a list of suggestions."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "1. Review code\n2. Write tests\n3. Update docs"
        mock_client.chat.completions.create.return_value = mock_response
        
        suggestions = suggest_tasks(temp_store)
        
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0

    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_suggest_uses_correct_model(self, mock_openai_class, temp_store):
        """Verify suggest uses gpt-4o-mini model."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Task 1\nTask 2"
        mock_client.chat.completions.create.return_value = mock_response
        
        suggest_tasks(temp_store)
        
        call_args = mock_client.chat.completions.create.call_args
        assert call_args.kwargs['model'] == 'gpt-4o-mini'

    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_suggest_includes_pending_tasks(self, mock_openai_class, temp_store):
        """Verify suggest includes existing pending tasks in context."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "New task 1\nNew task 2"
        mock_client.chat.completions.create.return_value = mock_response
        
        add_task(temp_store, title="Existing Task 1", description="Some work")
        add_task(temp_store, title="Existing Task 2", description="More work")
        
        suggest_tasks(temp_store)
        
        call_args = mock_client.chat.completions.create.call_args
        prompt = call_args.kwargs['messages'][0]['content']
        assert "Existing Task 1" in prompt
        assert "Existing Task 2" in prompt

    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_suggest_includes_context(self, mock_openai_class, temp_store):
        """Verify suggest includes user-provided context."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Prepare presentation\nReview slides"
        mock_client.chat.completions.create.return_value = mock_response
        
        suggest_tasks(temp_store, context="work project deadline next week")
        
        call_args = mock_client.chat.completions.create.call_args
        prompt = call_args.kwargs['messages'][0]['content']
        assert "work project deadline next week" in prompt

    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_suggest_cleans_list_prefixes(self, mock_openai_class, temp_store):
        """Verify suggest removes common list prefixes from suggestions."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "1. Review code\n2. Write tests\n- Update docs"
        mock_client.chat.completions.create.return_value = mock_response
        
        suggestions = suggest_tasks(temp_store)
        
        assert "Review code" in suggestions
        assert "Write tests" in suggestions
        assert "Update docs" in suggestions
        # Should not have prefixes
        assert not any(s.startswith("1.") or s.startswith("2.") or s.startswith("-") for s in suggestions)

    @patch.dict(os.environ, {}, clear=True)
    def test_suggest_without_api_key(self, temp_store):
        """Verify suggest returns error message without API key."""
        suggestions = suggest_tasks(temp_store)
        
        assert len(suggestions) == 1
        assert "unavailable" in suggestions[0].lower()

    @patch('task_manager.OpenAI', None)
    def test_suggest_without_openai_package(self, temp_store):
        """Verify suggest returns error message without openai package."""
        suggestions = suggest_tasks(temp_store)
        
        assert len(suggestions) == 1
        assert "unavailable" in suggestions[0].lower()

    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_suggest_handles_api_error(self, mock_openai_class, temp_store):
        """Verify suggest handles API errors gracefully."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = ValueError("API Error")
        
        suggestions = suggest_tasks(temp_store)
        
        assert len(suggestions) == 1
        assert "error" in suggestions[0].lower()

    @patch('task_manager.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_suggest_filters_empty_lines(self, mock_openai_class, temp_store):
        """Verify suggest filters out empty lines from response."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Task 1\n\n\nTask 2\n\nTask 3"
        mock_client.chat.completions.create.return_value = mock_response
        
        suggestions = suggest_tasks(temp_store)
        
        assert len(suggestions) == 3
        assert all(s.strip() for s in suggestions)  # No empty strings
