from application.interfaces.visualization import app
from application.services import stock_exchange as se
from core.entities.eager_broker import EagerBroker
from core import setup as core_setup


if __name__ == "__main__":
    # core_setup.run()
    app.run_server(debug=True)