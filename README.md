# Telegram Check Bot

A simple Telegram bot that generates customized PDF invoices based on user input. It allows adding multiple line items with descriptions and prices, calculates the total, and includes payment details at the bottom of the invoice.

## Features

- **Multiple Line Items**: Users can specify multiple items with descriptions and prices for each invoice.
- **Total Calculation**: Automatically calculates the total based on line items.
- **PDF Generation**: Creates a professional-looking PDF invoice.
- **Payment Details**: Displays payment instructions and bank details at the bottom of each invoice.

## Getting Started

### Prerequisites

- Python 3.6+
- A Telegram bot token from BotFather
- The required Python packages, as listed in `requirements.txt`

### Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/telegram-check-bot.git
    cd telegram-check-bot
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables:
   - Create a `.env` file in the project root and add your Telegram bot token:
     ```plaintext
     TELEGRAM_API_KEY=your_telegram_api_key
     ```

### Usage

1. Start the bot:
    ```bash
    python main.py
    ```

2. Interact with the bot on Telegram by sending messages in the following format:
    ```
    Month, Holder Name, Mobile, Item1:Price1, Item2:Price2, ...
    ```
   **Example**: `October 2024, John Doe, +1234567890, Yoga Classes:500, Pilates:300`

3. The bot will generate and send a PDF invoice based on the provided data.

## Example Invoice

An example invoice includes:
- Descriptions and prices for each line item
- Dotted lines between item descriptions and prices
- Total amount at the end
- Bank payment details centered at the bottom

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
