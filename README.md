
# NASA Space Apps Cairo 2024 Chatbot
![Image](https://github.com/user-attachments/assets/c4c26111-6a7b-434c-9acd-a2a7708bc423)
## Project Overview

This project is a chatbot developed to assist participants in understanding the challenges presented during the NASA Space Apps Hackathon Cairo 2024. The chatbot interacts with users to provide information about various challenges, potential considerations, and outcome topics using a MySQL database.

## Features

- **Natural Language Processing**: Utilizes LangChain for processing user queries and generating relevant responses.
- **Speech Recognition**: Supports voice input for user queries.
- **Database Integration**: Connects to a MySQL database to fetch challenge-related data dynamically.

## Technology Stack

- **Python**: The primary programming language.
- **Streamlit**: For creating the web interface.
- **MySQL**: For managing challenge data.
- **LangChain**: For handling natural language processing tasks.
- **SpeechRecognition**: For converting speech to text.

## Files Included

- `chatbot.py`: The main application file containing the chatbot logic.
- `Test.py`: A test file for the chatbot interface.
- `modified_database.sql`: SQL script to set up the database schema and tables.
- `mentors_analysis.ipynb`: Jupyter notebook for analyzing mentor schedules.
- `Challanges Explanation.csv`: CSV file containing challenge details for database population.
- `mentors' System - Timetable.csv`: CSV file with mentor timetable data.

## How to Run the Project

1. **Install Dependencies**:
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up the Database**:
   Execute the `modified_database.sql` script in your MySQL server to create the necessary tables.

3. **Run the Application**:
   ```bash
   streamlit run chatbot.py
   ```

4. **Access the Chatbot**:
   Open your browser and go to `http://localhost:8501` to interact with the chatbot.

## Contribution

I contributed to developing this chatbot during my participation as a competition team member in the NASA Space Apps Cairo 2024 event. My role involved:

- Designing and implementing the chatbot's logic.
- Integrating the chatbot with the MySQL database to retrieve challenge information.
- Ensuring a user-friendly interface for participants.

**[Youssef Husseiny](https://github.com/yuseiff) - NASA Space Apps Cairo Competition Team 2024**
