"""A compact visualization of a gradient-descent step."""

from collections.abc import Callable

from manim import (
    DOWN,
    LEFT,
    RIGHT,
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

CURVE_COLOR = "#5DA9E9"
NEUTRAL_COLOR = "#B8C0CC"
GOLD_COLOR = "#F4B942"
SLOPE_COLOR = "#FF6B6B"
ACTION_COLOR = "#2EC4B6"
BACKGROUND_COLOR = "#0B1020"


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
        self.camera.background_color = BACKGROUND_COLOR

        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[0, 6, 1],
            x_length=10,
            y_length=5.8,
            axis_config={
                "color": NEUTRAL_COLOR,
                "include_tip": False,
                "stroke_width": 3,
            },
        ).shift(DOWN * 0.25)
        axis_labels = axes.get_axis_labels(
            Text("Weight", font_size=30, color=NEUTRAL_COLOR),
            Text("Loss", font_size=30, color=NEUTRAL_COLOR),
        )
        curve = axes.plot(
            loss, x_range=[-2.4, 2.4], color=CURVE_COLOR, stroke_width=6
        )

        self.play(Create(axes), Create(curve), Write(axis_labels), run_time=1.8)

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
                color=GOLD_COLOR,
            )
        )
        start_marker = Dot(
            start_point,
            radius=0.14,
            color=GOLD_COLOR,
            fill_opacity=0.25,
            stroke_opacity=0.4,
        )
        current_loss_label = Text(
            "Current loss", font_size=30, color=GOLD_COLOR
        ).next_to(
            dot, LEFT, buff=0.3
        )
        self.play(
            FadeIn(start_marker),
            FadeIn(dot),
            Write(current_loss_label),
            run_time=1.2,
        )
        self.play(FadeOut(current_loss_label), run_time=0.3)

        tangent = axes.plot(
            tangent_function(start),
            x_range=[1.65, 2.25],
            color=SLOPE_COLOR,
            stroke_width=7,
        )
        slope_label = Text("slope", font_size=30, color=SLOPE_COLOR).move_to(
            axes.c2p(0.95, 4.8)
        )
        self.play(Create(tangent), Write(slope_label), run_time=1.3)
        self.wait(0.5)
        self.play(FadeOut(tangent), FadeOut(slope_label), run_time=0.6)

        direction_arrow = Arrow(
            axes.c2p(start, 0.55),
            axes.c2p(next_weight, 0.55),
            buff=0,
            color=ACTION_COLOR,
            stroke_width=7,
        )
        adjustment_label = Text(
            "Adjust weight", font_size=28, color=ACTION_COLOR
        ).next_to(direction_arrow, DOWN, buff=0.18)
        self.play(Create(direction_arrow), Write(adjustment_label), run_time=0.9)

        self.play(
            weight.animate.set_value(next_weight),
            run_time=2.4,
        )
        self.play(
            FadeOut(direction_arrow), FadeOut(adjustment_label), run_time=0.3
        )
        lower_loss = Text("Lower loss", font_size=34, color=ACTION_COLOR).next_to(
            end_point, RIGHT, buff=0.3
        )
        self.play(Write(lower_loss), run_time=1.0)
        self.wait(1.8)
