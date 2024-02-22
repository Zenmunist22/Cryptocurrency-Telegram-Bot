import datetime
from zoneinfo import ZoneInfo
order = {
    "orderId": "",
    "name":"",
    "chatId":"",
    "cart" : [],
    "orderTotalUSD": 0,
    "orderTotalBTC": 0,
    "address":"",
    "delivery instructions":"",
    "status":"",
    "tracking":"",
    "txId":"",
    "orderDate": datetime.datetime.now(tz=ZoneInfo("America/Los_Angeles"))
}