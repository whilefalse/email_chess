import logging, re
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from game import Game
import runner
import emails
import errors

class PlayGameHandler(InboundMailHandler):
    def receive(self, mail_message):
        match = re.search(r'chess-(.+)@', mail_message.to)
        game_key = match.groups()[0]

        game = Game.get(game_key)
        # Stop duplicate processing
        if mail_message.original['Message-ID'] in game.processed:
            return

        payload = mail_message.bodies('text/plain').next()[1]
        if payload.encoding == '8bit' and payload.charset:
            body = payload.payload.decode(payload.charset)
        else:
            body = payload.decode()

        first_line = body.split("\n")[0]

        try:
            game.processed.append(mail_message.original['Message-ID'])
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
