from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def chat():
    question = request.args.get("question")

    if not question:
        return jsonify({"message": "من فضلك ابعتلي سؤال."})

    # تهيئة الأسلوب
    system_prompt = (
        "أنت شات بوت ذكي جدًا ودمه خفيف. بتتكلم باللهجة المصرية أو العربية الفصحى حسب المستخدم. "
        "اتكلم كأنك صاحب المستخدم. لو طلب هزار، اهزر. لو طلب جدية، كن جدي. "
        "لو المستخدم قال إنه زعلان أو فرحان أو عايز حالة أو شعر أو كلمات رومانسية أو حزينة، اديله اللي يناسب حالته. "
        "لو حسيت إنه ولد كلمه كأنك صاحبه، ولو بنت كأنك صحبتها. أهم حاجة تخليه حاسس إنه بيكلم شخص حقيقي بيحبه وبيفهمه."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
        )
        reply = response.choices[0].message.content
        return jsonify({"message": reply})

    except Exception as e:
        return jsonify({"message": f"حصل خطأ: {str(e)}"})
