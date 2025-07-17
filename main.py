# Flask app.py – already complete
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'WhatsApp Bot is running'

@app.route('/message', methods=['POST'])
def message():
    data = request.get_json()

    from_id = data.get('from')
    text = data.get('text', '').lower()
    is_group = data.get('isGroup', False)
    participants = data.get('participants', [])

    if not from_id or not text:
        return jsonify({'reply': None})

    # Respond to .tagall
    if is_group and text == '.tagall':
        mention_text = '👥 Tagging all:\n' + ' '.join([f'@{p.split("@")[0]}' for p in participants])
        
        return jsonify({'reply': mention_text, 'mentions': participants})
        


    # Basic replies
    if 'hi' in text or 'hello' in text:
        return jsonify({'reply': f'👋 Hello from the bot!'})

    if 'help' in text:
        return jsonify({'reply': 'Commands:\n- `.tagall` to tag everyone\n- `hello` or `hi` for greetings'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
