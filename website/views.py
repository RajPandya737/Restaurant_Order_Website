from flask import Blueprint, render_template, request, flash
from .models import Ord
from . import db
data = {'spaghetti': 0, 'pasta': 0, 'ravioli': 0, 'risoto': 0, 'pizza': 0}


views = Blueprint('views', __name__)

class Order:
    def __init__(self, order: dict, price: dict):
        self.order = order
        self.price = price
        self.spaghetti = order['spaghetti'] * price['spaghetti']
        self.pasta = order['pasta'] * price['pasta']
        self.ravioli = order['ravioli'] * price['ravioli']
        self.risotto = order['risoto'] * price['risoto']
        self.pizza = order['pizza'] * price['pizza']
        self.chefs = {'Mario': {'spaghetti': 10, 'risoto': 15}, 'Luca': {'pasta': 10, 
                        'pizza': 15}, 'Marco': {'ravioli': 15}}
    def __convert(self, min):
        if min<60:
            return str(min) + ' minutes'
        elif min == 60:
            return '1 hour'
        elif min%60 == 0:
            return str(min//60) + ' hours'
        else:
            hours = min//60
            minutes = min%60
            return str(hours) + ' hours ' + str(minutes) + ' minutes'

    def estimated_time(self):
        max = 0
        for chef in self.chefs:
            temp = 0
            for r in self.chefs[chef]:
                temp+=self.chefs[chef][r]*self.order[r]
            if temp>max:
                max = temp
        return self.__convert(max)

    def __interest(self, cost):
        return str('{:.2f}'.format(cost * 1.13, 2))

    def cost(self):
        cost = self.spaghetti+self.pasta+self.ravioli+self.risotto+self.pizza
        return '$'+ self.__interest(cost)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        spaghetti = request.form.get('spaghetti')
        pasta = request.form.get('pasta')
        ravioli = request.form.get('ravioli')
        risoto = request.form.get('risoto')
        pizza = request.form.get('pizza')

        if spaghetti.isdigit() and pasta.isdigit() and ravioli.isdigit() and risoto.isdigit() and pizza.isdigit():
            price = {'spaghetti': 12, 'pasta': 12, 'ravioli': 10, 'risoto': 10, 'pizza': 13}
            data['spaghetti'] = int(spaghetti)
            data['pasta'] = int(pasta)
            data['ravioli'] = int(ravioli)
            data['risoto'] = int(risoto)
            data['pizza'] = int(pizza)
            
            order = Order(data, price)

            flash("Successfully Created Order")
            return render_template('index.html', t=order.estimated_time(), p=order.cost())

        flash('Your inputs MUST be numbers')
        return render_template('index.html', t="", p="")
    return render_template('index.html', t="", p="")
