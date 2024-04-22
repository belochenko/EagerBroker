# Eager Broker Project

This project implements the Eager Broker, a system for making buy/sell decisions in the stock market based on predefined conditions.

# Considerations and Approach

**Class Structure**:
- Define classes for Stock Exchange, Eager Broker, and Stock Symbol.
- Stock Exchange class will handle communication with the stock exchange, while Eager Broker will make buy/sell decisions.
**Subscription and Updates**:
- Implement methods in Eager Broker for subscribing to Stock Exchanges and receiving share price updates.
- Utilize Observer pattern for subscription mechanism to receive updates from Stock Exchanges.
**Decision Making**:
- Develop algorithms within Eager Broker to determine when to buy and sell shares based on specified conditions.
- Use the Strategy pattern to encapsulate different buy/sell strategies, allowing for flexibility and easy modification.
**Random Share Generation**:
- Create functions to generate random share sales or purchases with a uniform probability distribution.
- Utilize Factory pattern to generate random share transactions.
**Share Price Update**:
- Define a method for updating share prices based on the number of shares sold and bought since the last update, considering the probability distribution.
- Use the Observer pattern to notify Eager Broker of price updates from Stock Exchanges.
**Handling Multiple Stock Symbols**:
- Implement logic to handle updates for both Amazon (AMZN) and Apple (AAPL) shares separately.
- Utilize Composite pattern to manage multiple Stock Symbols efficiently.
**Testing**:
- Write unit tests for each component to ensure the correctness of the implementation.
- Use mocking frameworks to simulate interactions with Stock Exchanges for testing purposes.
**Documentation and Optimization**:
- Document the code thoroughly and provide clear instructions for usage.
- Optimize the code for efficiency and readability, adhering to clean architecture principles and design patterns.

## Project Structure

The project structure is organized as follows:
```
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
```

## Decomposition Steps

- [x] Define classes for Stock Exchange, Eager Broker, and Stock Symbol
- [x] Implement methods for subscribing to Stock Exchanges and receiving share price updates
- [x] Develop algorithms for Eager Broker to determine when to buy and sell shares
- [x] Create functions to generate random share sales or purchases
- [x] Define a method for updating share prices based on transactions
- [x] Implement logic to handle updates for both Amazon (AMZN) and Apple (AAPL) shares separately
- [ ] Write unit tests to ensure correctness of implementation
- [ ] Document the code and provide clear instructions for usage
- [ ] Optimize the code for efficiency and readability

## Usage

To run the project, execute the `main.py` file:

```bash
python main.py
```

# Dependencies

```
Python 3.x
Plotly (if visualization is enabled)
```
