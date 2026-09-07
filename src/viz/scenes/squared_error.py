"""A beginner-friendly visualization of squared error for one example."""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    BraceBetweenPoints,
    Create,
    FadeIn,
    FadeOut,
    Line,
    Scene,
    Text,
    Transform,
    VGroup,
    Write,
)

from viz.calculations import squared_error

BACKGROUND_COLOR = "#0B1020"
NEUTRAL_COLOR = "#B8C0CC"
PREDICTION_COLOR = "#F4B942"
TARGET_COLOR = "#2EC4B6"
ERROR_COLOR = "#FF6B6B"
LOSS_COLOR = "#5DA9E9"


class SquaredErrorScene(Scene):
    """Explain squared error using one prediction-target example."""

    PREDICTION = 7
    TARGET = 5

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND_COLOR

        prediction = self.PREDICTION
        target = self.TARGET
        error = prediction - target
        loss = squared_error(prediction, target)

        line = Line(LEFT * 4.5, RIGHT * 4.5, color=NEUTRAL_COLOR, stroke_width=5)
        positions = {
            value: line.point_from_proportion((value - 4) / 4) for value in range(4, 9)
        }
        ticks = VGroup()
        number_labels = VGroup()
        for value, point in positions.items():
            ticks.add(Line(point + DOWN * 0.14, point + UP * 0.14, color=NEUTRAL_COLOR))
            number_labels.add(
                Text(str(value), font_size=30, color=NEUTRAL_COLOR).next_to(
                    point, DOWN, buff=0.25
                )
            )
        number_line = VGroup(line, ticks, number_labels).shift(DOWN * 0.35)

        target_point = positions[target] + DOWN * 0.35
        prediction_point = positions[prediction] + DOWN * 0.35
        target_marker = Line(
            target_point + DOWN * 0.22,
            target_point + UP * 0.22,
            color=TARGET_COLOR,
            stroke_width=9,
        )
        prediction_marker = Line(
            prediction_point + DOWN * 0.22,
            prediction_point + UP * 0.22,
            color=PREDICTION_COLOR,
            stroke_width=9,
        )
        prediction_label = Text(
            f"Prediction: {prediction}", font_size=42, color=PREDICTION_COLOR
        ).move_to(UP * 2.25 + RIGHT * 2.4)
        target_label = Text(
            f"Target: {target}", font_size=42, color=TARGET_COLOR
        ).move_to(UP * 2.25 + LEFT * 2.4)

        self.play(Create(number_line), run_time=1.0)
        self.play(FadeIn(prediction_marker), Write(prediction_label), run_time=0.8)
        self.play(FadeIn(target_marker), Write(target_label), run_time=0.8)
        self.wait(1.0)

        brace = BraceBetweenPoints(
            target_point + UP * 0.4,
            prediction_point + UP * 0.4,
            direction=UP,
            color=ERROR_COLOR,
        )
        error_label = Text(f"Error: {error}", font_size=42, color=ERROR_COLOR).next_to(
            brace, UP, buff=0.2
        )
        self.play(Create(brace), Write(error_label), run_time=0.8)
        self.wait(1.2)

        number_line_stage = VGroup(
            number_line,
            target_marker,
            prediction_marker,
            prediction_label,
            target_label,
            brace,
        )
        error_expression = Text(
            f"Error: {prediction} - {target} = {error}",
            font_size=52,
            color=ERROR_COLOR,
        )
        self.play(
            FadeOut(number_line_stage),
            Transform(error_label, error_expression),
            run_time=0.8,
        )
        self.wait(1.2)

        final_label = Text(
            f"Squared loss: {error} × {error} = {loss:g}",
            font_size=52,
            color=LOSS_COLOR,
        )
        self.play(Transform(error_label, final_label), run_time=0.8)
        self.wait(2.0)
