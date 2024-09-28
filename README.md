# NutriScan

**NutriScan** is a web-based solution designed to simplify food safety for health-conscious individuals. The platform helps users analyze food items based on their medical conditions or dietary restrictions, providing personalized dietary guidance.

## Problem Statement

Many food products pose health risks to individuals with certain medical conditions. It can be challenging for patients to identify safe food options, and they often lack personalized guidance. Additionally, there is limited access to reliable information about ingredients, allergens, and alternatives to unhealthy choices.

Key challenges include:
- Difficulty identifying safe foods based on health conditions.
- Lack of personalized dietary guidance.
- Limited access to reliable ingredient safety information.
- Risk of trial and error, compromising health.
- Finding suitable alternatives that meet dietary needs.

## Solution

NutriScan solves these challenges by offering a personalized food analysis platform. Users can input health conditions or prescriptions, and the system will analyze food items based on their names, images, or ingredient lists. It evaluates the safety of these foods, suggests alternatives if needed, and offers consumption guidelines to help users make informed dietary decisions.

## Target Audience

NutriScan is designed for:
- Individuals with chronic health conditions (e.g., diabetes, hypertension, food allergies).
- Patients with specific dietary restrictions based on medical prescriptions.
- Health-conscious consumers aiming to improve their nutrition.
- Caregivers and healthcare professionals seeking dietary tools for patients.
- Fitness enthusiasts looking to optimize their diet for performance.

## Market Selection

NutriScan has potential applications in the following markets:
- **Healthcare Sector**: Hospitals, clinics, and nutritionists providing dietary guidance.
- **Food and Beverage Industry**: Health-oriented companies interested in collaboration.
- **Wellness and Lifestyle**: Catering to the demand for personalized health tech solutions.
- **E-commerce Platforms**: Online grocery stores and health food retailers enhancing their offerings.
- **Educational Institutions**: Promoting healthy eating habits in schools and universities.
- **Technologically Savvy Consumers**: Younger demographics familiar with health apps and tech-driven solutions.

## Process Flow

1. **User Input**: Users input health conditions or dietary requirements.
2. **Food Item Submission**: Food items can be submitted via name, image, or ingredient list.
3. **Data Analysis**: NutriScan processes the input using ML models and APIs.
4. **Suitability Check**: The system determines whether the food is safe to consume.
5. **Report Generation**: A detailed report is generated for the user.
6. **Alternative Suggestions**: If necessary, safe alternatives are suggested.
7. **Real-time Feedback**: The platform provides real-time feedback based on analysis.
8. **Recommendations and Advice**: Users receive personalized dietary recommendations.

## Tech Stack

The NutriScan platform is built with the following technologies:
- **Flask (Python)**: Backend framework to handle routing and server-side logic.
- **HTML & Bootstrap**: For responsive and user-friendly frontend design.
- **Tailwind CSS**: Modern CSS framework for styling.
- **VGG19**: A machine learning model used for food image classification.
- **Gemini API**: Currently used for data parsing and analysis, which will later be replaced by a custom ML model.

## Future Developments

In future iterations, NutriScan will transition to a self-developed machine learning model to enhance the accuracy and depth of food analysis. This upgrade aims to provide users with even more precise dietary recommendations.

---