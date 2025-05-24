import reflex as rx
from app.states.health_state import HealthState
from app.components.user_input_form import user_input_form
from app.components.results_display import results_display
from app.components.recipe_suggestions import (
    recipe_suggestions,
)
from rxconfig import config


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "SimplyNourished",
                        class_name="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl md:text-6xl",
                    ),
                    class_name="flex items-center gap-4 mb-2",
                ),
                rx.el.p(
                    "Enter your details to get a personalized diet plan and recipe suggestions.",
                    class_name="text-lg text-gray-600 mb-8",
                ),
                rx.el.div(
                    user_input_form(),
                    class_name="mb-8 w-full max-w-lg",
                ),
                rx.cond(
                    HealthState.error_message != "",
                    rx.el.div(
                        HealthState.error_message,
                        class_name="p-4 mb-4 text-sm text-red-700 bg-red-100 rounded-lg border border-red-300",
                        role="alert",
                    ),
                    rx.el.div(),
                ),
                rx.cond(
                    HealthState.user_data,
                    rx.el.div(
                        results_display(),
                        recipe_suggestions(),
                        class_name="mt-8 w-full max-w-lg",
                    ),
                    rx.el.div(),
                ),
                class_name="flex flex-col items-center justify-center min-h-screen py-12 px-4 sm:px-6 lg:px-8",
            ),
            class_name="font-['Inter'] bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50",
        )
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(
            rel="preconnect",
            href="https://fonts.googleapis.com",
        ),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            crossorigin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, title="SimplyNourished")