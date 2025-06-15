import streamlit as st
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

# 🔑 Load API Key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Subject and Topic Map (English)
subject_map = {
    "Physics": ["Force", "Light", "Sound", "Energy", "Electricity"],
    "Biology": ["Cells of living things", "Photosynthesis", "Respiratory system", "Excretory system", "Genetics"],
    "Chemistry": ["Properties of substances", "Chemical changes", "Acids and bases", "Solutions"],
    "Astronomy": ["Solar system", "Moon cycle", "Introduction to the universe"],
    "Earth and Environment": ["Earth changes", "Natural resources", "Living things and the environment"]
}

st.title("❓QUIZ ME if you CAN 😎")

# Select subject and topic
subject = st.selectbox("Select a subject", list(subject_map.keys()))
topic = st.selectbox("Select a topic", subject_map[subject])

# Generate Quiz button
if st.button("✨ Generate Quiz"):
    with st.spinner("Generating summary and questions..."):

        # 🔹 Generate summary
        summary_prompt = f"Summarize the topic '{topic}' in simple English for lower secondary school students in no more than 6 lines."
        summary_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": summary_prompt}]
        )
        st.session_state["summary_text"] = summary_response.choices[0].message.content.strip()

        # 🔹 Generate quiz
        quiz_prompt = f"""
Topic: "{topic}"
Generate 10 multiple choice questions for lower secondary school students.
Each question should include:
- A clear question
- 4 answer choices
- One correct answer

Output ONLY JSON (no descriptions, no headings). Format:
[
  {{
    "question": "....",
    "options": ["A", "B", "C", "D"],
    "answer": "...."
  }},
  ...
]
"""
        quiz_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": quiz_prompt}]
        )

        raw = quiz_response.choices[0].message.content.strip()
        try:
            st.session_state["quiz_data"] = json.loads(raw)
        except Exception as e:
            st.error("❌ Failed to parse quiz. Please try again.")
            st.write("📦 GPT Output:", raw)
            st.write("📛 Error:", e)
            st.stop()

# ✅ Display quiz if available
if "quiz_data" in st.session_state:
    quiz_data = st.session_state["quiz_data"]
    summary_text = st.session_state["summary_text"]

    st.subheader("📘 Summary")
    st.info(summary_text)

    st.subheader("🧪 10-Question Quiz")

    if "user_answers" not in st.session_state:
        st.session_state["user_answers"] = {}

    for idx, q in enumerate(quiz_data):
        st.markdown(f"**{idx+1}. {q['question']}**")
        st.session_state["user_answers"][idx] = st.radio(
            "Choose your answer:",
            q["options"],
            key=f"q{idx}",
            index=q["options"].index(st.session_state["user_answers"].get(idx, q["options"][0]))
        )

    if st.button("✅ Submit Answers"):
        st.session_state["checked"] = True

# ✅ Answer checking and ask AI feature
if st.session_state.get("checked", False):
    st.subheader("📝 Answer Review and Follow-Up")
    score = 0
    quiz_data = st.session_state["quiz_data"]
    user_answers = st.session_state["user_answers"]

    for idx, q in enumerate(quiz_data):
        user_ans = user_answers[idx]
        is_correct = user_ans == q["answer"]

        if is_correct:
            st.success(f"Question {idx+1}: ✅ Correct")
        else:
            st.error(f"Question {idx+1}: ❌ Incorrect (Correct answer: {q['answer']})")

        # 💬 Ask AI section
        with st.expander(f"💬 Ask AI more about Question {idx+1}"):
            follow_up = st.text_input(f"❓ Your follow-up question (Q{idx+1})", key=f"follow_q{idx}")
            if st.button(f"Ask AI (Q{idx+1})", key=f"ask_q{idx}"):
                full_prompt = f"""
Topic: {topic}
Original question: {q['question']}
Correct answer: {q['answer']}
Student's follow-up question: {follow_up}

Explain clearly in simple English for a lower secondary school student.
"""
                with st.spinner("AI is explaining..."):
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": full_prompt}]
                    )
                    st.info(response.choices[0].message.content)

        score += int(is_correct)

    st.subheader("📊 Total Score")
    st.write(f"You got **{score} / 10** questions correct 🎉")