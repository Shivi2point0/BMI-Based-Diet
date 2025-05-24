import reflex as rx
import openai
import os
from typing import TypedDict, List, Tuple, Optional


class UserData(TypedDict):
    weight_lbs: float
    height_in: float
    age: int
    gender: str
    goal_weight_lbs: float


class HealthState(rx.State):
    user_data: UserData | None = None
    bmi: float = 0.0
    daily_calories: float = 0.0
    daily_protein: float = 0.0
    recipes: List[str] = []
    is_loading_recipes: bool = False
    error_message: str = ""
    FORM_FIELDS: List[
        Tuple[str, str, str, Optional[str]]
    ] = [
        (
            "weight_lbs",
            "Weight (lbs)",
            "number",
            "e.g., 150",
        ),
        ("age", "Age", "number", "e.g., 30"),
        (
            "goal_weight_lbs",
            "Goal Weight (lbs)",
            "number",
            "e.g., 140",
        ),
    ]
    GENDERS: List[str] = ["male", "female"]

    def _calculate_bmi(
        self, weight_kg: float, height_m: float
    ) -> float:
        if height_m == 0:
            return 0.0
        return round(weight_kg / height_m**2, 1)

    def _calculate_bmr(
        self,
        weight_kg: float,
        height_cm: float,
        age: int,
        gender: str,
    ) -> float:
        if gender.lower() == "male":
            return (
                10 * weight_kg
                + 6.25 * height_cm
                - 5 * age
                + 5
            )
        else:
            return (
                10 * weight_kg
                + 6.25 * height_cm
                - 5 * age
                - 161
            )

    @rx.event
    def handle_form_submit(self, form_data: dict):
        self.error_message = ""
        try:
            height_ft = float(form_data["height_ft"])
            height_in_partial = float(
                form_data["height_in_partial"]
            )
            if (
                height_ft < 0
                or height_in_partial < 0
                or height_in_partial >= 12
            ):
                self.error_message = "Invalid height: ensure feet is non-negative and inches are between 0 and 11."
                self.user_data = None
                self.bmi = 0.0
                self.daily_calories = 0.0
                self.daily_protein = 0.0
                return
            total_height_in = (
                height_ft * 12 + height_in_partial
            )
            self.user_data = UserData(
                weight_lbs=float(form_data["weight_lbs"]),
                height_in=total_height_in,
                age=int(form_data["age"]),
                gender=form_data["gender"],
                goal_weight_lbs=float(
                    form_data["goal_weight_lbs"]
                ),
            )
            weight_kg = (
                self.user_data["weight_lbs"] * 0.453592
            )
            height_m = self.user_data["height_in"] * 0.0254
            height_cm = self.user_data["height_in"] * 2.54
            self.bmi = self._calculate_bmi(
                weight_kg, height_m
            )
            bmr = self._calculate_bmr(
                weight_kg,
                height_cm,
                self.user_data["age"],
                self.user_data["gender"],
            )
            tdee = bmr * 1.2
            calorie_adjustment = 0
            if (
                self.user_data["goal_weight_lbs"]
                < self.user_data["weight_lbs"]
            ):
                calorie_adjustment = -500
            elif (
                self.user_data["goal_weight_lbs"]
                > self.user_data["weight_lbs"]
            ):
                calorie_adjustment = 500
            self.daily_calories = round(
                tdee + calorie_adjustment
            )
            goal_weight_kg = (
                self.user_data["goal_weight_lbs"] * 0.453592
            )
            self.daily_protein = round(1.6 * goal_weight_kg)
            self.recipes = []
        except ValueError:
            self.error_message = "Invalid input. Please ensure all fields are filled correctly with numbers."
            self.user_data = None
            self.bmi = 0.0
            self.daily_calories = 0.0
            self.daily_protein = 0.0
        except KeyError:
            self.error_message = "Missing input. Please fill all fields, including feet and inches for height."
            self.user_data = None
            self.bmi = 0.0
            self.daily_calories = 0.0
            self.daily_protein = 0.0

    @rx.event(background=True)
    async def fetch_recipes(self):
        async with self:
            if (
                not self.user_data
                or self.daily_calories == 0
                or self.daily_protein == 0
            ):
                self.error_message = (
                    "Please calculate your diet plan first."
                )
                return
            self.is_loading_recipes = True
            self.recipes = []
            self.error_message = ""
        try:
            if not os.getenv("OPENAI_API_KEY"):
                async with self:
                    self.error_message = (
                        "OpenAI API key not configured."
                    )
                    self.is_loading_recipes = False
                return
            client = openai.AsyncOpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
            prompt = f"Generate 3 simple meal ideas (breakfast, lunch, dinner) for a diet with approximately {self.daily_calories} calories and {self.daily_protein}g of protein per day. Provide a brief description for each meal. Format as a list, e.g., 'Breakfast: [description]. Lunch: [description]. Dinner: [description].'"
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides meal suggestions.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=300,
                n=1,
                stop=None,
                temperature=0.7,
            )
            content = response.choices[0].message.content
            if content:
                meal_suggestions = []
                parts = {}
                current_meal = None
                for line in content.splitlines():
                    line_lower = line.lower()
                    if "breakfast:" in line_lower:
                        current_meal = "Breakfast"
                        parts[current_meal] = line.split(
                            ":", 1
                        )[1].strip()
                    elif "lunch:" in line_lower:
                        current_meal = "Lunch"
                        parts[current_meal] = line.split(
                            ":", 1
                        )[1].strip()
                    elif "dinner:" in line_lower:
                        current_meal = "Dinner"
                        parts[current_meal] = line.split(
                            ":", 1
                        )[1].strip()
                    elif (
                        current_meal
                        and line.strip()
                        and (
                            not (
                                ":" in line
                                and any(
                                    (
                                        m.lower()
                                        in line_lower
                                        for m in [
                                            "breakfast",
                                            "lunch",
                                            "dinner",
                                        ]
                                    )
                                )
                            )
                        )
                    ):
                        parts[current_meal] += (
                            " " + line.strip()
                        )
                if parts.get("Breakfast"):
                    meal_suggestions.append(
                        f"Breakfast: {parts['Breakfast']}"
                    )
                if parts.get("Lunch"):
                    meal_suggestions.append(
                        f"Lunch: {parts['Lunch']}"
                    )
                if parts.get("Dinner"):
                    meal_suggestions.append(
                        f"Dinner: {parts['Dinner']}"
                    )
                if not meal_suggestions:
                    meal_suggestions = [
                        line.strip()
                        for line in content.splitlines()
                        if line.strip()
                    ]
                async with self:
                    self.recipes = meal_suggestions
            else:
                async with self:
                    self.error_message = (
                        "No recipes received from AI."
                    )
        except Exception as e:
            async with self:
                self.error_message = (
                    f"Error fetching recipes: {str(e)}"
                )
        finally:
            async with self:
                self.is_loading_recipes = False