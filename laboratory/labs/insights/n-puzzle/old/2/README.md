# CI2024_lab3
To solve this n*n-1 puzzle problem I build a Uniform-Cost algorithm. I have decided to adopt a Breadth-first approach, instead of a Depth-first search, because a solution for this type of problem, in general, requires a huge number of steps, so I think it is faster in that way. Furthermore, I applied to it some considerations that take to exploring states in a different order than the one in which they are discovered.
In particular, I have choosen as fronteer a priority queue that give precedence to state in which, in order:
 - the moved element is in a different position from the one in the final instance, if it is already in the right position it is preferable not to migrate it;
 - the shifted number is relocated in a position that is closer to the final one than the prevoius one.

I noticed that, in most cases, like in the example that is present in the outputs of the file (in red), this algorithm compared to a Breadth-first one that I have implemented too, leads to a solution that includes a bigger number of steps , but is reached in a smaller number of total trials.
