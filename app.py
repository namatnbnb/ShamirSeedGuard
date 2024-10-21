import os
import base64
import logging
from flask import Flask, render_template, request, jsonify
from secretsharing import SecretSharer
from models import Session, EncryptedShare, encrypt_share, decrypt_share
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/split', methods=['POST'])
def split_seed():
    seed = request.form['seed']
    shares = int(request.form['shares'])
    threshold = int(request.form['threshold'])

    logging.debug(f"Received seed phrase (first 10 chars): {seed[:10]}...")
    logging.debug(f"Shares: {shares}, Threshold: {threshold}")

    if not is_valid_seed(seed):
        return jsonify({'error': 'Invalid seed format'}), 400

    if shares < threshold or threshold < 2:
        return jsonify({'error': 'Invalid shares or threshold'}), 400

    try:
        # Convert seed to hex
        hex_seed = seed.encode('utf-8').hex()
        logging.debug(f"Hex seed (first 10 chars): {hex_seed[:10]}...")

        # Use SecretSharer to split the secret
        split_shares = SecretSharer.split_secret(hex_seed, threshold, shares)
        logging.debug("Successfully split using SecretSharer")

        # Encrypt and store shares in the database
        session = Session()
        stored_shares = []
        for share in split_shares:
            share_id = str(uuid.uuid4())
            encrypted_share = encrypt_share(share)
            new_share = EncryptedShare(share_id=share_id, encrypted_share=encrypted_share)
            session.add(new_share)
            stored_shares.append(share_id)
        session.commit()

        return jsonify({'share_ids': stored_shares})
    except Exception as e:
        logging.error(f"Error in split_seed: {str(e)}")
        return jsonify({'error': f"An error occurred while splitting the seed: {str(e)}"}), 500
    finally:
        session.close()

@app.route('/reconstruct', methods=['POST'])
def reconstruct_seed():
    data = request.get_json()
    share_ids = data.get('share_ids', [])

    logging.debug(f"Received share_ids: {share_ids}")

    if len(share_ids) < 2:
        return jsonify({'error': 'At least 2 shares are required'}), 400

    try:
        session = Session()
        shares = []
        for share_id in share_ids:
            encrypted_share = session.query(EncryptedShare).filter_by(share_id=share_id).first()
            if encrypted_share:
                decrypted_share = decrypt_share(encrypted_share.encrypted_share)
                shares.append(decrypted_share)
        
        if len(shares) < 2:
            return jsonify({'error': 'Not enough valid shares provided'}), 400

        # Use SecretSharer to reconstruct the secret
        reconstructed_hex_seed = SecretSharer.recover_secret(shares)
        logging.debug("Successfully reconstructed using SecretSharer")

        # Convert hex back to seed phrase
        reconstructed_seed = bytes.fromhex(reconstructed_hex_seed).decode('utf-8')
        logging.debug("Successfully decoded hex seed")

        return jsonify({'seed': reconstructed_seed})
    except Exception as e:
        logging.error(f"Error in reconstruct_seed: {str(e)}")
        return jsonify({'error': f"An error occurred while reconstructing the seed: {str(e)}"}), 500
    finally:
        session.close()

def is_valid_seed(seed):
    # Basic validation: check if the seed consists of 12, 15, 18, 21, or 24 words
    word_count = len(seed.split())
    return word_count in [12, 15, 18, 21, 24]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
