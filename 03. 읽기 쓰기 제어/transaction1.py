from pymongo import MongoClient
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from pymongo.errors import ConnectionFailure, OperationFailure
import certifi

conn = "mongodb+srv://kwonshzzang:kkpig1484@cluster0.7rkwg4n.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(conn, tlsCAFile=certifi.where())

client.test.orders.drop()
client.test.inventory.drop()

client.test.inventory.insert_one(
    {
        "name": "pencil",
        "qty": 1000
    }
)

def run_transaction_with_retry(transaction_func, session):
    while True:
        try:
            transaction_func(session)
            break
        except(ConnectionError, OperationFailure) as err:
            if err.has_error_label("TransientTransactionError"):
                print("TransientTransactionError, retrying transaction....")
                continue
            else:
                raise
        
def update_orders_and_inventory(session):
    orders = session.client.test.orders
    inventory = session.client.test.inventory

    with session.start_transaction(read_concern=ReadConcern('majority'), write_concern=WriteConcern(w='majority')):
        order = 100
        orders.insert_one({
            "name": "pencil",
            "qty": order
        },session=session)
        inventory.update_one(
            {
                "name": "pencil",
                "qty": {"$gte": order}
            },
            {
                "$inc": {"qty": order * -1}
            }
        )
        commit_with_retry(session)

def commit_with_retry(session):
    while True:
        try:
            session.commit_transaction()
            print("Transaction Commited")
            print(session.client.test.orders.find_one({"name": "pencil"}))
            print(session.client.test.inventory.find_one({"name": "pencil"}))
            break
        except(ConnectionFailure, OperationFailure) as err:
            if err.has_error_label("UnknownTransactionCommitResult"):
                print("UnknownTransactionCommitResult, retrying commit operation...")
                continue
            else:
                print("Error during commit...")
                raise

        

with client.start_session() as session:
    try:
        run_transaction_with_retry(update_orders_and_inventory, session)
    except:
        raise