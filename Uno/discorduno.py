import discord
from discord.ext import commands
import apikeys
import json
import random

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)  # Replace '!' with your desired prefix

gamestarted = False

class Uno:
    def draw_card():
        cardlist = {
            1: "1",
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
            10: "0",
            11: "skip",
            12: "reverse",
            13: "+2",
            14: "wild",
            15: "wild+4",
        }
        colorlist = {
            0: "wild",
            1: "red",
            2: "yellow",
            3: "green",
            4: "blue"
        }
        cardId = random.randint(1, 15)
        if cardId < 14:
            colorId = random.randint(1, 4)
        else:
            colorId = 0
        cardContent = cardlist[cardId]
        cardColor = colorlist[colorId]
        return (cardContent, cardColor)

    def display_uno_card(number, color):
        # Define Unicode characters for card symbols
        symbols = {
            'red': '[0;31m',
            'green': '[0;32m',
            'yellow': '[0;33m',
            'blue': '[0;34m',
            'wild': '[0;35m'
        }
        if color == 'wild':
            text = f"{symbols[color]}{number}"
            return text
        else:
            text = f"{symbols[color]}{number}"
            return text

    def add_player(id, name):
        with open('Uno/gamedata.json', 'r') as f:
            gamedata = json.load(f)
        player = []
        cardtext = []
        carddata = []
        startCards = 7

        # draw starting hand
        for i in range(startCards):
            number, color = Uno.draw_card()
            text = Uno.display_uno_card(number, color)
            cardtext.append(text)
            carddata.append((number, color))
        
        # add card data to player list
        player.append(id)
        player.append(name)
        player.append(cardtext)
        player.append(carddata)

        gamedata['playerData'].append(player)
        
        with open('Uno/gamedata.json', 'w') as f:
            json.dump(gamedata, f)

    def add_card(player):
        newplayer = []
        id = player[0]
        name = player[1]
        cardtext = player[2]
        carddata = player[3]

        number, color = Uno.draw_card()
        text = Uno.display_uno_card(number, color)
        cardtext.append(text)
        carddata.append((number, color))

        newplayer.append(id)
        newplayer.append(name)
        newplayer.append(cardtext)
        newplayer.append(carddata)
        return newplayer

    def remove_card(player, index):
        newplayer = []
        id = player[0]
        name = player[1]
        playerhand = player[2]
        carddata = player[3]

        playerhand.pop(index)
        carddata.pop(index)

        newplayer.append(id)
        newplayer.append(name)
        newplayer.append(playerhand)
        newplayer.append(carddata)
        return newplayer

    def is_number(string):
        try:
            int(string)
            return True
        except:
            return False

    def new_game():
        # rewrite json with new players
        gamedata = {
            'playerData': [],
            'roundPlayedCards': [],
            'topCard': Uno.draw_card(),
            'currentPlus': 0,
            'roundNum': 1,
            'gameTxt': [],
            'currentPlayer': 0,
            'playerOrder': 1,
            'wildselector': ''
        }
        
        with open('Uno/gamedata.json', 'w') as f:
            json.dump(gamedata, f)

    def getcurrentPlayer():
        with open('Uno/gamedata.json', 'r') as f:
            gamedata = json.load(f)
        currentPlayer = gamedata['currentPlayer']
        print(currentPlayer)
        if gamedata['playerOrder'] == 1:
            if currentPlayer >= len(gamedata['playerData']) - 1: # check if currentplayer higher than player
                gamedata['currentPlayer'] = -1
                currentPlayer = gamedata['currentPlayer']
        if gamedata['playerOrder'] == -1:
            print('switch')
            if currentPlayer < 0: # check if currentplayer lower than 0
                gamedata['currentPlayer'] = len(gamedata['playerData']) - 1
                currentPlayer = gamedata['currentPlayer']
        with open('Uno/gamedata.json', 'w') as f:
            json.dump(gamedata, f)

    def bot_message(addtext = None):
        with open('Uno/gamedata.json', 'r') as f:
            gamedata = json.load(f)
        # create message
        message = ''
        # check if player has no more cards
        for player in gamedata['playerData']:
            if player[3] == []:
                message = f'{player[1]} won'
                Uno.new_game()
                global gamestarted
                gamestarted = False
                return message
        # check which player turn
        currentPlayer = gamedata['currentPlayer']
        Uno.getcurrentPlayer()
        for players in range(len(gamedata['playerData'])):
            message += gamedata['playerData'][players][1] + '\t\t\t\t\t\t' 
            message += 'remaining cards: ' + str(len(gamedata['playerData'][players][2]))
            message += '||```ansi\n'
            for cardtext in gamedata['playerData'][players][2]:
                cardtext = cardtext.replace('\u001b', ' ')
                message += cardtext
            message += '```||'
        topcard = gamedata['topCard']
        topcard = Uno.display_uno_card(topcard[0], topcard[1])
        topcard = topcard.replace('\u001b', '')
        message += f'Top card is:```ansi\n{topcard}```'
        if addtext is not None:
            message += addtext + '\n'
        if gamedata['currentPlus'] > 0:
            message += f'draw stack: {gamedata["currentPlus"]}\n'
        message += 'It is ' + gamedata['playerData'][currentPlayer][1] + "'s turn\n"
        return message

    def wildcard(gamedata, currentPlayer, selectedCard, player, cardpos):
        gamedata['playerData'][currentPlayer] = Uno.remove_card(player, cardpos)
        gamedata['roundPlayedCards'].append(selectedCard)
        gamedata['topCard'] = selectedCard
        gamedata['currentPlayer'] += gamedata['playerOrder']
        gamedata['wildselector'] = player[0]
        Uno.getcurrentPlayer()
        with open('Uno/gamedata.json', 'w') as f:
            json.dump(gamedata, f)
        message = f'{player[1]} please select with !c (r, g, b, y)'
        return message

@bot.event
async def on_ready():
    print('Bot is ready')
    Uno.new_game()

@bot.command()
async def join(ctx):
    global gamestarted
    with open('Uno/gamedata.json', 'r') as f:
        gamedata = json.load(f)
    if gamestarted:
        await ctx.send('game has started')
    else:
        user_id = ctx.author.id
        username = ctx.author.name
        joined = False
        for players in range(len(gamedata['playerData'])):
            if gamedata['playerData'][players][0] == user_id:
                joined = True
        if joined:
            await ctx.send('you have already joined')
        else:
            await ctx.send(f'{username} joined Uno')
            Uno.add_player(user_id, username)

@bot.command()
async def leave(ctx):
    with open('Uno/gamedata.json', 'r') as f:
        gamedata = json.load(f)
    user_id = ctx.author.id
    user_name = ctx.author.name
    for player in gamedata['playerData']:
        if player[0] == user_id:
            gamedata['playerData'].remove(player)
            await ctx.send(f'{user_name} has left')
    if len(gamedata['playerData']) <= 1:
        global gamestarted
        await ctx.send('not enough players, game restarting')
        gamestarted = False
        Uno.new_game()
    with open('Uno/gamedata.json', 'w') as f:
        json.dump(gamedata, f)

@bot.command()
async def a(ctx):
    with open('Uno/gamedata.json', 'r') as f:
        gamedata = json.load(f)
    print(gamedata['currentPlayer'])
    print(len(gamedata['playerData']))

@bot.command()
async def startgame(ctx):
    with open('Uno/gamedata.json', 'r') as f:
        gamedata = json.load(f)
    minplayer = 1    # set min players

    # check if enough players to start game
    if len(gamedata['playerData']) < minplayer:
        waitfor = minplayer - len(gamedata['playerData'])
        await ctx.send(f'need {waitfor} Player(s) to start')
    else:
        # game starts
        global gamestarted
        gamestarted = True

        # message players cards, top card and turn
        message = Uno.bot_message()
        await ctx.send(message)

@bot.command()
async def playcard(ctx, cardpos):
    global gamestarted
    with open('Uno/gamedata.json', 'r') as f:
        gamedata = json.load(f)
    user_id = ctx.author.id
    Uno.getcurrentPlayer()
    # check if game started
    if gamestarted:
        
        currentPlayer = gamedata['currentPlayer']
        
        if int(gamedata['playerData'][currentPlayer][0]) == int(user_id):
            player = gamedata['playerData'][currentPlayer]
            # check if input is a number or string
            is_a_number = Uno.is_number(cardpos)
            if is_a_number:
                cardpos = int(cardpos)
                # check if number is higher than number of cards in hand
                if len(gamedata['playerData'][currentPlayer][2]) < cardpos:
                    await ctx.send(f'{cardpos} is higher than ' + str(len(gamedata['playerData'][currentPlayer][2])))
                # check if number is lower than 0
                elif cardpos <= 0:
                    await ctx.send(f'enter a number above 0')
                # play card
                else:
                    # get selected card with position according to the message
                    cardpos = cardpos - 1
                    selectedCard = gamedata['playerData'][currentPlayer][3][cardpos]
                    # check if player have to play a '+' card
                    nodrawstack = True
                    if gamedata['currentPlus'] > 0:
                        nodrawstack = False
                    # check if no wildcard is played
                    # do not allow player to play a card till the color is selected
                    if gamedata['wildselector'] == '':
                        # check if wild card (wild, wild+4) is played
                        if selectedCard[1] == 'wild':
                            if nodrawstack:      # if player do not need to play + card
                                # play wild card
                                if selectedCard[0] == 'wild':
                                    print('wild')
                                    message = Uno.wildcard(gamedata, currentPlayer, selectedCard, player, cardpos)
                                    await ctx.send(message)
                                # play wild+4 card
                                elif selectedCard[0] == 'wild+4':
                                    print('wild+4')
                                    gamedata['currentPlus'] += 4
                                    with open('Uno/gamedata.json', 'w') as f:
                                        json.dump(gamedata, f)
                                    message = Uno.wildcard(gamedata, currentPlayer, selectedCard, player, cardpos)
                                    await ctx.send(message)
                            else:    # there is a '+' stack
                                # player cannot play wild card
                                if selectedCard[0] == 'wild':
                                    print('wild')
                                    await ctx.send('cannot play wildcard')
                                # play wild+4
                                elif selectedCard[0] == 'wild+4':
                                    print('wild+4')
                                    gamedata['currentPlus'] += 4
                                    with open('Uno/gamedata.json', 'w') as f:
                                        json.dump(gamedata, f)
                                    message = Uno.wildcard(gamedata, currentPlayer, selectedCard, player, cardpos)
                                    await ctx.send(message)
                        # check +2 card played:
                        elif not nodrawstack and selectedCard[0] == '+2':
                            print('+2')
                            gamedata['playerData'][currentPlayer] = Uno.remove_card(player, cardpos)
                            gamedata['roundPlayedCards'].append(selectedCard)
                            gamedata['topCard'] = selectedCard
                            gamedata['currentPlus'] += 2
                            gamedata['currentPlayer'] += gamedata['playerOrder']
                            with open('Uno/gamedata.json', 'w') as f:
                                json.dump(gamedata, f)
                            await ctx.send(Uno.bot_message())
                        # check if number or color is the same
                        elif (selectedCard[0] == gamedata['topCard'][0] or selectedCard[1] == gamedata['topCard'][1]):
                            # check if in draw stack
                            if nodrawstack:
                                # number cards
                                if selectedCard[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'wild']:
                                    print('number')
                                    gamedata['playerData'][currentPlayer] = Uno.remove_card(player, cardpos)
                                    gamedata['roundPlayedCards'].append(selectedCard)
                                    gamedata['topCard'] = selectedCard
                                    gamedata['currentPlayer'] += gamedata['playerOrder']
                                    with open('Uno/gamedata.json', 'w') as f:
                                        json.dump(gamedata, f)
                                    await ctx.send(Uno.bot_message())
                                # +2 cards
                                elif selectedCard[0] == '+2':
                                    print('+2')
                                    gamedata['playerData'][currentPlayer] = Uno.remove_card(player, cardpos)
                                    gamedata['roundPlayedCards'].append(selectedCard)
                                    gamedata['topCard'] = selectedCard
                                    gamedata['currentPlus'] += 2
                                    gamedata['currentPlayer'] += gamedata['playerOrder']
                                    with open('Uno/gamedata.json', 'w') as f:
                                        json.dump(gamedata, f)
                                    await ctx.send(Uno.bot_message())
                                # reverse cards
                                elif selectedCard[0] == 'reverse':
                                    print('reverse')
                                    gamedata['playerData'][currentPlayer] = Uno.remove_card(player, cardpos)
                                    gamedata['roundPlayedCards'].append(selectedCard)
                                    gamedata['topCard'] = selectedCard
                                    gamedata['playerOrder'] *= -1
                                    Uno.getcurrentPlayer()
                                    if len(gamedata['playerData']) > 2:
                                        gamedata['currentPlayer'] += gamedata['playerOrder']
                                        Uno.getcurrentPlayer()
                                    with open('Uno/gamedata.json', 'w') as f:
                                        json.dump(gamedata, f)
                                    await ctx.send(Uno.bot_message())
                                # skip cards
                                elif selectedCard[0] == 'skip':
                                    print('skip')
                                    gamedata['playerData'][currentPlayer] = Uno.remove_card(player, cardpos)
                                    gamedata['roundPlayedCards'].append(selectedCard)
                                    gamedata['topCard'] = selectedCard
                                    if len(gamedata['playerData']) > 2:
                                        gamedata['currentPlayer'] += gamedata['playerOrder']
                                        gamedata['currentPlayer'] += gamedata['playerOrder']
                                    with open('Uno/gamedata.json', 'w') as f:
                                        json.dump(gamedata, f)
                                    await ctx.send(Uno.bot_message())
                            else:
                                # only allow +2
                                if selectedCard[0] == '+2':
                                    gamedata['playerData'][currentPlayer] = Uno.remove_card(player, cardpos)
                                    gamedata['roundPlayedCards'].append(selectedCard)
                                    gamedata['topCard'] = selectedCard
                                    gamedata['currentPlus'] += 2
                                    gamedata['currentPlayer'] += gamedata['playerOrder']
                                    with open('Uno/gamedata.json', 'w') as f:
                                        json.dump(gamedata, f)
                                    await ctx.send(Uno.bot_message())
                                else:
                                    await ctx.send("if you do not have a '+' card do !draw")
                        # check if top card is wild ( if starting card happens to be a wild or wild+4)
                        elif gamedata['topCard'][1] == 'wild':
                            # allow only number cards
                            if selectedCard[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                                gamedata['playerData'][currentPlayer] = Uno.remove_card(player, cardpos)
                                gamedata['roundPlayedCards'].append(selectedCard)
                                gamedata['topCard'] = selectedCard
                                gamedata['currentPlayer'] += gamedata['playerOrder']
                                with open('Uno/gamedata.json', 'w') as f:
                                    json.dump(gamedata, f)
                                await ctx.send(Uno.bot_message())
                            else:
                                await ctx.send('play a number card')
                        # forgot wat is tis
                        elif gamedata['topCard'][1] == 'wild' and not nodrawstack:
                            if selectedCard[0] == '+2':
                                gamedata['playerData'][currentPlayer] = Uno.remove_card(player, cardpos)
                                gamedata['roundPlayedCards'].append(selectedCard)
                                gamedata['topCard'] = selectedCard
                                gamedata['currentPlus'] += 2
                                gamedata['currentPlayer'] += gamedata['playerOrder']
                                with open('Uno/gamedata.json', 'w') as f:
                                    json.dump(gamedata, f)
                                await ctx.send(Uno.bot_message())
                            else:
                                await ctx.send("if you do not have a '+' card do !drawzzzz")
                        else:
                            if nodrawstack:
                                await ctx.send('cannot play card')
                            else:
                                await ctx.send("if you do not have a '+' card do !draw")
                    else:
                        await ctx.send('a wild card is played!')
            
        else:
            await ctx.send('It is not your turn')
    
    else:
        await ctx.send('game has not started')

@bot.command()
async def draw(ctx):
    # draw card
    global gamestarted
    with open('Uno/gamedata.json', 'r') as f:
        gamedata = json.load(f)
    # get user id and currentPlayer
    user_id = ctx.author.id
    currentPlayer = gamedata['currentPlayer']
    Uno.getcurrentPlayer()
    # check if game started
    if gamestarted:
        # check if it is player turn
        if int(gamedata['playerData'][currentPlayer][0]) == int(user_id):
            # check if there is a draw stack and draw the total amount of cards
            if gamedata['currentPlus'] > 0:
                print('draw stack')
                player = gamedata['playerData'][currentPlayer]
                addcard = gamedata['currentPlus']
                # repeat adding card to player
                for i in range(addcard):
                    gamedata['playerData'][currentPlayer] = Uno.add_card(player)
                name = gamedata['playerData'][currentPlayer][1]
                # remove the stack
                gamedata['currentPlus'] = 0
                # increment player
                gamedata['currentPlayer'] += gamedata['playerOrder']
                Uno.getcurrentPlayer()
                with open('Uno/gamedata.json', 'w') as f:
                    json.dump(gamedata, f)
                await ctx.send(Uno.bot_message( f'{name} drew {str(addcard)} card'))
            # regular draw
            else:
                print('draw')
                player = gamedata['playerData'][currentPlayer]
                # add card to playerData
                gamedata['playerData'][currentPlayer] = Uno.add_card(player)
                gamedata['roundPlayedCards'].append('draw')
                gamedata['currentPlayer'] += gamedata['playerOrder']
                with open('Uno/gamedata.json', 'w') as f:
                    json.dump(gamedata, f)
                name = gamedata['playerData'][currentPlayer][1]
                            
                await ctx.send(Uno.bot_message( f'{name} drew a card'))
        else:
            await ctx.send('It is not your turn')
    else:
        await ctx.send('game has not started')

@bot.command()
async def c(ctx, color):
    # color choosing after wild card played
    print('color choose')
    with open('Uno/gamedata.json', 'r') as f:
        gamedata = json.load(f)
    # check if user that user command is the player that played a wild card
    if gamedata['wildselector'] == ctx.author.id:
        if color in ['r', 'g', 'b', 'y']:
            if color == 'r':
                gamedata['topCard'][1] = 'red'
                gamedata['wildselector'] = ''
                with open('Uno/gamedata.json', 'w') as f:
                    json.dump(gamedata, f)
                message = Uno.bot_message(f'{ctx.author.name} chose red')
                await ctx.send(message)
            elif color == 'g':
                gamedata['topCard'][1] = 'green'
                gamedata['wildselector'] = ''
                with open('Uno/gamedata.json', 'w') as f:
                    json.dump(gamedata, f)
                message = Uno.bot_message(f'{ctx.author.name} chose green')
                await ctx.send(message)
            elif color == 'b':
                gamedata['topCard'][1] = 'blue'
                gamedata['wildselector'] = ''
                with open('Uno/gamedata.json', 'w') as f:
                    json.dump(gamedata, f)
                message = Uno.bot_message(f'{ctx.author.name} chose blue')
                await ctx.send(message)
            elif color == 'y':
                gamedata['topCard'][1] = 'yellow'
                gamedata['wildselector'] = ''
                with open('Uno/gamedata.json', 'w') as f:
                    json.dump(gamedata, f)
                message = Uno.bot_message(f'{ctx.author.name} chose yellow')
                await ctx.send(message)
        else:
            await ctx.send('invalid')
    else:
        await ctx.send(f'{ctx.author.name} did not play a wild card')

bot.run(apikeys.DISCORD_TOKEN)