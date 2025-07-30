from decimal import Decimal
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re
import markdown

register = template.Library()


@register.filter(needs_autoescape=True)
def wrap_marked_scalables(value, autoescape=True):
    # This regex matches @<int> patterns
    pattern = r"@(\d+(.\d+)?)"

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    # Function to wrap matched pattern with a span
    def replace(match):
        return f'<span class="scalable" data-original-value="{match.group(1)}">{match.group(1)}</span>'

    # Use re.sub to replace the pattern with the wrapped version
    return mark_safe(re.sub(pattern, replace, esc(value)))


@register.filter(needs_autoescape=True)
def wrap_scalable(value, autoescape=True):
    # Deal with autoescape
    clean_value = conditional_escape(value) if autoescape else value

    # Wrap value with a span
    return mark_safe(f'<span class="scalable" data-original-value="{clean_value}">{clean_value}</span>')

@register.filter()
def pluralise_unit(value, quantity):
    pluralised = value.singular if quantity <= 1 else value.plural
    return pluralised if pluralised is not None else value.name


@register.filter()
def render_markdown(value):
    return mark_safe(markdown.markdown(value))


@register.filter()
def format_timer(value):
    total_seconds = value.total_seconds()
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) / 60
    seconds = total_seconds % 60
    return (
        "%d:%02d:%02d" % (hours, minutes, seconds)
        if hours > 0
        else "%02d:%02d" % (minutes, seconds)
    )


@register.filter
def detrail(value):
    """Removes trailing zeros from a number (float or decimal)."""
    return re.sub(r"0+$", "", value) if "." in str(value) else str(value)


@register.filter
def format_duration(value):
    total_seconds = value.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) / 60)

    return f"{hours} hr " * (hours > 0) + f"{minutes} min" * (minutes > 0)
    # if hours > 0 and minutes != 0:
    #     return f"{hours} hr {minutes} min"
    # elif hours > 0:
    #     return f"{hours} hr"
    # else:
    #     return f"{minutes} min"
