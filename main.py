from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ WhatsApp Bot is running'

@app.route('/message', methods=['POST'])
def message():
    data = request.get_json()

    from_id = data.get('from')
    text = data.get('text', '').strip().lower()
    is_group = data.get('isGroup', False)
    participants = data.get('participants', [])
    admins = data.get('admins', [])
    sender = data.get('sender')

    if not from_id or not text:
        return jsonify({'reply': None})

    if is_group and text == '.tagall':
        if sender not in admins:
            return jsonify({'reply': '🚫 Only *group admins* can use `.tagall`.'})

        mention_text = '👥 Tagging all:\n' + ' '.join([f'@{p.split("@")[0]}' for p in participants])
        return jsonify({'reply': mention_text, 'mentions': participants})

    if 'hi' in text or 'hello' in text:
        return jsonify({'reply': '👋 Hello there!'})

    if 'help' in text:
        return jsonify({'reply': '📋 Commands:\n• `.tagall` (admin only)\n• `hello` or `hi` to greet'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

