# Smart Calculator Bot

## Overview

The **Smart Calculator Bot** is a versatile Telegram bot designed to perform a wide range of calculations and data visualizations. It supports multiple modes, including scientific, financial, and statistical calculations, and can handle both text and voice inputs. The bot is built using Python and leverages various libraries such as `numpy`, `matplotlib`, `requests`, and `speech_recognition` to provide a rich set of functionalities.

## Features

### 1. **Multiple Calculation Modes**
   - **Scientific Mode**: Perform complex mathematical calculations, including trigonometric functions, logarithms, and more.
   - **Financial Mode**: Handle financial calculations such as currency conversions.
   - **Statistical Mode**: Perform statistical analysis and data visualization.

### 2. **Mathematical Expressions**
   - The bot can evaluate mathematical expressions using the `asteval` library, which provides a safe environment for evaluating Python expressions.
   - Example: `2 + 2 * 3` will return `8`.

### 3. **Graph Plotting**
   - The bot can plot mathematical functions using `matplotlib`.
   - Example: `plot sin(x) from 0 to 10` will generate and send a graph of the sine function from 0 to 10.

### 4. **Currency Conversion**
   - The bot can convert currencies using real-time exchange rates from an external API.
   - Example: `convert 100 USD to EUR` will return the equivalent amount in Euros.

### 5. **Stock Lookup**
   - The bot can provide stock prices for given stock symbols.
   - Example: `stock AAPL` will return the current price of Apple Inc. stock (dummy value in the current implementation).

### 6. **Voice Input**
   - The bot can process voice messages by converting them to text using the `speech_recognition` library.
   - Example: Sending a voice message saying "2 + 2" will return `4`.

### 7. **Inline Keyboard for Mode Selection**
   - The bot provides an inline keyboard for users to select their preferred calculation mode (Scientific, Financial, Statistical).

## Code Structure

### 1. **Dependencies**
   - `telegram`: For interacting with the Telegram API.
   - `numpy`: For numerical computations.
   - `matplotlib`: For plotting graphs.
   - `requests`: For making HTTP requests to external APIs.
   - `asteval`: For safely evaluating mathematical expressions.
   - `speech_recognition`: For converting voice messages to text.
   - `pydub`: For converting audio formats.

### 2. **Configuration**
   - **API Keys**: The bot requires API keys for Telegram, currency conversion, and stock lookup. These are currently hardcoded but should be stored securely in a production environment.
   - **Logging**: The bot uses Python's `logging` module to log events and errors.

### 3. **Handlers**
   - **Start Command**: Initializes the bot and presents the mode selection keyboard.
   - **Button Handler**: Processes inline button presses to set the calculation mode.
   - **Text Handler**: Processes text messages and directs them to the appropriate function based on the content.
   - **Voice Handler**: Processes voice messages by converting them to text and then handling the text as a regular message.

### 4. **Functions**
   - **`plot_expression`**: Generates and sends a plot of a given mathematical expression.
   - **`currency_conversion`**: Converts an amount from one currency to another using real-time exchange rates.
   - **`stock_calculation`**: Provides stock prices for given stock symbols (currently a dummy implementation).
   - **`handle_voice`**: Converts voice messages to text and processes them.

## Usage

1. **Start the Bot**: Send `/start` to the bot to initialize it and select a calculation mode.
2. **Send Calculations**: Enter mathematical expressions, currency conversion requests, or stock lookup commands.
3. **Voice Input**: Send a voice message with your calculation request.
4. **Plot Graphs**: Use the `plot` command to generate and send graphs of mathematical functions.

## Example Commands

- `/start`: Start the bot and select a mode.
- `2 + 2 * 3`: Evaluate the expression.
- `plot sin(x) from 0 to 10`: Plot the sine function from 0 to 10.
- `convert 100 USD to EUR`: Convert 100 USD to Euros.
- `stock AAPL`: Get the current price of Apple Inc. stock.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MuddassirSiddiqi/SmartCalculatorBot.git
   cd SmartCalculatorBot
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
   export CURRENCY_API_KEY="your_currency_api_key"
   export STOCK_API_KEY="your_stock_api_key"
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/MuddassirSiddiqi/SmartCalculatorBot).

---

**Note**: This bot is for educational purposes and may require additional setup and API keys for full functionality. Always secure your API keys and sensitive information.
