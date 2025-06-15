import streamlit as st
from openai import OpenAI
import json

# 🔑 API Key
client = OpenAI(api_key="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")

# หัวข้อวิชา
subject_map = {
    "ฟิสิกส์": ["แรง", "แสง", "เสียง", "พลังงาน", "ไฟฟ้า"],
    "ชีววิทยา": ["เซลล์ของสิ่งมีชีวิต", "การสังเคราะห์ด้วยแสง", "ระบบหายใจ", "ระบบขับถ่าย", "พันธุกรรม"],
    "เคมี": ["สมบัติของสาร", "การเปลี่ยนแปลงทางเคมี", "กรด-เบส", "สารละลาย"],
    "ดาราศาสตร์": ["ระบบสุริยะ", "วัฏจักรของดวงจันทร์", "จักรวาลเบื้องต้น"],
    "โลกและสิ่งแวดล้อม": ["การเปลี่ยนแปลงของโลก", "ทรัพยากรธรรมชาติ", "สิ่งมีชีวิตกับสิ่งแวดล้อม"]
}

st.title("🧪 QUIZ ME if you CAN ")

# เลือกวิชาและหัวข้อ
subject = st.selectbox("เลือกหมวดวิชา", list(subject_map.keys()))
topic = st.selectbox("เลือกหัวข้อ", subject_map[subject])

# ปุ่มสร้างแบบทดสอบ
if st.button("✨ สร้างแบบทดสอบ"):
    with st.spinner("กำลังสร้างเนื้อหาและคำถาม..."):

        # 🔹 สรุปเนื้อหา
        summary_prompt = f"สรุปเนื้อหาหัวข้อ '{topic}' สำหรับนักเรียนมัธยมต้น ให้เข้าใจง่าย ไม่เกิน 6 บรรทัด"
        summary_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": summary_prompt}]
        )
        st.session_state["summary_text"] = summary_response.choices[0].message.content.strip()

        # 🔹 สร้างคำถาม
        quiz_prompt = f"""
        สร้างคำถามปรนัย 10 ข้อเกี่ยวกับหัวข้อ "{topic}" สำหรับนักเรียนมัธยมต้น
        แต่ละข้อมีคำถาม, ตัวเลือก 4 ข้อ, และคำตอบที่ถูกต้อง
        ส่งมาในรูปแบบ JSON ล้วน ๆ ห้ามมีคำอธิบาย ข้อความ หรือคำเกริ่นใด ๆ ทั้งก่อนและหลัง JSON:
        [
            {{
                "question": "...",
                "options": ["...", "...", "...", "..."],
                "answer": "..."
            }},
            ...
        ]
        ย้ำอีกที ตอบมาเป็น JSON ล้วนๆเท่านั้น เท่านั้นเท่านั้นเท่่านั้น
        """
        quiz_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": quiz_prompt}]
        )

        try:
            st.session_state["quiz_data"] = json.loads(quiz_response.choices[0].message.content)
        except:
            st.error("❌ แปลงคำถามไม่สำเร็จ ลองกดสร้างใหม่อีกครั้ง")
            st.stop()

# ✅ แสดงแบบทดสอบ ถ้ามีใน session_state
if "quiz_data" in st.session_state:
    quiz_data = st.session_state["quiz_data"]
    summary_text = st.session_state["summary_text"]

    st.subheader("📘 สรุปเนื้อหา")
    st.info(summary_text)

    st.subheader("🧪 แบบทดสอบ 10 ข้อ")

    if "user_answers" not in st.session_state:
        st.session_state["user_answers"] = {}

    for idx, q in enumerate(quiz_data):
        st.markdown(f"**{idx+1}. {q['question']}**")
        st.session_state["user_answers"][idx] = st.radio(
            "เลือกคำตอบ",
            q["options"],
            key=f"q{idx}",
            index=q["options"].index(st.session_state["user_answers"].get(idx, q["options"][0]))
        )

    if st.button("✅ ตรวจคำตอบ"):
        st.session_state["checked"] = True

# ✅ เฉลยและช่องถามเพิ่มเติม
if st.session_state.get("checked", False):
    st.subheader("📝 เฉลยพร้อมถามต่อ")
    score = 0
    quiz_data = st.session_state["quiz_data"]
    user_answers = st.session_state["user_answers"]

    for idx, q in enumerate(quiz_data):
        user_ans = user_answers[idx]
        is_correct = user_ans == q["answer"]

        if is_correct:
            st.success(f"ข้อ {idx+1}: ✅ ถูกต้อง")
        else:
            st.error(f"ข้อ {idx+1}: ❌ ผิด (คำตอบที่ถูกคือ: {q['answer']})")

        # 💬 ช่องถาม AI
        with st.expander(f"💬 ถาม AI เพิ่มเติม (ข้อ {idx+1})"):
            follow_up = st.text_input(f"❓ คำถามเพิ่มเติมสำหรับข้อ {idx+1}", key=f"follow_q{idx}")
            if st.button(f"ถาม AI ข้อ {idx+1}", key=f"ask_q{idx}"):
                full_prompt = f"""
หัวข้อ: {topic}
คำถามต้นฉบับ: {q['question']}
คำตอบที่ถูกต้อง: {q['answer']}
คำถามเพิ่มเติมจากนักเรียน: {follow_up}

อธิบายให้เข้าใจง่ายแบบนักเรียนมัธยมต้น
"""
                with st.spinner("AI กำลังช่วยอธิบาย..."):
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": full_prompt}]
                    )
                    st.info(response.choices[0].message.content)

        score += int(is_correct)

    st.subheader("📊 คะแนนรวม")
    st.write(f"คุณตอบถูกทั้งหมด **{score} / 10** ข้อ 🎉")