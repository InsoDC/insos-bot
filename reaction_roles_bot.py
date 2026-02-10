import discord
from discord.ext import commands
import json
import os

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

REACTION_ROLES = {
    # Message 1: Age Roles
    "1470561837979533395": {
        "🩷": 1469013876988448789,
        "💙": 1469014188407128248
    },
    
    # Message 2: Gender Roles
    "1470561844509806724": {
        "🌸": 1469017019276853249,
        "🪼": 1469016916172472555,
        "🪻": 1469017117020917992,
        "🐬": 1469017314530693376,
        "🌻": 1469017530516635739
    },
    
    # Message 3: Content Warning Channels
    "1470561857122078751": {
        "🩸": 1469019898100449333,
        "🔖": 1469032422879531029,
        "📌": 1469032900656889980,
        "🪷": 1469035754255810602,
        "🪽": 1469043257257492551
    },
    
    # Message 4: Ping Roles
    "1470561870208434256": {
        "💚": 1469038319416639488,
        "💛": 1469037762694091048,
        "💜": 1469037403963392011,
        "🩷": 1469038043477315725,
        "🩵": 1469037472955633754
    }
}

@bot.event
async def on_ready():
    print(f'✅ Bot is online as {bot.user}!')
    print(f'Bot ID: {bot.user.id}')
    print('━' * 50)
    print('Reaction Roles Bot is ready!')
    print('━' * 50)

@bot.event
async def on_raw_reaction_add(payload):
    """When someone adds a reaction"""
    # Ignore bot's own reactions
    if payload.member.bot:
        return
    
    message_id = str(payload.message_id)
    
    # Check if this message has reaction roles configured
    if message_id not in REACTION_ROLES:
        return
    
    emoji = str(payload.emoji)
    
    # Check if this emoji is configured for this message
    if emoji not in REACTION_ROLES[message_id]:
        return
    
    # Get the role
    guild = bot.get_guild(payload.guild_id)
    role_id = REACTION_ROLES[message_id][emoji]
    role = guild.get_role(role_id)
    
    if role:
        try:
            await payload.member.add_roles(role)
            print(f"✅ Added {role.name} to {payload.member.name}")
        except Exception as e:
            print(f"❌ Error adding role: {e}")

@bot.event
async def on_raw_reaction_remove(payload):
    """When someone removes a reaction"""
    message_id = str(payload.message_id)
    
    # Check if this message has reaction roles configured
    if message_id not in REACTION_ROLES:
        return
    
    emoji = str(payload.emoji)
    
    # Check if this emoji is configured for this message
    if emoji not in REACTION_ROLES[message_id]:
        return
    
    # Get the role
    guild = bot.get_guild(payload.guild_id)
    role_id = REACTION_ROLES[message_id][emoji]
    role = guild.get_role(role_id)
    member = guild.get_member(payload.user_id)
    
    if role and member:
        try:
            await member.remove_roles(role)
            print(f"➖ Removed {role.name} from {member.name}")
        except Exception as e:
            print(f"❌ Error removing role: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx, channel_id: int = None):
    """Create all 4 reaction role messages"""
    
    if channel_id:
        channel = bot.get_channel(channel_id)
    else:
        channel = ctx.channel
    
    if not channel:
        await ctx.send("❌ Channel not found!")
        return
    
    # Message 1: Age Roles
    embed1 = discord.Embed(
        title="🎂 Age Roles",
        description="React below to select your age group!\n\n🩷 <@&1469013876988448789>\n💙 <@&1469014188407128248>",
        color=0xFFC0CB  # Pink
    )
    embed1.set_footer(text="react to get your role")
    msg1 = await channel.send(embed=embed1)
    await msg1.add_reaction("🩷")
    await msg1.add_reaction("💙")
    
    # Message 2: Gender Roles
    embed2 = discord.Embed(
        title="🏳️‍⚧️ Pronoun Roles",
        description="Let us know your pronouns!\n\n🌸 <@&1469017019276853249>\n🪼 <@&1469016916172472555>\n🪻 <@&1469017117020917992>\n🐬 <@&1469017314530693376>\n🌻 <@&1469017530516635739>",
        color=0xB19CD9  # Purple
    )
    embed2.set_footer(text="react to get your role")
    msg2 = await channel.send(embed=embed2)
    await msg2.add_reaction("🌸")
    await msg2.add_reaction("🪼")
    await msg2.add_reaction("🪻")
    await msg2.add_reaction("🐬")
    await msg2.add_reaction("🌻")
    
    # Message 3: Content Warning Channels
    embed3 = discord.Embed(
        title="⚠️ Content Warning Channels",
        description="These channels contain sensitive content. Only react if you're comfortable.\n\n🩸 <@&1469019898100449333>\n🔖 <@&1469032422879531029>\n📌 <@&1469032900656889980>\n🪷 <@&1469035754255810602>\n🪽 <@&1469043257257492551>",
        color=0xED4245  # Red
    )
    embed3.set_footer(text="react with caution")
    msg3 = await channel.send(embed=embed3)
    await msg3.add_reaction("🩸")
    await msg3.add_reaction("🔖")
    await msg3.add_reaction("📌")
    await msg3.add_reaction("🪷")
    await msg3.add_reaction("🪽")
    
    # Message 4: Ping Roles
    embed4 = discord.Embed(
        title="🔔 Notification Roles",
        description="Choose which pings you want to receive!\n\n💚 <@&1469038319416639488>\n💛 <@&1469037762694091048>\n💜 <@&1469037403963392011>\n🩷 <@&1469038043477315725>\n🩵 <@&1469037472955633754>",
        color=0x57F287  # Green
    )
    embed4.set_footer(text="you can toggle these anytime")
    msg4 = await channel.send(embed=embed4)
    await msg4.add_reaction("💚")
    await msg4.add_reaction("💛")
    await msg4.add_reaction("💜")
    await msg4.add_reaction("🩷")
    await msg4.add_reaction("🩵")
    
    # Send configuration instructions
    config_message = f"""
✅ **All 4 reaction role messages created!**

📝 **IMPORTANT: Update the bot code with these message IDs:**

```python
REACTION_ROLES = {{
    # Message 1: Age Roles
    "{msg1.id}": {{
        "🩷": 1469013876988448789,
        "💙": 1469014188407128248
    }},
    
    # Message 2: Gender Roles
    "{msg2.id}": {{
        "🌸": 1469017019276853249,
        "🪼": 1469016916172472555,
        "🪻": 1469017117020917992,
        "🐬": 1469017314530693376,
        "🌻": 1469017530516635739
    }},
    
    # Message 3: Content Warning Channels
    "{msg3.id}": {{
        "🩸": 1469019898100449333,
        "🔖": 1469032422879531029,
        "📌": 1469032900656889980,
        "🪷": 1469035754255810602,
        "🪽": 1469043257257492551
    }},
    
    # Message 4: Ping Roles
    "{msg4.id}": {{
        "💚": 1469038319416639488,
        "💛": 1469037762694091048,
        "💜": 1469037403963392011,
        "🩷": 1469038043477315725,
        "🩵": 1469037472955633754
    }}
}}
```

Copy this and replace the REACTION_ROLES dictionary in your bot code, then restart the bot!
    """
    
    await ctx.send(config_message)



@bot.command()
async def verification_guide(ctx):
    embed = discord.Embed(
        title=" Verification Guide",
        description="Please read carefully before verifying.",
        color=0x1ABC9C  # teal color
    )
    
    embed.add_field(
        name=" Denied Users",
        value=(
            "• Users below or above the allowed age limit\n"
            "• Users identifying as `comboy` or `comgirl`\n"
            "• Users sending inappropriate or unwanted messages, especially requests for pictures\n"
            "• Users who do not disclose problematic behavior"
        ),
        inline=False
    )
    
    embed.add_field(
        name="✅ Allowed",
        value=(
            "• Users who behave appropriately\n"
            "• Political discussion is allowed if mentioned respectfully"
        ),
        inline=False
    )
    
    embed.set_footer(text="— inso • 2/8/2026 12:30 AM")
    
    await ctx.send(embed=embed)

# existing ping command
@bot.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
    """Check if bot is responsive"""
    await ctx.send(f'🏓 Pong! Latency: {round(bot.latency * 1000)}ms')

# Run the bot

@bot.command()
async def rules(ctx):
    embed = discord.Embed(
        title=" Psychiatric Units Rules",
        description="**ଘ(੭◌ˊᵕˋ)੭* ੈ♡‧₊˚ ݁ꕤ ݁₊ ⊹ . ݁˖ . ݁·ꕤ**",
        color=0x9B59B6  # nice purple color
    )
    
    embed.add_field(
        name="1️⃣ No mini modding",
        value="It undermines staff and makes our jobs difficult. Just tag a staff member.",
        inline=False
    )
    
    embed.add_field(
        name="2️⃣ No trying to “cancel” people",
        value="This server is BASED on problematic alters and allowing them a space to be raw and unfiltered. That’s the whole point!",
        inline=False
    )
    
    embed.add_field(
        name="3️⃣ Age limits",
        value="No one under the age of 13 is allowed. No one over 25 is allowed. It’s Discord TOS and for safety.",
        inline=False
    )
    
    embed.add_field(
        name="4️⃣ All “slash flash” pictures MUST be censored",
        value="Make sure any images shared are properly censored before posting.",
        inline=False
    )
    
    embed.add_field(
        name="5️⃣ Use the respected channels",
        value="The channels have a specific use, SO USE THEM appropriately.",
        inline=False
    )
    
    embed.add_field(
        name="6️⃣ Don’t be a fool",
        value="Behave respectfully. Do not cause intentional harm or disruption.",
        inline=False
    )
    
    embed.add_field(
        name="⚠️ DISCLAIMER",
        value=(
            "Our staff have the ability to decide if something you said or did was out of line. "
            "Some things go without being said, like claiming to have a disorder you don’t, self promotion, etc. "
            "DO NOT do things that you KNOW are out of line."
        ),
        inline=False
    )
    
    embed.set_footer(text="— inso • 2/8/2026 12:30 AM")
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    
    if not TOKEN:
        print("❌ ERROR: No bot token found!")
        print("Please set DISCORD_BOT_TOKEN environment variable")
        print("\nOn Windows (Command Prompt):")
        print('set DISCORD_BOT_TOKEN=your_token_here')
        print("\nOn Windows (PowerShell):")
        print('$env:DISCORD_BOT_TOKEN="your_token_here"')
        print("\nOn Linux/Mac:")
        print('export DISCORD_BOT_TOKEN=your_token_here')
    else:
        bot.run(TOKEN)

# Run the bot
if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    
    if not TOKEN:
        print("❌ ERROR: No bot token found!")
        print("Please set DISCORD_BOT_TOKEN environment variable")
        print("\nOn Windows (Command Prompt):")
        print('set DISCORD_BOT_TOKEN=your_token_here')
        print("\nOn Windows (PowerShell):")
        print('$env:DISCORD_BOT_TOKEN="your_token_here"')
        print("\nOn Linux/Mac:")
        print('export DISCORD_BOT_TOKEN=your_token_here')
    else:
        bot.run(TOKEN)
