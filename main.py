from application.interfaces.vizualization import app
from application.services import stock_exchange as se
from core.entities.eager_broker import EagerBroker
from core import setup


if __name__ == "__main__":
    setup.run()
    #app.run_server(debug=True)
