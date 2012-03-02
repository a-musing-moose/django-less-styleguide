
TOKEN_AT = '[AT]'
TOKEN_SPACE = '[SPACE]'
TOKEN_ALPHANUM = '[CHAR]'
TOKEN_COLON = '[COLON]'
TOKEN_SEMICOLON = 'SEMICOLON'
TOKEN_NEWLINE = '[NEWLINE]'
TOKEN_MISC = '[MISC]'
TOKEN_OPEN_CURL = '[OPEN_CURL]'
TOKEN_CLOSE_CURL = '[CLOSE_CURL]'

TOKENS = (
    TOKEN_AT,
    TOKEN_SPACE,
    TOKEN_ALPHANUM,
    TOKEN_COLON,
    TOKEN_SEMICOLON,
    TOKEN_NEWLINE,
    TOKEN_MISC,
    TOKEN_OPEN_CURL,
    TOKEN_CLOSE_CURL,
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

    filename = None
    f = None

    def __init__(self, filename):
        self.filename = filename
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
        elif "{" == c:
            token = Token(c, TOKEN_OPEN_CURL)
        elif "}" == c:
            token = Token(c, TOKEN_CLOSE_CURL)
        elif c.isalnum():
            token = Token(c, TOKEN_ALPHANUM)

        return token


class Variable():

    name = None
    value = None
    line_number = None

    def __str__(self):
        return "%s = %s" % (self.name, self.value)

STATE_NONE = 0
STATE_VAR = 1
STATE_VAL = 2
STATE_IN_BLOCK = 3
STATE_FINISHED = 99


class Parser():

    def __init__(self, tokenizer):
        self._variables = []
        self._state = STATE_NONE
        self._stack = ""
        self._var = Variable
        self._line_no = 1
        self._tokenizer = tokenizer

    def _add_to_stack(self, char):
        self._stack = self._stack + char

    def _get_stack(self):
        s = self._stack
        self._stack = ""
        return s.strip()

    def _set_state(self, state):
        self._state = state

    def _is_at_state(self, state):
        return state == self._state

    @property
    def variables(self):
        if not self._is_finished():
            self._parse()
        return self._variables

    def _is_finished(self):
        return self._state == STATE_FINISHED

    def _parse(self):

        self._var = Variable()

        dispatcher = {
            TOKEN_ALPHANUM: self._is_alphanum,
            TOKEN_AT: self._is_at,
            TOKEN_COLON: self._is_colon,
            TOKEN_MISC: self._is_misc,
            TOKEN_NEWLINE: self._is_newline,
            TOKEN_SEMICOLON: self._is_semicolon,
            TOKEN_SPACE: self._is_space,
            TOKEN_OPEN_CURL: self._is_open_curl,
            TOKEN_CLOSE_CURL: self._is_close_curl,
        }

        for token in self._tokenizer:
            f = dispatcher[token.token_type]
            f(token)

        self.state = STATE_FINISHED

    def _is_at(self, token):
        if self._is_at_state(STATE_NONE):
            self._set_state(STATE_VAR)
            self._get_stack()
            self._add_to_stack(token.value)
            self._var.line_number = self._line_no
        else:
            self._add_to_stack(token.value)

    def _is_open_curl(self, token):
        self._set_state(STATE_IN_BLOCK)

    def _is_close_curl(self, token):
        self._set_state(STATE_NONE)

    def _is_colon(self, token):
        if self._is_at_state(STATE_IN_BLOCK):
            return
        if self._is_at_state(STATE_VAR):
            self._set_state(STATE_VAL)
            self._var.name = self._get_stack()
        else:
            self._add_to_stack(token.value)

    def _is_alphanum(self, token):
        if self._is_at_state(STATE_IN_BLOCK):
            return
        self._add_to_stack(token.value)

    def _is_misc(self, token):
        if self._is_at_state(STATE_IN_BLOCK):
            return
        if self._is_at_state(STATE_VAR):
            self._set_state(STATE_NONE)
            self._var = Variable();
        else:
            self._add_to_stack(token.value)

    def _is_space(self, token):
        if self._is_at_state(STATE_IN_BLOCK):
            return
        self._add_to_stack(token.value)

    def _is_semicolon(self, token):
        if self._is_at_state(STATE_IN_BLOCK):
            return
        if self._is_at_state(STATE_VAL):
            self._var.value = self._get_stack()
            self._variables.append(self._var)
            self._var = Variable()
        self._set_state(STATE_NONE)
        self._var = Variable()

    def _is_newline(self, token):
        if self._is_at_state(STATE_IN_BLOCK):
            return
        if self._is_at_state(STATE_VAL):
            self._var.value = self._get_stack()
            self._variables.append(self._var)
            self._var = Variable()
        self._set_state(STATE_NONE)
        self._var = Variable()
        self._line_no += 1
