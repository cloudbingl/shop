from django import template

register = template.Library()


@register.simple_tag()
def filter_phone(phone):
    phone = str(phone)
    new_num = phone[0:3] + "****" + phone[8:12]
    return new_num