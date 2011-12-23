import logging, email, re, pickle
from google.appengine.api import mail
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from game import Game
from board import Board
import runner
import emails
import errors

class PlayGameHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.debug(mail_message.to)

        match = re.search(r'chess-(.+)@', mail_message.to)
        game_key = match.groups()[0]

        game = Game.get(game_key)

        payload = mail_message.bodies('text/plain').next()[1]
        if payload.encoding == '8bit' and payload.charset:
            body = payload.payload.decode(payload.charset)
        else:
            body = payload.decode()

        first_line = body.split("\n")[0]

        try:
            game.do_move(first_line)
            game.put()

            emails.play_game_email(game, first_line).send()
        except errors.InvalidMove:
            emails.invalid_move_email(game, first_line).send()
        except errors.Undo:
            game.put()
            emails.undo_move_email(game, first_line).send()

if __name__ == '__main__':
    runner.run(PlayGameHandler)
