import markdown as md

from django.template import Library
from django.template.defaultfilters import stringfilter


register = Library()

@register.filter('markdown')
@stringfilter
def markdown(text):
    return md.markdown(
        text,
        extensions=['fenced_code', 'tables', 'attr_list', 'legacy_attrs'],
        output_format='html5'
    )