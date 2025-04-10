from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/chat', methods=['GET'])
def chat():
    question = request.args.get('question')

    if not question:
        return jsonify({"error": "برجاء إرسال سؤال"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            temperature=0.7
        )
        answer = response['choices'][0]['message']['content']
        return jsonify({"message": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
