from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# استخدم مفتاح OpenRouter مباشرة (مش آمن - الأفضل استخدام environment variable)
OPENROUTER_API_KEY = "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"
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/", methods=["GET"])
def chat():
    question = request.args.get("question")

    if not question:
        return jsonify({"message": "من فضلك ابعتلي سؤال."})

    system_prompt = (
        "أنت شات بوت ذكي جدًا ودمه خفيف. بتتكلم باللهجة المصرية أو العربية الفصحى حسب المستخدم. "
        "اتكلم كأنك صاحب المستخدم. لو طلب هزار، اهزر. لو طلب جدية، كن جدي. "
        "لو المستخدم قال إنه زعلان أو فرحان أو عايز حالة أو شعر أو كلمات رومانسية أو حزينة، اديله اللي يناسب حالته. "
        "لو حسيت إنه ولد كلمه كأنك صاحبه، ولو بنت كأنك صحبتها. أهم حاجة تخليه حاسس إنه بيكلم شخص حقيقي بيحبه وبيفهمه."
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(BASE_URL, headers=headers, json=payload)
        response_data = response.json()

        if "choices" in response_data:
            reply = response_data["choices"][0]["message"]["content"]
            return jsonify({"message": reply})
        else:
            return jsonify({"message": f"حصل خطأ: {response_data}"})

    except Exception as e:
        return jsonify({"message": f"حصل خطأ: {str(e)}"})
