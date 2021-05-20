module Problem12 where

import Data.List

{-------------------------------------------------------------------------------

This problem focuses on satisfiability for a very simple language of logical
formulae.  Recall that a formula is satisfiable if there is some assignment of
truth values to its variables such that the formula as a whole is true.  We're
going to consider formulae of the following forms, given variables xⱼ:

     x₁ ∧ x₂ ̣∧ ... ∧ xᵢ ⇒ xᵢ₊₁
     ¬(x₁ ∧ x₂ ∧ ... ∧ xᵢ)

We will assume that all the variables in an individual formulae are distinct.
We allow the set of hypotheses of an implication to be empty. For example, a
formula of the first kind with i = 0 is "⇒ x₁" and is true if and only if the
variable x₁ is true. Our goal is to discover whether conjunctions of sets of
such formulae are satisfiable.  We also allow the set of conjuncts in a formula
of the second type to be empty.  Such a formula is false for all assignments.
For example, the following set of formulae is satisfiable:

    ⇒ x₁, x₁ ⇒ x₂, x₃ ⇒ x₂, ¬(x₁ ∧ x₂ ∧ x₃)

with the following satisfying assignment

    x₁ ↦ t, x₂ ↦ t, x₃ ↦ f

The following set of formulae is not satisfiable:

    ⇒ x₁, x₁ ⇒ x₂, x₂ ⇒ x₃, ¬(x₁ ∧ x₂ ∧ x₃)

because any satisfying assignment of the first three formulae must set x₁, x₂
and x₃ to true.

We'll represent these formulae as follows.

-------------------------------------------------------------------------------}

type Var  = Int
data Form = [Var] :=> Var | Nand [Var]
  deriving Show

{-------------------------------------------------------------------------------

For example, we would represent the first set of formulae above:

    ⇒ x₁, x₁ ⇒ x₂, x₃ ⇒ x₂, ¬(x₁ ∧ x₂ ∧ x₃)

by the Haskell list

    [ [] :=> 1, [1] :=> 2, [3] :=> 2, Nand [1,2,3] ]

In general, we'll want to know which variables appear in a given set of
formulae.  The following functions will do the trick.

-------------------------------------------------------------------------------}

vars :: [Form] -> [Var]
vars []                = []
vars ((vs :=> v) : cs) = ws ++ filter (`notElem` ws) (vars cs)
    where ws = v : vs
vars (Nand vs : cs)    = vs ++ filter (`notElem` vs) (vars cs)

-- >>> vars [ [] :=> 1, [1] :=> 2, [3] :=> 2, Nand [1,2,3] ]
-- [1,2,3]

{-------------------------------------------------------------------------------

Part (a)
--------

The first part of the problem is to develop an exhaustive approach to
determining the satisfiability of a set of formulae: we'll enumerate every
possible assignment for the variables in the formulae, and then see if any of
them are satisfying.

We need a representation of assignments.  We could consider a mapping of
variables to Booleans, but there's an easier approach: we'll just keep a list of
those variables which are true.  Any variable which doesn't appear in the
assignment is (implicitly) false.

-------------------------------------------------------------------------------}

type Assign = [Var]

{------------------------------------------------------------------------------

Your first task, then, is to define a function from a set of variables to every
assignment over those variables.  (For those of you keep track at home: yes,
this is yet another justification for a function you've written more than once
before.)

-------------------------------------------------------------------------------}

assignments :: [Var] -> [Assign] -- just sublists
assignments [] = [[]]
assignments (x:xs) = [x:s | s <- assignments xs] ++ assignments xs

-- >>> assignments [0, 1, 2]
-- [[0,1,2],[0,1],[0,2],[0],[1,2],[1],[2],[]]

{-------------------------------------------------------------------------------

Next, define a function "satisfying" that returns all satisfying assignments for
a given set of formulae.  You may find it helpful to separate out the logic for
testing whether a particular assignment satisfies a set of formulae.

-------------------------------------------------------------------------------}


imply :: [Var] -> Var -> [Var] -> Bool
imply [] v = \l -> if elem v l then True else False
imply vs v = \l -> if all (flip elem l) vs then
                    if elem v l then True else False 
                    else True

nand vs = \l -> 
    let vl = map (flip elem l) vs in
        not $ foldr (&&) (head vl) (tail vl)

satisfying :: [Form] -> [Assign]
satisfying forms = try forms 
    where
        try :: [Form] -> [Assign]
        try [] = assignments $ vars forms
        try (f:fs) = case f of
            (vs :=> v) -> [x | x <- try fs, imply vs v x] 
            Nand vs -> [x | x <- try fs, nand vs x]

-- >>> satisfying [[] :=> 1, [1] :=> 2, [0] :=> 1]
-- [[1,2,0],[1,2]]

-- [[1,2],[1,2,0]]

-- >>> satisfying [[] :=> 1, [1] :=> 2, [0] :=> 1, Nand  [0, 1, 2]]
-- [[1,2]]

-- >>> satisfying [[] :=> 1, [1] :=> 2, [0] :=> 1, Nand  [1, 2]]
-- []

{-------------------------------------------------------------------------------

Part (b)
--------

Unfortunately, a set of formulae with n variables has 2ⁿ possible assignments,
so the above approach won't scale very well.  Your final task is to develop a
polynomial time algorithm for finding *one* satisfying assignment for a set of
formulae, *if it exists*.  You should argue informally why your solution works,
and why it takes polynomial time.

You may find it helpful to think of the problem as follows: suppose that you
have an assignment that does not satisfy a set of formulae.  How could you
repair the assignment so that it comes closer to satisfying that set of
formulae?

Note: I do not necessarily expect you to come up with the optimal algorithm,
just one that runs in polynomial time.

-------------------------------------------------------------------------------}

imps :: [Form] -> [Form]
imps [] = []
imps (f:fs) = case f of
    vs :=> v -> f : imps fs
    _ -> imps fs

nands :: [Form] -> [Form]
nands [] = []
nands (f:fs) = case f of
    Nand vs -> f : nands fs
    _ -> nands fs

antecedent :: Form -> [Var]
antecedent (vs :=> _) = vs

precedent :: Form -> Var
precedent (_ :=> v) = v

satisfying' :: [Form] -> Maybe Assign
satisfying' f = let impassign = checkimps in checknand impassign
    where
        ifs = imps f
        nfs = nands f

        checkimps = until (null . (unsatimp ifs)) stepimp [] -- first try to satisfy all imp assignments

        stepimp :: Assign -> Assign -- original assignment and all new "satisfied" implications's precedent
        stepimp a = union a (map precedent $ unsatimp ifs a) 
        
        unsatimp :: [Form] -> Assign -> [Form]
        unsatimp fs a = [f | f <- fs,
                             (not $ elem (precedent f) a), -- the v is not assigned
                             (all (flip elem a) (antecedent f))] -- the vs are all assigned

        checknand a = if null $ unsatnand nfs a then Just a else Nothing -- then check if there are unsatified nands

        unsatnand :: [Form] -> Assign -> [Form]
        unsatnand fs a = [f | f <- fs, all (flip elem a) (vars [f])] -- the vs are all assigned

-- >>> satisfying' [[] :=> 1, [1] :=> 2, [0] :=> 1]
-- Just [1,2]

-- >>> satisfying' [[] :=> 1, [1] :=> 2, [0] :=> 1, Nand  [0, 1, 2]]
-- Just [2,1]

-- >>> satisfying' [[] :=> 2, [] :=> 4, [1,2] :=> 3, [2] :=> 1, [4] :=> 6, [4,2] :=> 7, Nand [1,2,5], Nand [6,7,8]]
-- Just [3,7,6,1,4,2]
