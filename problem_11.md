# Problem 11

### Part a

| Letter    | a      | b      | c     | d    | e    | f    | g    |
| --------- | ------ | ------ | ----- | ---- | ---- | ---- | ---- |
| Frequency | 1      | 1      | 2     | 3    | 5    | 8    | 13   |
| Code      | 000000 | 000001 | 00001 | 0001 | 001  | 01   | 1    |

### Part b

Claim: The Huffman tree produced with Fibonacci number's frequency is always "heavily unbalanced": All branch nodes must have a leaf as their children. Corresponded to the code, the nth element(starting from 1) in m letters will have code length of m-n+1.

Denote the Fibonacci sequence by $f_n$. From the definition of Fibonacci sequence we have 
$$
f_n = f_{n-1} + f_{n-2}, n \ge 3
$$
We're going to prove
$$
\sum^{n}_{i=1}f_i \le f_{n+2}, n \ge 2
$$
Base case: $f_1 + f_2 = 2 \le f_4 = 3$.

Step case: Suppose $\sum^{n}_{i=1}f_i \le f_{n+2}$. Add $f_{n+1}$ to both sides and we get $\sum^{n+1}_{i=1} \le f_{n+3}$.

When every time the tree construction goes, the total weight of the tree being constructed must be $\sum_{i=1}^{n}f_i$. Since $f_{n+1} \le f_{n+2}$ by definition of Fibonacci sequence, it must be that the smallest two number at the current stage is $\sum_{i=1}^{n}f_i$ and $f_{n+1}$. Therefore, at every stage of the construction, one leaf node must be added into the tree. Corresponded to the code, since they're being added into the tree at different stages, and the largest number will be added in the latest stage, therefore they will have code length of m-n+1.