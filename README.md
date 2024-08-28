# Chess AI Optimization: MCTS & Alpha-Beta Pruning

This project focuses on optimizing Chess AI capabilities using Monte Carlo Tree Search (MCTS) and Alpha-Beta Pruning techniques. Implemented in Python, the AI competes against human players and other AIs, showcasing advanced decision-making and strategic depth. Explore how these algorithms improve game performance and their practical applications in artificial intelligence.

## Project Overview

- **Monte Carlo Tree Search (MCTS)**: A heuristic search algorithm for decision processes, particularly effective in game AI.
- **Alpha-Beta Pruning**: An optimization technique for minimax algorithms, used to decrease the number of nodes evaluated in the search tree.
- **AI Competition**: The AI competes against human players and other AIs, demonstrating its enhanced strategy and performance.

## Features

- **Enhanced Decision-Making**: Implements MCTS and Alpha-Beta Pruning to improve the AI’s ability to make strategic decisions in complex game scenarios.
- **Competitive AI**: The AI is capable of competing at different difficulty levels, offering a challenging experience for players.
- **Python Implementation**: The project is fully implemented in Python, ensuring flexibility and ease of integration.

## How It Works

### Monte Carlo Tree Search (MCTS)

MCTS is used to explore possible moves by simulating many random games and selecting the move that leads to the best outcome. The algorithm involves four key steps:

1. **Selection**: Choose the node to explore based on a balance of exploration and exploitation.
2. **Expansion**: Add one or more child nodes to expand the tree.
3. **Simulation**: Play out a random simulation from the newly added node.
4. **Backpropagation**: Update the values of nodes based on the simulation results.

### Alpha-Beta Pruning

Alpha-Beta Pruning is applied to minimize the number of nodes evaluated in the minimax algorithm's search tree. It eliminates branches that do not influence the final decision, thereby optimizing the decision-making process.

## Demo Video

Watch the demo video on YouTube: [Point of Sale System Demo](https://www.youtube.com/watch?v=Yi2cku5pkWQ)

## Installation

1. Clone the repository:
    git clone https://github.com/Faiqster/Optimizing-Chess-AI-MCTS-Alpha-Beta-Pruning.git
    cd chess-ai-optimization

2. Install the required dependencies:
    pip install -r requirements.txt

3. Run the Chess AI:
    python chess_ai.py

## Requirements

- Python 3.x
- NumPy
- Chess libraries (e.g., `python-chess`)

## Install the dependencies using
pip install -r requirements.txt

## Project Structure
    chess_ai.py: Main script to run the Chess AI.
    mcts.py: Implements the Monte Carlo Tree Search algorithm.
    alpha_beta_pruning.py: Implements the Alpha-Beta Pruning technique.
    requirements.txt: Lists the Python dependencies needed to run the project.
    
## Future Work
Implementing additional AI techniques like Neural Networks for deeper learning.
Enhancing the UI for better user interaction.
Exploring the integration of real-time player feedback to adapt AI strategies.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
