"""Show why gradient descent moves left or right on a loss curve."""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Axes,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    Scene,
    Text,
    ValueTracker,
    VGroup,
    Write,
    always_redraw,
)

from viz.calculations import gradient_descent_step, weight_gradient, weight_loss

BACKGROUND_COLOR = "#0B1020"
CURVE_COLOR = "#5DA9E9"
NEUTRAL_COLOR = "#B8C0CC"
POINT_COLOR = "#F4B942"
GRADIENT_COLOR = "#FF6B6B"
DESCENT_COLOR = "#2EC4B6"


class GradientDirectionScene(Scene):
    """Teach that the gradient is uphill and descent goes the other way."""

    LEARNING_RATE = 0.1

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND_COLOR

        title = Text("Which way should the weight move?", font_size=42, color=NEUTRAL_COLOR)
        title.to_edge(UP, buff=0.25)
        axes = Axes(
            x_range=[1.5, 8.5, 1],
            y_range=[0, 13, 4],
            x_length=10.4,
            y_length=5.0,
            axis_config={"color": NEUTRAL_COLOR, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.35)
        x_label = Text("Weight", font_size=30, color=NEUTRAL_COLOR).next_to(axes.x_axis, DOWN, buff=0.18)
        y_label = Text("Loss", font_size=30, color=NEUTRAL_COLOR).next_to(axes.y_axis, LEFT, buff=0.18)
        curve = axes.plot(weight_loss, x_range=[1.5, 8.5], color=CURVE_COLOR, stroke_width=6)
        minimum = Dot(axes.c2p(5, 0), color=DESCENT_COLOR, radius=0.11)
        minimum_label = Text("Lowest loss", font_size=30, color=DESCENT_COLOR).next_to(minimum, UP, buff=0.22)
        five = Text("5", font_size=26, color=NEUTRAL_COLOR).next_to(axes.c2p(5, 0), DOWN, buff=0.2)

        self.play(Write(title), Create(axes), FadeIn(x_label, y_label), run_time=1.0)
        self.play(Create(curve), FadeIn(minimum, minimum_label, five), run_time=1.0)
        self.wait(0.8)

        permanent = VGroup(title, axes, x_label, y_label, curve, minimum, minimum_label, five)
        self._show_side(axes, start=7, probe=8)
        self._show_side(axes, start=3, probe=4)
        self.play(FadeOut(permanent), run_time=0.6)
        self._show_cheat_sheet()

    def _point(self, axes: Axes, weight: float):
        return axes.c2p(weight, weight_loss(weight))

    def _direction_arrow(self, axes: Axes, weight: float, *, descent: bool) -> Arrow:
        """Build an arrow from the derivative sign, never a hard-coded side."""

        sign = np.sign(weight_gradient(weight))
        direction = -sign if descent else sign
        center = self._point(axes, weight) + UP * 0.62
        return Arrow(
            center - RIGHT * direction * 0.08,
            center + RIGHT * direction * 1.15,
            buff=0,
            color=DESCENT_COLOR if descent else GRADIENT_COLOR,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.22,
        )

    def _show_side(self, axes: Axes, *, start: float, probe: float) -> None:
        tracker = ValueTracker(start)
        dot = always_redraw(lambda: Dot(self._point(axes, tracker.get_value()), color=POINT_COLOR, radius=0.15))
        current = Text(f"Current weight = {start:g}", font_size=34, color=POINT_COLOR)
        current.move_to((RIGHT if start > 5 else LEFT) * 4.45 + UP * 2.15)
        question = Text("What if weight increases?", font_size=34, color=NEUTRAL_COLOR).to_edge(UP, buff=0.95)

        self.play(FadeIn(dot), Write(current), run_time=0.55)
        self.play(Write(question), run_time=0.45)

        ghost_tracker = ValueTracker(start)
        ghost_dot = always_redraw(lambda: Dot(self._point(axes, ghost_tracker.get_value()), color=POINT_COLOR, radius=0.12, fill_opacity=0.45))
        ghost_path = axes.plot(
            weight_loss,
            x_range=[start, probe],
            color=POINT_COLOR,
            stroke_width=8,
            stroke_opacity=0.5,
        )
        result = Text(
            "Loss gets worse" if weight_loss(probe) > weight_loss(start) else "Loss gets better",
            font_size=34,
            color=GRADIENT_COLOR if weight_loss(probe) > weight_loss(start) else DESCENT_COLOR,
        ).to_edge(RIGHT if start > 5 else LEFT, buff=0.45).shift(DOWN * 0.5)
        self.add(ghost_dot)
        self.play(Create(ghost_path), ghost_tracker.animate.set_value(probe), run_time=0.85)
        self.play(Write(result), run_time=0.4)
        self.wait(0.35)
        self.play(FadeOut(ghost_dot, ghost_path, result, question), run_time=0.4)

        gradient_arrow = self._direction_arrow(axes, start, descent=False)
        descent_arrow = self._direction_arrow(axes, start, descent=True).shift(DOWN * 1.25)
        gradient_text = Text(
            "Gradient →" if weight_gradient(start) > 0 else "← Gradient",
            font_size=32,
            color=GRADIENT_COLOR,
        ).next_to(gradient_arrow, UP, buff=0.1)
        descent_text = Text(
            "Gradient descent ←" if weight_gradient(start) > 0 else "Gradient descent →",
            font_size=32,
            color=DESCENT_COLOR,
        ).next_to(descent_arrow, DOWN, buff=0.1)
        self.play(GrowArrow(gradient_arrow), Write(gradient_text), run_time=0.55)
        self.play(GrowArrow(descent_arrow), Write(descent_text), run_time=0.55)

        decrease = Text("Loss decreases", font_size=34, color=DESCENT_COLOR).to_edge(UP, buff=0.95)
        destination = gradient_descent_step(start, self.LEARNING_RATE)
        # Repeated mathematically valid steps produce a clear glide toward (not through) five.
        for _ in range(3):
            destination = gradient_descent_step(destination, self.LEARNING_RATE)
        self.play(Write(decrease), tracker.animate.set_value(destination), run_time=1.1)
        lesson = Text("Move opposite the gradient", font_size=38, color=NEUTRAL_COLOR).to_edge(DOWN, buff=0.12)
        self.play(Write(lesson), run_time=0.45)
        self.wait(0.45)
        self.play(FadeOut(dot, current, gradient_arrow, gradient_text, descent_arrow, descent_text, decrease, lesson), run_time=0.55)

    def _show_cheat_sheet(self) -> None:
        heading = Text("Gradient direction cheat sheet", font_size=44, color=NEUTRAL_COLOR).to_edge(UP, buff=0.35)
        center = VGroup(
            Text("Minimum", font_size=30, color=DESCENT_COLOR),
            Text("5", font_size=56, color=POINT_COLOR),
            Text("At 5", font_size=30, color=NEUTRAL_COLOR),
            Text("Gradient = 0", font_size=34, color=GRADIENT_COLOR),
        ).arrange(DOWN, buff=0.17).move_to(UP * 0.55)
        left = VGroup(
            Text("Current < 5", font_size=32, color=NEUTRAL_COLOR),
            Text("← Gradient", font_size=34, color=GRADIENT_COLOR),
            Text("Descent →", font_size=34, color=DESCENT_COLOR),
        ).arrange(DOWN, buff=0.28).move_to(LEFT * 4.25 + UP * 0.55)
        right = VGroup(
            Text("Current > 5", font_size=32, color=NEUTRAL_COLOR),
            Text("Gradient →", font_size=34, color=GRADIENT_COLOR),
            Text("Descent ←", font_size=34, color=DESCENT_COLOR),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 4.25 + UP * 0.55)
        rule = VGroup(
            Text("Gradient = uphill", font_size=40, color=GRADIENT_COLOR),
            Text("Gradient descent = opposite direction", font_size=40, color=DESCENT_COLOR),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        self.play(Write(heading), FadeIn(left, center, right), run_time=0.9)
        self.play(Write(rule), run_time=0.8)
        self.wait(2.0)
