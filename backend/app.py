from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))

from predict import predict
from database import init_db, save_log, get_history, get_log_by_id
from pdf_generator import generate_pdf
from log_parser import parse_log

app = Flask(__name__)
CORS(app)
init_db()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'mode': 'offline'})

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    raw_log = data.get('log', '').strip()
    if not raw_log:
        return jsonify({'error': 'No log provided'}), 400
    cleaned_log = parse_log(raw_log)
    result = predict(cleaned_log)
    log_id = save_log(raw_log, result)
    result['log_id'] = log_id
    return jsonify(result)

@app.route('/history', methods=['GET'])
def history():
    return jsonify(get_history(limit=20))

@app.route('/report/<int:log_id>', methods=['GET'])
def get_report(log_id):
    row = get_log_by_id(log_id)
    if not row:
        return jsonify({'error': 'Not found'}), 404
    path = generate_pdf(row['result'], row['raw_log'], str(log_id))
    return send_file(path, as_attachment=True,
                     download_name=f'logsense_{log_id}.pdf',
                     mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True, port=5000)