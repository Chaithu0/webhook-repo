from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client.github_events

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == "push":
        event_data = {
            "author": data['pusher']['name'],
            "to_branch": data['ref'].split('/')[-1],
            "timestamp": datetime.utcnow(),
            "event_type": "push"
        }
    elif event_type == "pull_request":
        event_data = {
            "author": data['pull_request']['user']['login'],
            "from_branch": data['pull_request']['head']['ref'],
            "to_branch": data['pull_request']['base']['ref'],
            "timestamp": datetime.utcnow(),
            "event_type": "pull_request"
        }
    elif event_type == "merge":
        event_data = {
            "author": data['pull_request']['merged_by']['login'],
            "from_branch": data['pull_request']['head']['ref'],
            "to_branch": data['pull_request']['base']['ref'],
            "timestamp": datetime.utcnow(),
            "event_type": "merge"
        }
    else:
        return jsonify({"message": "Event type not supported"}), 400

    db.events.insert_one(event_data)
    return jsonify({"message": "Event received"}), 200

# Endpoint to retrieve events
@app.route('/events', methods=['GET'])
def get_events():
    events = list(db.events.find().sort("timestamp", -1).limit(50))
    for event in events:
        event['_id'] = str(event['_id'])
    return jsonify(events)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
