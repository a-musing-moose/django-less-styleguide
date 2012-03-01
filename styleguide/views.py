from django.views.generic import TemplateView
from django.conf import settings
from styleguide.parser import Parser, Tokenizer

from glob import glob
from os.path import join


class StyleGuideView(TemplateView):

    template_name = "styleguide/index.html"

    def get_context_data(self, **kwargs):
        context = super(StyleGuideView, self).get_context_data(**kwargs)
        context['less_variables'] = []

        for f in self.get_files_to_parse(settings.STYLEGUIDE_PATH):
            t = Tokenizer(f)
            p = Parser(t)
            for var in p.variables:
                context['less_variables'].append({
                     'name': var,
                     'value': p.variables[var]
                 })
        return context

    def get_files_to_parse(self, path):
        file_list = []
        for f in glob(join(path, '*.less')):
            file_list.append(f)
        return file_list
