#!/usr/bin/env python
# coding: utf-8

# In[6]:


from openai import OpenAI
import os

# สร้าง client ใส่ API key ของตัวเอง
client = OpenAI(api_key="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")

# ข้อมูลเนื้อหาแต่ละหัวข้อ (ใส่เพิ่มได้เรื่อยๆ)
topics = [
    {
        "level": "ม.1",
        "subject": "ฟิสิกส์",
        "topic": "แรงเสียดทาน",
        "content": "แรงเสียดทานคือแรงที่ต้านการเคลื่อนที่ของวัตถุ เมื่อวัตถุเคลื่อนที่หรือต้องการเคลื่อนที่บนพื้นผิวหนึ่ง..."
    },
    {
        "level": "ม.1",
        "subject": "ฟิสิกส์",
        "topic": "แรงลัพธ์",
        "content": "แรงลัพธ์คือแรงรวมที่เกิดจากแรงหลายแรงกระทำต่อวัตถุพร้อมกัน แรงลัพธ์จะเป็นตัวบอกว่าวัตถุจะเคลื่อนที่หรือไม่..."
    },
    {
        "level": "ม.1",
        "subject": "ฟิสิกส์",
        "topic": "พลังงานไฟฟ้า",
        "content": "พลังงานไฟฟ้าคือพลังงานที่ได้จากการเคลื่อนที่ของอิเล็กตรอนในวงจรไฟฟ้า อุปกรณ์ไฟฟ้าต่าง ๆ..."
    }
]

# ลูปสร้าง prompt และส่งไปยัง GPT-4o
for item in topics:
    prompt = f"""
คุณเป็น AI ครู{item["subject"]}ไทยระดับ{item["level"]} ให้อธิบายสรุปเนื้อหา และสร้างแบบทดสอบแบบปรนัยจากเนื้อหาด้านล่างนี้ โดยให้ผลลัพธ์อยู่ในรูปแบบนี้:

Summary:
[สรุปเนื้อหา 2-3 บรรทัดแบบเข้าใจง่าย]

Multiple Choice Questions:
**สร้างแบบทดสอบปรนัยจำนวน 10 ข้อ** โดยมี format ตามนี้

1. [คำถาม]
A. ...
B. ...
C. ...
D. ...
คำตอบที่ถูกต้อง: ข้อ...
คำอธิบาย: [อธิบายเหตุผลว่าทำไมข้อนี้ถึงถูก]

(ทำแบบนี้จนครบ 10 ข้อ)

เนื้อหา:
{item["content"]}
"""

    # เรียกใช้ GPT-4o
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    result_text = response.choices[0].message.content

    # สร้างชื่อไฟล์ เช่น ม.1_ฟิสิกส์_แรงเสียดทาน.txt
    safe_topic = item["topic"].replace(" ", "_")
    filename = f"{item['level']}_{item['subject']}_{safe_topic}.txt"

    # บันทึกเป็นไฟล์
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result_text)

    print(f"✅ สร้างไฟล์เรียบร้อย: {filename}")


# In[7]:


import os

# แสดงไฟล์ทั้งหมดใน directory ปัจจุบัน
print(os.listdir())


# In[5]:


"ครูฟิสิกส์ไทย".encode("ascii")  # → จะ error เหมือนกัน


# In[9]:


pip install streamlit


# In[10]:


jupyter nbconvert --to script Demo2.ipynb


# In[ ]:




