from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ WhatsApp Bot is running'

@app.route('/message', methods=['POST'])
def message():
    data = request.get_json()

    from_id = data.get('from')
    text = data.get('text', '').strip().lower() if data.get('text') else ''
    is_group = data.get('isGroup', False)
    participants = data.get('participants', [])
    admins = data.get('admins', [])
    sender = data.get('sender')
    joined = data.get('joined', [])

    # ✅ 1. Welcome message for new members
    if is_group and joined:
        mention_text = '👋 Welcome:\n' + ' '.join([f'@{p.split("@")[0]}' for p in joined])
        return jsonify({'reply': mention_text, 'mentions': joined})

    # ✅ 2. .tagall for admins
    if is_group and text == '.tagall':
        if sender not in admins:
            return jsonify({'reply': '🚫 Only *group admins* can use `.tagall`.'})
        mention_text = '👥 Tagging all:\n' + ' '.join([f'@{p.split("@")[0]}' for p in participants])
        return jsonify({'reply': mention_text, 'mentions': participants})

    # ✅ 3. .online for SCN members only
    if is_group and text == '.online':
        scn_members = [p for p in participants if 'scn' in p.lower()]
        if not scn_members:
            return jsonify({'reply': '⚠️ No SCN members found online.'})
        mention_text = '🟢 Online SCN members:\n' + ' '.join([f'@{p.split("@")[0]}' for p in scn_members])
        return jsonify({'reply': mention_text, 'mentions': scn_members})

    # ✅ 4. Greetings
    if 'hi' in text or 'hello' in text:
        return jsonify({'reply': '👋 Hello there!'})

    # ✅ 5. Help
    if 'help' in text:
        return jsonify({'reply': '📋 Commands:\n• `.tagall` (admin only)\n• `hello` or `hi`\n• `.online` to tag SCN members'})

    return jsonify({'reply': None})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
