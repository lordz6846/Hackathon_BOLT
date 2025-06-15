# ❓QUIZ ME if you CAN 😎

This is a Streamlit-based web app that generates science quizzes for lower secondary school students using OpenAI's GPT-4. Select a topic, get a summary, take a quiz, and ask follow-up questions — all in one place.

---

## ✨ Features

- 📘 Simple topic summaries
- 🧪 Auto-generated 10-question quizzes
- ✅ Answer checking with immediate feedback
- 💬 Ask AI more about any question
- 🚀 Built with Streamlit for quick deployment

---

## 🛠 Tech Stack

- Python
- Streamlit
- OpenAI GPT-4
- python-dotenv

---

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/lordz6846/Hackathon_BOLT.git
cd Hackathon_BOLT

# 2. Create a .env file with your OpenAI API key
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env

# 3. (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate         # On Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
streamlit run app.py
```

> Replace `app.py` with your actual filename if it's different.<br>
> Make sure `.env` is in the **root directory** and contains your OpenAI key.<br>
> ⚠️ Do **not** share your API key publicly!

---

Feel free to fork, use, or contribute to this project!
