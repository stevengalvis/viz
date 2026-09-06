"""A compact visualization of a gradient-descent step."""

from collections.abc import Callable

from manim import (
    BLUE,
    DOWN,
    GREEN,
    RED,
    RIGHT,
    UL,
    UP,
    WHITE,
    YELLOW,
    Arrow,
    Axes,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    MathTex,
    Scene,
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
        ).add_coordinates()
        labels = axes.get_axis_labels(MathTex("w"), MathTex("L(w)"))
        curve = axes.plot(loss, x_range=[-2.4, 2.4], color=BLUE)
        equation = MathTex(r"L(w)=w^2", color=BLUE).to_corner(UL)

        self.play(Create(axes), Write(labels), run_time=1.2)
        self.play(Create(curve), Write(equation), run_time=1.2)

        start = self.START_WEIGHT
        gradient = 2 * start
        next_weight = start - self.LEARNING_RATE * gradient
        start_point = axes.c2p(start, loss(start))
        end_point = axes.c2p(next_weight, loss(next_weight))

        dot = Dot(start_point, color=YELLOW)
        guide = DashedLine(axes.c2p(start, 0), start_point, color=WHITE)
        weight_label = MathTex(r"w_0", color=YELLOW).next_to(dot)
        self.play(Create(guide), FadeIn(dot), Write(weight_label), run_time=0.8)

        tangent = axes.plot(
            tangent_function(start), x_range=[0.9, 2.35], color=RED
        )
        slope_label = MathTex(r"\nabla L(w_0)=2w_0>0", color=RED).to_edge(UP)
        self.play(Create(tangent), Write(slope_label), run_time=1.0)

        direction_arrow = Arrow(
            axes.c2p(start, 0.45),
            axes.c2p(next_weight, 0.45),
            buff=0,
            color=GREEN,
        )
        direction_label = MathTex(r"-\nabla L", color=GREEN).next_to(
            direction_arrow, direction=DOWN
        )
        self.play(Create(direction_arrow), Write(direction_label), run_time=0.8)

        end_guide = DashedLine(axes.c2p(next_weight, 0), end_point, color=WHITE)
        update = MathTex(
            r"w_1=w_0-\eta\nabla L(w_0)", color=GREEN
        ).to_edge(UP)
        self.play(
            dot.animate.move_to(end_point),
            FadeOut(guide),
            FadeOut(weight_label),
            FadeIn(end_guide),
            slope_label.animate.become(update),
            run_time=1.3,
        )
        new_label = MathTex(r"w_1", color=YELLOW).next_to(dot)
        lower_loss = MathTex(r"L(w_1)<L(w_0)", color=GREEN).next_to(
            new_label, direction=RIGHT
        )
        self.play(Write(new_label), Write(lower_loss), run_time=0.8)
        self.wait(0.5)
