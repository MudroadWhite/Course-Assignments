module Problem10 where

import Data.Function (on)
import Data.List (maximumBy, nub)
import qualified Data.Map as M

{-------------------------------------------------------------------------------

Problem 10
==========

This problem focuses on greedy algorithms.  Our context here is balanced strings
of parentheses.  A string of parentheses is balanced if, informally, every open
parenthesis has a matching closed parenthesis.  For example, the following
strings are balanced:

 * ()
 * ((())()())
 *                      [That's the empty string. It's balanced.]

The following strings are not:

 * ()(
 * (()
 * ())(

Formally, a string is balanced iff:

 * it is the empty string; or,
 * it is of the form "(" ++ s ++ ")", where s is balanced; or,
 * it is of the form s ++ t, where s and t are balanced.

Part (a)
--------

Write a function "balanced" which returns true if a string is balanced, and
false otherwise.  Your function should run in time linear in the length of the
input string.  You should assume that the input string will NOT contain any
characters other than '(' and ')'.

-------------------------------------------------------------------------------}

balanced :: String -> Bool
balanced s = if (traverse 0 s) == 0 then True else False
    where
        traverse :: Int -> String -> Int
        traverse x [] = x
        traverse x s = if x < 0 then -1
            else 
                case head s of
                '(' -> traverse (x+1) (tail s)
                ')' -> traverse (x-1) (tail s)

-- >>> map balanced ["((())()())", "", "())(", "(()", "()("]
-- [True,True,False,False,False]

{-------------------------------------------------------------------------------

Part (b)
--------

Write a function "subsequences" which returns all the subsequences of a given
input string.  A string is a subsequence of another string if it can be obtained
by removing any number of characters from the original string.  For example,
among the subsequences of "abcd" are "ab", "ac", "cd".  Note that a subsequence
does not have to be contiguous in the original string!  (The contiguous notion
is called a substring or segment; we'll see more about them later.)  However,
you cannot change the ordering of characters in the original string; for
example, "cb" is not a subsequence of "abcd".  Your "subsequences" function will
run in time (and produce results) exponential in the length of the input string.


-------------------------------------------------------------------------------}

subsequences :: String -> [String]
subsequences [] = [[]]
subsequences (x:xs) = [x:s | s <- subsequences xs] ++ subsequences xs

-- >>> subsequences "abcd"
-- ["abcd","abc","abd","ab","acd","ac","ad","a","bcd","bc","bd","b","cd","c","d",""]

-- Of course, you may not generate subsequences in the same order that I did, so
-- you might find the following function helpful for testing:

same :: Ord a => [a] -> [a] -> Bool
same xs ys = freqs xs == freqs ys
    where freqs = M.assocs . foldr ins M.empty
          ins c = M.insertWith (+) c 1

-- >>> same (subsequences "abcd") ["","d","c","cd","b","bd","bc","bcd","a","ad","ac","acd","ab","abd","abc","abcd"]
-- True

{-------------------------------------------------------------------------------

Also, write a function "balancedSubsequences" which returns all of the
subsequences of the input string that are balanced.  This is likely to include
many duplicates.

-------------------------------------------------------------------------------}

balancedSubsequences :: String -> [String]
balancedSubsequences s = [x | x <- subsequences s, balanced x] -- why not nub it?

-- >>> same (balancedSubsequences "()())(()") ["","()","()","()","()","()()","()()","()","()()","()()","()","()","()()","()()","()","()()","()()","(())","(())","(())","(())()","(())()","()","()()","()()","()()","()()","()()()","()()()","()()","()()()","()()()"]
-- True

{-------------------------------------------------------------------------------

Part (c)
--------

We're now going to combine the previous parts, looking for the longest balanced
subsequence of an original string.

-------------------------------------------------------------------------------}

maxWith f = maximumBy (compare `on` f)

lbs :: String -> String
lbs = maxWith length . balancedSubsequences

-- >>> lbs "(()))(()"
-- "(())()"

{-------------------------------------------------------------------------------

As you can imagine, however, computing the longest balanced subsequence
exhaustively becomes infeasible as soon as you have a string of even moderate
length.  While it is possible to devise a greedy algorithm for the longest
balanced subsequence, it's actually easier to find a greedy algorithm to compute
the *length* of the longest balanced subsequence.  Here's the exhaustive
implementation:

-------------------------------------------------------------------------------}

llbs :: String -> Int
llbs = maximum . map length . balancedSubsequences

-- >>> llbs "()())(()"
-- 6

{-------------------------------------------------------------------------------

Your task is to write a function "llbs'" which greedily computes the length of
the longest balanced subsequence.  Your function should execute in time linear
in the length of the input list.

I didn't find it very helpful to think of fusing (map length) into (balanced
subsequences) directly.  Rather, what I Found helpful was to think about how the
maximum length is changed by each character you encounter.

-------------------------------------------------------------------------------}

llbs' :: String -> Int
llbs' s = traverse (0, 0) s where
    traverse :: (Int, Int) -> String -> Int
    traverse (x, y) [] = x - y
    traverse (x, y) s = 
        case head s of
        '(' -> traverse (x+1, y+1) (tail s)
        ')' -> 
            if y == 0 then traverse (x, y) (tail s)
            else traverse (x+1, y-1) (tail s)

-- >>> llbs' "()()"
-- 4
-- >>> llbs' "(()"
-- 2
-- >>> llbs' "()())(()"
-- 6
-- >>> llbs' "(()((()))()())))(())("
-- 18
