from bit.network import currency_to_satoshi_cached
from bit import Key, PrivateKey, PrivateKeyTestnet
def getMainMenu(name:str=""):
    msg =  f"""
    Hey, {name}!\n\nWelcome to Tommy's Peanut Butter & Jelly Sandwich Stand, below are buttons on navigating, ordering and information.
    """
    keyboard=[
        [
            "Menu"
        ],
        [
            "About Us",
            "Contact Us"
        ],
        [
            "Shipping/Payment",
            "Bulk Buyers"
        ],
    ]
    return msg, keyboard


def getAboutUsKeyboard():
    msg = """
Welcome to the Peanut Butter Jelly Stand, where we celebrate the timeless combination of peanut butter and jelly in all its delicious forms!\n\nAt our store, we specialize in offering a wide variety of products centered around this beloved duo, from classic sandwiches to innovative twists that will tantalize your taste buds.
    """
    keyboard=[
        ["Back"]
    ]
    return msg, keyboard


def getContactUsKeyboard():
    msg = """
     <CONTACT US INFORMATION HERE>
    """
    keyboard=[
        ["Back"]
    ]
    return msg, keyboard

def getShippingPaymentKeyboard():
    msg = """
    ▶ WE SHIP WITHIN 24HRS AFTER PAYMENT HAS BEEN CONFIRMED
    ▶ WE ACCEPT BTC, USDT (TRC20)
        ▶ VENMO/CASHAPP USERS CAN PURCHASE/SEND BTC DIRECTLY THROUGH THE APP
    """
    keyboard=[
        ["Back"]
    ]
    return msg, keyboard

def getBulkBuyersKeyboard():
    msg = """
    ▶ Want massive amounts of Peanut Butter and Jelly Sandwiches?.
    \n▶ Contact Details coming soon!
    """
    keyboard=[
        ["Back"]
    ]
    return msg, keyboard

def getShippingPaymentKeyboard():
    msg = """
    ▶ Can't wait for your PB&J order? Track it here!
    ▶ Shipping & Tracking Information Here
    """
    keyboard=[
        ["Back"]
    ]
    return msg, keyboard

### MENU KEYBOARD DEPENDENCIES


def getOrderKeyBoard(cart:[]=[]):
    btc, usd = calculateCart(cart)
    msg=f"This is your current cart\n(Item | Weight | QTY | Cost (USD))\n{getCartString(cart)}\nTotal: ${usd:.2f} USD\nPlease choose one of the following options."

    keyboard=[
        ["Browse Items"],
        ["Clear Cart"],
        ["View Cart"],
        ["Checkout"],
        ["Back"]
    ]
    return msg, keyboard

def getBrowseItemsKeyboard():
    msg="""Click an item to add to cart
\nPB&J Classic - The classic sandwich, can't go wrong  ¯\_(ツ)_/¯
\nPB&J Classic (No Crust) - The classic sandwich, crust not included
\nPB&J Sushi - For those classy PB&J Enjoyers
\nPB&J Cookies - Best cookies you'll ever eat
\nPB&J Milkshake - Ice Cream with PB&J
\nPB&J Soup - This option is if you ever wanted to try drinking PB&J
\n MORE OPTIONS COMING, STAY SUBBED TO THIS CHANNEL
"""
    keyboard=[
        ["PB&J Classic"],
        ["PB&J Classic (No Crust)"],
        ["PB&J Sushi"],
        ["PB&J Cookies"],
        ["PB&J Milkshake"],
        ["PB&J Soup"],
        ["Back"]
    ]
    return msg, keyboard



def getStandardWeightKeyboard(text:str=""):
    msg=f"Please select the bread for {text}, and yes it always has bread."
    keyboard=[
        ["White Bread"],
        ["Whole Wheat"],
        ["Honey Wheat"],
        ["Back"]
    ]
    return msg, keyboard


def getQuantityKeyBoard(text:str=""):
    msg=f"Please select the quantity for {text}"
    keyboard=[
        ["1"],
        ["2"],
        ["3"],
        ["4"],
        ["5"],
        ["Back"]
    ]
    return msg, keyboard

def getViewCartKeyboard(cart:[]=[]):
    btc, usd = calculateCart(cart)
    msg=f"This is your current cart\n(Item | Weight | QTY | Cost (USD))\n{getCartString(cart)} \n Your total comes to ${usd:.2f} USD\n"
    keyboard=[
        ["Back"]
    ]
    return msg, keyboard

def getViewCartKeyboard2(cart:[]=0, btc:float=0, usd:float=0):
    msg=f"This is your current cart\n(Item | Weight | QTY | Cost (USD))\n{getCartString(cart)} \n Your total comes to ${usd:.2f} USD\n"
    keyboard=[
        ["Back"]
    ]
    return msg, keyboard

def getCheckoutKeyboard(cart:[]=[]):
    btc, usd = calculateCart(cart)
    msg=f"This is your current cart\n(Item | Weight | QTY | Cost (USD))\n{getCartString(cart)}\nYour total comes to ${usd:.2f} USD\n\nSelect \'Proceed\' to continue with the purchase"
    keyboard=[
        ["Proceed"],
        ["Back"]
    ]
    return msg, keyboard, usd

def getAddress():
    msg=f"Please enter your FULL address for shipping.\nPlease follow this format to ensure fast shipping. <Street Address>, <City>, <State> <ZipCode>"
    keyboard=[
    ]
    return msg, keyboard
def getBitCoinKeyboard(cart:[]=[], btc:float=0, usd:float=0):
    btc = currency_to_satoshi_cached(usd, "usd")
    msg=f"Please send {btc} Satoshis to this address\n"
    
    keyboard=[
        ["Continue"],
        ["Back"]
    ]
    return msg, keyboard, btc, usd

def getFinishedKeyboard():
    msg=f"Thank you for your purchase, please keep this transaction id with you.\n"
    
    keyboard=[
        ["Main Menu"],
    ]
    return msg, keyboard

def getBackKeyBoard():
    keyboard=[
        ["Back"]
    ]
    return keyboard

def getCartString(cart:[]=[]):
    res = ""
    for item in cart:
        res += f'{item}\n'
    if (len(res) == 0):
        res = "Nothing in your cart right now."
    return res


menu = {
    "PB&J Classic":{
        "White Bread":2,
        "Whole Wheat":3,
        "Honey Wheat":4
    },
    "PB&J Classic (No Crust)":{
        "White Bread":2,
        "Whole Wheat":3,
        "Honey Wheat":4
    },
    "PB&J Sushi":{
        "White Bread":2,
        "Whole Wheat":3,
        "Honey Wheat":4
    },
    "PB&J Cookies":{
        "White Bread":2,
        "Whole Wheat":3,
        "Honey Wheat":4
    },
    "PB&J Milkshake":{
        "White Bread":2,
        "Whole Wheat":3,
        "Honey Wheat":4
    },
    "PB&J Soup":{
        "White Bread":2,
        "Whole Wheat":3,
        "Honey Wheat":4
    },
}
def calculateCart(cart:[]=[]):
    # itemDesc[0] = ItemName
    # itemDesc[1] = ItemWeight
    # itemDesc[2] = QTY
    # itemDesc[3] = Cost

    cost = 0.0
    for item in cart:
        itemDesc = item.split("|")
        cost += float(itemDesc[3])
    return currency_to_satoshi_cached(cost, "usd"), round(cost,2)