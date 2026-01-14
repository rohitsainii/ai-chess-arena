import sys, os, time
import streamlit as st
import chess
import chess.svg

# -------------------------------------------------
# Path Fix
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from agents.minimax_agent import MinimaxAgent
from agents.mcts_agent import MCTSAgent

# -------------------------------------------------
# Streamlit Config
# -------------------------------------------------
st.set_page_config(page_title="AI Chess Arena", layout="wide")
st.title("♟️ AI Chess Arena — Autonomous AI vs AI")

# -------------------------------------------------
# CSS Animation
# -------------------------------------------------
st.markdown(
    """
    <style>
    .chess-board {
        animation: moveFade 0.25s ease-in-out;
    }
    @keyframes moveFade {
        from {
            opacity: 0.4;
            transform: scale(0.98);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

if "running" not in st.session_state:
    st.session_state.running = False

if "status" not in st.session_state:
    st.session_state.status = "Game not started."

if "last_move" not in st.session_state:
    st.session_state.last_move = None

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.title("🎮 Controls")

white_choice = st.sidebar.selectbox("White Player", ["Minimax++", "MCTS"])
black_choice = st.sidebar.selectbox("Black Player", ["Minimax++", "MCTS"])

st.sidebar.markdown("### ⏱ Move Speed")
move_delay = st.sidebar.slider(
    "Seconds per move",
    min_value=0.05,
    max_value=1.5,
    value=0.3,
    step=0.05
)

def create_agent(name):
    return MinimaxAgent() if name == "Minimax++" else MCTSAgent()

if st.sidebar.button("▶ Start Autoplay"):
    st.session_state.board = chess.Board()
    st.session_state.white_agent = create_agent(white_choice)
    st.session_state.black_agent = create_agent(black_choice)
    st.session_state.running = True
    st.session_state.status = "Game started."
    st.session_state.last_move = None
    st.rerun()

if st.sidebar.button("⏹ Stop"):
    st.session_state.running = False
    st.session_state.status = "Game paused."

if st.sidebar.button("🔄 Reset"):
    st.session_state.board = chess.Board()
    st.session_state.running = False
    st.session_state.status = "Game reset."
    st.session_state.last_move = None
    st.rerun()

# -------------------------------------------------
# Layout
# -------------------------------------------------
left, right = st.columns([2, 1])
board = st.session_state.board

# -------------------------------------------------
# Board Rendering (Animated + Highlight)
# -------------------------------------------------
with left:
    fill = {}

    # Highlight last move
    if st.session_state.last_move:
        from_sq = chess.parse_square(st.session_state.last_move[:2])
        to_sq = chess.parse_square(st.session_state.last_move[2:4])
        fill[from_sq] = "#fff2a8"
        fill[to_sq] = "#ffd54f"

    # Highlight king in check
    if board.is_check():
        king_sq = board.king(board.turn)
        fill[king_sq] = "#ff4d4d"

    svg = chess.svg.board(board, size=520, fill=fill)
    st.markdown(
        f'<div class="chess-board">{svg}</div>',
        unsafe_allow_html=True
    )

# -------------------------------------------------
# Game Info Panel
# -------------------------------------------------
with right:
    st.subheader("📊 Game Information")

    st.markdown(
        f"""
        **White:** {white_choice}  
        **Black:** {black_choice}  
        **Turn:** {"White" if board.turn else "Black"}  
        """
    )

    if st.session_state.last_move:
        st.markdown(f"**Last Move:** `{st.session_state.last_move}`")
    else:
        st.markdown("**Last Move:** —")

    st.markdown("---")
    st.subheader("📝 Status")
    st.info(st.session_state.status)

# -------------------------------------------------
# AUTOPLAY ENGINE
# -------------------------------------------------
if st.session_state.running and not board.is_game_over():

    agent = (
        st.session_state.white_agent
        if board.turn
        else st.session_state.black_agent
    )

    move = agent.select_move(board)

    if move is None:
        st.session_state.status = "No legal moves available. Game stopped."
        st.session_state.running = False

    else:
        board.push(move)
        st.session_state.last_move = move.uci()

        if board.is_checkmate():
            winner = "Black" if board.turn else "White"
            st.session_state.status = f"♚ CHECKMATE — {winner} wins!"
            st.session_state.running = False

        elif board.is_check():
            checked = "White" if board.turn else "Black"
            st.session_state.status = f"⚠️ CHECK — {checked} king is under attack."

        elif board.is_stalemate():
            st.session_state.status = "🤝 DRAW — Stalemate."
            st.session_state.running = False

        else:
            st.session_state.status = "Game in progress..."

    time.sleep(move_delay)
    st.rerun()
