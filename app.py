from flask import Flask, render_template, request, flash
import guilded
from guilded.ext import commands

app = Flask(__name__)
app.secret_key = 'minecraft1234'  # Change this!

# Guilded bot setup
bot_token = 'gapi_kzRKtqipCX6IGNNS8K1FNIFzH6dv3KjS6SF3+mKCpNDsFx5u1V4zf6i4p/IWIsFTExnUkEbOYEpJKhCJDxAYhw=='
bot = commands.Bot(command_prefix='!')

class ControlPanel:
    def __init__(self, bot):
        self.bot = bot

    async def ban_user(self, server_id, user_id, reason):
        server = await self.bot.fetch_server(server_id)
        user = await server.fetch_member(user_id)
        await user.ban(reason=reason)
        return True

    async def kick_user(self, server_id, user_id, reason):
        server = await self.bot.fetch_server(server_id)
        user = await server.fetch_member(user_id)
        await user.kick(reason=reason)
        return True

panel = ControlPanel(bot)

@app.route('/', methods=['GET', 'POST'])
async def index():
    server_id = 'jb7M2B1R'  # Replace with your server ID
    if request.method == 'POST':
        action = request.form.get('action')
        user_id = request.form.get('user_id')
        reason = request.form.get('reason') or "No reason provided"

        try:
            if action == 'ban':
                await panel.ban_user(server_id, user_id, reason)
                flash(f'Successfully banned user {user_id}', 'success')
            elif action == 'kick':
                await panel.kick_user(server_id, user_id, reason)
                flash(f'Successfully kicked user {user_id}', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

    # Fetch server information
    server = await bot.fetch_server(server_id)
    return render_template('index.html', server=server)

if __name__ == '__main__':
    bot.run(bot_token)
    app.run(debug=False)