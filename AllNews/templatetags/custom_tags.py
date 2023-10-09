from django import template
from AllNews.models import CommentReaction


register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v

    return d.urlencode()


@register.simple_tag()
def isReacted(comment_id, user, reaction):
    if str(user) == 'AnonymousUser':
        return

    request = CommentReaction.objects.filter(
        comment=comment_id,
        user=user,
    ).values('reaction')

    if request:
        request = request[0]['reaction']

    if request == reaction:
        return 'reacted'
    else:
        return