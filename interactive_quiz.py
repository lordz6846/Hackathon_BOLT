import streamlit as st
from openai import OpenAI
import json
import os
import time
from dotenv import load_dotenv

# 🔑 Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Subject and Topic Map
subject_map = {
    "Physics": ["Force", "Light", "Sound", "Energy", "Electricity"],
    "Biology": ["Cells of living things", "Photosynthesis", "Respiratory system", "Excretory system", "Genetics"],
    "Chemistry": ["Properties of substances", "Chemical changes", "Acids and bases", "Solutions"],
    "Astronomy": ["Solar system", "Moon cycle", "Introduction to the universe"],
    "Earth and Environment": ["Earth changes", "Natural resources", "Living things and the environment"]
}

st.title("❓QUIZ ME if you CAN 😎")

# Subject selection
subject = st.selectbox("Select a subject", list(subject_map.keys()))
topic = st.selectbox("Select a topic", subject_map[subject])

# 🔘 Enable timer BEFORE generating quiz
use_timer = st.checkbox("⏱ Enable timer challenge", value=False)
if use_timer:
    time_limit = st.selectbox("⏲ Choose time limit", [60, 120, 180, 240], format_func=lambda x: f"{x//60} minutes")
else:
    time_limit = None

# Generate Quiz
if st.button("✨ Generate Quiz"):
    with st.spinner("Generating summary and questions... Please WAIT"):

        summary_prompt = f"Summarize the topic '{topic}' in simple English for lower secondary school students in no more than 6 lines."
        summary_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": summary_prompt}]
        )

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
            st.session_state["summary_text"] = summary_response.choices[0].message.content.strip()
            st.session_state["start_time"] = time.time() if use_timer else None
            st.session_state["checked"] = False
            st.session_state["user_answers"] = {}  # ✅ Reset answers to avoid index bug
        except Exception as e:
            st.error("❌ Failed to parse quiz. Please try again.")
            st.write("📦 GPT Output:", raw)
            st.write("📛 Error:", e)
            st.stop()

# Display Quiz
if "quiz_data" in st.session_state:
    quiz_data = st.session_state["quiz_data"]
    summary_text = st.session_state["summary_text"]

    st.subheader("📘 Summary")
    st.info(summary_text)

    st.subheader("🧪 10-Question Quiz")

    if "user_answers" not in st.session_state:
        st.session_state["user_answers"] = {}

    # ⏳ Countdown timer
    if use_timer and st.session_state.get("start_time") and not st.session_state.get("checked", False):
        elapsed = int(time.time() - st.session_state["start_time"])
        remaining = time_limit - elapsed
        if remaining <= 0:
            st.warning("⏰ Time is up! Please submit your answers.")
        else:
            st.info(f"⏳ Time remaining: {remaining} seconds")

    for idx, q in enumerate(quiz_data):
        # 🔐 Safely get default answer
        default_ans = st.session_state["user_answers"].get(idx, q["options"][0])
        if default_ans not in q["options"]:
            default_ans = q["options"][0]

        st.markdown(f"**{idx+1}. {q['question']}**")
        st.session_state["user_answers"][idx] = st.radio(
            "Choose your answer:",
            q["options"],
            key=f"q{idx}",
            index=q["options"].index(default_ans)
        )

    # ✅ Safe submit_disabled logic
    if use_timer and st.session_state.get("start_time") and time_limit is not None:
        submit_disabled = (time.time() - st.session_state["start_time"]) > time_limit
    else:
        submit_disabled = False

    if st.button("✅ Submit Answers", disabled=submit_disabled):
        st.session_state["checked"] = True
        if use_timer and st.session_state.get("start_time"):
            end_time = time.time()
            st.session_state["time_used"] = int(end_time - st.session_state["start_time"])
        st.session_state["start_time"] = None  # ⏹ Stop Timer

# Check Answers
if st.session_state.get("checked", False):
    score = 0
    quiz_data = st.session_state["quiz_data"]
    user_answers = st.session_state["user_answers"]

    for idx, q in enumerate(quiz_data):
        user_ans = user_answers[idx]
        is_correct = user_ans == q["answer"]
        score += int(is_correct)

    if use_timer and "time_used" in st.session_state:
        t = st.session_state["time_used"]
        minutes, seconds = divmod(t, 60)
        st.info(f"⏱ You spent **{minutes} minutes {seconds} seconds** on this quiz.")

    st.subheader("📊 Total Score")
    if score >= 9:
        feedback = "🌟 Excellent!"
    elif score >= 7:
        feedback = "👍 Great job!"
    elif score >= 5:
        feedback = "😊 Not bad! Keep practicing."
    elif score >= 3:
        feedback = "🤔 You can do better!"
    else:
        feedback = "🥲 Don't give up! Try again."

    st.write(f"You got **{score} / 10** questions correct. {feedback}")

    # 🔁 Try Again
    if st.button("🔁 Try Again"):
        for key in ["quiz_data", "summary_text", "user_answers", "checked", "start_time", "time_used"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    st.subheader("📝 Answer Review and Follow-Up")

    for idx, q in enumerate(quiz_data):
        user_ans = user_answers[idx]
        is_correct = user_ans == q["answer"]

        if is_correct:
            st.success(f"Question {idx+1}: ✅ Correct")
        else:
            st.error(f"Question {idx+1}: ❌ Incorrect (Correct answer: {q['answer']})")

        with st.expander(f"💬 Ask AI more about Question {idx+1}"):
            if all([topic, q.get("question"), q.get("answer")]):
                follow_up = st.text_input(f"❓ Your follow-up question (Q{idx+1})", key=f"follow_q{idx}")
                if st.button(f"Ask AI (Q{idx+1})", key=f"ask_q{idx}"):
                    if not follow_up.strip():
                        st.warning("⚠️ Please enter a follow-up question before asking.")
                    else:
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
            else:
                st.warning("⚠️ This question is no longer available. Please regenerate the quiz.")