from django.conf.urls.defaults import patterns, url
from styleguide.views import StyleGuideView

urlpatterns = patterns('',
    url(r'^$', StyleGuideView.as_view(), name='less.style_guide'),
)
