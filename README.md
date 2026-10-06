# NatureQuest AI — Your AI Outdoor Mission Coach

An AI outdoor mission coach that gets you off the screen and into the real world with short, personalized outdoor quests.

---

## 🌿 What It Does

NatureQuest AI provides a distraction-free, screen-minimal experience with a clear, deliberate user journey:

1. **Enter Preferences:** Select your available time (10 to 60 minutes), outdoor environment (Park, Garden, Campus, Neighborhood, Balcony, Beach, Other), mood, energy level, and difficulty.
2. **AI Quest Generation:** The AI generates one short, practical, zero-equipment outdoor quest tailored to your selections.
3. **Put Phone Away:** The interface displays a clear screen-off prompt encouraging you to put your phone away and step outside.
4. **Go Outside & Complete Quest:** Complete your mission using only your senses and surroundings—no screens, cameras, or notebooks required.
5. **Return:** Come back to the application once your quest is complete.
6. **Share Observations:** Describe what you noticed, discovered, heard, saw, or felt.
7. **AI Reflection:** Receive a short, encouraging reflection strictly grounded in your actual notes.

---

## 🎯 Why I Built It

Modern technology often keeps people glued to screens and locked into endless chatbot conversations. NatureQuest AI was built to flip this pattern: using AI not to keep you online, but to coach you into the real world.

The screen is only a brief starting and ending point. Quests strongly prefer zero equipment—no phones, notebooks, headphones, cameras, or special gear—encouraging users to explore safely, listen, observe natural details, and reconnect with nature.

---

## 🤖 AI at the Core

NatureQuest AI uses the open-weight **Llama 3.1 8B Instruct** (`meta-llama/Llama-3.1-8B-Instruct`) model accessed via the **Hugging Face Inference API**.

AI is used for two distinct, focused tasks:
1. **Generating the Outdoor Quest:** Creates a single, realistic mission tailored to the user's time, environment, mood, energy, and difficulty. Built-in safety rules ensure the quest avoids unsafe areas, trespassing, hazardous situations, wild animals, and illegal activities.
2. **Generating a Grounded Reflection:** Reviews the user's written observations and provides a warm, 2–3 sentence reflection. The model is strictly constrained to avoid hallucinating or assuming unmentioned plants, animals, sounds, weather, locations, or feelings.

The project deliberately avoids unnecessary frameworks, databases, vector stores, and complex infrastructure to remain clean, transparent, and beginner-friendly.

---

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python** | Primary programming language |
| **Streamlit** | Interactive web frontend and session management |
| **Hugging Face Inference API** | Cloud inference endpoint for open-weight models |
| **Llama 3.1 8B Instruct** | Open-weight instruction-following AI model (`meta-llama/Llama-3.1-8B-Instruct`) |
| **python-dotenv** | Secure local loading of credentials from `.env` |

---

## 🚀 Getting Started

Follow these steps to run NatureQuest AI locally using Windows PowerShell:

### 1. Open the Project Directory
```powershell
cd NatureQuest-AI
```

### 2. Set Up a Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Your Environment Variables
Create a file named `.env` in the root directory:
```env
HF_TOKEN=your_huggingface_token_here
```
*(The `.env` file is included in `.gitignore` to prevent secret tokens from being committed).*

### 5. Run the Application
```powershell
streamlit run app.py
```
Open `http://localhost:8501` in your browser to start your first outdoor quest!
