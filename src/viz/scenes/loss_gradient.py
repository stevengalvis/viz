"""A compact visualization of a gradient-descent step."""

from collections.abc import Callable

from manim import (
    BLUE,
    DOWN,
    GREEN,
    LEFT,
    RED,
    RIGHT,
    YELLOW,
    Arrow,
    Axes,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Scene,
    Text,
    ValueTracker,
    Write,
    always_redraw,
)


def loss(weight: float) -> float:
    """Return the scalar convex loss used in this proof of concept."""

    return weight**2


def tangent_function(weight: float) -> Callable[[float], float]:
    """Build the tangent to ``loss`` at ``weight``."""

    slope = 2 * weight
    return lambda x: loss(weight) + slope * (x - weight)


class LossGradientScene(Scene):
    """Show one gradient-descent step on :math:`L(w) = w^2`."""

    START_WEIGHT = 2.0
    LEARNING_RATE = 0.2

    def construct(self) -> None:
        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[0, 6, 1],
            x_length=10,
            y_length=5.8,
            axis_config={"include_tip": False, "stroke_width": 3},
        ).shift(DOWN * 0.25)
        axis_labels = axes.get_axis_labels(
            Text("Weight", font_size=30), Text("Loss", font_size=30)
        )
        curve = axes.plot(
            loss, x_range=[-2.4, 2.4], color=BLUE, stroke_width=6
        )

        self.play(Create(axes), Create(curve), Write(axis_labels), run_time=1.5)

        start = self.START_WEIGHT
        gradient = 2 * start
        next_weight = start - self.LEARNING_RATE * gradient
        start_point = axes.c2p(start, loss(start))
        end_point = axes.c2p(next_weight, loss(next_weight))

        weight = ValueTracker(start)
        dot = always_redraw(
            lambda: Dot(
                axes.c2p(weight.get_value(), loss(weight.get_value())),
                radius=0.16,
                color=YELLOW,
            )
        )
        start_marker = Dot(
            start_point,
            radius=0.14,
            color=YELLOW,
            fill_opacity=0.25,
            stroke_opacity=0.4,
        )
        weight_label = Text("Start here", font_size=30, color=YELLOW).next_to(
            dot, LEFT, buff=0.3
        )
        self.play(
            FadeIn(start_marker), FadeIn(dot), Write(weight_label), run_time=1.0
        )

        tangent = axes.plot(
            tangent_function(start),
            x_range=[1.65, 2.25],
            color=RED,
            stroke_width=7,
        )
        slope_label = Text("slope", font_size=30, color=RED).move_to(
            axes.c2p(0.95, 4.8)
        )
        self.play(Create(tangent), Write(slope_label), run_time=1.0)
        self.wait(0.3)
        self.play(FadeOut(tangent), FadeOut(slope_label), run_time=0.5)

        direction_arrow = Arrow(
            axes.c2p(start, 0.55),
            axes.c2p(next_weight, 0.55),
            buff=0,
            color=GREEN,
            stroke_width=7,
        )
        self.play(Create(direction_arrow), run_time=0.7)

        self.play(
            weight.animate.set_value(next_weight),
            FadeOut(weight_label),
            FadeOut(direction_arrow),
            run_time=1.8,
        )
        lower_loss = Text("lower loss", font_size=34, color=GREEN).next_to(
            end_point, RIGHT, buff=0.3
        )
        self.play(Write(lower_loss), run_time=0.8)
        self.wait(1.5)
