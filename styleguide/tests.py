from django.test import TestCase
from django.test.client import RequestFactory

from styleguide.parser import Token, Tokenizer, TOKEN_AT, Parser
from styleguide.views import StyleGuideView


LESS_FILE = """
@blue:                  #049cdb;
@blueDark:              #0064cd;
@green:                 #46a546;
@red:                   #9d261d;
@yellow:                #ffc40d;
@orange:                #f89406;
@pink:                  #c3325f;
@purple:                #7a43b6;
@linkColorHover:        darken(@linkColor, 15%);
"""

TMP_FILE = '/tmp/less_test.less'

class TokenTests(TestCase):

    def test_string(self):
        expected = "[AT] @"
        token = Token('@', TOKEN_AT)
        self.assertEqual(expected, token.__str__())

class TokenizerTests(TestCase):

    def setUp(self):
        f = open(TMP_FILE, 'w')
        f.write(LESS_FILE)
        f.close()

    def test_token_stream(self):
        t = Tokenizer(TMP_FILE)
        for token in t:
            self.assertIsInstance(token, Token)

class ParserTests(TestCase):

    def setUp(self):
        f = open(TMP_FILE, 'w')
        f.write(LESS_FILE)
        f.close()

    def test_parsing(self):
        t = Tokenizer(TMP_FILE)
        p = Parser(t)

        expected = {
            '@blue': '#049cdb',
            '@purple': '#7a43b6',
            '@pink': '#c3325f',
            '@blueDark': '#0064cd',
            '@orange': '#f89406',
            '@yellow': '#ffc40d',
            '@linkColorHover': 'darken(@linkColor, 15%)',
            '@green': '#46a546',
            '@red': '#9d261d',
        }

        for v in p.variables:
            print v

#       self.assertDictEqual(expected, p.variables)


class StyleGuideViewTests(TestCase):

    def setUp(self):
        f = open(TMP_FILE, 'w')
        f.write(LESS_FILE)
        f.close()

        self.factory = RequestFactory()

    def test_view(self):
        request = self.factory.get('/')
        v = StyleGuideView.as_view()
        response = v(request)
        response.render()

#        self.assertEqual(response.status_code, 200)
#        self.assertContains(response, '<dt>@blue</dt>')
#        self.assertContains(response, '<dd>darken(@linkColor, 15%)</dd>')
