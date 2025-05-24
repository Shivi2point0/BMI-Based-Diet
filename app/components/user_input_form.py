import reflex as rx
from app.states.health_state import HealthState
from typing import Optional

COMMON_INPUT_CLASS = "block px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"


def _standard_input_field(
    name: str,
    label_text: str,
    placeholder: Optional[str],
    input_type: str = "number",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label_text,
            html_for=name,
            class_name="block text-sm font-medium text-gray-700",
        ),
        rx.el.input(
            type=input_type,
            name=name,
            id=name,
            placeholder=placeholder,
            required=True,
            min=rx.cond(input_type == "number", "0", None),
            class_name=f"mt-1 w-full {COMMON_INPUT_CLASS}",
        ),
    )


def user_input_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            _standard_input_field(
                name="weight_lbs",
                label_text="Weight (lbs)",
                placeholder="e.g., 150",
            ),
            rx.el.div(
                rx.el.label(
                    "Height",
                    html_for="height_ft",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.div(
                    rx.el.input(
                        type="number",
                        name="height_ft",
                        id="height_ft",
                        placeholder="Feet",
                        required=True,
                        min="0",
                        class_name=f"{COMMON_INPUT_CLASS} flex-1 min-w-0",
                    ),
                    rx.el.span(
                        "ft",
                        class_name="text-sm text-gray-600 self-center whitespace-nowrap",
                    ),
                    rx.el.input(
                        type="number",
                        name="height_in_partial",
                        id="height_in_partial",
                        placeholder="Inches",
                        required=True,
                        min="0",
                        max="11",
                        step="1",
                        class_name=f"{COMMON_INPUT_CLASS} flex-1 min-w-0",
                    ),
                    rx.el.span(
                        "in",
                        class_name="text-sm text-gray-600 self-center whitespace-nowrap",
                    ),
                    class_name="mt-1 flex gap-x-2 items-center",
                ),
            ),
            _standard_input_field(
                name="age",
                label_text="Age",
                placeholder="e.g., 30",
            ),
            _standard_input_field(
                name="goal_weight_lbs",
                label_text="Goal Weight (lbs)",
                placeholder="e.g., 140",
            ),
            rx.el.div(
                rx.el.label(
                    "Gender",
                    html_for="gender",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.select(
                    rx.foreach(
                        HealthState.GENDERS,
                        lambda gender: rx.el.option(
                            gender.capitalize(),
                            value=gender,
                        ),
                    ),
                    name="gender",
                    id="gender",
                    required=True,
                    class_name=f"mt-1 block w-full {COMMON_INPUT_CLASS}",
                ),
                class_name="mb-2",
            ),
            rx.el.button(
                "Calculate Diet Plan",
                type="submit",
                class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-500 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
            ),
            class_name="space-y-4",
        ),
        on_submit=HealthState.handle_form_submit,
        reset_on_submit=True,
        class_name="p-6 bg-white rounded-lg shadow-md",
    )