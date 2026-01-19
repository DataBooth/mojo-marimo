"""Test that all reference .mojo files compile and run."""

import pytest
from pathlib import Path
from mojo_marimo import run_mojo


# Find all reference .mojo files
EXAMPLES_DIR = Path(__file__).parent.parent / "examples" / "reference"
REFERENCE_FILES = sorted(EXAMPLES_DIR.glob("*.mojo"))


@pytest.mark.parametrize("mojo_file", REFERENCE_FILES, ids=lambda p: p.name)
def test_reference_file_compiles(mojo_file):
    """Test that reference .mojo file compiles and runs."""
    result = run_mojo(str(mojo_file))
    
    # Should compile and run successfully (even if output is empty)
    # None means compilation failed
    assert result is not None, f"{mojo_file.name} failed to compile/run"


def test_reference_files_exist():
    """Ensure we have reference files to test."""
    assert len(REFERENCE_FILES) > 0, "No reference .mojo files found"
    
    # List what we're testing
    print(f"\nFound {len(REFERENCE_FILES)} reference files:")
    for f in REFERENCE_FILES:
        print(f"  - {f.name}")
