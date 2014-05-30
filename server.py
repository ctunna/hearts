#!/usr/bin/env python2.6

import select
import socket
import sys
import string
import json
import hearts

BUFSIZ = 1024

class Cardinal:
    North, East, South, West = range(4)

class Server(object):

    def __init__(self):
        self.host = ''
        self.backlog = 5
        self.size = 4096
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, int(sys.argv[1])))
        self.server.listen(self.backlog)
        self.game = hearts.Hearts()
        self.player_map = {}

    def format_request(self, type, body):
        t = 'Type: %s\n' % (type)
        b = '\n%s#' % (json.dumps(body))
        return t + b

    def handle_response(self, data):
        body_start = data.rfind('\n\n')
        body = data[body_start:len(data)]
        if data.rfind('CARD', 0, 20):
            return json.loads(body)

    def deal(self):
        hands = self.game.deal()
        for player in self.game.players:
            self.player_map[player.get_seat()].send(self.format_request('DEAL', player.get_hand()))
        
    def do_trick(self, lead):
        cards_played = list([])
        for i in range(4):
            psock = self.player_map[(lead + i) % 4]
            encoded = json.dumps(cards_played)
            req = self.format_request('PLAY', encoded)
            psock.send(req)

            resp = self.recvall(psock)
            while len(resp) <= 0:
                resp = self.recvall(psock)

            card = self.handle_response(resp)
            self.game.players[(lead + i) % 4].play_card((card[0], card[1]))
            cards_played.append([card[0], card[1], (lead + i) % 4])
          
        self.game.score_trick(cards_played)

        print self.game.get_score()

    def broadcast_score(self):
        req = self.format_request('SCORE', self.game.get_score())
        for player in self.game.players:
            self.player_map[player.get_seat()].send(req)

    def assign_seats(self):
        seats = ['North', 'East', 'South', 'West']
        for player in self.game.players:
            req = self.format_request('SEAT', seats[player.get_seat()])
            self.player_map[player.get_seat()].send(req)

    def shutdown(self):
        sys.exit()

    def recvall(self, sock):
        buf = ''
        while '#' not in buf:
            newbuf = sock.recv(BUFSIZ)
            buf += newbuf

        return buf[:-1]

    def serve(self):
        input = [self.server,sys.stdin]
        running = start_game = 1
        pc = playing = players_turn = 0

        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:
                if s == self.server and pc < 4:
                    # handle the server socket
                    client, address = self.server.accept()
                    input.append(client)
                    self.player_map[pc] = client
                    pc += 1

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

                else:

                    # if self.player_map[players_turn] != s:
                    #     continue

                    buffer = s.recv(BUFSIZ)
                    
                    if buffer.rfind('EOT', 0, 3) != -1:
                        input.remove(s)

                    if pc == 4 and start_game:
                        self.assign_seats()
                        start_game = 0
                        playing = 1

                    # TODO: adjust so player with 2C leads
                    if playing:
                        while not self.game.game_over():
                            self.deal()

                            for tricks_left in range(13):
                                self.do_trick(Cardinal.North)

                            self.broadcast_score()

                        self.server.close() 
                        self.shutdown()

if  __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.exit('Usage: %s <Port Number>' % sys.argv[0])

    server = Server()
    server.serve()
