import time
import json
import requests

# Level Constants
##############################
trading_account = "RAH69427139"
venue = "YFNBEX"
ticker = "MAI"
##############################


# Stockfigther API Constants
#######################################################################################################
auth = {'X-Starfighter-Authorization': 'AUTH_TOKEN_HERE'}
make_order_url = "https://api.stockfighter.io/ob/api/venues/" + venue + "/stocks/" + ticker + "/orders"
get_orderbook_url = "https://api.stockfighter.io/ob/api/venues/" + venue + "/stocks/" + ticker
get_stock_quote = "https://api.stockfighter.io/ob/api/venues/" + venue + "/stocks/" + ticker + "/quote"
get_order_status = "https://api.stockfighter.io/ob/api/venues/" + venue + "/stocks/" + ticker + "/orders/" #plus id
#######################################################################################################


# Methods
#########################################
def hit_endpoint_get(url):
    r = requests.get(url, headers = auth)
    return r.json()

def hit_endpoint_post(url, data):
    r = requests.post(url, data, headers = auth)
    return r.json()

def make_order(price, qty):

    data = json.dumps({
      "account": trading_account,
      "venue": venue,
      "stock": ticker,
      "qty": qty,
      "price": price,
      "direction": "buy",
      "orderType": "limit"
    })

    return hit_endpoint_post(make_order_url, data)

def check_orders():
    return hit_endpoint_get(get_orderbook_url)

def check_quote():
    return hit_endpoint_get(get_stock_quote)

def check_previous_order(id):
    return hit_endpoint_get(get_order_status + str(id))

def get_last_bought():
    return check_quote()["last"] / 100.00
##########################################

# MAIN
def algorithm():

    print "Working with (" + ticker + ") from " + venue + "."

    failed_times = 0
    price = 1800
    qty = 3000

    while True:

        if (failed_times == 3):
            print "INCREASING PRICE BY 50 CENTS"
            price = price + 20
            failed_times = 0

        if (failed_times == -3):
            print "DECREASING PRICE BY 25 CENTS"
            price = price - 10
            failed_times = 0

        print "buying " + str(qty) + " @ " + str(price)
        r = make_order(price, qty)

        #print r

        id = r["id"]
        filled = r["totalFilled"] > (0.50 * qty)

        if (filled == False):
            print "not 75% filled -- only " + str((r["totalFilled"] * 100.00 / qty)) + "%"
            print "waiting 5 secs..."
        else:
            print "filled! -- continuing in 5 secs"
            failed_times = failed_times - 1
            time.sleep(1)
            continue

        time.sleep(1)

        if (filled == False):
            total = check_previous_order(id)["totalFilled"]
            filled = total > (0.50 * qty)
            if (filled):
                print "now it is filled -- continuing"
                failed_times = failed_times - 1
                continue
            else:
                print "not completely filled (now " + str(total) + ")" + " -- wait"
                failed_times = failed_times + 1
                time.sleep(1)




algorithm()