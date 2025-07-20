from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import re
import requests
import random

app = Flask(__name__)

BOT_NAME = "💖Bot"
user_activity = {}  # user_id -> last_active_time

# ✅ Funny replies without "gg"
funny_gg_responses = [
    "That move was smoother than butter! 🧈",
    "Is it over already? I blinked! 👀",
    "I felt that in my soul 😤",
    "You deserve an Oscar for that performance 🎭",
    "That was more intense than a soap opera 😱",
    "You just invented a new game mode 😂",
    "MVP! Most Valuable Prankster 🏆",
    "Okay, who taught you those moves? 😮",
    "Legends say they're still recovering from that 🔥",
    "Someone call the drama police! 🚨",
    "💥🔊 പൊളിച്ചു ബ്രോ... ഗെയിം കഴിഞ്ഞതും സർവർ തകര്ന്ന് കിടക്കുന്നു! 🧨🔥",
    "😵‍💫 നിന്റെ ഗെയിംപ്ലേ കണ്ട റഫറി നേരെ രാജിവച്ചു 😂🎮",
    "🧨 കളി കഴിഞ്ഞതുമാത്രം... നമ്മളെല്ലാവരും നേരെ ആശുപത്രിയിൽ അഡ്മിറ്റ്! 🔥🩻",
    "🎧 ഹെഡ്‌സെറ്റ് ഇടുമ്പോൾ ഞാന് ഷോക്കായി പോയി ഡാ... കിടപ്പിലാണിപ്പോൾ 😳💣",
    "⚡ അതു മാച്ച് അല്ല... പൂർണ്ണ ഇലക്ട്രിക് ഷോക്ക് ആണല്ലേ? 😵🔌",
    "🚁 നീ join ചെയ്‌തപ്പോള്‍ ലാഗ് കൂടി, ഹെലികോപ്റ്റര്‍ വരേണ്ടി വന്നു ഇവാക്വേറ്റ് ചെയ്യാൻ 😆🛩",
    "👽 കളിയുടെ ലെവൽ കണ്ട aliens പറഞ്ഞു: 'ഇത് കളിയാണോ അല്ലേ ദുരന്തം?' പിന്നെ പേടിച്ചു പോയി, മാക്സിൽ വന്നില്ല 😭🛸",
    "🫠 കളി കണ്ടിട്ട് ഞാൻ കീബോർഡ് പറത്തി... വീട്ടുകാർ ഇപ്പോ വരെ തിരഞ്ഞിരിക്കുന്നു 💀⌨️",
    "🔥 നീയാണ് ഗെയിമിന്റെ മോഹൻലാൽ... മാസ് എൻട്രിയിലൂടെ പൊളിച്ചു ബ്രോ 🎬👑",
    "🎮 അടിപൊളി ക്ലച്ച്... ഫോൺ കിട്ടിയില്ല, vibration കൊണ്ടാണ് പോയി കിട്ടിയത് 😭📱"
]
# ✅ Your allowed group IDs (copy them from WhatsApp)
ALLOWED_GROUPS = [
    "120363048505746465@g.us",  # MCS
    "120363419378716476@g.us",  # TESTING"
]

def get_leaderboard_image():
    url = "https://challenge.place/c/620a9e6f8aac547bb479cfd5/stage/63a493ea3b719273d482344a"

    # Example using screenshotmachine (you can also use others)
    api_url = "https://api.screenshotmachine.com"
    params = {
        "key": "YOUR_API_KEY",   # <- Get free API key
        "url": url,
        "dimension": "1024xfull",
        "format": "png",
    }

    screenshot_url = f"{api_url}?{urlencode(params)}"
    return screenshot_url


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


    # ✅ 7. Morning greeting
    if 'mrng' in text or 'good morning' in text:
        mention_text = f'☀️ Morning @{sender.split("@")[0]}! Wake up, check memes, ignore responsibilities. Repeat.'
        return jsonify({'reply': mention_text, 'mentions': [sender]})

    # ✅ 8. bot command
    if text == 'bot':
        return jsonify({'reply': f"I am here! Your fabulous digital bestie 💅", 'mentions': [sender]})

    # ✅ 9. who are you
    if text == 'who are you':
        return jsonify({'reply': f"I'm {BOT_NAME} — cooler than your ex and smarter than your crush 😘", 'mentions': [sender]})

    # ✅ 10. Track user activity
    if is_group and sender:
            sender_id = sender.split('@')[0]
            user_activity[sender_id] = datetime.datetime.now()

    # ✅ 11. activity
    if is_group and text == 'activity':
            active_members = []

            for p in participants:
                pid = p.split('@')[0]  # normalize participant ID
                if user_activity.get(pid):
                    active_members.append(p)

            active_text = 'Active Members:\n' + (
                '\n'.join([f'@{p.split("@")[0]}' for p in active_members]) if active_members else 'No one has been active yet 💤'
            )

            return jsonify({
                'reply': active_text,
                'mentions': active_members
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
        user_activity[sender_id] = datetime.datetime.now()
    
    # ✅ 14. FRIENDLY ANYONE TRIGGER
    if is_group and ('friendly anyone' in text or 'anyone friendly' in text or 'friendly' in text):
                    now = datetime.datetime.now()
                    active_threshold = now - timedelta(hours=12)
                    active_members = []
                    mention_text = "😴 No one is active right now. Maybe playing later!" # Initialize mention_text
                    for p in participants:
                        pid = p.split('@')[0]
                        last_seen = user_activity.get(pid)
                        if last_seen and last_seen >= active_threshold and p != sender:
                            active_members.append(p)
                            mention_text = (
                                "🎮 Let’s get friendly! Who’s up for a match or game?\n\n"
                                "🔥 Active players: " + ' '.join([f'@{p.split("@")[0]}' for p in active_members])
                             )

                    return jsonify({
                        'reply': mention_text,
                        'mentions': active_members
                    })

    # ✅ 15. Friendly-sticker trigger: Only when sticker text includes "friendly"
    if is_group and data.get('type') == 'sticker':
        sticker_text = data.get('sticker_text', '').lower()  # This works if your stickers have alt/caption text

        # Only respond if sticker includes keywords like "friendly"
        if any(kw in sticker_text for kw in ['friendly', 'anyone friendly', 'friendly anyone']):
            now = datetime.datetime.now()
            active_threshold = now - timedelta(hours=12)

            active_members = []
            for p in participants:
                pid = p.split('@')[0]
                last_seen = user_activity.get(pid)
                if last_seen and last_seen >= active_threshold and p != sender:
                    active_members.append(p)

            if active_members:
                mention_text = (
                    "🎮 A friendly sticker? Let’s vibe!\n\n"
                    "🔥 Active friends online: " +
                    ' '.join([f'@{p.split("@")[0]}' for p in active_members])
                )
            else:
                mention_text = "😴 No one is active now to vibe with your sticker..."

            return jsonify({
                'reply': mention_text,
                'mentions': active_members
            })


    # ✅ 16. Block links if not sent by admin
    if is_group and re.search(r'https?://', text):  # If message has a link
        if sender not in admins:
            return jsonify({
                'delete': True,  # Tell Baileys to delete the message
                'reply': '❌ Only admins are allowed to share links.'
            })

    # ✅ 17. Trigger only if someone types exactly "gg"
    if is_group and text == "gg":
        response_text = random.choice(funny_gg_responses)
        return jsonify({'reply': response_text})

    # ✅ 18. Only respond to 'point' in allowed groups
    if text == "point" and from_id in allowed_groups:
        leaderboard_img = get_leaderboard_image()
        return jsonify({
            "image": leaderboard_img,
            "caption": "🏆 *Current Leaderboard*"
        })
       

    # ✅ 19. Help
    if 'help' in text:
        return jsonify({'reply': '📋 Commands:\n• `tagall`\n• `groupinfo`\n• `admins`\n• `owner`\n• `.rules`\n• `mrng` or `good morning`\n• `bot`\n• `who are you`\n• `.champion`\n• `activity`\n• `friendly anyone` or `anyone friendly` or `friendly`\n• `gg`\n• `point`'})

    return jsonify({'reply': None})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
