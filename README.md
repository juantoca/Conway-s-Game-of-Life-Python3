# Conway's Game of Life Python3.0

<b>What's this?</b>

This is Yet Another Conway's Game Implementation. Isn't the best far away but I used this challenge to improve my Python skills.
If you haven't heard about CGL(Conway's Game of Life), I'll explain later on.

<b>So, what is this game about?</b>


Well, this game is an ZPG(Zero Game Player) that gets an initial state and calculates a simulation to get a final state(or continues the
simulation without an end)

We have a grid(in the case of my program, it haven't got a limit) in which each square(commonly known as cells) is a boolean(alive or death). Using a set of rules, we change this boolean on the grids. These rules are the following:

1- If a living cell has less than 2 living neighbours, in the next round it'll die

2- If a living cell has more than 3 living neighbours, it'll die

3- Otherwise, it'll survive(it needs 2 or 3 neighbours)

4- If a death cell have exactly 3 living neighbours it'll "born"


<img src=https://upload.wikimedia.org/wikipedia/commons/e/e5/Gospers_glider_gun.gif>

On this example, black tiles represents living ones and is one of the most famous patterns(Gosper's glider gun)

For farther riding, the game has a <a href=http://www.conwaylife.com/wiki/Main_Page>wiki</a>
