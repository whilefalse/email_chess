from google.appengine.api import mail
import re

def base_email(game):
    message = mail.EmailMessage()
    message.sender = "chess-%s@email-chess.appspotmail.com" % game.key()
    message.to = game.whose_go_email()

    return message

def textify(html):
    return re.sub(r'<[^>]*?>', '', html).replace('&nbsp;', ' ')

def footer(game):
    return """
<p>
Here's the current board:
</p>

<center>
<font size="5" face="mono" color="blue">
%s
</font>
</center>

<p>
You're %s and it's your move...
</p>

<h3>Instructions:</h3>

<p>
Reply to this email, entering your move in the first line of the response.
</p>

<p>
A move is the form of "a4 to b5". Be sure to get it in the right format.
</p>
""" % (unicode(game.board).replace("\n", "<br/>").replace(" ", "&nbsp;"), game.whose_go)

def start_game_email(game):
    message = base_email(game)

    message.subject = "%s would like to start a chess game with you." % game.other_email()
    message.html = "<p><strong>%s</strong> challenges you to a game of chess!</p>" % (textify(game.other_email()))
    message.html += footer(game)
    message.body = textify(message.html)

    return message

def play_game_email(game, move):
    message = base_email(game)
    message.subject="Your chess game with %s" % game.other_email()

    message.html = """
<p>
Here's the latest move from <strong>%s</strong>:
</p>

<center>
<font size="5" face="mono" color="red">
%s
</font>
</center>
""" % (textify(game.other_email()), move)
    message.html += footer(game)
    message.body = textify(message.html)

    return message

def invalid_move_email(game, move):
    message = base_email(game)
    message.subject="Your chess game with %s" % game.other_email()

    message.html = """
<p>
Your last move was invalid. Please resend a valid move. Your last move was:
</p>

<center>
<font size="5" face="mono" color="red">
%s
</font>
</center>
""" % (move)
    message.html += footer(game)
    message.body = textify(message.html)

    return message
