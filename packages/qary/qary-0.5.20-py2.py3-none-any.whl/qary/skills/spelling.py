""" spell checker bot based on Peter Norvig's spell checker """

from qary.etl.spell import make_spelling_corrections


class Skill:
    def reply(self, statement):
        r""" Chatbot "main" function to respond to a user command or statement

        >>> skill = Skill()
        >>> skill.reply('What is probabillity?')
        'What is probability?'
        >>> skill.reply('When was the telefone inventid?')
        'When was the telephone invented?'
        """
        corrected_statement = make_spelling_corrections(statement)
        confidence = 1.0 if corrected_statement.strip().lower() != statement.strip().lower() else 0.9
        return [(confidence, corrected_statement)]
