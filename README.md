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

## Local grading (trial = 8 games vs the house engines)

| Version | Trial | Elo | W-D-L |
| --- | --- | --- | --- |
| v2 | t0 | 1173 | 2-1-5 |
| v3 (this entry) | t0 | 1326 | 2-3-3 |
| v3 (this entry) | t1 | 1598 | 4-3-1 |
| v4 | t0 | 1173 | 1-3-4 |
| v5 | t0 | 1396 | 3-2-3 |

v3 was picked as the entry: its two-trial mean (~1462) beats every other version, and it clears the 1154 practice floor for the finals.

## Run it

```sh
python3 main.py
```

`main.py` is the packed entry (LZMA stub + compressed source, ≤ 4,096 bytes).
The readable source lives in `src/main.py`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=dhamskie-ai&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
