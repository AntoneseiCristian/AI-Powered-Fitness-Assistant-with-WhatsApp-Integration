def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 2)

def get_recommendation(bmi):
    if bmi < 18.5:
        return "You are underweight. It's recommended to consult a nutritionist for a balanced diet plan."
    elif 18.5 <= bmi < 25:
        return "You have a normal weight. Keep maintaining a balanced diet and regular physical activity."
    elif 25 <= bmi < 30:
        return "You are overweight. Consider a balanced diet and regular physical activity. Consult a healthcare professional if needed."
    else:
        return "You are in the obesity range. It's highly recommended to consult a healthcare professional for guidance and support."


def calculate_recommended_bmi_and_weight(height):
    # Convert height from cm to m
    height_m = height / 100

    # Calculate the weight that corresponds to a BMI of 22
    recommended_weight = 22 * (height_m ** 2)

    # Calculate the BMI that corresponds to the recommended weight
    recommended_bmi = calculate_bmi(recommended_weight, height)

    return recommended_bmi, recommended_weight