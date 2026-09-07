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

## Render a scene

With the virtual environment activated, render a low-quality preview:

```bash
manim -pql src/viz/scenes/loss_gradient.py LossGradientScene
```

To render the squared-error example instead, run:

```bash
manim -pql src/viz/scenes/squared_error.py SquaredErrorScene
```

To learn why gradient descent moves a weight left or right, run:

```bash
manim -pql src/viz/scenes/gradient_direction.py GradientDirectionScene
```

Manim writes the rendered video under `media/videos/` by default. The `-p`
flag opens the result when the host environment supports it; omit `-p` in a
headless environment.

## Pull request video previews

The `Manim PR preview` GitHub Actions workflow renders `LossGradientScene`,
`SquaredErrorScene`, and `GradientDirectionScene` in
the official Manim Community 0.21 Docker image for every opened, reopened, or
updated pull request. If rendering succeeds, it publishes a small HTML page at
a PR-specific path such as `https://<owner>.github.io/<repository>/pr-1/` and
adds or updates a comment on the pull request with that link. The page embeds
the MP4 in a mobile-friendly HTML5 video player, so it can be watched directly
in Safari on an iPhone or iPad. Before publishing, CI re-encodes the preview as
H.264 with a `yuv420p` pixel format, optional AAC audio, and fast-start metadata,
and extracts a scene-specific poster frame from the middle of each animation. Generated videos
remain CI artifacts and Pages content; they are not committed to the working
branch.

Each scene section also offers commit-versioned **Download 1080p MP4** and
**Download 720p preview** links, plus an **Open 1080p video** fallback. The
1080p file is rendered natively by Manim at 1920×1080 and 60 FPS, then encoded
as H.264 with `yuv420p`, CRF 18, and fast-start metadata. CI verifies its
resolution and frame rate with FFprobe and fully decodes both published videos
before deploying the page.

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
