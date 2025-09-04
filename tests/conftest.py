import pytest
import tempfile
import os
import shutil
from unittest.mock import Mock, MagicMock
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def temp_file():
    """Create a temporary file for tests."""
    fd, temp_file_path = tempfile.mkstemp()
    os.close(fd)
    yield temp_file_path
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)


@pytest.fixture
def mock_update():
    """Mock Telegram update object."""
    update = Mock()
    update.message = Mock()
    update.message.from_user = Mock()
    update.message.from_user.id = 12345
    update.message.text = "/test command"
    update.message.reply_text = Mock()
    update.effective_message = Mock()
    update.effective_message.reply_text = Mock()
    update.callback_query = Mock()
    return update


@pytest.fixture
def mock_context():
    """Mock Telegram context object."""
    context = Mock()
    context.bot = Mock()
    context.error = None
    return context


@pytest.fixture
def mock_file_operations(temp_dir):
    """Mock file operations with a temporary directory."""
    original_cwd = os.getcwd()
    os.chdir(temp_dir)
    yield temp_dir
    os.chdir(original_cwd)


@pytest.fixture
def sample_config():
    """Provide sample configuration for tests."""
    return {
        "admin_password": "TEST_ADMIN_PASSWORD",
        "user_password": "TEST_USER_PASSWORD",
        "bot_token": "TEST_TOKEN",
        "rclone_command": "rclone ls remote:",
        "backup_command": "rclone sync source: dest:"
    }


@pytest.fixture
def mock_subprocess():
    """Mock subprocess operations."""
    mock_process = Mock()
    mock_process.stdout = Mock()
    mock_process.stdout.readline = Mock(side_effect=[b"line1\n", b"line2\n", b""])
    return mock_process


@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Automatically cleanup test files after each test."""
    test_files = ["user.txt", "userA.txt", "adress.txt", "link.txt"]
    
    # Clean up before test
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
    
    yield
    
    # Clean up after test
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)


@pytest.fixture
def mock_telegram_updater():
    """Mock Telegram Updater for integration tests."""
    updater = Mock()
    updater.dispatcher = Mock()
    updater.dispatcher.add_handler = Mock()
    updater.dispatcher.add_error_handler = Mock()
    updater.start_polling = Mock()
    updater.idle = Mock()
    return updater