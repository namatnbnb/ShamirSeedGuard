import os
from flask import Flask, render_template, request, jsonify
from secretsharing import SecretSharer

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/split', methods=['POST'])
def split_seed():
    seed = request.form['seed']
    shares = int(request.form['shares'])
    threshold = int(request.form['threshold'])

    if not is_valid_seed(seed):
        return jsonify({'error': 'Invalid seed format'}), 400

    if shares < threshold or threshold < 2:
        return jsonify({'error': 'Invalid shares or threshold'}), 400

    try:
        split_shares = SecretSharer.split_secret(seed, threshold, shares)
        return jsonify({'shares': split_shares})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reconstruct', methods=['POST'])
def reconstruct_seed():
    shares = request.form.getlist('shares[]')

    if len(shares) < 2:
        return jsonify({'error': 'At least 2 shares are required'}), 400

    try:
        reconstructed_seed = SecretSharer.recover_secret(shares)
        return jsonify({'seed': reconstructed_seed})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def is_valid_seed(seed):
    # Basic validation: check if the seed consists of 12, 15, 18, 21, or 24 words
    word_count = len(seed.split())
    return word_count in [12, 15, 18, 21, 24]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
