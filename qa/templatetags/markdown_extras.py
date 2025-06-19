from django import template
from django.template.defaultfilters import stringfilter
import markdown

register = template.Library()

@register.filter
@stringfilter
def convert_markdown(value):
    # Converts Markdown text to HTML.
    # Extensions can be added for more features, e.g., 'fenced_code'
    return markdown.markdown(value, extensions=['nl2br'])
    # 'nl2br' extension converts newlines to <br> for plain text too,
    # which can be useful if the AI sometimes just uses newlines.