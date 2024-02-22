import asyncio
import os
import zoneinfo
import usermodel
import logging
import keyboards
import decimal
import ordermodel
import chatmodel
import re
import db
import datetime
from copy import deepcopy
from urllib.parse import quote_plus
from bit import Key, PrivateKey, PrivateKeyTestnet
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)




MAINMENU, ABOUTUS, CONTACTUS, SHIPPINGPAYMENT, BULKBUYERS, ORDER, BROWSEITEMS, VIEWCART, CHECKOUT, WEIGHT, QTY, BITCOINPAYMENT, FINISHED, ADDRESS, SENDTXID = range(1, 16)

class PBJ_BOT:
    activityLog = {}
    def __init__(self, user, password, host, token):
        self.user = user
        self.password = password
        self.host = host
        self.token = token

    def establishDBConnection(self):
        try:
            self.PBJ_DB = db.PBJ_DB(self.user, self.password, self.host)
            return True
        except Exception as e:
            print(e)
            return False

    def main(self):
        print("Connecting to database...\n")
        if self.establishDBConnection() == True:
            print("Connection to database is established.\n")
        else:
            print("Connection to database failed.")
        

        print("Initializing User Activity Log...")
        self.activityLog = self.PBJ_DB.getLogActivity(datetime.datetime.now(tz=zoneinfo.ZoneInfo("America/Los_Angeles")))
        if self.activityLog == False:
            self.activityLog = {}
        print("Today's log: {0}".format(self.activityLog))


        print("Initializing Pickle Persistance...")
        self.persistance = PicklePersistence("db")
        print("Using the bot token to build the Bot...")
        self.application = Application.builder().token(self.token).persistence(self.persistance).build()
        print("Setting up the job queue...")
        self.job_queue = self.application.job_queue
        job_repeating = self.job_queue.run_repeating(self.sendActivity, interval = 1800, first = 1)
        job_repeating = self.job_queue.run_daily(self.clearLog, datetime.time(tzinfo=zoneinfo.ZoneInfo("America/Los_Angeles")))
        print("Job queue setup finished.")
        
        print("Initializing conversation handler...")
        
        
        self.conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                MAINMENU:[
                    MessageHandler(filters.Regex("^(Menu)$"), self.order),
                    MessageHandler(filters.Regex("^(About Us)$"), self.aboutUs),
                    MessageHandler(filters.Regex("^(Contact Us)$"), self.contactUs),
                    MessageHandler(filters.Regex("^(Shipping/Payment)$"), self.shippingPayment),
                    MessageHandler(filters.Regex("^(Bulk Buyers)$"), self.bulkBuyers),
                    
                ],
                ABOUTUS:[
                    MessageHandler(filters.Regex("^(Back)$"), self.start),
                ],
                CONTACTUS:[
                    MessageHandler(filters.Regex("^(Back)$"), self.start),
                ],
                SHIPPINGPAYMENT:[
                    MessageHandler(filters.Regex("^(Back)$"), self.start),
                ],
                BULKBUYERS:[
                    MessageHandler(filters.Regex("^(Back)$"), self.start),
                ],
                ORDER: [
                    MessageHandler(filters.Regex("^(Browse Items)$"), self.browseItems),
                    MessageHandler(filters.Regex("^(View Cart)$"), self.viewCart),
                    MessageHandler(filters.Regex("^(Clear Cart)$"), self.clearCart),
                    MessageHandler(filters.Regex("^(Checkout)$"), self.checkout),
                    MessageHandler(filters.Regex("^(Back)$"), self.start)
                ],
                BROWSEITEMS: [
                    MessageHandler(filters.Regex("^(PB&J Classic)$"), self.weight),
                    MessageHandler(filters.Regex("^(PB&J Classic (No Crust))$"), self.weight),
                    MessageHandler(filters.Regex("^(PB&J Sushi)$"), self.weight),
                    MessageHandler(filters.Regex("^(PB&J Cookies)$"), self.weight),
                    MessageHandler(filters.Regex("^(PB&J Milkshake)$"), self.weight),
                    MessageHandler(filters.Regex("^(PB&J Soup)$"), self.weight),
                    MessageHandler(filters.Regex("^(Back)$"), self.order),
                ],
                WEIGHT: [
                    MessageHandler(filters.Regex("^(White Bread)$"), self.qty),
                    MessageHandler(filters.Regex("^(Whole Wheat)$"), self.qty),
                    MessageHandler(filters.Regex("^(Honey Wheat)$"), self.qty),
                    MessageHandler(filters.Regex("^(Back)$"), self.browseItems),
                ],
                QTY: [
                    MessageHandler(filters.Regex("^(\d)$"), self.addItemToCart),
                    MessageHandler(filters.Regex("^(Back)$"), self.browseItems),
                ],
                VIEWCART: [
                    MessageHandler(filters.Regex("^(Back)$"), self.order)
                ],
                CHECKOUT: [
                    MessageHandler(filters.Regex("^(Proceed)$"), self.address),
                    MessageHandler(filters.Regex("^(Back)$"), self.order)
                ],
                ADDRESS:[
                    MessageHandler(filters.ALL, self.bitcoinPayment)
                ],
                BITCOINPAYMENT: [
                    MessageHandler(filters.Regex("^(Continue)$"), self.sendTxID),
                    MessageHandler(filters.Regex("^(Back)$"), self.order)
                ],
                SENDTXID:[
                    MessageHandler(filters.TEXT, self.finished)
                ],
                FINISHED: [
                    MessageHandler(filters.Regex("^(Main Menu)$"), self.start),
                ]

            },
            fallbacks=[MessageHandler(filters=None,callback=self.start)],
            name="my-conversation",
            persistent=True
        )   
        self.application.add_handler(self.conv_handler)
        # Run the bot until the user presses Ctrl-C
        print("Bot is successfully running.")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    

    # Main Menu Buttons
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if ("user" not in context.user_data):
            context.user_data["user"] = deepcopy(usermodel.user)
            context.user_data["user"]["chatId"] = context._chat_id
            context.user_data["user"] = self.PBJ_DB.findUser(context.user_data["user"])
            if (not context.user_data["user"]):
                context.user_data["user"] = deepcopy(usermodel.user)
                context.user_data["user"]["chatId"] = context._chat_id
                print("User not found;")

        if ("chat" not in context.user_data):
            context.user_data["chat"] = deepcopy(chatmodel.chat)
        
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])

        context.user_data["chat"]["chatId"] = context._chat_id
        context.user_data["chat"]["chat"].append(update.message.text)
        context.user_data["user"]["name"]=update.message.from_user.full_name

        reply_text, reply_keyboard = keyboards.getMainMenu(update.message.from_user.full_name)
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markup)

        return MAINMENU

    async def aboutUs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        reply_text, reply_keyboard = keyboards.getAboutUsKeyboard()
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return ABOUTUS

    async def contactUs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        reply_text, reply_keyboard = keyboards.getContactUsKeyboard()
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return CONTACTUS

    async def shippingPayment(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        reply_text, reply_keyboard = keyboards.getShippingPaymentKeyboard()
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return SHIPPINGPAYMENT

    async def bulkBuyers(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        reply_text, reply_keyboard = keyboards.getBulkBuyersKeyboard()
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return BULKBUYERS




    """
    Sending a photo
    try:
            image = open('Telegram_Bot\\Menu.jpg', 'rb')
            await context.bot.send_photo(context._chat_id, photo=image)
        except Exception as e:
            print(e)
        
    """
    ### ORDERING SECTION ###
    async def order(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        
        
        context.user_data["chat"]["chat"].append(update.message.text)
        if ("cart" not in context.user_data):
            context.user_data["cart"] = {}
        if ("order" not in context.user_data):
            context.user_data["order"]=deepcopy(ordermodel.order)
        context.user_data["order"]["cart"]=context.user_data["cart"]
        reply_text, reply_keyboard = keyboards.getOrderKeyBoard(self.getCart(context.user_data["cart"]))
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return ORDER

    async def browseItems(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        reply_text, reply_keyboard = keyboards.getBrowseItemsKeyboard()
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return BROWSEITEMS

    async def viewCart(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        reply_text, reply_keyboard = keyboards.getViewCartKeyboard(self.getCart(context.user_data["cart"]))
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return VIEWCART

    async def checkout(self, update: Update, context: ContextTypes.DEFAULT_TYPE): # add to unprocessed orders [proceed]
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        if context.user_data["cart"]:
            context.user_data["order"]["cart"]=context.user_data["cart"]
            reply_text, reply_keyboard, context.user_data["usd"] = keyboards.getCheckoutKeyboard(self.getCart(context.user_data["cart"]))
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            await update.message.reply_text(reply_text, reply_markup=markup)
            return CHECKOUT
        else: # cart doesn't exist (Total = $0)
            reply_text, reply_keyboard = keyboards.getOrderKeyBoard(self.getCart(context.user_data["cart"]))
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            await update.message.reply_text("There's nothing in your cart.", reply_markup=markup)
            await update.message.reply_text(reply_text, reply_markup=markup)
            return ORDER

    async def address(self, update: Update, context: ContextTypes.DEFAULT_TYPE): # User puts in address 
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        reply_text, reply_keyboard = keyboards.getAddress()
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return ADDRESS

    async def bitcoinPayment(self, update: Update, context: ContextTypes.DEFAULT_TYPE): # this is where the btc is asked for
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        context.user_data["order"]["address"] = update.message.text
        current_date = datetime.datetime.now()
        context.user_data["order"]["orderId"] = str(context._user_id) + "" + str(int(current_date.strftime("%Y%m%d%H%M%S")))
        context.user_data["order"]["chatId"] = str(context._user_id)
        context.user_data["btc"], context.user_data["usd"] = keyboards.calculateCart(self.getCart(context.user_data["cart"]))

        reply_text, reply_keyboard = keyboards.getViewCartKeyboard2(self.getCart(context.user_data["cart"]), context.user_data["btc"], context.user_data["usd"])
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markup)
        reply_text, reply_keyboard, btc, usd = keyboards.getBitCoinKeyboard(self.getCart(context.user_data["cart"]), context.user_data["btc"], context.user_data["usd"])
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        

        await update.message.reply_text(reply_text, reply_markup=markup)
        await update.message.reply_text("17RXFAhsTTKrKPJ84AnrVXM1hbNUhS9idi", reply_markup=markup)
        context.user_data["order"]["orderTotalUSD"] = usd
        context.user_data["order"]["orderTotalBTC"] = btc
        context.user_data["orderId"]=context.user_data["order"]["orderId"]

        return BITCOINPAYMENT

    async def sendTxID(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        await update.message.reply_text("Please enter the TxID to confirm your payment.")
        return SENDTXID

    async def finished(self, update: Update, context: ContextTypes.DEFAULT_TYPE): 
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        reply_text, reply_keyboard = keyboards.getFinishedKeyboard()
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markup)
        await update.message.reply_text(context.user_data["orderId"], reply_markup=markup)
        

        context.user_data["order"]["cart"] = self.getCart(context.user_data["cart"])
        context.user_data["order"]["status"] = "Awaiting Payment"
        context.user_data["order"]["txId"] = update.message.text


        context.user_data["orderId"]=context.user_data["order"]["orderId"]
        context.user_data["user"]["relatedOrders"].append(context.user_data["orderId"])
        context.user_data["order"]["orderDate"]= datetime.datetime.now(tz=zoneinfo.ZoneInfo("America/Los_Angeles"))
        context.user_data["order"]["name"] = context.user_data["user"]["name"]
        self.PBJ_DB.insertUnpaidOrder(context.user_data["order"])
        self.PBJ_DB.upsertUser(context.user_data["user"])
        self.PBJ_DB.upsertChat(context.user_data["chat"])
        context.user_data["cart"] = {}
        
        del context.user_data["order"]
        


        # ORDER HAS BEEN ADDED TO DATABASE

        return FINISHED

    async def weight(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        reply_text, reply_keyboard = keyboards.getStandardWeightKeyboard(update.message.text)

        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        

        await update.message.reply_text(reply_text, reply_markup=markup)
        context.user_data["item"] = update.message.text
        return WEIGHT

    async def qty(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        reply_text, reply_keyboard = keyboards.getQuantityKeyBoard(context.user_data["item"])
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markup)
        context.user_data["weight"] = update.message.text
        return QTY

    async def addItemToCart(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        cart = context.user_data["cart"]
        
        if (context.user_data["item"] not in cart):
            cart[context.user_data["item"]] = {}
            cart[context.user_data["item"]][context.user_data["weight"]] = int(update.message.text)
        elif (context.user_data["weight"] not in cart[context.user_data["item"]]):
            cart[context.user_data["item"]][context.user_data["weight"]] = int(update.message.text)
        else:
            print(str(cart[context.user_data["item"]][context.user_data["weight"]]))
            cart[context.user_data["item"]][context.user_data["weight"]] = int(update.message.text) + cart[context.user_data["item"]][context.user_data["weight"]]

        reply_text, reply_keyboard = keyboards.getViewCartKeyboard(self.getCart(cart))
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return VIEWCART

    async def clearCart(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        context.user_data["cart"]={}
        reply_text, reply_keyboard = keyboards.getViewCartKeyboard(context.user_data["cart"])
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return VIEWCART
    

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.logActivity(update.message.text, context.user_data["user"]["chatId"])
        context.user_data["chat"]["chat"].append(update.message.text)
        """Displays info on how to use the bot."""
        await update.message.reply_text("Use /start to start this bot.")
        

    async def sendActivity(self, context: ContextTypes.DEFAULT_TYPE):
        self.PBJ_DB.logActivity(datetime.datetime.now(), self.activityLog)
        await asyncio.sleep(1)


    async def clearLog(self, context: ContextTypes.DEFAULT_TYPE):
        self.activityLog.clear()
        print("It's all gone")
        await asyncio.sleep(1)

    def sanitize_input(self, input):
        sanitized_str = re.sub(r'', input, flags=re.IGNORECASE)
        return sanitized_str

    def getCart(self, cart):
        items = list(cart.keys())
        currentCart = []
        for item in items:
            weights = list(cart[item].keys())
            for weight in weights:
                price = decimal.Decimal(keyboards.menu[item][weight] * cart[item][weight]).quantize(decimal.Decimal('0.00'))
                res = item + "|" + weight + "|" + str(cart[item][weight]) + "|" + str(price) # itemName + itemWeight + itemQty + price
                currentCart.append(res)
        return currentCart
    
    def logActivity(self, activity: str, chatID: str):
        time = datetime.datetime.now(tz=zoneinfo.ZoneInfo("America/Los_Angeles"))
        timeStamp = time.strftime("%X") 
        if str(chatID) in self.activityLog:
            self.activityLog[str(chatID)][timeStamp] = activity
        else:
            self.activityLog[str(chatID)] = dict()
            self.activityLog[str(chatID)][timeStamp] = activity

if __name__ == "__main__":
    user = input("Enter username for DB: ")
    password = input("Enter password for DB: ")
    host = input("Enter host (URI) for DB: ")
    token = input("Enter Telegram Token: ")
    bot = PBJ_BOT(user, password, host, token)
    bot.main()