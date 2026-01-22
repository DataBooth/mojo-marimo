# Forum Response: Maturin and mojo-marimo

Thanks for the question! I want to make sure I understand correctly, as I'm not entirely certain about your use case.

## Current Architecture

`mojo-marimo` bridges **Mojo → Python**, not Mojo → Rust. It provides three patterns:

1. **Decorator/Executor**: Compile Mojo to binaries, run via subprocess
2. **Extension modules**: Compile Mojo to `.so` files that Python imports via FFI

Maturin, on the other hand, bridges **Rust → Python** (building Python packages from Rust code).

## Possible Approaches

**If you want Mojo and Rust in the same Python environment:**

You could have both Mojo and Rust extension modules loaded in Python and call between them through Python:

```
Mojo (.so) → Python ← Rust (.so via Maturin)
```

Both would expose C-ABI functions that Python can call.

**If you want direct Mojo → Rust (bypassing Python):**

This wouldn't involve `mojo-marimo` at all. You'd need both languages to expose C-compatible FFI and link them directly.

## Clarification

Could you elaborate on what you're trying to achieve? Are you looking to:
- Call Mojo code from Rust code?
- Use both Mojo and Rust extension modules in Python notebooks?
- Something else I haven't considered?

Understanding your goal would help me provide a more useful answer!
