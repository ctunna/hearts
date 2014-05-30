#!/usr/bin/env python2.6

import socket
import sys
import os
import select
import json
import string
import hearts

BUFSIZ = 1024

class Client(object):

    def __init__(self, host='127.1', port=3000):
        self.flag = False
        self.port = int(port)
        self.host = host
        self.me = hearts.Player('me')

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            print 'Connected to chat server@%d' % self.port
        except socket.error, e:
            print 'Could not connect to chat server @%d' % self.port
            sys.exit(1)

    def handle_request(self, data):
        body_start = data.rfind('\n\n')
        body = data[body_start:len(data)]

        if data.rfind('DEAL', 0, 20) >= 0:
            self.me.set_hand(json.loads(body))
            print 'Your hand: \n' + self.me.show()

        if data.rfind('PLAY', 0, 20) >= 0:
            cards_played = json.loads(json.loads(body.strip())) # sad face
            card = self.get_card(cards_played)
            resp = 'Type: CARD\n\n' + json.dumps(card) + '#'
            self.sock.send(resp)

        if data.rfind('SCORE', 0, 20) >= 0:
            print 'Score: ' + body.strip()

        if data.rfind('SEAT', 0, 20) >= 0:
            self.me.set_seat(body.strip())
            
    def get_card(self, cards_played):
        print 'You\'re seated: ' + self.me.get_seat()
        print 'Cards played: ' + str(cards_played)
        inp = raw_input('Play a card please: ')
        suit, rank = inp.split(',')
        card = [suit, int(rank)]

        (valid, error_msg) = self.valid_play(card, cards_played)
        while not valid:
            print error_msg
            inp = raw_input('Play a card please: ')
            suit, rank = inp.split(',')
            card = [suit, int(rank)]
            (valid, error_msg) = self.valid_play(card, cards_played)

        self.me.play_card(card)

        os.system('clear')

        print 'Your hand: \n' + self.me.show()

        return card

    def valid_play(self, card, cards_played):
        error = ''
        if card not in self.me.hand:
            error = str(card) + " is not in your hand!"
            return (False, error)

        if len(cards_played) > 0:
            lead_suit = cards_played[0][0][0]

            if card[0] == lead_suit:
                return (True, error)
            else:
                for each_card in self.me.hand:
                    if each_card[0] == lead_suit:
                        error = 'You must play a %s' % hearts.get_suit_name(lead_suit)
                        return (False, error)

        return (True, error)
        
    def recvall(self, sock):
        buf = ''
        while '#' not in buf:
            newbuf = sock.recv(BUFSIZ)
            buf += newbuf

        return buf.strip()

    def next_request(self, data):
        delim_pos = data.find('#')
        
        assert(delim_pos >= 0)

        return data[delim_pos+1:], data[:delim_pos].strip('#') # data, req

    def start(self):

        self.sock.send("North")

        data = ''
        while not self.flag:
            try:
                data += self.recvall(self.sock)

                while data:
                    data, req = self.next_request(data)

                    if req:
                        self.handle_request(req)
#                    print 'data: ' + data
#                    print 'req: ' +  req
            except KeyboardInterrupt:
                print 'Interrupted.'
                self.sock.send('EOT')
                self.sock.close()
                break
                
if __name__ == "__main__":

    if len(sys.argv) < 2:
        sys.exit('Usage: %s <Port Number>' % sys.argv[0])
        
    client = Client(sys.argv[1], int(sys.argv[2]))
    client.start()
