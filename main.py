import yagmail
import json
import time
import requests
import logging
from logging.handlers import RotatingFileHandler

LOG_FILENAME = 'AlgoTracker.log'
logger = logging.getLogger("RotatingLog")

def setupLogger():
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(LOG_FILENAME, maxBytes=1024*1024*20,
                                  backupCount=5)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def getTransactionAlgoExplorer(address, txn_type, limit):
    r = requests.get('https://algoindexer.algoexplorerapi.io/v2/transactions?limit='+limit+'&tx-type='+txn_type+'&address='+address)
    return r.json()

def SendNotificationMail(subject, contents):
    try:
        yag = yagmail.SMTP(user='ctyieldlydevtest@gmail.com', password='5@ZCScZ0ssE0')
        yag.send(to='cstummon@hotmail.com', subject=subject, contents=contents)
        logger.info("Email sent successfully")
    except:
        logger.warning("Error, email was not sent")

setupLogger()
logger.info("Starting AlgoTracker")
SendNotificationMail("Algotracker Restarted", "")

txn_type = "axfer" #asset transfer
account_address = "GIUGZKIDGW2DFRL4OLBCU7NNJQPAYCVDMAIQCG757JE75KAMZ3Y22LDWZI"
limit = "1"

previous_txn_id = ""
try:
    logger.info("Getting first transaction")
    r = getTransactionAlgoExplorer(account_address, txn_type, limit)
    txn = r['transactions'][0]
    previous_txn_id = txn['id']
    logger.info("Transaction search: " + json.dumps(r, indent=2, sort_keys=True))
except Exception:
    logger.warning("Initial transaction request failed")

exit = False
while not exit:
    logger.info("Waiting 30Mins before checking for new transaction")
    time.sleep(30*60)
    try:
        logger.info("Requesting new transaction info")
        r = getTransactionAlgoExplorer(account_address, txn_type, limit)
        txn = r['transactions'][0]
        new_id = txn['id']
        if previous_txn_id != new_id:
            logger.info("PreviousId: " + previous_txn_id + " , NewId: " + new_id)
            previous_txn_id = new_id
            asset_transfer_txn = txn['asset-transfer-transaction']
            if asset_transfer_txn["receiver"] == account_address:
                SendNotificationMail('Yieldly Account change', 'New transaction')
            logger.info("Transaction search: " + json.dumps(r, indent=2, sort_keys=True))
    except:
        logger.warning("Error parsing response.")
