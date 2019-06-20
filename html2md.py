from html.parser import HTMLParser


class Html2Markdown(HTMLParser):
    # output markdown text
    output = ''

    # take a unique placeholder then replace text
    _placeholder = '3f4ec2b893ce4f1ab0f4c0861ef9dae7'

    # mark content between start tag and end tag
    _content = ''

    # mark hidden between start tag and end tag
    _hidden = False

    # mark new line between start tag and end tag
    _newline = True

    # mark prefix line between start tag and end tag
    _prefix = False

    # define replacemen rules - 0: starttag, 1: endtag
    _rule_replacement = {
        'a': ('', ''),
        'blockquote': ('\n', '\n'),
        'code': (' ``` ', ' ``` '),
        'em': ('*', '*'),
        'h1': ('# ', '\n'),
        'h2': ('## ', '\n'),
        'h3': ('### ', '\n'),
        'h4': ('#### ', '\n'),
        'h5': ('##### ', '\n'),
        'h6': ('###### ', '\n'),
        'hr': ('', ' ----- \n'),
        'img': ('', '\n'),
        'p': ('', '\n'),
        'pre': ('', '\n'),
        'strong': ('**', '**'),
        'ul': ('\n', '\n')
    }

    # default parse
    def default_parse(self, tag, alone):
        if alone is True:
            i = 0
        else:
            i = 1
        if tag in self._rule_replacement:
            it = self._rule_replacement[tag]
            self.output += it[i]

    # handle start tag
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, val) in attrs:
                if key == 'href':
                    self._content = f'[{self._placeholder}]({val})'

        if tag == 'blockquote':
            self._prefix = True

        if tag == 'code':
            self._content = self._placeholder

        if tag == 'figcaption':
            self._hidden = True

        if tag == 'li':
            if self._prefix is True:
                self.output += '>'
            else:
                self.output += '* '
            self._newline = False

        if tag == 'p':
            if self._newline is True:
                self.output += '\n'

        if tag == 'pre':
            self._rule_replacement['code'] = (' ``` \n', ' ``` ')

        # default parse
        self.default_parse(tag, True)

    # handle text data
    def handle_data(self, data):
        if len(self._content) > 0:
            self.output += self._content.replace(self._placeholder, data)
            self._content = ''
        elif self._hidden is False:
            self.output += data

    # handle end tag
    def handle_endtag(self, tag):
        if tag == 'blockquote':
            self.output += '\n'
            self._prefix = False

        if tag == 'figcaption':
            self._hidden = False

        if tag == 'li':
            self._newline = True

        if tag == 'pre':
            self._rule_replacement['code'] = (' ``` ', ' ``` ')

        # default parse
        self.default_parse(tag, False)

    # handle never end tag
    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            if self._newline is True:
                self.output += '\n'

        if tag == 'img':
            for (key, val) in attrs:
                if key == 'data-src':
                    self.output += f'![]({val}&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)'

        # default parse
        self.default_parse(tag, True)
