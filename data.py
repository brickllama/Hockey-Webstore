from datetime import datetime


class Data:
    # account information
    first_name: str = ''
    last_name: str = ''
    username: str = ''
    email: str = ''
    password: str = ''
    confirmation: str = ''

    # payment information
    credit_card: str = ''
    payment_network = ['VISA', 'MasterCard', 'AMEX', 'Discover']
    date: str = ''
    time: str = ''

    # date and time
    date = datetime.today()
    date = date.strftime("%m/%d/%y")
    time = datetime.now()
    time = time.strftime("%H:%M")
