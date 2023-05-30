from django import template

register = template.Library()


@register.filter(name='stars')
def stars(rating, max=5):
    """Turns a note into a chain of stars."""
    return " ".join("★" if i <= rating else "✩" for i in range(1, max + 1))
