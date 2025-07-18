from flask import Flask, request, jsonify
import datetime
from datetime import timedelta

app = Flask(__name__)

BOT_NAME = "💖Bot"
user_activity = {}  # user_id -> last_active_time


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

    # ✅ Track user activity
    if is_group and sender:
        sender_id = sender.split('@')[0]
        user_activity[sender_id] = datetime.datetime.now()

    # ✅ 1. Welcome message with rules & admin mentions
    if is_group and joined:
        mention_text = '👋 Welcome to our fam:\n' + ' '.join([f'@{p.split("@")[0]}' for p in joined])
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

    # ✅ 2. tagall
    if is_group and text == 'tagall':
        if sender not in admins:
            return jsonify({'reply': '🚫 Only *group admins* can use `.tagall`.'})
        mention_text = '👥 Tagging all:\n' + ' '.join([f'@{p.split("@")[0]}' for p in participants])
        return jsonify({'reply': mention_text, 'mentions': participants})

    # ✅ 3. groupinfo
    if is_group and text == 'groupinfo':
        group_size = len(participants)
        admin_count = len(admins)
        return jsonify({'reply': f'📊 Group Info:\n• Members: {group_size}\n• Admins: {admin_count}'})

    # ✅ 4. admins
    if is_group and text == 'admins':
        mention_text = '🛡️ Admins:\n' + ' '.join([f'@{p.split("@")[0]}' for p in admins])
        return jsonify({'reply': mention_text, 'mentions': admins})

    # ✅ 5. owner
    if is_group and text == 'owner':
        owner = admins[0] if admins else None
        if owner:
            return jsonify({'reply': f'👑 Group Owner: @{owner.split("@")[0]}', 'mentions': [owner]})
        else:
            return jsonify({'reply': '⚠️ No owner info available.'})

    # ✅ 6. rules
    if is_group and text == '.rules':
        return jsonify({'reply': '📜 Group Rules:\n1. Be respectful\n2. No spamming\n3. Follow admin instructions\n4. No unrelated content'})

    # ✅ 7. Greetings
    if 'hi' in text or 'hello' in text:
        return jsonify({'reply': '👋 Hello there!'})

    # ✅ 8. Morning greeting
    if 'mrng' in text or 'good morning' in text:
        mention_text = f'☀️ Morning @{sender.split("@")[0]}! Wake up, check memes, ignore responsibilities. Repeat.'
        return jsonify({'reply': mention_text, 'mentions': [sender]})

    # ✅ 9. bot command
    if text == 'bot':
        return jsonify({'reply': f"I am here! Your fabulous digital bestie 💅", 'mentions': [sender]})

    # ✅ 10. who are you
    if text == 'who are you':
        return jsonify({'reply': f"I'm {BOT_NAME} — cooler than your ex and smarter than your crush 😘", 'mentions': [sender]})

    # ✅ 11. activity
    if is_group and text == 'activity':
        now = datetime.datetime.now()
        active_threshold = now - timedelta(days=30)

        active_members = []
        inactive_members = []

        for p in participants:
            pid = p.split('@')[0]
            last_seen = user_activity.get(pid)
            if last_seen and last_seen >= active_threshold:
                active_members.append(p)
            else:
                inactive_members.append(p)

        active_text = '✅ Active Members (last 30 days):\n' + (
            '\n'.join([f'@{p.split("@")[0]}' for p in active_members]) if active_members else 'No one is active 💤'
        )
        inactive_text = '\n\n⚠ Inactive Members:\n' + (
            '\n'.join([f'@{p.split("@")[0]}' for p in inactive_members]) if inactive_members else 'All members are active 🎉'
        )

        return jsonify({
            'reply': active_text + inactive_text,
            'mentions': active_members + inactive_members
        })

    # ✅ 12. .champion – Hall of Fame
    if is_group and text == '.champion':
        hof_message = (
            '🎖✨ *MANIACS – OFFICIAL TOURNAMENT HALL OF FAME* ✨🎖\n'
            '🔥 Where Legends Are Crowned… 🔥\n'
            '━━━━━━━━━━━━━━━━━━━━━━━\n\n'
            '🔰 🏆 *LEAGUE OF LEGENDS – CHAMPIONS* 🏆 🔰\n'
            '🎮 Victory isn’t luck — it’s legacy.\n\n'
            '🥇 Season 1 – *KARTHIK* 🌪\n'
            '🥇 Season 2 – *MANOJ* 💥\n'
            '🥇 Season 3 – *MANOJ* ⚔\n'
            '🥇 Season 4 – *MANOJ* 👑 (Hat-trick King!)\n'
            '🥇 Season 5 – *HARI* 🔥\n\n'
            '━━━━━━━━━━━━━━━━━━━━━━━\n\n'
            '🔰 🏆 *MASTER CUP – CHAMPIONS* 🏆 🔰\n'
            '🎯 The finest of the finest clash here.\n\n'
            '🥇 Season 1 – *ALBI* 🚀\n'
            '🥇 Season 2 – *SHARON* 🧊\n\n'
            '━━━━━━━━━━━━━━━━━━━━━━━\n\n'
            '👑 *RESPECT THE CHAMPIONS*\n'
            '📈 Train hard. Think sharp. Stay deadly.\n'
            '🕹 Next Season Loading… Are *YOU* Ready?\n'
            '#MANIACS🔥 #LegendsOfManiacs #HallOfFame #GamingGlory'
        )
        return jsonify({'reply': hof_message})

    # ✅ 13. Track user activity on all group messages
    if is_group and sender:
        sender_id = sender.split('@')[0]
        user_activity[sender_id] = datetime.now()

    # ✅ 14. FRIENDLY ANYONE TRIGGER
    if is_group and 'friendly anyone' in text:
        now = datetime.datetime.now()
        active_threshold = now - timedelta(hours=12)

        active_members = []
        for p in participants:
            pid = p.split('@')[0]
            last_seen = user_activity.get(pid)
            if last_seen and last_seen >= active_threshold:
                active_members.append(p)

        mention_text = (
            "🎮 Let’s get friendly! Who’s up for a match or game?\n\n"
            "🔥 Active players: " +
            (' '.join([f'@{p.split("@")[0]}' for p in active_members]) if active_members else '😴 Nobody active right now… Wake them up! 🔔')
        )

        return jsonify({
            'reply': mention_text,
            'mentions': active_members
        })


    # ✅ 15. Help
    if 'help' in text:
        return jsonify({'reply': '📋 Commands:\n• `tagall`\n• `groupinfo`\n• `admins`\n• `owner`\n• `.rules`\n• `hello` or `hi`\n• `mrng` or `good morning`\n• `bot`\n• `who are you`\n• `.champion`\n• `activity`\n• `friendly anyone`'})

    return jsonify({'reply': None})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
