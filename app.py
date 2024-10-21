import os
import logging
from flask import Flask, render_template, request, jsonify
from secretsharing import SecretSharer

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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
        # Convert seed phrase to hexadecimal
        hex_seed = seed.encode('utf-8').hex()
        logging.debug(f"Hex seed: {hex_seed}")

        # Try with a simple string first
        test_secret = "test secret"
        logging.debug(f"Testing with simple string: {test_secret}")
        test_shares = SecretSharer.split_secret(test_secret, threshold, shares)
        logging.debug(f"Test shares: {test_shares}")

        # Now try with the actual seed
        split_shares = SecretSharer.split_secret(hex_seed, threshold, shares)
        logging.debug(f"Generated shares: {split_shares}")
        return jsonify({'shares': split_shares})
    except Exception as e:
        logging.error(f"Error in split_seed: {str(e)}")
        return jsonify({'error': f"An error occurred while splitting the seed: {str(e)}"}), 500

@app.route('/reconstruct', methods=['POST'])
def reconstruct_seed():
    shares = request.form.getlist('shares[]')

    if len(shares) < 2:
        return jsonify({'error': 'At least 2 shares are required'}), 400

    try:
        reconstructed_hex_seed = SecretSharer.recover_secret(shares)
        logging.debug(f"Reconstructed hex seed: {reconstructed_hex_seed}")

        # Convert hexadecimal back to seed phrase
        reconstructed_seed = bytes.fromhex(reconstructed_hex_seed).decode('utf-8')
        logging.debug(f"Reconstructed seed: {reconstructed_seed}")

        return jsonify({'seed': reconstructed_seed})
    except Exception as e:
        logging.error(f"Error in reconstruct_seed: {str(e)}")
        return jsonify({'error': f"An error occurred while reconstructing the seed: {str(e)}"}), 500

def is_valid_seed(seed):
    # Basic validation: check if the seed consists of 12, 15, 18, 21, or 24 words
    word_count = len(seed.split())
    return word_count in [12, 15, 18, 21, 24]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
