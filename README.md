# Serendib Guide – Intelligent Travel Chatbot for Sri Lanka 🇱🇰

Serendib Guide is an intelligent, user-friendly travel assistant chatbot built using Rasa (NLU engine), Flask (API bridge), and MySQL (data layer). It helps users plan trips, explore destinations in Sri Lanka, and receive real-time travel suggestions using natural language queries.

🧠 Built as part of the AI Coursework 2 for the Artificial Intelligence module in the BEng (Hons) in Software Engineering (Top-Up) degree program, offered by London Metropolitan University through ESOFT Metro Campus, Kurunegala, Sri Lanka.

---

## 📂 Project Overview

This project demonstrates how conversational AI can be applied in the travel domain by integrating:
- Natural Language Understanding (NLU) using Rasa
- Flask-based middleware to handle web requests
- MySQL for dynamic travel data retrieval
- A responsive frontend UI for interactive chatting

Users can:
- Ask about travel destinations (e.g., “Tell me about Ella”)
- Plan trips with duration and budget (e.g., “Plan a 2-day trip to Nuwara Eliya with 15000 LKR”)
- Get greetings, travel suggestions, and assistance interactively

---

## 👥 Project Contributors

- Kalana Jayasekara
- Sanupa Marapana

Group Project for AI Coursework 2 (Artificial Intelligence module)

---

## 👨‍🏫 Acknowledgements

We would like to express our sincere gratitude to our module lecturer, Mr. Kalana Amarasekara, for his continuous support, guidance, and encouragement throughout the development of this project.

---

## 🏗️ Technologies Used

- Rasa Open Source (NLU + Core)
- Python 3.10
- Flask
- MySQL
- HTML, CSS, JavaScript (Frontend UI)
- RESTful APIs
- VS Code, GitHub

---

## 🚀 Getting Started

Follow these steps to install and run the chatbot locally.

### Prerequisites

- Python 3.8+ → https://www.python.org/downloads/
- Rasa → https://rasa.com/docs/rasa/installation/
- MySQL Server → https://dev.mysql.com/downloads/mysql/
- Git → https://git-scm.com/downloads

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/serendib-guide.git
   cd serendib-guide
   ```

2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your MySQL database:
   - Ensure MySQL is running
   - Update DB connection details in actions.py

5. Train the chatbot:
   ```bash
   rasa train
   ```

6. Start the Rasa server:
   ```bash
   rasa run actions & rasa run
   ```

7. Start the Flask server:
   ```bash
   python app.py
   ```

8. Open the chatbot in your browser:
   - http://localhost:5000

---

## 🔧 Project Structure

- /actions.py — Custom Rasa actions (e.g., trip planning, city info)
- /data/nlu.yml — Training examples for intents and entities
- /domain.yml — Rasa domain configuration
- /templates/index.html — Frontend UI
- /app.py — Flask bridge between UI and Rasa
- /config.yml — NLU pipeline and policy setup
- /requirements.txt — Python dependencies

---

## 📌 Notes

- This is a local demo. Deployment options (Heroku, Docker, etc.) can be added later.
- Voice interface and advanced ML features are planned in future releases.

---

## 📃 License

This project is part of academic coursework and not licensed for commercial use. Educational use only.

