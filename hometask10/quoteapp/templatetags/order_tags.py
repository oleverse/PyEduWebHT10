from django import template

register = template.Library()


def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)


register.filter('order_by', order_by)
