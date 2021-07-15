from django import template

register = template.Library()


@register.filter
def switch_symb(text: str, arg: str = ',&•') -> str:
    # заменяет в полученной строке символ до & на символ после &
    [prev, new] = arg.split('&')

    new_string = ""
    for char in text:
        if char != prev:
            new_string += char
        else:
            new_string += new
    return new_string
