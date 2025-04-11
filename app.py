from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

apapp = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "GPT API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

MODELS = [ ("mistralai/mistral-nemo", "Mistral: Mistral Nemo (رقم 1 في البرمجة)"), ("google/learnlm-1.5-7b", "Google: LearnLM 1.5 Pro Experimental (رقم 2 في البرمجة)"), ("google/gemini-pro", "Google: Gemini 2.5 Pro Experimental (رقم 3 في البرمجة)"), ("meta-llama/llama-4-maverick", "Meta: Llama 4 Maverick (رقم 4 في البرمجة)"), ("meta-llama/llama-4-scout", "Meta: Llama 4 Scout (رقم 5 في البرمجة)"), ("deepseek/deepseek-v3", "DeepSeek: DeepSeek V3 0324 (رقم 6 في البرمجة)"), ("nousresearch/deepseek-coder-33b", "Nous: DeepHermes 3 Llama 3 8B Preview (رقم 7 في البرمجة)"), ("cognitivecomputations/dolphin-2.9", "Dolphin3.0 R1 Mistral 24B (رقم 8 في البرمجة)"), ("google/gemma-3-27b", "Google: Gemma 3 27B (رقم 9 في البرمجة)"), ("google/gemma-3-12b", "Google: Gemma 3 12B (رقم 10 في البرمجة)"), ("google/gemma-3-4b", "Google: Gemma 3 4B (رقم 11 في البرمجة)"), ("google/gemma-3-1b", "Google: Gemma 3 1B (رقم 12 في البرمجة)"), ("reka/reka-flash", "Reka: Flash 3 (رقم 13 في البرمجة)"), ("olympus/olympiccoder-32b", "OlympicCoder 32B (رقم 14 في البرمجة)"), ("olympus/olympiccoder-7b", "OlympicCoder 7B (رقم 15 في البرمجة)"), ("moonshot/moonlight-16b", "Moonshot AI: Moonlight 16B A3B Instruct (رقم 16 في البرمجة)"), ("qwen/qwen1.5-32b", "Qwen: QwQ 32B (free) (رقم 17 في البرمجة)"), ("deepseek/deepseek-r1-zero", "DeepSeek: DeepSeek R1 Zero (رقم 18 في البرمجة)"), ("deepseek/deepseek-v3-base", "DeepSeek: DeepSeek V3 Base (رقم 19 في البرمجة)"), ("deepseek/r1-distill-qwen-32b", "DeepSeek: R1 Distill Qwen 32B (رقم 20 في البرمجة)"), ("deepseek/r1-distill-qwen-14b", "DeepSeek: R1 Distill Qwen 14B (رقم 21 في البرمجة)"), ("deepseek/r1-distill-llama-70b", "DeepSeek: R1 Distill Llama 70B (رقم 22 في البرمجة)"), ("qwen/qwen2.5-vl-32b", "Qwen: Qwen2.5 VL 32B Instruct (رقم 23 في البرمجة)"), ("qwen/qwen2.5-coder-32b", "Qwen: Qwen2.5 Coder 32B Instruct (رقم 24 في البرمجة)"), ("qwen/qwq-32b-preview", "Qwen: QwQ 32B Preview (رقم 25 في البرمجة)"), ("google/gemini-2-9b", "Google: Gemini 2 9B (رقم 26 في البرمجة)"), ("google/gemini-2.0-flash-thinking", "Google: Gemini 2.0 Flash Thinking Experimental (رقم 27 في البرمجة)"), ("google/gemini-2.0-flash-thinking-01", "Google: Gemini 2.0 Flash Thinking Experimental 01 - 21 (رقم 28 في البرمجة)"), ("google/gemini-2.0-flash", "Google: Gemini 2.0 Flash Experimental (رقم 29 في البرمجة)"), ("meta-llama/llama-3.3-70b", "Meta: Llama 3.3 70B Instruct (رقم 30 في البرمجة)"), ("meta-llama/llama-3.1-8b", "Meta: Llama 3.1 8B Instruct (رقم 31 في البرمجة)"), ("nvidia/llama-3.3-nemotron-super-49b", "NVIDIA: Llama 3.3 Nemotron Super 49B v1 (رقم 32 في البرمجة)"), ("nvidia/llama-3.1-nemotron-ultra-253b", "NVIDIA: Llama 3.1 Nemotron Ultra 253B v1 (رقم 33 في البرمجة)"), ("nvidia/llama-3.1-nemotron-nano-8b", "NVIDIA: Llama 3.1 Nemotron Nano 8B v1 (رقم 34 في البرمجة)"), ("allenai/molmo-7b-d", "AllenAI: Molmo 7B D (رقم 35 في البرمجة)"), ("rogue/rogue-rose-103b", "Rogue Rose 103B v0.2 (رقم 36 في البرمجة)"), ("bytedance/ui-tars-72b", "Bytedance: UI-TARS 72B (رقم 37 في البرمجة)"), ("moonshot/kimi-vl-a3b", "Moonshot AI: Kimi VL A3B Thinking (رقم 38 في البرمجة)") ]

لتخزين النموذج الحالي (بسيط ومؤقت)

current_model = MODELS[0][0]

@app.route("/", methods=["GET"]) def welcome(): return jsonify({ "message": "اختار نموذج من النماذج الآتية (من الأقوى للأضعف):", "models": [model[1] for model in MODELS] })

@app.route("/set_model", methods=["POST"]) def set_model(): global current_model data = request.get_json() model_index = data.get("index") try: current_model = MODELS[int(model_index)][0] return jsonify({"message": f"تم اختيار النموذج بنجاح: {MODELS[int(model_index)][1]}"}) except: return jsonify({"message": "رقم النموذج غير صحيح."})

@app.route("/chat", methods=["POST"]) def chat(): data = request.get_json() question = data.get("question") if not question: return jsonify({"message": "من فضلك ابعتلي سؤال."})

headers = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    "HTTP-Referer": "https://yourdomain.com",
    "X-Title": "Your App",
    "Content-Type": "application/json"
}

payload = {
    "model": current_model,
    "messages": [
        {"role": "system", "content": "أنت مساعد ذكي تتفاعل بمرونة مع المستخدم."},
        {"role": "user", "content": question}
    ]
}

try:
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()
    if "choices" in response_data:
        return jsonify({"message": response_data["choices"][0]["message"]["content"]})
    else:
        return jsonify({"message": f"حصل خطأ: {response_data}"})
except Exception as e:
    return jsonify({"message": f"حصل خطأ: {str(e)}"})

