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
