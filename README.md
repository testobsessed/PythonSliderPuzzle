# What Is This?

TL;DR: this is a personal project intended to help me learn
Python. 
I did not create this with anyone else in mind. 
The code is a bit of a mess but
I'm setting it down for 
now without cleaning it up because I need to move
on to other things.

## Backstory
It all started about 10 years ago when I spotted a slider
puzzle challenge on
[The Daily WTF](http://thedailywtf.com/articles/Sliding-Around).
"Oh, that sounds easy," I thought. Naively. 

Three days later I
staggered away from the keyboard with
[a solution in Ruby](https://github.com/testobsessed/Ruby-Slider-Puzzle-Sample)
that worked for a bunch of configurations.
I gave up working on the puzzle after a while, without figuring
out how good (or not) my algorithm was.

Fast forward a decade. 
I'm currently on a haitus, taking time to sharpen my saw, get
my hands on tech again after a few years in a purely management
role, and explore things
I am curious about. Rabbit holes I'm falling down include
VR, Unity, and ML. That last thing is what led me to want to 
brush up my Python skills. 

I needed a project, something that would give me a reason to
really learn Python, and preferably lend itself to ML. 
I remembered
the slider puzzle challenge. It's just complex enough to exercise
multiple facets of the language while being familiar territory.
And maybe I could figure out how to write a reinforcement learning
algorithm?
"Perfect!"
I thought. 

Naively.

Better yet, when I searched for the original slider puzzle
challenge I found an 
[updated one on Reddit.](https://www.reddit.com/r/dailyprogrammer/comments/62ktmx/20170331_challenge_308_hard_slider_game_puzzle/)

So this repo contains the somewhat cluttered detritus 
of my attempt at the slider puzzle problem in
Python. 

I mostly-but-not-entirely TDD'd it. However 
as I reached the frustration point with each approach I took,
I stopped running the entire suites and moved to running
individual tests. Thus the build isn't green.

Also, the code is inefficient in its implementation and 
inconsistent in its expression.

But I'm setting it down for 
now without cleaning it up because I need to move on to
other things if only for my own sanity.

## About Slider Puzzles

Slider puzzles are rectangular or square boards with a number
of tiles and an empty space. You solve the puzzle by rearranging
the tiles to get them in order.

If you search for slider puzzles you'll find a wealth of 
resources (including some fascinating history). 
I am not going to cover things here that are
better covered elsewhere. This is more like a cheatsheet
of things you need to know if you're going to tackle this space.

###Not all configurations are solvable. 
This is one of the
big mistakes I made when I tackled this the first time in
Ruby.
Here is an [approachable explanation](https://datawookie.netlify.com/blog/2019/04/sliding-puzzle-solvable/)
of how to 
tell if a puzzle is solvable.
And here is a 
[more academic but thorough](https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html)
paper
with a deeper explanation.

Imagine a 2x2 slider puzzle. Here's one solved:

|     |     |
|:---:|:---:|
| 1   | 2   |
| 3   |     |
 
If you slide the 3 to the right it becomes:

|     |     |
|:---:|:---:|
| 1   | 2   |
|     | 3   |


There are 4 x 3 x 2 x 1 = 24 possible permutations of the board.
However only 10 of those are solvable. As an example of
an unsolvable configuration, consider:

|     |     |
|:---:|:---:|
| 1   | 3   |
| 2   |     |

No matter how much you slide the tiles around, you can't get the 
2 and 3 to switch their order. (*Hmmm...move the 2, then the 1,
then the 3...no...* Seriously, the thing that's kinda special about 
a 2x2 slider puzzle is that at any given moment in time if you just
did a move, there is only 1 move available to you that doesn't undo
what you just did. So basically all you can do is push the puzzle
pieces around in a circle.)

Although once you know what to look for, it's easy to see when a 
2x2 configuration isn't solvable, and much harder to see in a 3x3.
Thus
the resources linked above are super helpful.

###You can think of it like a maze.

Instead of thinking about shuffling tiles around, think 
about moving the empty space. The catch is that if you think
of it like a maze, each time you move the empty space, the board
changes state. So it's like moving into a new "room" in the maze.

If we say that only solvable configurations of tiles on the board
are "valid," then
ou can---with enough moves---eventually get from any valid configuration
to any other valid configuration.

(Consider it this way: if a valid board is one you can solve, then
you can go from that board state to the solution through a series
of moves. If you reverse the series of moves you can go from the
solved board to the unsolved configuration. If you go from one
unsolved state to the solved state, then you can go to any other
unsolved state.)

## A Solution in Code

My ultimate goal this time around was to write something that 
could "learn" how to solve puzzles of arbitrary size. 
To be clear: I came nowhere near achieving that goal.

Here's what I did do.

I attempted 3 different approaches in this project...

Approach #1 ("solve_by_choose_move") was my first attempt at 
a "choose the best move" approach. In it I started to recreate
some of the logic I had written a decade ago, specifically 
around "locking in" rows once they were done. It wasn't working,
and I got wrapped around the axel in my head.
So I tried again...

Approach #2 ("solve_by_prioritized_search" and "solve_by_walk_paths") 
took the ideas in
the first approach, ripped out the "locking" logic, and distilled
out a set of attributes of a board that could score a resulting
state as better or worse, allowing the logic to prioritize which
move to make. It's one step closer to having something that could
move toward reinforcement learning. But before I could even
think about tackling such a thing, I had an AHA moment.

Approach #3---my AHA moment---works backward from a solved
puzzle. Applying the realization that a slider puzzle is like
a maze, I wondered how hard it would be to generate all the
unsolved puzzles that were X moves away from the solution.
You can find this approach in "slider_puzzle_generator."

### Working Backward

If a slider puzzle is like a maze, what are all the "rooms" in
a 3x3 puzzle that you can get to if you start at the solution?

This is the question that set me down the path of generating
unsolved states by moving away from the solved state.

It turns out, if you have a 3x3 puzzle in the solved state, there
are only 2 places you can go.


|     |     |     |
|:---:|:---:|:---:|
| 1   | 2   | 3   |
| 4   | 5   |     |
| 7   | 8   | 6   |

or

|     |     |     |
|:---:|:---:|:---:|
| 1   | 2   | 3   |
| 4   | 5   | 6   |
| 7   |     | 8   |

If you then take the next step, you can see that there are 2 new
states you can get to from each of those states. And so on.

The Reddit puzzle had a particularly difficult puzzle that 
claimed to be solvable in 25 moves. That puzzle consistently
hung up my initial attempts at solving the puzzle by choosing
better moves. When I attempted to solve the puzzle manually
the best I could do was 30-some moves.

Could I find the solution by backing into it?

Turns out, yes I could. I generated all the puzzle states
that were 25 moves away from the solution, then searched for
the Reddit puzzle board in that set of boards. Bingo! I found
the solution:
 
[ 8, 6, 4, 1, 6, 3, 5, 6, 3, 5, 2, 8, 7, 4, 1, 3, 5, 2, 8, 7, 4, 1, 2, 5, 6 ]
 
So I wondered...if I generated all the board states that were
from 1 to N moves away, what % of valid 3x3s could be solved in
N moves?

Here's where I learned exactly how O^N inefficient my code is...
10 moves away takes a few minutes. 100 moves away didn't finish.
20 moves away took an hour? 2? I lost count. 

But I did at least partly answer my question.
     
There are 181,439 valid / solvable 3x3 board configuration.

Only 37,808 (just over 20%) of those can be solved in 20 
moves or fewer.

It turns out 140,134 (77%) can be solved in 25 moves or fewer.

Perhaps in the future I'll get around to doing a little 
table to show the
progression of counts of puzzles that can be solved in a
given number of moves. But not today.

## What I Learned

I learned a bunch about slider puzzles (see above).

I also learned a bunch about Python. As that was my actual
goal, I'm pleased.

Probably my biggest Python lesson is that default values
for parameters 
[can mutate.](https://stackoverflow.com/questions/1132941/least-astonishment-and-the-mutable-default-argument)
I lost a day or so to that. (Note that this is "pandemic days" which
means in practice probably 5 hours of work but it felt like 7362 days.)

I have not yet learned what I wanted to about ML, and may pick
this project up again at some point in the future to pursue that
goal. Until then, this README captures the current state of this
project.

# License?

This work is licensed under a 
Creative Commons Attribution-NonCommercial-ShareAlike 
4.0 International License.

That is: you can use it if you want to, but it's probably
not good for much.

