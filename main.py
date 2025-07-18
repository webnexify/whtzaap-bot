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
    joined = data.get('joined', [])  # ✅ NEW: list of new member IDs if someone joined

    if not from_id:
        return jsonify({'reply': None})

    # ✅ Welcome Message if someone joined
    if is_group and joined:
        mentions = joined
        welcome_text = '🎉 Welcome ' + ' '.join([f'@{u.split("@")[0]}' for u in joined])
        return jsonify({'reply': welcome_text, 'mentions': mentions})

    if not text:
        return jsonify({'reply': None})

    # ✅ .tagall command
    if is_group and text == '.tagall':
        if sender not in admins:
            return jsonify({'reply': '🚫 Only *group admins* can use `.tagall`.'})

        mention_text = '👥 Tagging all:\n' + ' '.join([f'@{p.split("@")[0]}' for p in participants])
        return jsonify({'reply': mention_text, 'mentions': participants})

    # ✅ .online command (non-admin)
    if is_group and text == '.online':
        mention_text = '✅ Online:\n' + ' '.join([f'@{p.split("@")[0]}' for p in participants])
        return jsonify({'reply': mention_text, 'mentions': participants})

    # ✅ Greetings
    if 'hi' in text or 'hello' in text:
        return jsonify({'reply': '👋 Hello there!'})

    # ✅ Help
    if 'help' in text:
        return jsonify({'reply': '📋 Commands:\n• `.tagall` (admin only)\n• `.online`\n• `hello` or `hi`'})

    return jsonify({'reply': None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
