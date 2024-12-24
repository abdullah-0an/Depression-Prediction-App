import pandas as pd
import joblib
import re
import streamlit as st

# Load the saved model
model = joblib.load('model.pkl')

# Load the label encoders using sanitized filenames
categorical_columns = [
    'Gender', 
    'Working Professional or Student', 
    'Profession', 
    'Sleep Duration', 
    'Dietary Habits', 
    'Degree', 
    'Have you ever had suicidal thoughts ?',
    'Family History of Mental Illness'
]

label_encoders = {}
for column in categorical_columns:
    sanitized_column = re.sub(r'[^a-zA-Z0-9]', '_', column)  # Sanitize column name
    label_encoders[column] = joblib.load(f'label_encoder_{sanitized_column}.pkl')

# Streamlit Interface
st.set_page_config(page_title="Mental Health Prediction App", page_icon="🧠", layout="centered")
st.title("Mental Health Prediction App 🧠")

# Add some description
st.markdown("""
Welcome to the **Mental Health Prediction App**!  
Here, you can input your personal information, and based on machine learning, we will predict whether you may be at risk for depression.
""")

# Create an informative sidebar
st.sidebar.title("Input Your Data")
st.sidebar.markdown("Please provide the following details:")

# Input fields for user data
age = st.sidebar.slider("Age", 18, 80, 25)
gender = st.sidebar.selectbox("Gender", ["Female", "Male"])
profession = st.sidebar.selectbox("Profession", ['Chef', 'Teacher', 'Business Analyst', 'Financial Analyst', 'Chemist', 'Electrician', 'Other'])
sleep_duration = st.sidebar.selectbox("Sleep Duration", ["Less than 5 hours", "5-6 hours", "7-8 hours", "More than 8 hours"])
dietary_habits = st.sidebar.selectbox("Dietary Habits", ["Healthy", "Moderate", "Unhealthy"])
degree = st.sidebar.selectbox("Degree", ['BHM', 'LLB', 'B.Pharm', 'BBA', 'MCA', 'MD', 'BSc', 'ME'])
suicidal_thoughts = st.sidebar.selectbox("Have you ever had suicidal thoughts?", ['Yes', 'No'])
family_history = st.sidebar.selectbox("Family History of Mental Illness", ['Yes', 'No'])

# New input fields for the additional features
academic_pressure = st.sidebar.slider("Academic Pressure", 0.0, 10.0, 5.0, step=0.1)
work_pressure = st.sidebar.slider("Work Pressure", 0.0, 10.0, 5.0, step=0.1)
cgpa = st.sidebar.slider("CGPA", 0.0, 10.0, 7.0, step=0.1)
study_satisfaction = st.sidebar.slider("Study Satisfaction", 0.0, 10.0, 5.0, step=0.1)
job_satisfaction = st.sidebar.slider("Job Satisfaction", 0.0, 10.0, 5.0, step=0.1)
work_study_hours = st.sidebar.slider("Work/Study Hours", 0.0, 16.0, 8.0, step=0.5)
financial_stress = st.sidebar.slider("Financial Stress", 0.0, 10.0, 5.0, step=0.1)

# Button to trigger prediction
if st.sidebar.button("Predict Depression"):

    # Prepare input data for prediction
    input_data = pd.DataFrame({
        'Age': [age],
        'Academic Pressure': [academic_pressure],
        'Work Pressure': [work_pressure],
        'CGPA': [cgpa],
        'Study Satisfaction': [study_satisfaction],
        'Job Satisfaction': [job_satisfaction],
        'Work/Study Hours': [work_study_hours],
        'Financial Stress': [financial_stress],
        'Gender': [gender],
        'Working Professional or Student': ['Working Professional' if 'Working Professional' in profession else 'Student'],
        'Profession': [profession],
        'Sleep Duration': [sleep_duration],
        'Dietary Habits': [dietary_habits],
        'Degree': [degree],
        'Have you ever had suicidal thoughts ?': [suicidal_thoughts],
        'Family History of Mental Illness': [family_history]
    })

    # Encode categorical data using the loaded encoders
    for column in categorical_columns:
        input_data[column] = label_encoders[column].transform(input_data[column])

    # Display a loading spinner while prediction is being made
    with st.spinner('Making prediction...'):
        # Make prediction using the trained model
        prediction = model.predict(input_data)

    # Display the result with emoji-based feedback
    if prediction == 1:
        st.success("🧠 The person may be **depressed**.")
    else:
        st.success("😊 The person may **not be depressed**.")

# Add a footer for engagement
st.markdown("---")
st.markdown("""
    Made with ❤️ by the Mental Health Prediction Team  
    [More Info](https://www.mentalhealth.org/)
""")
