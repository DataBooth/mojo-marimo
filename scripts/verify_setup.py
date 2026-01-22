"""Test script to verify both Mojo execution approaches work correctly.

This script:
1. Checks if mojo is available on PATH
2. Tests cached binary approach (via examples)
3. Tests decorator approach
4. Compares results for consistency

Run this before using the marimo notebooks to ensure your environment is set up correctly.
"""

import subprocess
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def check_mojo_available():
    """Check if mojo command is available on PATH."""
    print("=" * 60)
    print("Checking Mojo availability...")
    print("=" * 60)

    try:
        result = subprocess.run(
            ["mojo", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Mojo found: {version}")
            return True
        else:
            print("❌ Mojo command failed")
            return False
    except FileNotFoundError:
        print("❌ Mojo not found on PATH")
        print("\nTo fix this:")
        print("1. Install Mojo:")
        print("   curl https://get.modular.com | sh -")
        print("   modular install mojo")
        print("\n2. Add to PATH (example for macOS/Linux):")
        print('   export PATH="$HOME/.modular/pkg/packages.modular.com_mojo/bin:$PATH"')
        print("\n3. Verify:")
        print("   mojo --version")
        return False


def test_approach(name, test_func, *args):
    """Test a single approach and return result."""
    print(f"\n{name}:")
    print("-" * 60)
    try:
        result = test_func(*args)
        print(f"✅ Success: {result}")
        return result
    except Exception as e:
        print(f"❌ Failed: {e}")
        return None


def main():
    """Run all tests."""
    # Check mojo availability first
    if not check_mojo_available():
        print("\n⚠️  Cannot proceed without mojo on PATH")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Testing both approaches...")
    print("=" * 60)

    # Import after checking mojo is available
    # Add examples to path
    examples_path = Path(__file__).parent.parent / "examples"
    sys.path.insert(0, str(examples_path))

    from examples import fibonacci as fib_example
    from py_run_mojo.decorator import fibonacci as fib_decorator
    from py_run_mojo.executor import clear_cache

    # Clear cache to ensure fair test
    clear_cache()
    print("\nCache cleared for testing")

    # Test value
    n = 10
    expected = 55  # fibonacci(10) = 55

    # Test each approach
    results = {}

    results["cached_first"] = test_approach(
        "1. Cached Binary (first call - will compile)", fib_example, n
    )

    results["decorator"] = test_approach(
        "2. Decorator (first call - will compile)", fib_decorator, n
    )

    # Test warm cache performance
    results["cached_warm"] = test_approach(
        "3. Cached Binary (second call - using cache)", fib_example, n
    )

    results["decorator_warm"] = test_approach(
        "4. Decorator (second call - using cache)", fib_decorator, n
    )

    # Verify results
    print("\n" + "=" * 60)
    print("Results Summary")
    print("=" * 60)

    all_correct = True
    for approach, result in results.items():
        if result is None:
            print(f"❌ {approach}: FAILED")
            all_correct = False
        elif int(result) == expected:
            print(f"✅ {approach}: {result} (correct)")
        else:
            print(f"❌ {approach}: {result} (expected {expected})")
            all_correct = False

    # Final verdict
    print("\n" + "=" * 60)
    if all_correct:
        print("🎉 Both approaches working correctly!")
        print("\nYou can now use:")
        print("  marimo edit notebooks/example_notebook.py     # Interactive example")
        print("  marimo edit notebooks/benchmark_notebook.py   # Benchmarks")
        print("\nOr with pixi:")
        print("  pixi run notebook-example    # Interactive example")
        print("  pixi run notebook-benchmark  # Benchmarks")
    else:
        print("⚠️  Some approaches failed - check output above")
        sys.exit(1)


if __name__ == "__main__":
    main()
