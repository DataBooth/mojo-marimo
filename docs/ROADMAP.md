# Roadmap

## Current Status (v0.1.0)

`mojo-marimo` is a **notebook-agnostic** library for running Mojo code from Python. Despite the name, the core library has no marimo-specific dependencies and works in any Python environment (Jupyter, marimo, VSCode notebooks, IPython REPL, etc.).

### What Works Now
- ✅ Three integration patterns (decorator, executor, extension modules)
- ✅ SHA256-based binary caching
- ✅ Pre-compilation validation
- ✅ Interactive examples in marimo format
- ✅ Jupyter notebook exports (`.ipynb` format)
- ✅ 44 passing tests (75% coverage)
- ✅ Comprehensive documentation

## Future Direction

### Package Identity & Naming

**Current Challenge:** The package is named `mojo-marimo` but works with any notebook system, not just marimo.

**Options Under Consideration:**
1. **Keep current name** - Acknowledge historical origin, document multi-notebook support
2. **Rename to `mojo-notebooks`** - More accurate, but loses branding/recognition
3. **Rename to `mojo-py`** - Broader scope (works in any Python context)
4. **Create umbrella package** - `mojo-notebooks` with `mojo-marimo`, `mojo-jupyter` sub-packages

**Decision Timeline:** Community feedback during v0.1.x → decision by v0.2.0

### Near-term (v0.1.x - Next 1-2 months)

#### Multi-Notebook Support
- [ ] Validate Jupyter notebook compatibility
- [ ] Test VSCode notebook integration
- [ ] Document notebook-specific considerations
- [ ] Add Jupyter-specific examples if needed

#### Developer Experience
- [ ] Auto-generate extension module boilerplate
- [ ] Improve error messages and debugging
- [ ] Add `mojo-marimo init` CLI command
- [ ] Template/scaffolding for new projects

#### Performance & Reliability
- [ ] Benchmark extension module overhead vs subprocess
- [ ] Support multiple Mojo versions
- [ ] Improve cache invalidation logic
- [ ] Add telemetry for performance monitoring

### Mid-term (v0.2.0 - Next 3-6 months)

#### Pattern Library
- [ ] Common algorithms (sorting, searching, numerical)
- [ ] Data processing patterns
- [ ] ML/AI building blocks
- [ ] Finance/quant patterns

#### Enhanced Extension Module Support
- [ ] Automatic PythonModuleBuilder generation
- [ ] Type hints from Mojo → Python
- [ ] Multi-function extension modules
- [ ] Hot reloading during development

#### Documentation & Community
- [ ] Video tutorials
- [ ] Interactive documentation site
- [ ] Gallery of community examples
- [ ] Best practices guide

### Long-term (v0.3.0+ - 6+ months)

#### Advanced Features
- [ ] Direct Mojo REPL integration
- [ ] Debug mode with breakpoints
- [ ] Profiling integration
- [ ] GPU/accelerator support examples

#### Ecosystem Integration
- [ ] Poetry plugin
- [ ] pip-installable package (PyPI)
- [ ] conda-forge distribution
- [ ] IDE extensions (VSCode, PyCharm)

#### Production Readiness
- [ ] Production deployment patterns
- [ ] Container images
- [ ] Cloud notebook integration (Colab, Databricks, SageMaker)
- [ ] Enterprise authentication/authorization

## Open Questions

### Community Input Needed

1. **Naming:** Should we rename the package? If so, what name best captures the scope?

2. **Patterns:** Which of the three patterns (decorator, executor, extension) do you use most? Should we simplify to fewer patterns?

3. **Use Cases:** What are you building with this? What features would unlock new use cases?

4. **Jupyter Priority:** How critical is first-class Jupyter support vs marimo?

5. **Extension Modules:** Is the complexity of `PythonModuleBuilder` worth the performance gain? Should we auto-generate boilerplate?

### Technical Decisions

1. **Mojo Version Support:** Support multiple Mojo versions or always require latest?

2. **Cache Strategy:** Current SHA256 approach or support versioned caching?

3. **Type Safety:** Auto-generate Python type stubs from Mojo signatures?

4. **Distribution:** Stay development-only or publish to PyPI?

## Contributing

This roadmap evolves based on community feedback. See [`FEEDBACK_REQUESTED.md`](FEEDBACK_REQUESTED.md) for specific areas where input is valuable.

To suggest changes to the roadmap:
1. Open an issue with the `roadmap` label
2. Start a discussion in GitHub Discussions
3. Submit a PR updating this document

## Timeline Philosophy

**Iterative & Feedback-driven:** We prioritise shipping working code quickly over extensive upfront planning. Timelines are estimates; actual priorities shift based on community needs and real-world usage.
