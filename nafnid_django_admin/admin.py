from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter, DropdownFilter
from .models import *


def merkja_rett(modeladmin, request, queryset):
    queryset.update(okay='True')


merkja_rett.short_description = "Merkja valin örnefni sem rétt"


class OrnefniInline(admin.TabularInline):
    model = Ornefni
    fields = ('ornefni', 'tvitak', 'okay')
    ordering = ('ornefni',)
    show_change_link = False
    view_on_site = False
    extra = 0


class SkjalSkrarInline(admin.TabularInline):
    model = Ornefnaskrar
    extra = 0
    fields = ('id', 'titill', 'stafraent', 'pappir')


class PdfSkrarFinnurAdmin(admin.ModelAdmin):
    def to_str(self, obj):
        return obj.__str__()

    fields = (
        'sysla_id',
        'hreppur_id',
        'bt_hreppur',
        'bt_sysla',
        'sysla',
        'hreppur',
        'slod',
        'file_tag',
        ('artal_skrar', 'artal_stadfest'),
        ('rannsakad', 'fjoldi_ornefna', 'ornefni_vantar'),
        ('handrit', 'handrit_orn'),
        'ocr_text',
    )
    inlines = [
        SkjalSkrarInline,
        OrnefniInline
    ]
    readonly_fields = ['file_tag', 'fjoldi_ornefna']
    list_display = ('to_str', 'sysla', 'hreppur', 'hastext', 'rannsakad')
    search_fields = ['slod', 'sysla', 'hreppur', 'ocr_text']
    list_filter = (
        'handrit',
        'rannsakad',
        ('ornefnaskrar__tegund', RelatedDropdownFilter),
        ('bt_sysla', RelatedDropdownFilter),
        ('bt_hreppur', RelatedDropdownFilter),
        ('sysla', DropdownFilter),
        ('hreppur', DropdownFilter),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(PdfSkrarFinnurAdmin, self).get_form(request, obj, **kwargs)
        widget = form.base_fields['bt_sysla'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        widget = form.base_fields['bt_hreppur'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        return form


class PdfSkrarAdmin(admin.ModelAdmin):
    def to_str(self, obj):
        return obj.__str__()

    fields = (
        'slod',
        'file_tag',
        'hastext'
    )
    inlines = [
        OrnefniInline
    ]
    readonly_fields = ['file_tag']
    list_display = ('to_str',)
    search_fields = ['slod', ]


class OrnefnaskrarTegundirInline(admin.TabularInline):
    list_display = ('tegund',)
    readonly_fields = ['id']
    view_on_site = False
    extra = 0
    model = Ornefnaskrar.tegund.through

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(OrnefnaskrarTegundirInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['tegund'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        return formset


class TegundirOrnefnaskrarInline(admin.TabularInline):
    list_display = ('skra',)
    readonly_fields = ['id']
    view_on_site = False
    extra = 0
    model = OrnefnaskrarTegundir

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(TegundirOrnefnaskrarInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['skra'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        return formset


class OrnefnaskrarStadaInline(admin.TabularInline):
    list_display = ('stada', 'athugasemd')
    readonly_fields = ['id']
    view_on_site = False
    extra = 0
    model = Ornefnaskrar.stada.through

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(OrnefnaskrarStadaInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['stada'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        return formset


class EinstaklingarStadirInline(admin.TabularInline):
    list_display = ('einstaklingur', 'baer')
    readonly_fields = ['id']
    raw_id_fields = ['baer']
    view_on_site = False
    extra = 0
    model = Einstaklingar.stadir.through

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(EinstaklingarStadirInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['einstaklingur'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        return formset


class OrnefnaskrarOrnefniInline(admin.TabularInline):
    list_display = ('ornefni',)
    readonly_fields = ['id']
    raw_id_fields = ['ornefni']
    show_change_link = True
    extra = 0
    model = Ornefnaskrar.ornefni.through


class BaeirOrnefniInline(admin.TabularInline):
    list_display = ('baer')
    readonly_fields = ['id']
    raw_id_fields = ['baer']
    show_change_link = True
    view_on_site = False
    extra = 0
    model = Ornefnaskrar.baeir.through

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(BaeirOrnefniInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['baer'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        return formset


class OrnefnaskrarBaeirInline(admin.TabularInline):
    list_display = ('ornefnaskra')
    readonly_fields = ['id']
    raw_id_fields = ['baer', 'ornefnaskra']
    show_change_link = True
    view_on_site = False
    extra = 0
    model = BaeirOrnefnaskrar

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(OrnefnaskrarBaeirInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['ornefnaskra'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        return formset


class OrnefnaskrarEinstaklingarInline(admin.TabularInline):
    list_display = ('einstaklingur',)
    raw_id_fields = ['einstaklingur', 'ornefnaskra']
    show_change_link = True
    view_on_site = False
    extra = 0
    model = OrnefnaskrarEinstaklingar

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(OrnefnaskrarEinstaklingarInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['ornefnaskra'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        return formset


class EinstaklingarOrnefnaskrarInline(admin.TabularInline):
    list_display = ('einstaklingur',)
    raw_id_fields = ['einstaklingur', 'ornefnaskra']
    show_change_link = True
    view_on_site = False
    extra = 0
    model = EinstaklingarOrnefnaskrar

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(EinstaklingarOrnefnaskrarInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['ornefnaskra'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        return formset


class OrnefnaskrarAdmin(admin.ModelAdmin):
    fields = (
        ('titill', 'id'),
        ('sysla', 'hreppur'),
        'texti',
        'stafraent',
        'pappir',
        'pdf_skra_id'
    )
    inlines = [
        OrnefnaskrarTegundirInline,
        OrnefnaskrarStadaInline,
        BaeirOrnefniInline,
        OrnefnaskrarEinstaklingarInline,
        # OrnefnaskrarOrnefniInline,
        OrnefniInline
    ]
    readonly_fields = ['id']
    raw_id_fields = ['pdf_skra_id']
    search_fields = ['titill', 'texti']
    list_display = ['titill', 'ornefna_link']
    list_filter = (
        'stada',
        'stafraent',
        'pappir',
        ('tegund', RelatedDropdownFilter),
        ('sysla', RelatedDropdownFilter),
        ('hreppur', RelatedDropdownFilter),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(OrnefnaskrarAdmin, self).get_form(request, obj, **kwargs)
        widget = form.base_fields['sysla'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        widget = form.base_fields['hreppur'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        return form


class TegundirAdmin(admin.ModelAdmin):
    pass


class StadaAdmin(admin.ModelAdmin):
    pass


'''class OrnefniAdmin(admin.ModelAdmin):
    pass
'''


class OrnefniAdmin(admin.ModelAdmin):
    fields = (
        ('ornefni', 'id'),
        ('lat', 'lon'),
        'okay',
        'pdf_skra_id'
    )
    list_display = ['ornefni', 'ornefnaskra', 'finnur', 'okay']
    list_filter = ('okay', )
    can_delete = False
    readonly_fields = ['id']
    raw_id_fields = ['pdf_skra_id', ]
    search_fields = ['ornefni']
    actions = [merkja_rett]


class OrnefninAdmin(admin.ModelAdmin):
    fields = (
        ('ornefni', 'id'),
        ('lat', 'lon'),
        'okay',
        'pdf_skra_id'
    )
    list_editable = ['ornefni', 'okay']
    list_display = ['id', 'ornefni', 'ornefnaskra', 'finnur', 'okay']
    list_filter = ('okay', )
    can_delete = False
    readonly_fields = ['id']
    raw_id_fields = ['pdf_skra_id', 'ornefnaskra']
    search_fields = ['ornefni']
    actions = [merkja_rett]


class BaejatalBaeirAdmin(admin.ModelAdmin):
    list_display = ['id', 'baejarnafn', 'sveitarfelag', 'hreppur', 'sysla', 'lbs_lykill', 'hnitsett']
    list_filter = [('sysla',RelatedDropdownFilter), ('sveitarfelag',RelatedDropdownFilter),('hreppur',RelatedDropdownFilter)]
    search_fields = ['baejarnafn', 'sysla__nafn', 'sveitarfelag__nafn', 'hreppur__nafn']
    inlines = [
        EinstaklingarStadirInline,
        OrnefnaskrarBaeirInline
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(BaejatalBaeirAdmin, self).get_form(request, obj, **kwargs)
        widget = form.base_fields['sveitarfelag'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        widget = form.base_fields['hreppur'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        widget = form.base_fields['sysla'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        return form


class EinstaklingarAdmin(admin.ModelAdmin):
    list_display = ['id', 'nafn', 'aukanafn', 'faedingarstadur', 'faedingarar', 'danarar']
    #list_editable = ['nafn', 'nafn', 'aukanafn', 'faedingarstadur', 'faedingarar', 'danarar']
    search_fields = ['nafn', 'aukanafn']
    raw_id_fields = ['stadir']
    inlines = [
        EinstaklingarStadirInline,
        EinstaklingarOrnefnaskrarInline
    ]


class BaejatalBaeirInline(admin.TabularInline):
    model = BaejatalBaeir
    fields = ['baejarnafn']
    readonly_fields = ['id']
    show_change_link = True
    can_delete = False
    view_on_site = False
    extra = 0


class BaejatalSveitarfelogGomulSyslurInline(admin.TabularInline):
    model = BaejatalSveitarfelogGomulSyslur
    readonly_fields = ['id']
    show_change_link = True
    view_on_site = False
    can_delete = False
    extra = 0


class BaejatalSveitarfelogNySyslurInline(admin.TabularInline):
    model = BaejatalSveitarfelogNySyslur
    list_display = ('sveitarfelag.nafn',)
    readonly_fields = ['id']
    show_change_link = True
    view_on_site = False
    can_delete = False
    extra = 0


class BaejatalSveitarfelogGomulAdmin(admin.ModelAdmin):
    model = BaejatalSveitarfelogGomul
    search_fields = ['nafn', ]

    inlines = [
        BaejatalBaeirInline
    ]


class BaejatalSveitarfelogNyAdmin(admin.ModelAdmin):
    model = BaejatalSveitarfelogNy
    search_fields = ['nafn',]

    inlines = [
        BaejatalBaeirInline
    ]


class BaejatalSyslurAdmin(admin.ModelAdmin):
    inlines = [
        BaejatalSveitarfelogGomulSyslurInline,
        BaejatalSveitarfelogNySyslurInline
    ]

class AbendingarAdmin(admin.ModelAdmin):
	search_fields = ['nafn', 'netfang', 'skilabod']
	list_filter = ['inserttime', 'entity_type']
	list_display = 'nafn', 'entity_name', 'entity_type', 'inserttime'
	fields = ('nafn', ('netfang', 'simanumer'), 'skilabod', 'entity_type', 'entity_link', 'inserttime')
	readonly_fields = ('nafn', 'netfang', 'simanumer', 'skilabod', 'entity_type', 'entity_link', 'inserttime')

admin.site.disable_action('delete_selected')
admin.site.view_on_site = False

admin.site.register(Ornefnaskrar, OrnefnaskrarAdmin)
##admin.site.register(Ornefni, OrnefniAdmin)
admin.site.register(Tegundir, TegundirAdmin)
admin.site.register(Stada, StadaAdmin)
admin.site.register(PdfSkrarFinnur, PdfSkrarFinnurAdmin)
#admin.site.register(PdfSkrarFinnur, PdfSkrarAdmin)
admin.site.register(Einstaklingar, EinstaklingarAdmin)
admin.site.register(Ornefni, OrnefniAdmin)

admin.site.register(BaejatalBaeir, BaejatalBaeirAdmin)
admin.site.register(BaejatalSveitarfelogGomul, BaejatalSveitarfelogGomulAdmin)
admin.site.register(BaejatalSveitarfelogNy, BaejatalSveitarfelogNyAdmin)
admin.site.register(BaejatalSyslur, BaejatalSyslurAdmin)

admin.site.register(Abendingar, AbendingarAdmin)
