module Problem15 where

import Data.Function
import Data.List

minWith :: Ord b => (a -> b) -> [a] -> a
minWith f = minimumBy (compare `on` f)

thinBy :: (a -> a -> Bool) -> [a] -> [a]
thinBy better = foldr keep []
    where keep x [] = [x]
          keep x (y : ys)
              | better x y = x : ys
              | better y x = y : ys
              | otherwise  = x : y : ys

{-------------------------------------------------------------------------------

Problem 15
==========

This problem revisits (in broad strokes) the books on shelves scenario from
problem 13---this time, 100% less theoretically impossible!

As before, the input is a shelf width and a list of books.  However, there are
two important differences from the previous problem:

 - First, we're now working in a library: the books must be placed on shelves in
   the same order in which they appear in the input list.  The "only" choice we
   have to make is when to move from one shelf to the next.

 - Second, books now have both widths and heights.  Our goal is no longer to
   minimize the number of shelves, but to minimize the total vertical height of
   our arrangement.  The vertical cost of a particular shelf in an arrangement
   is equal to the height of the tallest book in that shelf (in other words, no
   book is too tall to fit on a shelf).

Here's a collection of type synonyms intended to capture the intuition of the
problem.  The cost of an arrangement is the sum of the maximum height book in
each shelf---in other words, the sum of the vertical cost of each shelf.  We're
not concerned about the heights of the shelves themselves, space between
shelves, or so forth.

-------------------------------------------------------------------------------}

type Width       = Int
type Height      = Int
type Book        = (Width, Height)
type Shelf       = [Book]
type Arrangement = [Shelf]

shelfWidth :: Shelf -> Width
shelfWidth = sum . map fst

cost :: Arrangement -> Height
cost = sum . map (maximum . map snd)

--------------------------------------------------------------------------------
-- Sample data.  Best not to think too much about the realism of this data: in
-- actuality, I have very few books as wide as they are tall....
--------------------------------------------------------------------------------

books :: [Book]
books = [(1,7),(2,2),(4,7),(4,8),(5,5),(2,2),(2,7),(1,7),(4,4),(3,6),(5,8),
         (3,8),(4,2),(4,8),(4,4),(5,4),(2,6),(2,6),(4,5),(4,6)]

{-------------------------------------------------------------------------------

Part (a)
--------

Your first task is to write a function "arrangements" which, given a maximum
shelf width "w" and a list of books "bs", generates a list of all possible valid
arrangements of books.  A valid arrangement "ar" satisfies the following properties:

 - (i)   The books must appear in the same order they appear in the input list.
   That is to say: concat ar == bs.

 - (ii)  The sum of the widths of the books on each individual shelf must be less
   than the maximum shelf width.  That is: all (<= w) (map shelfWidth ar).

 - (iii) Each shelf must be non-empty.

For example, with a maximum shelf width of 5, the valid arrangements of

    [(1,7),(2,2),(4,7)]

are

    [[[(1,7),(2,2)],[(4,7)]],[[(1,7)],[(2,2)],[(4,7)]]]

Note that we do NOT include an option that switches the first two books, fitting
the books with width 1 and 5 on the same shelf, since this would violate part
(i) of the arrangement validity definition.  The patrons of our library would
likely find that such a step made the library more difficult to use.  Of course,
your solution may produce the arrangements in any order.

-------------------------------------------------------------------------------}

arrangements :: Width -> [Book] -> [Arrangement]
arrangements sw bs = map (reverse . (map reverse)) $ step sw bs [[]] -- final reversions
  where
    step :: Int -> [Book] -> [Arrangement] -> [Arrangement] -- append book to the very front
    step sw [] a = a
    step sw (b:bs) a = step sw bs (concatMap (ins sw b) a)

    ins :: Width -> Book -> [Shelf] -> [Arrangement]
    ins sw b@(bw, bh) [] = if bw <= sw then [ [ [b] ] ] else []
    ins sw b@(bw, bh) (s:ss) = if sum (map fst s) + bw <= sw 
                      then [(b:s) : ss] ++ [[b] : (s:ss)] -- either append to the frontmost shelve, or add a new shelve
                      else [[b]:(s:ss)]

bestArrangement :: Width -> [Book] -> Arrangement
bestArrangement maxw bs = minWith cost (arrangements maxw bs)

-- Some examples


-- >>> length $ arrangements 10 books
-- 48339
-- >>> let ar = bestArrangement 10 books in (ar, cost ar)
-- ([[(1,7),(2,2),(4,7)],[(4,8),(5,5)],[(2,2)],[(2,7),(1,7),(4,4),(3,6)],[(5,8),(3,8)],[(4,2)],[(4,8),(4,4)],[(5,4),(2,6)],[(2,6),(4,5),(4,6)]],54)

-- >>> length $ arrangements 12 books
-- 140192
-- >>> let ar = bestArrangement 12 books in (ar, cost ar)
-- ([[(1,7),(2,2),(4,7),(4,8)],[(5,5),(2,2),(2,7),(1,7)],[(4,4),(3,6),(5,8)],[(3,8),(4,2),(4,8)],[(4,4),(5,4)],[(2,6),(2,6),(4,5),(4,6)]],41)


{-------------------------------------------------------------------------------

Part (b)
--------

Your second task is to write a function "bestArrangement'" which, given a
maximum shelf width and a list of books, efficiently computes the arrangement
that takes up the least vertical space.  This problem does not admit a greedy
solution---for example, the minimum cost entry in "arrangements 10 books" is not
the one that uses the fewest shelves.  However, you can apply thinning to limit
the number of possibilities you consider.  In this case, the exact number of
possibilities is likely to be dependent on features of the input list, but
should remain a small constant (for my implementation, "arrangements 10 books"
and "arrangements 12 books" each considered fewer than 20 possibilities at each
iteration).

Note that, by "apply thinning", I do *not* mean that you must use the "thinBy"
function.  Instead, you should apply the *idea* of thinning: that is, of
limiting your enumeration of possibilities before a final "minWith" step.

-------------------------------------------------------------------------------}

-- >>> length (arrangements 10 books)
-- >>> length ((thinBy op) . (sortOn length) $ (arrangements 10 books))
-- 48339
-- 13

-- >>> length $ (minWith costs) . (thinBy op) . (sortOn length) $ (arrangements 10 books)
-- >>> costs $ bestArrangement' 10 books
-- 9
-- 54

costs :: Arrangement -> Int
costs [] = 0
costs (s:ss) = let height = map snd s in maximum height + costs ss

op :: Arrangement -> Arrangement -> Bool
op a1 a2 = 
  if length a1 == length a2 then
    costs a1 <= costs a2 
  else
    False

bestArrangement' :: Width -> [Book] -> Arrangement
bestArrangement' w bb = (minWith costs) . (thinBy op) . (sortOn length) $ (arrangements w bb)
