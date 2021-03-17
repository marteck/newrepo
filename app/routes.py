from flask import render_template
from flask import request, session
from app import app
from random import shuffle


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def card_value(self):
        if self.rank in ["Десятка", "Валет", "Дама", "Король"]:
            return 10
        else:
            return [" ", "Туз", "Двойка", "Тройка", "Четверка", "Пятерка", "Шестерочка", "Семерка", "Восьмерка",
                    "Девятка"].index(self.rank)

    def get_rank(self):
        return self.rank

    def __str__(self):
        return '{} {},'.format(self.rank, self.suit)


class Deck:
    def __init__(self):
        ranks = ["Двойка", "Тройка", "Четверка", "Пятерка", "Шестерочка", "Семерка", "Восьмерка", "Девятка", "Десятка",
                 "Валет", "Дама", "Король", "Туз"]
        suits = ["Черва", "Пик", "Бубен", "Треф"]
        self.cards = [Card(r, s) for r in ranks for s in suits]
        shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def new_4deck(self):
        return self.cards * 4


class Hand:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        points = 0
        ace = 0
        for card in self.cards:
            points += card.card_value()
            if card.get_rank() == "Туз":
                ace += 1
        if points + ace * 10 <= 21:
            points += ace * 10
        return points

    def __str__(self):
        message = "У {0}а на руках:".format('{}'.format(self.name))
        for card in self.cards:
            message += str(card) + " "
        return message


deck = Deck()
userhand = Hand('Игрок')
dealerhand = Hand("Дилер")
in_game = True


@app.route('/', methods=['GET', 'POST'])
def index():
    user = request.args.get("username", "")
    userhand.name = user
    del userhand.cards[:]
    del dealerhand.cards[:]
    Deck()
    return render_template('index.html', user=user)


@app.route('/startgame')
def startgame():
    userhand.add_card(deck.deal_card())
    userhand.add_card(deck.deal_card())
    dealerhand.add_card(deck.deal_card())
    userhands = str(userhand)
    dealerhands = str(dealerhand)
    mes1 = userhand.get_value()
    mes2 = dealerhand.get_value()
    return render_template('game.html', userhands=userhands, dealerhands=dealerhands, mes1=mes1, mes2=mes2)


@app.route('/addcard')
def addcard():
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
            mes4 = 'Перебор. Вы проиграли!'
            in_game = False
    return render_template('more.html', userhands=userhands, dealerhands=dealerhands, mes1=mes1, mes2=mes2, mes3=mes3,
                           mes4=mes4, mes5=mes5, mes6=mes6, mes7=mes7, userhands1more=userhands1more,
                           dealerhands1more=dealerhands1more)


@app.route('/result')
def result():
    mes3 = ''
    mes4 = ''
    mes5 = 'Продолжаем игру...'
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
                mes7 = "Победа! У Дилера перебор. Сегодня Ваш день!"
                in_game = False
    if in_game:
        if userhand.get_value() > dealerhand.get_value():
            mes8 = "Вы победили!"
        if userhand.get_value() == dealerhand.get_value():
            mes9 = "Это ничья!"
        if userhand.get_value() < dealerhand.get_value():
            mes10 = "Дилер выиграл!"
    return render_template('result.html', userhands=userhands, dealerhands=dealerhands, mes1=mes1, mes2=mes2, mes3=mes3,
                           mes4=mes4, mes5=mes5, mes6=mes6, mes7=mes7, mes8=mes8, mes9=mes9, mes10=mes10,
                           userhands1more=userhands1more,
                           dealerhands1more=dealerhands1more)
