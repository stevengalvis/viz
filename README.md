# viz

A small collection of [Manim Community](https://www.manim.community/)
animations for explaining deep-learning concepts.

## Setup

From the repository root, create a virtual environment and install the project
with its test dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

## Run the tests

```bash
python -m pytest
```

## Render the loss-gradient scene

With the virtual environment activated, render a low-quality preview:

```bash
manim -pql src/viz/scenes/loss_gradient.py LossGradientScene
```

Manim writes the rendered video under `media/videos/` by default. The `-p`
flag opens the result when the host environment supports it; omit `-p` in a
headless environment.

## Pull request video previews

The `Manim PR preview` GitHub Actions workflow renders `LossGradientScene` in
the official Manim Community 0.21 Docker image for every opened, reopened, or
updated pull request. If rendering succeeds, it publishes a small HTML page at
a PR-specific path such as `https://<owner>.github.io/<repository>/pr-1/` and
adds or updates a comment on the pull request with that link. The page embeds
the MP4 in a mobile-friendly HTML5 video player, so it can be watched directly
in Safari on an iPhone or iPad. Before publishing, CI re-encodes the preview as
H.264 with a `yuv420p` pixel format, optional AAC audio, and fast-start metadata,
and extracts a poster frame from the middle of the animation. Generated videos
remain CI artifacts and Pages content; they are not committed to the working
branch.

### One-time GitHub Pages setup

After the workflow has run once and created the `gh-pages` branch:

1. Open the repository's **Settings → Pages**.
2. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
3. Select the **gh-pages** branch and the **/(root)** folder, then click
   **Save**.

The workflow needs permission to update `gh-pages` and the pull request
comment. If repository settings override workflow permissions, open
**Settings → Actions → General → Workflow permissions**, select **Read and
write permissions**, and enable **Allow GitHub Actions to create and approve
pull requests**.
