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

    # ✅ 1. Welcome message
    if is_group and joined:
        mention_text = '👋 Welcome:\n' + ' '.join([f'@{p.split("@")[0]}' for p in joined])
        return jsonify({'reply': mention_text, 'mentions': joined})

    # ✅ 2. .tagall
    if is_group and text == '.tagall':
        if sender not in admins:
            return jsonify({'reply': '🚫 Only *group admins* can use `.tagall`.'})
        mention_text = '👥 Tagging all:\n' + ' '.join([f'@{p.split("@")[0]}' for p in participants])
        return jsonify({'reply': mention_text, 'mentions': participants})

    # ✅ 3. .groupinfo
    if is_group and text == '.groupinfo':
        group_size = len(participants)
        admin_count = len(admins)
        return jsonify({'reply': f'📊 Group Info:\n• Members: {group_size}\n• Admins: {admin_count}'})

    # ✅ 4. .admins
    if is_group and text == '.admins':
        mention_text = '🛡️ Admins:\n' + ' '.join([f'@{p.split("@")[0]}' for p in admins])
        return jsonify({'reply': mention_text, 'mentions': admins})

    # ✅ 5. .owner
    if is_group and text == '.owner':
        owner = admins[0] if admins else None
        if owner:
            return jsonify({'reply': '👑 Group Owner:', 'mentions': [owner]})
        else:
            return jsonify({'reply': '⚠️ No owner info available.'})

    # ✅ 6. .rules
    if is_group and text == '.rules':
        return jsonify({'reply': '📜 Group Rules:\n1. Be respectful\n2. No spamming\n3. Follow admin instructions\n4. No unrelated content'})

    # ✅ 7. Greetings
    if 'hi' in text or 'hello' in text:
        return jsonify({'reply': '👋 Hello there!'})

    # ✅ 8. Help
    if 'help' in text:
        return jsonify({'reply': '📋 Commands:\n• `.tagall`\n• `.groupinfo`\n• `.admins`\n• `.owner`\n• `.rules`\n• `hello` or `hi`'})

    return jsonify({'reply': None})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
