import random
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_NAME = "💖Bot"


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

# ✅ 1. Welcome message with group rules and admin mentions
    if is_group and joined:
            mention_text = '👋 Welcome to our fam:\n' + ' '.join([f'@{p.split("@")[0]}' for p in joined])
        # Mention all admins
            admin_mentions = ' '.join([f'@{a.split("@")[0]}' for a in admins])

            rules = (
                '\n\n📜 *Group Rules:*\n'
                '1. Be respectful to everyone 🙏\n'
                '2. No spamming 🚫\n'
                '3. Keep conversations on topic 💬\n'
                '4. No offensive content ❌\n'
                f'5. Follow the admins 🛡️ {admin_mentions}'
            )

            return jsonify({
                'reply': mention_text + rules,
                'mentions': joined + admins
            })


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
            return jsonify({'reply': f'👑 Group Owner: @{owner.split("@")[0]}', 'mentions': [owner]})
        else:
            return jsonify({'reply': '⚠️ No owner info available.'})

    # ✅ 6. .rules
    if is_group and text == '.rules':
        return jsonify({'reply': '📜 Group Rules:\n1. Be respectful\n2. No spamming\n3. Follow admin instructions\n4. No unrelated content'})

    # ✅ 7. Greetings
    if 'hi' in text or 'hello' in text:
        return jsonify({'reply': '👋 Hello there!'})

    # ✅ 8. Morning greeting (mention only sender)
    if 'mrng' in text or 'good morning' in text:
            mention_text = f'☀️ Morning @{sender.split("@")[0]}! Wake up, check memes, ignore responsibilities. Repeat.'
            return jsonify({
                'reply': mention_text,
                'mentions': [sender]
            })

    # ✅ 9. bot command
    if text == 'bot':
        return jsonify({
            'reply': f"I am here! Your fabulous digital bestie 💅",
            'mentions': [sender]
        })

    # ✅ 10. who are you command
    if text == 'who are you':
        return jsonify({
            'reply': f"I'm {BOT_NAME} — cooler than your ex and smarter than your crush 😘",
            'mentions': [sender]
        })


    # ✅ 11. Help
    if 'help' in text:
        return jsonify({'reply': '📋 Commands:\n• `.tagall`\n• `.groupinfo`\n• `.admins`\n• `.owner`\n• `.rules`\n• `hello` or `hi`\n• `mrng` or `good morning`\n• `bot`\n• `who are you`'})

    return jsonify({'reply': None})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
