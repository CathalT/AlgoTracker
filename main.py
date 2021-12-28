from algosdk.v2client import indexer
import yagmail
import json
import time

def SendNotificationMail():
    try:
        #initializing the server connection
        yag = yagmail.SMTP(user='ctyieldlydevtest@gmail.com', password='5@ZCScZ0ssE0')
        #sending the email
        yag.send(to='cstummon@hotmail.com', subject='Yieldly Account change', contents='Hurray, it worked!')
        print("Email sent successfully")
    except:
        print("Error, email was not sent")

exit = False
#.idx_test_address = "https://testnet-algorand.api.purestake.io/idx2"
idx_main_address = "https://mainnet-algorand.api.purestake.io/idx2"

headers = {
   "X-API-Key": "ooglawu5Wm3nCvIuFzQLAaKzTswaNAwJkjJC24Ce",
}

indexer_client = indexer.IndexerClient("", idx_main_address, headers)

txn_type = "axfer" #asset transfer
account_address = 'GIUGZKIDGW2DFRL4OLBCU7NNJQPAYCVDMAIQCG757JE75KAMZ3Y22LDWZI'
limit = 1

previous_txn_id = ""
try:
    r = indexer_client.search_transactions_by_address(address=account_address, limit=limit, txn_type=txn_type)
    txn = r['transactions'][0]
    previous_txn_id = txn['id']
except:
    print("Initial transaction request failed")

while not exit:
    time.sleep(30*60)
    try:
        r = indexer_client.search_transactions_by_address(address=account_address, limit=limit, txn_type=txn_type)
        txn = r['transactions'][0]
        if previous_txn_id != txn['id']:
            transactions = r['transactions'][0]
            asset_transfer_txn = transactions['asset-transfer-transaction']
            if asset_transfer_txn["amount"] > 100:# and asset_transfer_txn["asset-id"] not algoID?:
                if asset_transfer_txn["receiver"] == account_address:
                    SendNotificationMail()
            print("Transaction search: " + json.dumps(r, indent=2, sort_keys=True))
    except:
        print("Error parsing response.")
