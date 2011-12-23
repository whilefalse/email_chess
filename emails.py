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
    history_html = 'No moves yet'
    if game.history:
        history_html = '<ul><li> %s </li></ul>' % '</li><li>'.join(game.history)

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
You're <strong>%s</strong> and it's your move...
</p>

<h3>Instructions:</h3>

<ul>
<li>Reply to this email, entering your move in the first line of the response.</li>
<li>A move is the form of "a4 to b5". Be sure to get it in the right format.</li>
<li>If you think your opponent has made an invalid move, reply with a reason inclduing the work "undo" in the first line. This will undo their move and give control back to them.</li>
<li>Castling is a special case, you can specify that by saying something like "e1 to g1 and h1 to f1". This will move both pieces in one go for you.</li>
</ul>

<h3>Game History</h3>
%s

""" % (unicode(game.board).replace("\n", "<br/>").replace(" ", "&nbsp;"), game.whose_go, history_html)

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

def undo_move_email(game, move):
    message = base_email(game)
    message.subject="Your chess game with %s" % game.other_email()

    message.html = """
<p>
%s said that your last move was invalid, so it has been undone. They said:
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
