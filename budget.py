class Category:
    def __init__(self,name):
        self.name = name
        self.ledger = list()
        self.balance = 0

    def deposit(self,amount,description = ""):
        self.ledger.append({"amount":amount,"description":description})
        self.edit_balance(amount)

    def check_funds(self,amount):
        if amount > self.balance: return False
        else: return True
    
    def withdraw(self,amount,description = ""):
        if self.check_funds(amount):
            self.ledger.append({"amount":-amount,"description":description})
            self.edit_balance(-amount)
            return True
        else: return False

    def edit_balance(self,amount):
        self.balance += amount

    def get_balance(self):
        return self.balance

    def get_name(self):
        return self.name

    def get_spent(self):
        spent = 0
        for move in self.ledger:
            if move["amount"] < 0:
                spent += move["amount"]
        return spent

    def transfer(self,amount,acount):
        if self.check_funds(amount):
            self.balance = self.balance - amount
            self.ledger.append({"amount":-amount,"description":'Transfer to ' + acount.name})
            acount.ledger.append({"amount":amount,"description":'Transfer from ' + self.name})
            acount.edit_balance(amount)
            return True
        else: return False

    def __str__(self) -> str:
        result = self.name.center(30,'*') + '\n'
        for move in self.ledger:
            result = result + move["description"][:23].ljust(23,' ') + format(move["amount"],'.2f').rjust(7,' ') + '\n'
        result = result + 'Total: ' + str(self.balance)
        return result

def create_spend_chart(categories):
    percentage = 100
    spent = list()
    total_spent = 0
    names = list()
    maxlen = 0
    i = 0
    for categori in categories:
        spent.append( categori.get_spent() )
        total_spent += spent[i]
        names.append((categori.get_name(),len(categori.get_name())))
        if len(categori.get_name()) > maxlen:
            maxlen = len(categori.get_name())
        i += 1
    i -= 1
    while i >=0:
        spent[i] = int((spent[i]/total_spent)*10)*10
        i -= 1
    graph = "Percentage spent by category\n"
    while percentage >= 0:
        graph += str(percentage).rjust(3,' ') + '|'
        for percent in spent:
            if percent >= percentage:
                graph += ' o '
            else:
                graph += '   '
        graph += ' \n'
        percentage -= 10
    graph += '    -'+'---' * len(spent)+'\n'
    i = 1
    while( i <= maxlen ):
        graph += '    '
        for name in names:
            if name[1] >= i:
                graph += ' ' +name[0][i - 1] + ' '
            else:
                graph += '   '
        graph += ' \n'
        i += 1
    return graph[:-1]