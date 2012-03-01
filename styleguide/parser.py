
TOKEN_AT = '[AT]'
TOKEN_SPACE = '[SPACE]'
TOKEN_ALPHANUM = '[CHAR]'
TOKEN_COLON = '[COLON]'
TOKEN_SEMICOLON = 'SEMICOLON'
TOKEN_NEWLINE = '[NEWLINE]'
TOKEN_MISC = '[MISC]'

TOKENS = (
    TOKEN_AT,
    TOKEN_SPACE,
    TOKEN_ALPHANUM,
    TOKEN_COLON,
    TOKEN_SEMICOLON,
    TOKEN_NEWLINE,
    TOKEN_MISC
)

class Token():

    value = None
    token_type = None

    def __init__(self, value, token_type):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return "%s %s" % (self.token_type, self.value)

class Tokenizer():

    f = None

    def __init__(self, filename):
        self.f = open(filename, 'r')

    def __iter__(self):
        return self

    def next(self):
        c = self.f.read(1)
        if not c:
            raise StopIteration

        token = Token(c, TOKEN_MISC)

        if '@' == c:
            token = Token(c, TOKEN_AT)
        elif ' ' == c:
            token = Token(c, TOKEN_SPACE)
        elif ':' == c:
            token = Token(c, TOKEN_COLON)
        elif ';' == c:
            token = Token(c, TOKEN_SEMICOLON)
        elif "\n" == c:
            token = Token(c, TOKEN_NEWLINE)
        elif c.isalnum():
            token = Token(c, TOKEN_ALPHANUM)

        return token

STATE_NONE = 0
STATE_VAR = 1
STATE_VAL = 2
STATE_FINISHED = 4

class Parser():



    _tokenizer = None
    _state = STATE_NONE

    _current_variable = ""
    _current_value = ""

    _variables = {}

    def __init__(self, tokenizer):
        self._tokenizer = tokenizer

    @property
    def variables(self):
        if not self._is_finished():
            self._parse()
        return self._variables

    def _is_finished(self):
        return self._state == STATE_FINISHED

    def _parse(self):

        dispatcher = {
            STATE_NONE: self._in_none,
            STATE_VAR: self._in_var,
            STATE_VAL: self._in_val
        }

        for token in self._tokenizer:
            f = dispatcher[self._state]
            f(token)

        self.state = STATE_FINISHED

    def _in_none(self, token):
        if TOKEN_AT == token.token_type:
            self._current_variable = token.value
            self._state = STATE_VAR

    def _in_var(self, token):
        if TOKEN_COLON == token.token_type:
            self._state = STATE_VAL
        elif TOKEN_ALPHANUM:
            self._current_variable += token.value
        else:
            self._state = STATE_NONE
            self._current_variable = ""


    def _in_val(self, token):
        if token.token_type in (TOKEN_SEMICOLON, TOKEN_NEWLINE):
            self._variables[self._current_variable.strip()] = self._current_value.strip()
            self._current_value = ""
            self._current_variable = ""
            self._state = STATE_NONE
        else:
            self._current_value += token.value


