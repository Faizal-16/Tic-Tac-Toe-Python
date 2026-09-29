## Objective
Design an intelligent agent that plays Tic-Tac-Toe optimally using
**adversarial search** (Minimax with Alpha-Beta pruning).

## How It Works
1. **Game tree:** every possible sequence of moves is a tree. The AI searches it.
2. **Minimax:** the AI (O) picks moves that *maximize* its score; it assumes the
   human (X) picks moves that *minimize* it.
   - AI win = `+10 - depth`, Human win = `depth - 10`, Draw = `0`
   - The depth term makes the AI prefer quick wins and delay losses.
3. **Alpha-Beta pruning:** skips branches that cannot affect the final decision,
   giving the same result with far fewer positions checked (shown in the GUI).

## How to Run
```bash
python tictactoe_ai.py          # play against the AI (Tkinter GUI)
```
