from django.views.generic import TemplateView
from django.conf import settings
from styleguide.parser import Parser, Tokenizer

import fnmatch
import os


class StyleGuideView(TemplateView):

    template_name = "styleguide/index.html"

    def get_context_data(self, **kwargs):
        context = super(StyleGuideView, self).get_context_data(**kwargs)
        context['less_variables'] = {}

        for f in self.get_files_to_parse(settings.STYLEGUIDE_PATH):
            t = Tokenizer(f)
            p = Parser(t)
            context['less_variables'][f] = []
            for var in p.variables:
                context['less_variables'][f].append(var)
        return context

    def get_files_to_parse(self, path):
        matches = []
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.less'):
                matches.append(os.path.join(root, filename))
        return matches
