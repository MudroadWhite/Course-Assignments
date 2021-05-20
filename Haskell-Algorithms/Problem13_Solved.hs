module Problem13 where

import Data.Function
import Data.List

{-------------------------------------------------------------------------------

This problem focuses on the increasingly obsolete, I'm told, problem of arranging
books on shelves.  The input is a shelf width (all our shelves are the same
size) and list of book widths, as (positive) integers.  Of course, this list
will contain repeats, and you should not assume anything about its order.  The
goal is to return an assignment of books (or at least their widths) to shelves,
minimizing the number of shelves required.

-------------------------------------------------------------------------------}

{-------------------------------------------------------------------------------

Part (a)
--------


We'll begin by generating an exhaustive list of possible arrangements.  You
should write a function "arrangements" such that (arrangements shelfWidth
bookWidths) returns every possible legal arrangement.

An arrangement is a list of lists of books---each shelf gets a list of books,
and an arrangement is a list of shelves.  That means the output of your
arrangements function should be a list of arrangements---that is, once you look
past the type synonyms, a [[[Int]]].

Beyond its type classification, a legal arrangement must satisfy the following
invariants:

 - Every book must occur in some shelf (i.e. you can't leave any books out)

 - The sum of the book widths on each shelf does not exceed shelfWidth

 - Each shelf contains at least one book

You may assume that every bookWidth is less than or equal to the shelfWidth, and
also that you have an unlimited supply of shelves (you can always go to the
store and buy another shelf to hold more books).  Finally, note that the order
in which you put books on the shelf doesn't matter---[1,2] is the same
arrangement of books on a shelf as [2,1].  Similarly, the order of shelves
doesn't matter---[[1,2],[3]] is the same arrangement as [[3],[2,1]].

-------------------------------------------------------------------------------}

type Book = Int
type Shelf = [Book]
type Arrangement = [Shelf]

-- >>> ins 36 1 [[2, 3], [4]]
-- [[[1,2,3],[4]],[[2,3],[1,4]]]

ins :: Int -> Book -> Arrangement -> [Arrangement] -- insert one element into one arrangement...
ins sw bw [] = if bw <= sw then [ [ [bw] ] ] else [] -- [Shelf] -> [ [Shelf] ]
ins sw bw (a:as) = if sum a + bw <= sw 
                   then [(bw : a) : as] ++ map (a:) (ins sw bw as)
                   else map (a:) (ins sw bw as)

arrangements :: Int -> [Book] -> [Arrangement]
arrangements sw bs = step sw bs [[]] --
    where
        step :: Int -> [Book] -> [Arrangement] -> [Arrangement]
        step sw [] a = a
        step sw (b:bs) a = step sw bs (concatMap (ins sw b) a)

{-------------------------------------------------------------------------------

Some sample outputs of the arrangements function.  Again, order doesn't
matter---the first result is the same as [[[1],[2]],[2,1]], for example.

-------------------------------------------------------------------------------}

-- >>> arrangements 3 [1,2]
-- [[[2,1]],[[1],[2]]]

-- [[[1,2]],[[2],[1]]]

-- >>> arrangements 6 [1,2,3]
-- [[[3,2,1]],[[2,1],[3]],[[3,1],[2]],[[1],[3,2]],[[1],[2],[3]]]

-- [[[1,2,3]],[[2,3],[1]],[[1,3],[2]],[[3],[1,2]],[[3],[2],[1]]]

-- >>> arrangements 4 [1,2,3]
-- [[[2,1],[3]],[[3,1],[2]],[[1],[2],[3]]]

-- [[[1,3],[2]],[[3],[1,2]],[[3],[2],[1]]]

{--------------------------------------------------------------------------------

Of course, to get the minimum number of shelves, we can introduce our usual
minWith function and then apply it to arrangements.  However, the number of
arrangements grows rapidly for even small numbers of books, so this approach
won't scale.

-------------------------------------------------------------------------------}

minWith f = minimumBy (compare `on` f)

-- >>> minWith length $ arrangements 6 [1,1,1,2,2,3,4]
-- [[2,1,1,1],[3,2],[4]]

-- [[2,4],[1,2,3],[1,1]]

{-------------------------------------------------------------------------------

Part (b)
--------

Your second task is to define "arrangements'", an efficient (i.e.,
sub-polynomial time) solution to arranging books on shelves.

You might expect that your algorithm would also be constrained by some kind of
optimality condition: perhaps that you should produce the arrangement that uses
the fewest shelves.  Unfortunately, your instructor messed up: this problem
provably has no sub-polynomial time optimal solution.

So, in fairness, the only criterion that I can apply is that your algorithm
returns *some* solution in sub-polynomial time.  There are certainly
approximately-optimal approaches that run in that time, if you'd like to have a
quick look around for one.

(To be clear: that also means your algorithm need not produce output equivalent
with the test cases below.  Up to you!)

-------------------------------------------------------------------------------}

{-  If I have understood correctly, to produce one valid solution,
    one just need to greedily stuff in shelves with as much books as one can.
    The solution should be linear time. -}

arrangements' :: Int -> [Book] -> Arrangement
arrangements' sw bs = foldr stuff [] bs
    where
        stuff :: Book -> Arrangement -> Arrangement
        stuff b [] = if b <= sw then [[b]] -- A book in one shelve
                     else []
        stuff b (s:ss) = if b + sum s <= sw then (b:s) : ss else s : (stuff b ss)



-- >>> arrangements' 5 [2,1,4,4,3]
-- [[1,3],[4],[4],[2]]

-- [[1,4],[4],[2,3]]

-- >>> arrangements' 5 [3,4,4,2,1]
-- [[2,1],[4],[4],[3]]


-- [[1,4],[4],[2,3]]

-- >>> arrangements' 10 [4, 1, 1, 1, 6, 6, 5, 6, 5, 3, 3, 2, 1, 1, 3]
-- [[3,2,1,1,3],[1,1,5,3],[1,6],[4,5],[6],[6]]


-- [[4,6],[1,3,6],[1,3,6],[5,5],[1,1,1,2,3]]
