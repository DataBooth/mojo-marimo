# Draft Reddit post: r/marimo_notebook

## Suggested title

`py-run-mojo – Run Mojo kernels from Python (with marimo notebooks)`

## Suggested body

This is my first post here, so apologies if I’m missing any conventions.

I’ve been experimenting with running Mojo code from marimo and ended up building a small library, `py-run-mojo` (also on PyPI under that name).

It provides a simple executor + decorator for running Mojo kernels from Python, and includes marimo/Jupyter notebooks that wrap the official Mojo GPU puzzles (no puzzle text copied, just scaffolding).

In practice it gives you:

- A raw `run_mojo` executor for compiling/running Mojo source from Python
- A cached-binary pattern so repeated calls are fast
- A docstring-based decorator pattern for writing a Python function whose docstring is Mojo code
- Example marimo notebooks showing how to turn Mojo scripts and GPU puzzles into interactive workflows

I’d love feedback from people using marimo with Mojo:

- Does this flow make sense?
- What would you want from a “Mojo from marimo” toolbox that isn’t here yet?

Happy to share links to the GitHub repo and PyPI page if that’s OK with the mods; otherwise I can keep things high level.

## Notes about AutoModerator / removal

- New accounts and first posts that contain links or look like self-promotion are often auto-removed.
- To reduce the chance of instant removal:
  - Post the announcement text **without links** in the main body.
  - Add the GitHub / PyPI URLs as a **comment on your own post** after it’s live.
  - Make it clear you are looking for feedback and discussion, not just dropping a link.
- If the post is still auto-removed, copy the removal reason and consider sending a short modmail explaining that this is an open-source project and you’re seeking feedback from marimo users.
