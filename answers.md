# CMPS 2200 Assignment 5
## Answers

**Name:**_Srikanya Garuda___

Place all written answers from `assignment-05.md` here for easier grading.


**1: Fixed-Length vs. Variable-Length Codes**

- **1d. (5 pts)** What trend do you see?
File	                        Fixed-Length Cost (bits)	Huffman Cost (bits)	 Space Saved (%)
File 1 (e.g., alice29.txt)	  1,039,367	                676,374	             ~34.9%
File 2 (e.g., asyoulik.txt)	  876,253	                  606,448	             ~30.8%
File 3 (grammar.lsp / small)	1,340	                    826	                 ~38.4%
File 4 (fields.c)	            78,050	                  56,206	             ~28.0%
File 5 (codes.c)	            26,047	                  17,356	             ~33.4%

Across the tested files, Huffman coding reduces the total bit cost by about ~32%. This comes from the non-uniform distribution in language, where frequent characters are assigned shorter prefixes, outweighing the cost of longer codes for rare characters

- **1e. (4 pts)** What is the expected
  cost of a Huffman encoding for the document? Is it consistent across
  documents?

The expected cost of a Huffman encoding for a document with uniformly distributed character frequencies is $\lceil \log_2(n) \rceil$ bits per character (where $n$ is the alphabet size), which is identical to the cost of a standard fixed-length encoding.This outcome is consistent across documents as long as the alphabet size ($n$) and the uniform frequency distribution are the same, because every document will produce the exact same perfectly balanced binary tree.


**2: Making Change**

- **2a. (5 pts)** Given a $N$ dollars, state a greedy algorithm for producing
as few coins as possible that sum to $N$.

Initialize an empty list or counter for the coins.
Find the largest coin denomination $2^i$ such that $2^i \le N$. While $N > 0$:Determine the maximum number of coins of denomination $2^i$ that fit into $N$ using integer division: $count = \lfloor N / 2^i \rfloor$.
Add $count$ coins of denomination $2^i$ to our collection.
Update $N$ to be the remainder: $N = N \pmod{2^i}$. Move to the next smaller power of 2 denomination ($2^{i-1}$) and keep going. Return the total collection of coins.



- **2b. (5 pts)** Prove that this algorithm is optimal by proving the greedy
  choice and optimal substructure properties.

Greedy Choice Property:
Statement: A global optimum can be reached by making the locally optimal choice—specifically, by picking the largest possible coin denomination $2^i \le N$.
Proof: Suppose there exists an optimal solution that does not use the largest available coin $2^i \le N$. Because all denominations in Geometrica are powers of 2, any value equal to $2^i$ must be formed using smaller denominations (e.g., two $2^{i-1}$ coins, four $2^{i-2}$ coins, etc.). If an optimal solution uses a collection of smaller coins whose values sum to $2^i$ (or more), we can replace that entire collection with a single coin of denomination $2^i$. This substitution strictly reduces (or keeps equal) the total number of coins used without exceeding the target amount $N$. This makes the greedy choice is always safe and optimal.

Optimal Substructure Property:
Statement: An optimal solution to the problem contains optimal solutions to sub-problems.
Proof: Once we make the greedy choice of taking the largest valid coin $2^i$, the remaining problem reduces to making change for the remainder $N' = N - 2^i$ using the available coin set. If there existed a more optimal set of coins to make change for $N'$. We could combine that superior sub-solution with our initial coin $2^i$ to form a total solution for $N$ that uses fewer coins than the supposed "optimal" solution, creating a contradiction. Thus, optimal sub-solutions compose an optimal global solution.


- **2c. (4 pts)** What is the work and span of your algorithm?
Work : $O(\log N)$
Span: $O(\log N)$


#question 3 space not given

- **3a.**
Let $E(i, j)$ be the edit distance between the prefix $S[0 \dots i-1]$ and $T[0 \dots j-1]$. 
The optimal substructure property states that:
If the last characters match ($S[i-1] == T[j-1]$): No edit is needed for this character, so $E(i, j) = E(i-1, j-1)$.
If they don't match, we take the minimum of three choices corresponding to our allowed operations: 
Deletion from $S$: $1 + E(i-1, j)$
Insertion into $S$ (matching $T$): $1 + E(i, j-1)$
Substitution of $S[i-1]$ with $T[j-1]$: $1 + E(i-1, j-1)$