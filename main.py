# Dev : AmirAliAbbasi (pa9da)
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
TOKEN = "YOUR_BOT_TOKEN"
bot = commands.Bot(command_prefix='!', intents=intents)

mail_channel_id = 1126976111323136062  # Replace with your text channel ID
mail_data = {}
message_cooldown = {}
# Dev : AmirAliAbbasi (pa9da)
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    while True:
        await asyncio.sleep(1)
        for user_id in list(message_cooldown.keys()):
            if message_cooldown[user_id] > 0:
                message_cooldown[user_id] -= 1
            else:
                del message_cooldown[user_id]

@bot.command()
async def help(ctx):
    ipembed = discord.Embed(color=discord.Color.green())
    ipembed.add_field(name="**📥 Dm :**", value="**<@your-bot-id>**",inline=False)
    ipembed.add_field(name="**📤 Reply:**", value="**For Staff Reply**",inline=False)
    ipembed.set_footer(text=f"™{ctx.guild.name}")
    await ctx.send(embed=ipembed)
# Dev : AmirAliAbbasi (pa9da)
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id

    # Check if the user is on cooldown
    if user_id in message_cooldown and message_cooldown[user_id] > 0:
        await message.channel.send(f"Please wait {message_cooldown[user_id]} seconds before sending another message.")
        return

    if isinstance(message.channel, discord.DMChannel):
        if user_id not in mail_data:
            mail_data[user_id] = []

        mail_data[user_id].append({
            'content': message.content,
            'timestamp': message.created_at
        })

        # Send an embed message to the specified text channel
        channel = bot.get_channel(mail_channel_id)
        if channel:
            embed = discord.Embed(
                title=f"New Message from {message.author}",
                description=message.content,
                timestamp=message.created_at,
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Message received by {bot.user.name}")
            await channel.send(embed=embed)

        await message.channel.send('Your message has been received!')

        # Apply cooldown
        message_cooldown[user_id] = 60  # 60 seconds cooldown
    else:
        await bot.process_commands(message)
# Dev : AmirAliAbbasi (pa9da)
@bot.command(name='checkmail')
async def check_mail(ctx):
    user_id = ctx.author.id

    if user_id in mail_data:
        messages = mail_data[user_id]

        if not messages:
            embed = discord.Embed(
                title='Mailbox',
                description='No new messages.',
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Mailbox',
                description='New messages:',
                color=discord.Color.blue()
            )
            for msg in messages:
                embed.add_field(name=f'[{msg["timestamp"]}]', value=msg["content"], inline=False)

            mail_data[user_id] = []  # Clear messages after reading
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title='Mailbox',
            description='No new messages.',
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
# Dev : AmirAliAbbasi (pa9da)
@bot.command(name='reply')
@commands.has_role('Staff')  # Replace 'Staff' with the actual role name
async def reply_mail(ctx, user_id: int, *, reply_content):
    if user_id in mail_data:
        # Find the user in mail_data and send a reply
        user = await bot.fetch_user(user_id)
        await user.send(f"Reply from Staff {ctx.author}:\n{reply_content}")
        await ctx.send(f'Reply sent to {user.name}#{user.discriminator}')
    else:
        await ctx.send('User not found in mail data.')

# Dev : AmirAliAbbasi (pa9da)
bot.run(TOKEN)
