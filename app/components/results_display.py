import reflex as rx
from app.states.health_state import HealthState


def results_display() -> rx.Component:
    return rx.cond(
        HealthState.user_data,
        rx.el.div(
            rx.el.h3(
                "Your Personalized Plan",
                class_name="text-xl font-semibold text-gray-800 mb-4",
            ),
            rx.el.div(
                rx.el.p(
                    rx.el.strong("BMI: "),
                    HealthState.bmi.to_string(),
                    class_name="text-gray-700",
                ),
                rx.el.p(
                    rx.el.strong(
                        "Recommended Daily Calories: "
                    ),
                    HealthState.daily_calories.to_string(),
                    " kcal",
                    class_name="text-gray-700",
                ),
                rx.el.p(
                    rx.el.strong(
                        "Recommended Daily Protein: "
                    ),
                    HealthState.daily_protein.to_string(),
                    " g",
                    class_name="text-gray-700",
                ),
                class_name="space-y-2 p-4 bg-blue-50 rounded-md border border-blue-200",
            ),
        ),
        rx.el.div(),
    )