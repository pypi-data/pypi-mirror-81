""" Pattern and template based chatbot dialog engines """
import re


# from .template_generators import generate_sentence  # noqa


class Skill:
    def reply(self, statement):
        r""" Chatbot "main" function to respond to a user command or statement

        >>> bot = Skill()
        >>> bot.reply('Hi')[0][1]
        'Hello!'
        >>> len(bot.reply('Hey Mycroft!'))
        5
        """
        responses = []
        match = re.match(r'\b(hi|hello|hey)\b(.*)', statement.lower())
        if match:
            responses.append((0.1, "Hello"))
            if 'mycroft' in match.groups()[1].lower():
                responses.append((0.2, "Hi!"))
                responses.append((0.2, "Hi! What would you like to talk about?"))
                responses.append((0.2, "Hi! You remembered me! How are you doing?"))
            if 'bot' in match.groups()[1].lower():
                responses.append((0.2, "Hey. That's a good one."))
        responses.append((0.05, "Wuh?"))
        if statement == 'Hi':
            responses = [(1.0, "Hello!")]
        return responses
