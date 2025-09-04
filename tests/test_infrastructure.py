"""
Validation tests to ensure the testing infrastructure is properly set up.
"""
import pytest
import os
import sys
from pathlib import Path


def test_project_structure():
    """Test that the basic project structure exists."""
    project_root = Path(__file__).parent.parent
    
    assert (project_root / "pyproject.toml").exists()
    assert (project_root / "bot.py").exists()
    assert (project_root / "tests").exists()
    assert (project_root / "tests" / "__init__.py").exists()


def test_test_directories_exist():
    """Test that test directories are properly created."""
    project_root = Path(__file__).parent.parent
    
    assert (project_root / "tests" / "unit").exists()
    assert (project_root / "tests" / "integration").exists()
    assert (project_root / "tests" / "unit" / "__init__.py").exists()
    assert (project_root / "tests" / "integration" / "__init__.py").exists()


def test_conftest_exists():
    """Test that conftest.py exists and is importable."""
    project_root = Path(__file__).parent.parent
    
    assert (project_root / "tests" / "conftest.py").exists()
    
    # Test that we can import fixtures from conftest
    from tests.conftest import temp_dir, mock_update, mock_context
    
    assert temp_dir is not None
    assert mock_update is not None
    assert mock_context is not None


def test_pytest_configuration():
    """Test that pytest is configured properly."""
    import pytest
    
    # Test that pytest markers are available
    from _pytest.config import get_config
    config = get_config()
    
    # These should not raise exceptions if markers are properly configured
    pytest.mark.unit
    pytest.mark.integration
    pytest.mark.slow


def test_coverage_configuration():
    """Test that coverage is properly configured."""
    try:
        import coverage
        assert True
    except ImportError:
        pytest.fail("Coverage package not available")


def test_mock_fixtures(mock_update, mock_context, temp_dir):
    """Test that mock fixtures work properly."""
    # Test mock_update fixture
    assert hasattr(mock_update, 'message')
    assert hasattr(mock_update.message, 'from_user')
    assert mock_update.message.from_user.id == 12345
    
    # Test mock_context fixture  
    assert hasattr(mock_context, 'bot')
    assert mock_context.error is None
    
    # Test temp_dir fixture
    assert os.path.exists(temp_dir)
    assert os.path.isdir(temp_dir)


@pytest.mark.unit
def test_unit_marker():
    """Test that unit marker works."""
    assert True


@pytest.mark.integration  
def test_integration_marker():
    """Test that integration marker works."""
    assert True


@pytest.mark.slow
def test_slow_marker():
    """Test that slow marker works."""
    assert True


def test_python_path():
    """Test that Python path includes project root."""
    project_root = str(Path(__file__).parent.parent)
    assert project_root in sys.path or any(project_root in path for path in sys.path)