module Problem9 where

import Data.Function (on)
import Data.List (minimumBy, sortBy, nub)

{-------------------------------------------------------------------------------

Problem 9
=========

This problem focuses on greedy algorithms.  The intuition is of a cross-country
drive.  We are given a total distance to traverse, our range on a single tank of
gas, and a list of gas stations.  The goal is to minimize the number of stops we
make (while still making it to our destination, of course).

--------------------------------------------------------------------------------}

minWith f = minimumBy (compare `on` f)

{-------------------------------------------------------------------------------

I'm including two sample sets of input---a "short" trip and a "long" trip.

-------------------------------------------------------------------------------}

-- range on a single gas tank for the short and long trips, respectively
rangeShort, rangeLong :: Int
rangeShort = 100
rangeLong  = 300

-- total distance to traverse for the short and long trips, respectively
endShort, endLong :: Int
endShort = 300
endLong  = 1860

-- the distance from the starting point of gas stations, on the short and long
-- trips, respectively
gasStationsShort, gasStationsLong :: [Int]
gasStationsShort = [22,92,123,147,187,220,251,257,276,282]
gasStationsLong  = [20,43,46,109,180,226,242,305,314,319,325,357,406,425,506,517,
                    653,667,718,762,791,797,797,848,895,908,943,954,965,970,1033,
                    1069,1073,1144,1152,1152,1196,1198,1234,1270,1272,1290,1292,
                    1346,1350,1390,1477,1536,1546,1561,1618,1623,1653,1653,1715,
                    1746,1779,1799,1801,1813]

{-------------------------------------------------------------------------------

Part (a)
--------

For the first part of the problem, we'll implement the exhaustive approach to
solving the problem.  (That is: we'll develop a specification to guide our later
greedy algorithm.)  Your goal is to define the trips function, below, which
takes three parameters:

 * The first parameter is the total distance;

 * The second parameter is the range distance; and,

 * The third parameter is the list  of gas station distances.

The function should return all valid lists of stops. Intuitively, a valid list
of stops is a sorted list where if you planned to only stop at those stations on
your trip, you would not run out of gas. More formally, a list of stops is valid
if and only if it is sorted and:

 * The first entry is less than range;

 * For each subsequent pair of stops d1 and d2, (d2 - d1) is less than range; and,

 * The last entry is less than range from the end point.

You may assume that the input list of gas stations is in sorted order.
Depending on how you define trips, you may not get the same result from bestTrip
that I did, but you should get a result of the same length.

You should probably not try this implementation for the long problem.

-------------------------------------------------------------------------------}

bestTrip :: Int -> Int -> [Int] -> [Int]
bestTrip end range = minWith length . trips end range

-- total distance, range distance, 
trips :: Int -> Int -> [Int] -> [[Int]]
trips t r s = (map (tail . reverse)) $ nub $ paths ++ (concatMap more paths)
    where
        paths = until allend step [[0]]
        
        allend :: [[Int]] -> Bool
        allend = all (\l -> head l == maximum s)

        step :: [[Int]] -> [[Int]] -- similar to BFS... add all elements in range and produce
        step ls = concatMap (\l -> ins (inrange (head l)) l) ls -- new paths respectively

        more :: [Int] -> [[Int]] -- sub paths that are acceptable for a single path
        more [] = []
        more [x] = [[x]]
        more (x:y:ls) = if y >= t-r then (y:ls) : (more (y:ls)) else []

        inrange :: Int -> [Int] -- all elements within the range
        inrange x = [y | y <- s, y - x <= r, y - x > 0]

        ins :: [Int] -> [Int] -> [[Int]]
        ins [] ls = [ls]
        ins [x] ls = [x:ls]
        ins (x:xs) ls = (x:ls) : (ins xs ls)

-- >>> length $ trips 16 10 [5,10,11,16]
-- 10

-- >>> length (bestTrip endShort rangeShort gasStationsShort)
-- 3

-- >>> bestTrip endShort rangeShort gasStationsShort
-- [92,187,282]

-- >>> length (trips endShort rangeShort gasStationsShort)
-- 344

{-------------------------------------------------------------------------------

Part (b)
--------

Develop bestTrip' as a greedy algorithm for bestTrip.  Your implementation
should run in time linear in the length of the list of gas stations.

-------------------------------------------------------------------------------}

bestTrip' :: Int -> Int -> [Int] -> [Int]
bestTrip' end r l = (tail . reverse . fst) (insmax ([0], 0, l))
    where
        fst (x, _, _) = x

        insmax :: ([Int], Int, [Int]) -> ([Int], Int, [Int])
        insmax (ls, p, []) = if p == head ls then (ls, p, []) else (p:ls, p, [])
        insmax (ls, p, rest@(x:rests)) = let s = head ls in
            if end - r <= s then (ls, p, rest)
            else
                if x - s <= r
                then insmax (ls, x, rests)
                else
                    insmax(p:ls, p, rests)

{-------------------------------------------------------------------------------

Part (c)
--------

Give an informal argument that your greedy algorithm finds an optimal solution.
In making your argument, you mind find the following approach helpful.  Suppose
that there is an optimal solution that is not found by your approach.  Can you
show, by induction, that an equally good solution would arise from your
approach?

-------------------------------------------------------------------------------}

{-

For a solution provided by greedy algorithm G and the actual answer A,
suppose G is not optimal, then G has more stations than A. 

It's trivial when A and G are all exactly the same. If at some point 
choosing the nth and n+1th stations, A and G has same nth station and
G has closer n+1th station then G isn't greedy, hence contradiction.

If A and G starts at the same station, A has closer station, since A's
still in the distance to start at G's nth station and end at G's n+1th 
station, we can collapse the case by assuming A's n+1th station is at the
place of G's n+1th station.

-}
