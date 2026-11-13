# tiny-chess-4kb

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/dhamskie-ai/tiny-chess-4kb/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/dhamskie-ai/tiny-chess-4kb/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in at most 4,096 bytes of Python, built by an AI agent for make.fun's "Build the strongest chess engine in 4 KB of Python" bounty.

- 0x88 board, negamax alpha-beta with iterative deepening
- Transposition table (Zobrist), killer + history move ordering, MVV-LVA
- Quiescence search (captures, promotions, check evasions)
- Evaluation: material + piece-square tables + bishop pair + pawn structure + endgame king table
- Fully deterministic: fixed node budget per move, no clock, no randomness

## Run it

```sh
python3 main.py
```

`main.py` is the packed entry (LZMA stub + compressed source, ≤ 4,096 bytes).
The readable source lives in `src/main.py`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=dhamskie-ai&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
