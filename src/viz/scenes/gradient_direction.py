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
    DecimalNumber,
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

BACKGROUND_COLOR = "#05070B"
CURVE_COLOR = "#8B5CF6"
NEUTRAL_COLOR = "#C7CEDB"
POINT_COLOR = "#F59E0B"
GRADIENT_COLOR = "#EF4444"
DESCENT_COLOR = "#22C55E"


class GradientDirectionScene(Scene):
    """Teach that the gradient is uphill and descent goes the other way."""

    LEARNING_RATE = 0.1

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND_COLOR

        title = Text(
            "Which way should the weight move?",
            font_size=42,
            color=NEUTRAL_COLOR,
        )
        title.to_edge(UP, buff=0.25)
        axes = Axes(
            x_range=[1.5, 8.5, 1],
            y_range=[0, 13, 4],
            x_length=10.4,
            y_length=5.0,
            axis_config={"color": NEUTRAL_COLOR, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.35)
        # Keep the axis name at the right end, away from the tick at five.
        x_label = Text("Weight", font_size=30, color=NEUTRAL_COLOR).next_to(
            axes.x_axis.get_right(), DOWN, buff=0.22
        ).align_to(axes.x_axis, RIGHT)
        y_label = Text("Loss", font_size=30, color=NEUTRAL_COLOR).next_to(
            axes.y_axis, LEFT, buff=0.18
        )
        curve = axes.plot(
            weight_loss, x_range=[1.5, 8.5], color=CURVE_COLOR, stroke_width=6
        )
        minimum = Dot(axes.c2p(5, 0), color=DESCENT_COLOR, radius=0.11)
        minimum_label = Text(
            "Lowest loss", font_size=30, color=DESCENT_COLOR
        ).next_to(minimum, UP, buff=0.22)
        five = Text("5", font_size=26, color=NEUTRAL_COLOR).next_to(
            axes.c2p(5, 0), DOWN, buff=0.2
        )

        self.play(Write(title), run_time=0.7)
        self.play(Create(axes), FadeIn(x_label, y_label), run_time=0.8)
        self.play(Create(curve), run_time=1.0)
        self.play(FadeIn(minimum, minimum_label, five), run_time=0.6)
        self.wait(1.0)

        permanent = VGroup(title, axes, x_label, y_label, curve, minimum, minimum_label, five)
        self._show_side(axes, start=7, probe=8)
        self._show_side(axes, start=3, probe=4)
        self.play(FadeOut(permanent), run_time=0.7)
        self._show_cheat_sheet()

    def _point(self, axes: Axes, weight: float):
        return axes.c2p(weight, weight_loss(weight))

    def _direction_arrow(self, axes: Axes, weight: float, *, descent: bool) -> Arrow:
        """Build an arrow from the derivative sign, never a hard-coded side."""

        sign = np.sign(weight_gradient(weight))
        direction = -sign if descent else sign
        side = RIGHT if weight > 5 else LEFT
        # Reserve the open area inside the bowl, above the moving dots.
        # Center each arrow so its label stays in the same safe column.
        center = axes.c2p(5, 0) + side * 2.0 + UP * (3.1 if descent else 4.3)
        return Arrow(
            center - RIGHT * direction * 0.615,
            center + RIGHT * direction * 0.615,
            buff=0,
            color=DESCENT_COLOR if descent else GRADIENT_COLOR,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.22,
        )

    def _show_side(self, axes: Axes, *, start: float, probe: float) -> None:
        tracker = ValueTracker(start)
        dot = always_redraw(
            lambda: Dot(
                self._point(axes, tracker.get_value()),
                color=POINT_COLOR,
                radius=0.15,
            )
        )
        side = RIGHT if start > 5 else LEFT
        current_prefix = Text("Current weight =", font_size=34, color=POINT_COLOR)
        current_value = DecimalNumber(
            tracker.get_value(),
            num_decimal_places=2,
            group_with_commas=False,
            edge_to_fix=LEFT,
            mob_class=Text,
            font_size=34,
            color=POINT_COLOR,
        )
        current = VGroup(current_prefix, current_value).arrange(
            RIGHT, buff=0.15
        ).move_to(side * 3.35 + UP * 2.65)

        self.play(FadeIn(dot), Write(current), run_time=0.7)
        # Attach only after Write completes, and bind to the MAIN tracker.
        # DecimalNumber keeps its left edge fixed as the digits change.
        current_value.add_updater(lambda number: number.set_value(tracker.get_value()))
        self.wait(0.4)

        ghost_tracker = ValueTracker(start)
        ghost_dot = always_redraw(
            lambda: Dot(
                self._point(axes, ghost_tracker.get_value()),
                color=POINT_COLOR,
                radius=0.12,
                fill_opacity=0.45,
            )
        )
        ghost_path = axes.plot(
            weight_loss,
            x_range=[start, probe],
            color=POINT_COLOR,
            stroke_width=8,
            stroke_opacity=0.5,
        )
        got_worse = weight_loss(probe) > weight_loss(start)
        result = Text(
            "Worse" if got_worse else "Better",
            font_size=34,
            color=GRADIENT_COLOR if got_worse else DESCENT_COLOR,
        ).move_to(side * 4.35 + DOWN * 0.15)
        self.add(ghost_dot)
        self.play(
            Create(ghost_path),
            ghost_tracker.animate.set_value(probe),
            run_time=1.0,
        )
        self.play(Write(result), run_time=0.35)
        self.wait(0.4)
        self.play(FadeOut(ghost_dot, ghost_path, result), run_time=0.35)
        self.wait(0.15)

        gradient_arrow = self._direction_arrow(axes, start, descent=False)
        descent_arrow = self._direction_arrow(axes, start, descent=True)
        gradient_text = Text(
            "Gradient →" if weight_gradient(start) > 0 else "Gradient ←",
            font_size=32,
            color=GRADIENT_COLOR,
        ).next_to(gradient_arrow, UP, buff=0.08)
        descent_text = Text(
            "Descent ←" if weight_gradient(start) > 0 else "Descent →",
            font_size=32,
            color=DESCENT_COLOR,
        ).next_to(descent_arrow, DOWN, buff=0.08)
        self.play(GrowArrow(gradient_arrow), Write(gradient_text), run_time=0.55)
        self.wait(0.2)
        self.play(GrowArrow(descent_arrow), Write(descent_text), run_time=0.55)
        self.wait(0.3)

        destination = gradient_descent_step(start, self.LEARNING_RATE)
        # Repeated mathematically valid steps produce a clear glide toward (not through) five.
        for _ in range(3):
            destination = gradient_descent_step(destination, self.LEARNING_RATE)
        self.play(tracker.animate.set_value(destination), run_time=1.3)
        self.wait(0.35)
        # Freeze the finished readout before fading; an updater must not
        # recreate fully opaque digits while FadeOut is running.
        current_value.set_value(tracker.get_value())
        current_value.clear_updaters()
        self.play(
            FadeOut(
                dot,
                current,
                gradient_arrow,
                gradient_text,
                descent_arrow,
                descent_text,
            ),
            run_time=0.45,
        )

    def _show_cheat_sheet(self) -> None:
        center = VGroup(
            Text("At 5", font_size=34, color=NEUTRAL_COLOR),
            Text("Gradient = 0", font_size=34, color=GRADIENT_COLOR),
        ).arrange(DOWN, buff=0.28).move_to(UP * 1.0)
        left = VGroup(
            Text("Current < 5", font_size=32, color=NEUTRAL_COLOR),
            Text("Gradient ←", font_size=34, color=GRADIENT_COLOR),
            Text("Descent →", font_size=34, color=DESCENT_COLOR),
        ).arrange(DOWN, buff=0.32).move_to(LEFT * 4.35 + UP * 1.0)
        right = VGroup(
            Text("Current > 5", font_size=32, color=NEUTRAL_COLOR),
            Text("Gradient →", font_size=34, color=GRADIENT_COLOR),
            Text("Descent ←", font_size=34, color=DESCENT_COLOR),
        ).arrange(DOWN, buff=0.32).move_to(RIGHT * 4.35 + UP * 1.0)
        rule = Text(
            "Gradient points uphill. Descent goes the other way.",
            font_size=38,
            color=DESCENT_COLOR,
        ).to_edge(DOWN, buff=0.65)
        self.play(FadeIn(left, center, right), run_time=1.0)
        self.wait(0.5)
        self.play(Write(rule), run_time=0.8)
        self.wait(2.0)
