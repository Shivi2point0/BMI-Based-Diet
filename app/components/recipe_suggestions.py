import reflex as rx
from app.states.health_state import HealthState


def recipe_suggestions() -> rx.Component:
    return rx.cond(
        HealthState.user_data,
        rx.el.div(
            rx.el.button(
                "Get Recipe Suggestions",
                on_click=HealthState.fetch_recipes,
                class_name="mt-6 w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50",
                disabled=HealthState.is_loading_recipes
                | (HealthState.daily_calories == 0),
            ),
            rx.cond(
                HealthState.is_loading_recipes,
                rx.el.div(
                    rx.el.p(
                        "Loading recipes...",
                        class_name="text-center text-gray-600 mt-4",
                    ),
                    class_name="flex justify-center items-center h-20",
                ),
                rx.el.div(),
            ),
            rx.cond(
                HealthState.recipes.length() > 0,
                rx.el.div(
                    rx.el.h4(
                        "Meal Ideas:",
                        class_name="text-lg font-semibold text-gray-800 mt-6 mb-3",
                    ),
                    rx.el.ul(
                        rx.foreach(
                            HealthState.recipes,
                            lambda recipe: rx.el.li(
                                recipe,
                                class_name="text-gray-700 p-2 bg-green-50 border-l-4 border-green-500 mb-2 rounded",
                            ),
                        ),
                        class_name="list-none space-y-2",
                    ),
                    class_name="mt-4 p-4 bg-white rounded-lg shadow",
                ),
                rx.el.div(),
            ),
            class_name="mt-6",
        ),
        rx.el.div(),
    )