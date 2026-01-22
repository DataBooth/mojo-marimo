# Contributing to py-run-mojo

Thank you for your interest in contributing to py-run-mojo! This is a living experiment, evolving based on real-world usage.

## Areas for Contribution

- **Additional notebook examples**: More marimo notebooks demonstrating different use cases
- **Performance profiling**: Benchmarks on diverse hardware (different CPUs, GPUs, platforms)
- **Integration**: Support for other notebook environments (Jupyter, VSCode notebooks)
- **Error handling**: Better error messages, debugging workflows
- **Documentation**: Improved guides, tutorials, API references
- **Testing**: More comprehensive test coverage, especially integration tests
- **Pattern library**: Common use case patterns (data transformations, simulations, etc.)

## Development Setup

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/databooth/mojo-marimo
cd mojo-marimo

# Create virtual environment and install
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Verify setup
python -m pytest tests/
```

### Using pixi

```bash
# Clone and install
git clone https://github.com/databooth/mojo-marimo
cd mojo-marimo
pixi install

# Verify setup
pixi run test-setup
```

## Running Tests

### uv

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/py_run_mojo --cov-report=html

# Format code
ruff format .

# Lint
ruff check .

# Type check
uvx ty check
```

### pixi

```bash
# Run tests
pixi run test-all

# Format
pixi run format

# Lint
pixi run lint

# Type check
pixi run typecheck

# All checks
pixi run check
```

## Code Quality

This project uses:
- **ruff** for linting and formatting
- **ty** for type checking (10-100× faster than mypy)
- **pytest** for testing

Please ensure:
- All tests pass before submitting a PR
- Code is formatted with `ruff format`
- No linting errors from `ruff check`
- Type hints are added for new functions

## Testing Mojo Integration

Note that integration tests require `mojo` on your PATH:

```bash
# Verify mojo is available
mojo --version

# Run integration test
pytest tests/
```

## Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Add tests** if adding new functionality
5. **Run quality checks**:
   ```bash
   # uv
   ruff format . && ruff check . && uvx ty check && pytest tests/
   
   # pixi
   pixi run check && pixi run test-all
   ```
6. **Commit with clear messages**:
   ```bash
   git commit -m "feat: add new feature description"
   ```
7. **Push to your fork**: `git push origin feature/your-feature-name`
8. **Open a Pull Request**

### Commit Message Convention

We follow conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions or changes
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `chore:` - Maintenance tasks

## Adding New Examples

To add a new notebook example:

1. Create the notebook in `notebooks/`:
   ```python
   import marimo
   
   app = marimo.App()
   
   @app.cell
   def __():
       # Your example code here
       return
   ```

2. Add documentation to the notebook explaining:
   - What the example demonstrates
   - When to use this pattern
   - Performance characteristics

3. Update the main README if adding a significant new pattern

## Documentation

- Use Australian English for all documentation and comments
- Keep code comments clear and concise
- Update relevant documentation when changing functionality
- Add docstrings to new functions following existing style

## Questions?

- Open an issue for questions or discussions
- Reach out via [databooth.com.au/about](https://www.databooth.com.au/about/)

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
