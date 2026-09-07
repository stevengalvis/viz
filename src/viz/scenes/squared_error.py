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
    Square,
    Text,
    VGroup,
    Write,
)

from viz.calculations import squared_error

BACKGROUND_COLOR = "#0B1020"
NEUTRAL_COLOR = "#B8C0CC"
PREDICTION_COLOR = "#F4B942"
TARGET_COLOR = "#2EC4B6"
ERROR_COLOR = "#FF6B6B"
SQUARE_COLOR = "#5DA9E9"


class SquaredErrorScene(Scene):
    """Explain squared error geometrically using one prediction."""

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
        self.wait(1.5)

        first_stage = VGroup(
            number_line,
            target_marker,
            prediction_marker,
            prediction_label,
            target_label,
            brace,
            error_label,
        )
        self.play(FadeOut(first_stage), run_time=0.6)

        square = Square(side_length=3.2, color=SQUARE_COLOR, stroke_width=6).shift(
            DOWN * 0.15
        )
        divider_v = Line(
            square.get_top(), square.get_bottom(), color=SQUARE_COLOR, stroke_width=4
        )
        divider_h = Line(
            square.get_left(), square.get_right(), color=SQUARE_COLOR, stroke_width=4
        )
        grid = VGroup(square, divider_v, divider_h)
        side_label = Text(f"error = {error}", font_size=34, color=ERROR_COLOR).next_to(
            square, LEFT, buff=0.45
        )
        equation = Text(
            f"{error} × {error} = {loss:g}", font_size=48, color=NEUTRAL_COLOR
        ).next_to(square, RIGHT, buff=0.65)
        self.play(Create(grid), Write(side_label), run_time=1.2)
        self.play(Write(equation), run_time=0.8)
        self.wait(0.8)

        final_label = Text(
            f"Squared loss: {loss:g}", font_size=50, color=SQUARE_COLOR
        ).to_edge(UP, buff=0.55)
        self.play(FadeIn(final_label), run_time=0.7)
        self.wait(2.0)
