# Eager Broker Project

This project implements the Eager Broker, a system for making buy/sell decisions in the stock market based on predefined conditions.

## Project Structure

The project structure is organized as follows:
eager_broker/
│
├── core/
│ ├── init.py
│ ├── entities/
│ │ ├── init.py
│ │ └── stock_symbol.py
│ ├── factories/
│ │ ├── init.py
│ │ └── stock_symbol_factory.py
│ ├── use_cases/
│ │ ├── init.py
│ │ └── stock_symbol_interactor.py
│ └── interfaces/
│ ├── init.py
│ └── stock_symbol_repository.py
│
├── application/
│ ├── init.py
│ ├── services/
│ │ ├── init.py
│ │ └── stock_exchange.py
│ └── interfaces/
│ ├── init.py
│ └── visualization.py
│
└── main.py

## Decomposition Steps

- [ ] Define classes for Stock Exchange, Eager Broker, and Stock Symbol
- [ ] Implement methods for subscribing to Stock Exchanges and receiving share price updates
- [ ] Develop algorithms for Eager Broker to determine when to buy and sell shares
- [ ] Create functions to generate random share sales or purchases
- [ ] Define a method for updating share prices based on transactions
- [ ] Implement logic to handle updates for both Amazon (AMZN) and Apple (AAPL) shares separately
- [ ] Write unit tests to ensure correctness of implementation
- [ ] Document the code and provide clear instructions for usage
- [ ] Optimize the code for efficiency and readability

## Usage

To run the project, execute the `main.py` file:

```bash
python main.py
```

# Dependencies

Python 3.x
Plotly (if visualization is enabled)

```

```
