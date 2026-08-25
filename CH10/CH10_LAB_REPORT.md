# Lab Report — Chapter 10: Greedy Algorithms

*Complete both sections and commit this file with your code.*

## Test Results

*Paste your scheduling result, both knapsack answers side by side, your set cover, and your subset counts.*
Part 1: Scheduled classes
[('Art', 9.0, 10.0), ('Math', 10.0, 11.0), ('Music', 11.0, 12.0)]

Part 2: Greedy knapsack choice
[('stereo', 3000, 4)]
Part 2: Greedy knapsack value
3000

Part 2: Brute-force knapsack choice
[('laptop', 2000, 3), ('guitar', 1500, 1)]
Part 2: Brute-force knapsack value
3500

Part 2: Gap between brute force and greedy
500

Part 3: Stations chosen, in order
['ktwo', 'kthree', 'kone', 'kfive']

Part 3: Exact solver combinations to check for 5 stations
32

Part 3: Exact solver combinations to check for 20 stations
1048576

Part 3: Exact solver combinations to check for 100 stations
1267650600228229401496703205376

## Reflection Questions

1. **Explain the greedy strategy to someone who has never programmed.**
   - *Packing a suitcase and choosing something that fits and is the best choice.So it keeps choosing the best option avaliable instead of looking at every option*

2. **Greedy was perfect for scheduling and wrong for the knapsack. What changed about the problem?**
- *Picking stero wasnt the best choice so algorith doesnt work for it*
3. **You already wrote a greedy algorithm in an earlier lab — building the Huffman tree in Chapter 7 repeatedly merges the two lowest-frequency nodes. Is that one exactly optimal, or an approximation?**
- *Huffman is optimal  *
