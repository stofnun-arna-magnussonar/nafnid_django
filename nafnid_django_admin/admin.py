from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter, DropdownFilter
from .models import *


def merkja_rett(modeladmin, request, queryset):
    queryset.update(okay='True')


merkja_rett.short_description = "Merkja valin örnefni sem rétt"


class OCROrnefniInline(admin.TabularInline):
    model = OCROrnefni
    fields = ('ornefni', 'okay', 'lat', 'lon')
    readonly_fields = ['pdf_skra_id', 'ornefnaskra']
    raw_id_fields = ['pdf_skra_id', 'ornefnaskra']
    show_change_link = False
    view_on_site = False
    extra = 0


class SkjalSkrarInline(admin.TabularInline):
    model = Ornefnaskrar
    extra = 0
    show_change_link = True
    view_on_site = False
    can_delete = False
    fields = ('id', 'titill', 'stafraent', 'pappir')
    readonly_fields = ['titill']


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
        'ocr_text'
    )
    inlines = [
        SkjalSkrarInline,
        OCROrnefniInline
    ]
    readonly_fields = ['file_tag']
    list_display = ('to_str', 'sysla', 'hreppur')
    search_fields = ['slod', 'sysla', 'hreppur', 'ocr_text']
    list_filter = (
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
    list_display = ('ornefni')
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


class OrnefnaskrarEinstaklingarInline(admin.TabularInline):
    list_display = ('einstaklingur')
    raw_id_fields = ['einstaklingur']
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
    list_display = ('einstaklingur')
    raw_id_fields = ['einstaklingur']
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
        OCROrnefniInline
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


class OrnefniAdmin(admin.ModelAdmin):
    pass


class OCROrnefniAdmin(admin.ModelAdmin):
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
    raw_id_fields = ['pdf_skra_id']
    search_fields = ['ornefni']
    actions = [merkja_rett]


class BaejatalBaeirAdmin(admin.ModelAdmin):
    list_display = ['id', 'baejarnafn', 'nuv_sveitarf', 'gamalt_sveitarf', 'sysla', 'lbs_lykill']
    list_filter = ['sysla', 'nuv_sveitarf', 'gamalt_sveitarf']
    search_fields = ['baejarnafn', 'sysla__nafn', 'nuv_sveitarf__nafn', 'gamalt_sveitarf__nafn']
    inlines = [
        EinstaklingarStadirInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(BaejatalBaeirAdmin, self).get_form(request, obj, **kwargs)
        widget = form.base_fields['nuv_sveitarf'].widget
        widget.can_add_related = False
        widget.can_change_related = True
        widget.can_delete_related = False
        widget = form.base_fields['gamalt_sveitarf'].widget
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
    list_editable = ['nafn', 'nafn', 'aukanafn', 'faedingarstadur', 'faedingarar', 'danarar']
    search_fields = ['nafn']
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
    inlines = [
        BaejatalBaeirInline
    ]


class BaejatalSveitarfelogNyAdmin(admin.ModelAdmin):
    model = BaejatalSveitarfelogNy
    inlines = [
        BaejatalBaeirInline
    ]


class BaejatalSyslurAdmin(admin.ModelAdmin):
    inlines = [
        BaejatalSveitarfelogGomulSyslurInline,
        BaejatalSveitarfelogNySyslurInline
    ]


admin.site.disable_action('delete_selected')
admin.site.view_on_site = False
admin.site.register(Ornefnaskrar, OrnefnaskrarAdmin)
admin.site.register(Ornefni, OrnefniAdmin)
admin.site.register(Tegundir, TegundirAdmin)
admin.site.register(Stada, StadaAdmin)
admin.site.register(PdfSkrarFinnur, PdfSkrarFinnurAdmin)
admin.site.register(Einstaklingar, EinstaklingarAdmin)
admin.site.register(OCROrnefni, OCROrnefniAdmin)

admin.site.register(BaejatalBaeir, BaejatalBaeirAdmin)
admin.site.register(BaejatalSveitarfelogGomul, BaejatalSveitarfelogGomulAdmin)
admin.site.register(BaejatalSveitarfelogNy, BaejatalSveitarfelogNyAdmin)
admin.site.register(BaejatalSyslur, BaejatalSyslurAdmin)
