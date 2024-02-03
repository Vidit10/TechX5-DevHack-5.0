import csv
from flask import Flask, jsonify, request, session, send_from_directory
from blockchain import Blockchain

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

blockchain = Blockchain()
voted_users = set()

def get_candidate_public_key(candidate_name):
    with open('candidates.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['candidate_name'] == candidate_name:
                return row['public_key']
    return None

@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    data = request.get_json()
    username = session.get('username')

    if not username:
        return jsonify({'error': 'User not logged in'}), 401

    if username in voted_users:
        return jsonify({'error': 'User has already voted'}), 403

    vote_data = f"Vote: {username} for {data['candidate']}"
    candidate_public_key = get_candidate_public_key(data['candidate'])

    if not candidate_public_key:
        return jsonify({'error': 'Candidate not found'}), 404

    if blockchain.verify_transaction(data, candidate_public_key):
        blockchain.new_transaction(username, data['candidate'], 1)  # Adjust to pass 1 as the amount
        voted_users.add(username)  # Track that the user has voted
        return jsonify({'message': 'Vote submitted successfully'}), 200
    else:
        return jsonify({'error': 'Invalid vote signature'}), 400

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)

