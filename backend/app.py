from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Import log_parser.py
sys.path.append(os.path.dirname(__file__))
from log_parser import parse_log

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'mode': 'offline'
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json() or {}

        raw_log = data.get('log', '').strip()

        if not raw_log:
            return jsonify({
                'error': 'No log provided'
            }), 400

        # Clean log
        cleaned_log = parse_log(raw_log)

        # Dummy response until predict.py is ready
        result = {
            'domain': 'it',
            'severity': 'warning',
            'confidence': 80,
            'diagnosis': 'Waiting for Member 2 predict.py',
            'cause': 'ML prediction module not connected yet',
            'fix_steps': [
                'Complete integration with predict.py',
                'Connect trained model',
                'Enable rule engine'
            ],
            'pattern_matched': 'DUMMY',
            'cleaned_log': cleaned_log,
            'log_id': 1
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/history', methods=['GET'])
def history():
    return jsonify([
        {
            'id': 1,
            'domain': 'it',
            'severity': 'warning',
            'timestamp': '2026-06-19T12:00:00'
        }
    ])


@app.route('/report/<int:log_id>', methods=['GET'])
def report(log_id):
    return jsonify({
        'message': f'PDF generation pending for log {log_id}'
    })


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )