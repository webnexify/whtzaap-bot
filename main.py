from flask import Flask, request
import requests

app = Flask(__name__)
group_members = {}

@app.route('/', methods=['GET'])
def home():
    return 'WhatsApp Bot is running '

@app.route('/webhook', methods=['POST'])
def webhook():
    message = request.form.get('Body')
    sender = request.form.get('From')
    group_id = request.form.get('GroupId')

    if not group_id:
        return 'Group ID missing', 400

    if group_id not in group_members:
        group_members[group_id] = get_group_members(group_id)

    if 'added' in message.lower() and 'to the group' in message.lower():
        new_member = message.split('added ')[1].split(' to the group')[0]
        send_whatsapp(group_id, f'Welcome @{new_member} to our group!')
        send_whatsapp(group_id, 'Audio: welcome-bgm.mp3', media_url='https://example.com/welcome-bgm.mp3')

    elif message.strip().lower() == '!mentionall':
        mentions = ', '.join([f'@{m}' for m in group_members[group_id]])
        send_whatsapp(group_id, f'Hey {mentions}!')

    elif message.lower().startswith('hello'):
        send_whatsapp(group_id, f'Hey @{sender}! How are you?')

    elif message.lower().startswith('!sticker'):
        send_whatsapp(group_id, 'Sticker', media_url='https://example.com/sticker.png')

    return 'OK', 200

def send_whatsapp(to, body, media_url=None):
    data = {'to': to, 'message': body}
    if media_url:
        data['media_url'] = media_url
    try:
        requests.post('http://localhost:3001/send', json=data)
    except Exception as e:
        print(f"Failed to send: {e}")

def get_group_members(group_id):
    return ['member1', 'member2', 'member3']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
