from ajax_select import register, LookupChannel
from enterprises.models import Responseteam
from .models import Qteam

@register('qteams')
class ResponseteamsLookup(LookupChannel):

    model = Responseteam

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q)

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name