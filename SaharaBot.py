import sys
import random
import traceback
import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space

"""
$ python3.5 guess.py <token>
Guess a number:
1. Send the bot anything to start a game.
2. The bot randomly picks an integer between 0-99.
3. You make a guess.
4. The bot tells you to go higher or lower.
5. Repeat step 3 and 4, until guess is correct.
"""

class Player(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.arrayOfTimesCooked = [0,0,0,0]
        # self._answer = random.randint(0,99)

    # def _hint(self, answer, guess):
    #     if answer > guess:
    #         return 'larger'
    #     else:
    #         return 'smaller'

    def open(self, initial_msg, seed):
        self.sender.sendMessage('Who cooked today? \n press 0 for nobody, 1 for Ana/Sikai, 2 for Celeste/Wenqi, 3 for Annabel/Drake')
        return True  # prevent on_message() from being called on the initial message

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
           self.sender.sendMessage('Give me a number, please.')
           return

        try:
           command = int(msg['text'])
        except ValueError:
            self.sender.sendMessage('Give me a number, please.')
            return

        self.arrayOfTimesCooked[command] += 1
        output = "The scoreboard is Ana & Sikai: %d, Celeste & Wenqi: %d, Annabel & Drake: %d, Times you guys got lazy" % self.arrayOfTimesCooked[1] % self.arrayOfTimesCooked[2] % self.arrayOfTimesCooked[3] % self.arrayOfTimesCooked[0]
        self.sender.sendMessage(output)
        # check the guess against the answer ...
        # if guess != self._answer:
        #     # give a descriptive hint
        #     hint = self._hint(self._answer, guess)
        #     self.sender.sendMessage(hint)
        # else:
        #     self.sender.sendMessage('Correct!')
        #     self.close()

    def on__idle(self, event):
        self.sender.sendMessage('Game expired. The answer is %d' % self._answer)
        self.close()


TOKEN = sys.argv[1]

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Player, timeout=10000000),
])
bot.message_loop(run_forever='Listening ...')