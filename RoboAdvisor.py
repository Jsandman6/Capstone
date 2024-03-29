!pip install intrinio-sdk
import intrinio_sdk
from __future__ import print_function
import time
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException

intrinio.ApiClient().set_api_key('OjMzM2YyMjRkZmIzMTIxZjA3ODgwYTVmNjViZGJiNzM0')
intrinio.ApiClient().allow_retries(True)

identifier = ''AAPL''
start_date = ''2023-01-01''
end_date = ''2024-01-01''
frequency = 'daily'
page_size = 100
next_page = ''~null''

response = intrinio.SecurityApi().get_security_stock_prices(identifier, start_date=start_date, end_date=end_date, frequency=frequency, page_size=page_size, next_page=next_page)
print(response)

class QLearningTrader:
    def __init__(self, num_actions, num_features, learning_rate, discount_factor, exploration_prob):
        self.num_actions = num_actions
        self.num_features = num_features
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob

        # Initialize Q-table with zeros
        self.q_table = np.zeros((num_actions, num_features))

        # Initialize state and action
        self.current_state = None
        self.current_action = None


    def choose_action(self, state):
        # Exploration-exploitation trade-off
        if np.random.uniform(0, 1) < self.exploration_prob:
            return np.random.choice(self.num_actions)  # Explore
        else:
            feature_index = np.argmax(state)
            return np.argmax(self.q_table[:, feature_index])  # Exploit


    def take_action(self, action, reward):
        # Update Q-table based on the observed reward
        if self.current_action is not None:
            feature_index = np.argmax(self.current_state)
            current_q_value = self.q_table[self.current_action, feature_index]
            new_q_value = (1 - self.learning_rate) * current_q_value + \
                           self.learning_rate * (reward + self.discount_factor * np.max(self.q_table[:, feature_index]))
            self.q_table[self.current_action, feature_index] = new_q_value


        # Update current state and action
        self.current_state = None
        self.current_action = action


    def observe_real_time_data(self, identifier):
        # Fetch real-time data
        real_time_data = fetch_real_time_data(identifier)


        # Extract features from real-time data
        self.current_state = np.array([real_time_data['open'], real_time_data['high'],
                                       real_time_data['low'], real_time_data['close'],
                                       real_time_data['volume']])


    def observe_next_state(self, identifier):
        # Update the current state with the observed next state
        self.current_state = fetch_real_time_data(identifier)


def fetch_real_time_data(identifier):
    source = 'nasdaq_basic'
    response = intrinio.SecurityApi().get_security_realtime_price(identifier, source=source)


    return {
        'open': response.open_price,
        'high': response.high_price,
        'low': response.low_price,
        'close': response.last_price,
        'volume': response.last_size
    }


def calculate_reward(action, current_close, next_close):
    if action == 0:  # Buy
        return 1.0 if next_close > current_close else -1.0
    elif action == 1:  # Sell
        return 1.0 if next_close < current_close else -1.0
    else:  # Hold
        return 1.0 if next_close > current_close else -1.0 if next_close < current_close else 0.0


def calculate_profit_loss(initial_balance, suggested_action, current_close, next_close, quantity):
    if suggested_action == "Buy":
        return (next_close - current_close) * quantity
    elif suggested_action == "Sell":
        return (current_close - next_close) * quantity
    else:  # Hold
        return 0.0


def calculate_final_profit(identifier, initial_balance, quantity, num_iterations, learning_rate, discount_factor, exploration_prob):
    num_actions = 3
    num_features = 5
    q_trader = QLearningTrader(num_actions, num_features, learning_rate, discount_factor, exploration_prob)


    for i in range(num_iterations):
        q_trader.observe_real_time_data(identifier)


        action = q_trader.choose_action(q_trader.current_state)
        current_close = q_trader.current_state[3]


        time.sleep(1)  # Introduce a delay before fetching the next real-time data


        q_trader.observe_next_state(identifier)
        next_close = q_trader.current_state['close']


        reward = calculate_reward(action, current_close, next_close)
        q_trader.take_action(action, reward)


    # Fetch real-time data just after the last iteration
    final_real_time_data = fetch_real_time_data(identifier)


    # Get the final suggested action based on the last state in the Q-table
    final_suggested_action = ["Buy", "Sell", "Hold"][np.argmax(q_trader.q_table[:, np.argmax(q_trader.current_state)])]


    # Calculate profit based on the final suggested action
    final_profit = calculate_profit_loss(initial_balance, final_suggested_action, current_close, final_real_time_data['close'], quantity)


    security_identifier = 'AAPL'
calculate_final_profit(security_identifier, initial_balance = 100, 
                       quantity = 10, num_iterations = 180, learning_rate = 0.1, 
                       discount_factor = 0.9, exploration_prob = 0.2)
