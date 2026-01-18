"""Test script to verify all three Mojo execution approaches work correctly.

This script:
1. Checks if mojo is available on PATH
2. Tests uncached subprocess approach
3. Tests cached binary approach
4. Tests decorator approach
5. Compares results for consistency

Run this before using the marimo notebooks to ensure your environment is set up correctly.
"""

import subprocess
import sys
from pathlib import Path


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
        print("   export PATH=\"$HOME/.modular/pkg/packages.modular.com_mojo/bin:$PATH\"")
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
    print("Testing all three approaches...")
    print("=" * 60)
    
    # Import after checking mojo is available
    from compute_wrapper import fibonacci as fib_uncached
    from mo_run_cached import fibonacci_cached as fib_cached, clear_cache
    from mojo_decorator import fibonacci as fib_decorator
    
    # Clear cache to ensure fair test
    clear_cache()
    print("\nCache cleared for testing")
    
    # Test value
    n = 10
    expected = 55  # fibonacci(10) = 55
    
    # Test each approach
    results = {}
    results["uncached"] = test_approach(
        "1. Uncached Subprocess",
        fib_uncached,
        n
    )
    
    results["cached"] = test_approach(
        "2. Cached Binary (first call - will compile)",
        fib_cached,
        n
    )
    
    results["decorator"] = test_approach(
        "3. Decorator",
        fib_decorator,
        n
    )
    
    # Test cached performance (should be faster)
    results["cached_warm"] = test_approach(
        "4. Cached Binary (second call - using cache)",
        fib_cached,
        n
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
        print("🎉 All approaches working correctly!")
        print("\nYou can now use:")
        print("  pixi run marimo-edit        # Interactive example notebook")
        print("  pixi run benchmark-marimo   # Comparison & benchmarks")
    else:
        print("⚠️  Some approaches failed - check output above")
        sys.exit(1)


if __name__ == "__main__":
    main()
