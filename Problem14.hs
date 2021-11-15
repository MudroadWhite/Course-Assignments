module Problem14 where

import Data.Function (on)
import Data.List (minimumBy, nub)
minWith f = minimumBy (compare `on` f)

{-------------------------------------------------------------------------------

Problem 14
==========

This problem returns to the road trip idea from Problem 9, albeit with new
constraints.  Now, we're no longer concerned about optimizing how often we stop,
but how much we spend on our trip.  We still can't run out of gas tho!

To account for cost, our list of stations is now a list of pairs: the first
component is the station's distance from the starting point and the second
component is the cost to fill up at that station.

Here are a couple of example lists; in each of these, distances range from
0-100, and costs range from 1-5.

-------------------------------------------------------------------------------}

type Stations = [(Int, Int)]

gs1, gs2, gs3 :: [(Int, Int)]
gs1 = [(8, 3), (22, 2), (24, 4), (38, 4), (48, 3), (51, 2), (54, 2), (64, 2), (84, 1), (88, 5)]
gs2 = [(9,4),(15,4),(19,4),(22,3),(29,2),(45,3),(46,1),(50,3),(50,1),(56,3),(58,3),(64,1),(65,2),(73,4),(87,5)]
gs3 = [(9,4),(14,1),(15,4),(19,4),(22,3),(27,5),(29,2),(45,3),(46,1),(50,3),(50,1),(56,3),(58,3),(64,1),(65,2),(67,4),(69,1),(73,4),(84,2),(87,5)]

{-------------------------------------------------------------------------------

Part (a)
-------

Your first task is to write a function "trips" that returns a list of all the
valid possible trips when given three arguments: ending point (as a total trip
distance), range, and list of stations. A trip includes not just the mile
markers of the stations you stop at, but also the cost to fill up at each
station.  A trip [(d₀, c₀), (d₁, cᵢ), ..., (dᵢ, cᵢ)] is valid (for a given
ending point "e" and range "r") iff:

 - The first stop is within the range of the starting point (that is: d₀ ≤
   r).

 - The distance between each subsequent pair of stops (d, c) and (d', c') is
   with in the range (that is, d' - d ≤ r)

 - The final stop is within the range of the end (that is, e - dᵢ ≤ r)

As in Problem 9, you may assume that the input list is sorted by distance.

This task is very similar to the one from Problem 9, even if the types are
slightly different.  I would certainly expect your implementation here to be
very structurally similar to your previous implementation---no need to worry
about self-plagiarism in this case.

-------------------------------------------------------------------------------}

type Trip = [(Int, Int)]

trips :: Int -> Int -> Stations -> [Trip] -- end range stations
trips t r ss = paths -- (map (tail . reverse)) $ nub $ paths ++ (concatMap more paths)
    where
        s = map fst ss

        paths = until allend step [[(0, 0)]]
        
        allend :: [Trip] -> Bool
        allend = all (\l -> ((fst . head) l) == maximum s)

        step :: [Trip] -> [Trip] -- similar to BFS... add all elements in range and produce
        step ls = concatMap (\l -> ins (inrange (fst $ head l)) l) ls -- new paths respectively

        more :: Trip -> [Trip] -- sub paths that are acceptable for a single path
        more [] = []
        more [x] = [[x]]
        more (x:y:ls) = if fst y >= t-r then (y:ls) : (more (y:ls)) else []

        inrange :: Int -> [(Int, Int)] -- all elements within the range
        inrange x = [y | y <- ss, fst y - x <= r, fst y - x > 0]

        ins :: [(Int, Int)] -> Trip -> [Trip]
        ins [] ls = [ls]
        ins [x] ls = [x:ls]
        ins (x:xs) ls = (x:ls) : (ins xs ls)

-- >>> length (trips 100 25 gs2)
-- 6567
{-------------------------------------------------------------------------------

The number of possible trips grows rapidly, making exhaustive search infeasible.
You should expect length ts3 and best ts3 to take a second to compute in the
following examples.

-------------------------------------------------------------------------------}

bestTrip end range = minWith (sum . map snd) . trips end range

-- >>> let ts1 = trips 100 25 gs1
-- >>> let ts2 = trips 100 25 gs2
-- >>> let ts3 = trips 100 25 gs3
-- >>> (length ts1, length ts2, length ts3)
-- ProgressCancelledException



-- (174,8919,589383)
-- >>> let best = minWith (sum . map snd)
-- >>> best ts1



-- >>> best ts2
-- Variable not in scope: best :: t0 -> t
-- Variable not in scope: ts2
-- >>> best ts3
-- Variable not in scope: best :: t0 -> t
-- Variable not in scope: ts3




-- [(22,3),(46,1),(69,1),(84,2)]

{-------------------------------------------------------------------------------

More significant, however, is that our existing greedy strategies may not
actually produce the best route.  Give an example set of stations, assuming 100
for the end and 25 for the range, so that if you naively adapted your algorithm
from Problem 9 to work with this problem, it would not produce the most cost
effective solution.  In other words, if you modified it to take in an element
"gs" of type [(Int, Int)] for the gas station argument, but the adapted Problem
9 algorithm ignores the second component of each member of "gs".  Explain
(informally) why it doesn't work.

-------------------------------------------------------------------------------}

gs4 :: Stations
gs4 = undefined

{-------------------------------------------------------------------------------

Part (b)
--------

Your next task, then, is to write a function "bestTrip'" that implements an
efficient algorithm that computes the most cost effective (valid) trip for a
given ending point, range, and list of stations.  (The definition of valid trips
hasn't changed from above).

You won't be able to do this with a greedy solution, but you can do it following
the "thinning" approach from the textbooks (and lectures).  That is, while you
can't pick a single best candidate along the way, you can keep a list of
possible candidates significantly shorter than enumerating all possible trips.

In addition to writing the "bestTrip'" function, you should also argue
(informally) for the efficiency of your approach by describing how many possible
candidates your approach needs to track---in terms of the ending point, range,
and station list.

You may assume, as before, that stations are sorted by distance.  You do NOT
need to optimize for number of stops in addition to cost---if there are two
trips with the same cost, you may return EITHER trip, even if one has more stops
than the other.

-------------------------------------------------------------------------------}

bestTrip' :: Int -> Int -> Stations -> Trip
bestTrip' = undefined
