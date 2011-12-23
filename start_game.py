from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from game import Game
import runner
import emails

class StartGameHandler(InboundMailHandler):
    def receive(self, mail_message):
        game = Game(
                black_email = mail_message.sender,
                white_email = mail_message.cc,
                whose_go = 'white')
        game.put()

        emails.start_game_email(game).send()

if __name__ == '__main__':
    runner.run(StartGameHandler)
