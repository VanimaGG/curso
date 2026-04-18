import discord
from bot_logic import gen_pass, gen_emoji, flip_coin

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logamos como {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # SENHA
    if message.content.startswith('$senha'):
        await message.channel.send("Sua senha: " + gen_pass(10))

    # EMOJI
    elif message.content.startswith('$emoji'):
        await message.channel.send(gen_emoji())

    # MOEDA
    elif message.content.startswith('$coin'):
        await message.channel.send("Resultado: " + flip_coin())

    # CONTADOR
    elif message.content.startswith('$count'):
        try:
            n = int(message.content.split()[1])

            if n > 50:
                await message.channel.send("Número muito grande! Máximo é 50.")
                return

            numeros = " ".join(str(i) for i in range(1, n + 1))
            await message.channel.send(numeros)

        except:
            await message.channel.send("Use assim: $count 5")

client.run("a")
