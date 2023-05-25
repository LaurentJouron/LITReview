from django import template

register = template.Library()


def stars(rating, max=5):
    """Turns a note into a chain of stars."""
    return " ".join("★" if i <= rating else "✩" for i in range(1, max + 1))
