from flask import Flask, render_template, request, jsonify
import uuid

from text_extractor import TextExtractor
from searching import SemanticSearch
from answering import AnswerFormatter

app = Flask(__name__)

text_storage = {}
text_extractor = TextExtractor()
formatter = AnswerFormatter()


#def llm_service(text, question):
    # интеграция с LLM
    #print(text)
    #return f"Ответ на вопрос '{question}' по тексту:"



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    text_id = str(uuid.uuid4())
    text_content = ""

    if 'file' in request.files:
        file = request.files['file']

        if file.filename != '':
            if file.filename.endswith(tuple(text_extractor.supported_extensions)):
                text_content = text_extractor.extract_from_uploaded_file(file)
            else:
                return jsonify({'error': f'Только {text_extractor.supported_extensions} файлы поддерживаются'}), 400

    if 'text' in request.form and request.form['text'].strip():
        text_content = request.form['text'].strip()

    if not text_content:
        return jsonify({'error': 'Не предоставлен текст или файл'}), 400

    text_storage[text_id] = text_content
    return jsonify({'text_id': text_id})


@app.route('/text/<text_id>')
def get_text(text_id):
    text = text_storage.get(text_id)
    if text:
        return jsonify({'text': ' '.join(text.split()[:150]) + ('...' if len(text.split()) > 150 else '')})
    return jsonify({'error': 'Текст не найден'}), 404


@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    text_id = data.get('text_id')
    question = data.get('question', '').strip()

    if not text_id or not question:
        return jsonify({'error': 'Отсутствует text_id или question'}), 400

    text = text_storage.get(text_id)
    if not text:
        return jsonify({'error': 'Текст не найден'}), 404

    found_context = SemanticSearch(text, question)
    context = found_context.context_preparation()

    # вызов LLM

    answer_text = formatter.generate_answer(question, context)
    return jsonify({'answer': answer_text})


if __name__ == '__main__':
    app.run(debug=True, port=5000)