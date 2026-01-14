# ♟️ AI Chess Arena

An autonomous **AI vs AI chess system** built using Python, Streamlit, and custom chess engines.

## Features
- Autonomous AI vs AI gameplay (no human input)
- International chess rules (FIDE compliant)
- Minimax AI with:
  - Dynamic depth
  - Check bonus
  - King safety heuristic
- Monte Carlo Tree Search (MCTS) AI
- Real-time animated chess board
- Highlight last move & check state
- Adjustable game speed
- Clean UI for demos & interviews

## AI Agents
- **Minimax++**: Alpha-beta pruning with heuristic evaluation
- **MCTS**: Simulation-based decision making

## Tech Stack
- Python
- Streamlit
- python-chess

## How to Run Locally

```bash
# Clone repo
git clone https://github.com/your-username/ai-chess-arena.git
cd ai-chess-arena

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run ui/app.py
