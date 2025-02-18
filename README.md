# Poker Bot

A Python-based poker bot designed to analyze the game state from screenshots, evaluate the best action, and provide recommendations for optimal gameplay.

## Features
- Captures and processes screenshots of a poker game
- Uses image recognition to detect cards, bets, and player actions
- Evaluates the current game state
- Sends extracted data to `pokerbot_api`, which utilizes an open-source GTO solver
- Receives the optimal strategy response from `pokerbot_api`

## Installation

### Prerequisites
- Python 3.8+
- Virtual environment (optional but recommended)
- Required dependencies (listed in `requirements.txt`)

### Setup
```sh
# Clone the repository
git clone https://github.com/yourusername/poker-bot.git
cd poker-bot

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the Bot
```sh
python main.py
```

### How It Works
1. The bot takes a screenshot of the real-time poker game.
2. It processes the image to extract relevant information (cards, bets, etc.).
3. The extracted data is sent to `pokerbot_api`, which utilizes an open-source GTO solver to calculate the best strategy.
4. The optimal action is returned to the application.
5. Future updates may include automated actions instead of just recommendations.

## System Architecture
This structure was chosen to allow renting six powerful virtual machines, setting up the `pokerbot_api` on them, and solving strategies simultaneously against each opponent in real-time poker games. This provides a significant advantage to the player by ensuring optimal decision-making at every stage.

## Configuration
- Modify `config.json` to customize settings such as detection accuracy and strategy preferences.

## Roadmap
- Improve image recognition accuracy
- Implement real-time decision-making with reinforcement learning
- Support for multiple poker platforms
- Automated mouse and keyboard control for fully autonomous play

## Contributing
Pull requests are welcome! Please open an issue first for major changes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer
This bot is for educational and research purposes only. The use of poker bots on real-money platforms may violate terms of service and result in account bans. Use responsibly.

