def calculate_sugar_intake(calories, percentage=10):
    sugar_calories = calories * (percentage / 100)
    sugar_grams = sugar_calories / 4
    return sugar_grams

def calculate_calories_based_on_age(gender, age, height, weight, activity_level):
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    if activity_level == 'low':
        factor = 1.2
    elif activity_level == 'medium':
        factor = 1.55
    elif activity_level == 'high':
        factor = 1.725
    else:
        factor = 1.2  # Default factor if something goes wrong

    tdee = bmr * factor
    return tdee