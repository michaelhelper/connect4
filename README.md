# connect4

This is our connect 4 project that we worked on for our minds and machines class. it uses basic look ahead functionality 
and minor minimaxing, along with a few other things to make it work. It is not perfect, but it is a good start.

If you would like to use it, run the server and the client in the "mindsmachines-connect4" folder.
Then when you use the program, you can either create a game and it will give you the ID or you can join a game with 
a randomly generated ID.

Eventually, we would increase the depth of the program, allowing it to look more moves into the future. In order to 
increase this depth, we would need to implement a more efficient data structure to store the Connect-4 board positions, 
and use a technique called alpha beta pruning which would disregard a branch of the move tree if the branch gives us an 
objectively losing position. We could also utilize a transposition table which would store all the board positions 
generated and save us the time of recreating board positions we previously generated.

Special thanks to exoRift for making the client!
