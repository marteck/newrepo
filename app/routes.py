from uuid import uuid4

from flask import render_template
from flask import request, redirect, url_for

from app import app
from game import Deck, Hand

deck = Deck()
userhand = Hand('Player')
dealerhand = Hand("Dealer")
in_game = True
status = dict()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        deck = Deck()
        user = request.form['username']
        userhand.name = user
        dealerhand.name = 'Dealer'
        Deck()
        _id = uuid4()
        status.update({str(_id): {'user': user, 'bot': dealerhand, 'deck': deck}})
        return redirect(url_for('startgame', id=_id))


@app.route('/startgame', methods=['GET'])
def startgame():
    _game = status[request.args['id']]
    user: Hand = _game['user']
    dealerhand: Hand = _game['bot']
    deck: Deck = _game['deck']

    del userhand.cards[:]
    del dealerhand.cards[:]
    Deck()

    userhand.add_card(deck.deal_card())
    userhand.add_card(deck.deal_card())
    dealerhand.add_card(deck.deal_card())
    userhands = str(userhand)
    dealerhands = str(dealerhand)
    mes1 = userhand.get_value()
    mes2 = dealerhand.get_value()
    return render_template('game.html', id=request.args['id'], userhands=userhands, dealerhands=dealerhands, mes1=mes1,
                           mes2=mes2, userhand=userhand)


@app.route('/addcard')
def addcard():
    _game = status[request.args['id']]
    user: Hand = _game['user']
    dealerhand: Hand = _game['bot']
    deck: Deck = _game['deck']
    mes3 = ''
    mes4 = ''
    mes5 = ''
    mes6 = ''
    mes7 = ''
    userhands = str(userhand)
    dealerhands = str(dealerhand)
    mes1 = userhand.get_value()
    mes2 = dealerhand.get_value()
    userhands1more = ''
    dealerhands1more = ''
    in_game = True
    if userhand.get_value() < 21:
        userhand.add_card(deck.deal_card())
        userhands1more = str(userhand)
        mes3 = userhand.get_value()
        if userhand.get_value() > 21:
            mes4 = 'You are overkill, you have lost!'
            status.pop(request.args['id'])
            in_game = False
    return render_template('more.html',id=request.args['id'], userhands=userhands, dealerhands=dealerhands, mes1=mes1,
                           mes2=mes2, mes3=mes3,
                           mes4=mes4, mes5=mes5, mes6=mes6, mes7=mes7, userhands1more=userhands1more,
                           dealerhands1more=dealerhands1more, userhand=userhand)


@app.route('/result', methods=['GET'])
def result():

    _game = status[request.args['id']]
    user: Hand = _game['user']
    dealerhand: Hand = _game['bot']
    deck: Deck = _game['deck']
    mes3 = ''
    mes4 = ''
    mes5 = 'We continue the game...'
    mes6 = ''
    mes7 = ''
    mes8 = ''
    mes9 = ''
    mes10 = ''
    userhands = str(userhand)
    dealerhands = str(dealerhand)
    mes1 = userhand.get_value()
    mes2 = dealerhand.get_value()
    userhands1more = ''
    dealerhands1more = ''
    in_game = True
    if in_game:
        while dealerhand.get_value() < 17:
            dealerhand.add_card(deck.deal_card())
            dealerhands1more = str(dealerhand)
            mes6 = dealerhand.get_value()
            if dealerhand.get_value() > 21:
                mes7 = "Victory! The Dealer is overkill. It's your day today!"
                in_game = False
    if in_game:
        if userhand.get_value() > dealerhand.get_value():
            mes8 = "You won!"
        if userhand.get_value() == dealerhand.get_value():
            mes9 = "It's draw game!"
        if userhand.get_value() < dealerhand.get_value():
            mes10 = "Dealer won!"
    status.pop(request.args['id'])
    return render_template('result.html', userhands=userhands, dealerhands=dealerhands, mes1=mes1, mes2=mes2, mes3=mes3,
                           mes4=mes4, mes5=mes5, mes6=mes6, mes7=mes7, mes8=mes8, mes9=mes9, mes10=mes10,
                           userhands1more=userhands1more, userhand=userhand,
                           dealerhands1more=dealerhands1more)
