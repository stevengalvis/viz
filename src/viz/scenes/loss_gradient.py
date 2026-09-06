"""A compact visualization of a gradient-descent step."""

from collections.abc import Callable

from manim import (
    BLUE,
    DOWN,
    GREEN,
    RED,
    RIGHT,
    UP,
    YELLOW,
    Arrow,
    Axes,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    MathTex,
    Scene,
    Text,
    Write,
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
            x_length=7,
            y_length=4.5,
            axis_config={"include_tip": False},
        )
        curve = axes.plot(loss, x_range=[-2.4, 2.4], color=BLUE)
        equation = MathTex(r"L(w)=w^2", color=BLUE).next_to(axes, UP)

        self.play(Create(axes), Create(curve), Write(equation), run_time=1.3)

        start = self.START_WEIGHT
        gradient = 2 * start
        next_weight = start - self.LEARNING_RATE * gradient
        start_point = axes.c2p(start, loss(start))
        end_point = axes.c2p(next_weight, loss(next_weight))

        dot = Dot(start_point, color=YELLOW)
        weight_label = Text("current weight", font_size=28, color=YELLOW).next_to(
            dot, UP
        )
        self.play(FadeIn(dot), Write(weight_label), run_time=0.8)

        tangent = axes.plot(
            tangent_function(start), x_range=[0.9, 2.35], color=RED
        )
        slope_label = Text("slope", font_size=28, color=RED).next_to(
            tangent, RIGHT
        )
        self.play(Create(tangent), Write(slope_label), run_time=1.0)

        direction_arrow = Arrow(
            start_point + DOWN * 0.4,
            end_point + UP * 0.25,
            buff=0.1,
            color=GREEN,
        )
        direction_label = Text("move downhill", font_size=28, color=GREEN).next_to(
            direction_arrow, DOWN
        )
        self.play(Create(direction_arrow), Write(direction_label), run_time=0.9)

        self.play(
            dot.animate.move_to(end_point),
            FadeOut(weight_label),
            FadeOut(tangent),
            FadeOut(slope_label),
            FadeOut(direction_arrow),
            FadeOut(direction_label),
            run_time=1.3,
        )
        lower_loss = Text("lower loss", font_size=32, color=GREEN).next_to(dot, RIGHT)
        self.play(Write(lower_loss), run_time=0.8)
        self.wait(0.6)
