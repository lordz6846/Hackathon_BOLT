# ❓QUIZ ME if you CAN 😎

This is a Streamlit-based web app that generates science quizzes for lower secondary school students using OpenAI's GPT-4. Select a topic, get a summary, take a quiz, and ask follow-up questions — all in one place.


<details>
<summary> 🗒️ Note for Teammates </summary>

  ⚠️ For now, only `interactive_quiz.py` and `interactive_quiz.ipynb` are actually used. Feel free to ignore the rest. It has been mainly developed solo so far (approx. 200 lines of code lol). If you’d like to continue building on top of it, feel free to do so — especially if you want to **redesign the frontend** or **improve the UI for presentation**.

  That said, please make sure to **pull before pushing**, since I’ve been using `git push --force` regularly to keep things clean while working in Jupyter.

  **No pressure at all — if you don’t feel like editing, this version should be enough to present at the hackathon. 😊**

</details>


<details>
<summary> ✨ Features </summary>

- 📘 Topic summaries with simple language
- 🧪 AI-generated 10-question quizzes
- ✅ Instant answer checking with feedback
- 💬 Ask follow-up questions for each item
- ⏱ Optional countdown timer
- 💯 Emoji-based score feedback
- 🔁 One-click Try Again
- 🛡 Safe session handling
- 🚀 Built with Streamlit

</details>


<details>
<summary> 🛠 Tech Stack </summary>

- Python
- Streamlit
- OpenAI GPT-4
- python-dotenv

</details>


<details>
<summary> 🚀 How to Run </summary>

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

  Replace `app.py` with your actual filename if it's different.<br>
  Make sure `.env` is in the **root directory** and contains your OpenAI key.<br>
  ⚠️ Do **not** share your API key publicly!

</details>


<details>
<summary> 🤖 Fun Fact </summary>

  90% of this repo was written by ChatGPT.  
  I just keep saying “next” — and telling it when things broke. 😅

</details>

---

**Feel free to fork, use, or contribute to this project!**
