from ajax_select import register, LookupChannel
from enterprises.models import Enterprise
from .models import Contract

@register('enterprises')
class EnterprisesLookup(LookupChannel):

    model = Enterprise

    def get_query(self, q, request):
        return self.model.objects.filter(fullname__icontains=q)

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.fullname