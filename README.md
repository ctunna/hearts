HEARTS v1.0 by Carson Tunna 10046942

This is an implementation of the classic card game hearts that was
used as tool to familiarize myself with socket programming. This
program is written using python2.7, but should be compatible with
python2.6. Python2.6 is installed on the EC2 servers.

* hearts/

    Hearts is a module I made to keep track of game state, the
    deck, and players.

* server.py

    Hearts server. Four clients connect to the server an are
    assigned names North, East, South, and west in the order they join.
    Obviously the server must be started before the clients can connect.
    Server keeps track of Hearts game state with the hearts module. Send a
    variety of requests to client including, PLAY, SCORE, and DEAL.

* client.py

    Keeps track of game state with Hearts module. Sends CARD
    reply to server after receiving a PLAY request.

* General

IMPORTANT
=========

    To play a card type [suit],[rank] when prompted. For
    example to play the queen of spades: s,12
            
    If your input isn't given in this format the behavior is undefined.
    
    Ace is 1 ..... King is 13.

    Game is over when a player racks up at least 100 points. Server shuts down.