from .models import *
from nafnid_django_admin.models import *
from django.db.models import F
from rest_framework import serializers
from rest_framework_recaptcha.fields import *


class SyslaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaejatalSyslur
        fields = ('id', 'nafn')


class SSyslaSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = BaejatalSyslur
        fields = ('id', 'nafn')

    def get_id(self, obj):
        return obj['syslan']


class SyslaGomulSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaejatalSyslur
        fields = ('id', 'nafn')


class SyslurSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaejatalSyslur
        fields = ('id', 'nafn')


class SveitarfelagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaejatalSveitarfelogNy
        fields = ('id', 'nafn')


class SveitarfelogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaejatalSveitarfelogNy
        fields = ('id', 'nafn')


class HreppurSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaejatalSveitarfelogGomul
        fields = ('id', 'nafn')


class HrepparSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaejatalSveitarfelogGomul
        fields = ('id', 'nafn')


class BaeirSveitarfelogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaejatalBaeirSveitarfelog
        fields = ('id', 'nafn')


class BaeirHrepparSerializer(serializers.ModelSerializer):
    '''    baeir = BaeirSerializer(many=True, read_only=True)
        ornefni = OrnefninSerializer(many=True, read_only=True)
        einstaklingar = serializers.SerializerMethodField()
        tegund = TegundSerializer(many=True, read_only=True)
        stada = StadaSerializer(many=True, read_only=True)
        sveitarfelag = HreppurSerializer(many=False, read_only=True)
        sysla = SyslaSerializer(many=False, read_only=True)
        pdf = PDFSerializer(source='pdf_skra_id', many=False, read_only=True)

        def get_einstaklingar(self, obj):
            qset = OrnefnaskrarEinstaklingar.objects.filter(ornefnaskra=obj.id)
            return [HlutverkEinstaklingsSerializer(m).data for m in qset]
    '''
    class Meta:
        model = BaejatalBaeirHreppar
        fields = '__all__'


class BaerSerializer(serializers.ModelSerializer):
    hreppur = HreppurSerializer(many=False, read_only=True)
    sveitarfelag = SveitarfelagSerializer(many=False, read_only=True)
    sysla = SyslaSerializer(many=False, read_only=True)
    skrar = serializers.SerializerMethodField()
    ornefni = serializers.SerializerMethodField()

    class Meta:
        model = BaejatalBaeir
        fields = ('id', 'baejarnafn', 'sveitarfelag', 'hreppur', 'sysla', 'lat', 'lng', 'lbs_lykill', 'skrar', 'ornefni')

    def get_skrar(self, obj):
        #qset =
        return Ornefnaskrar.objects.filter(baeirornefnaskrar__baer__id=obj.id).values('titill','artal_skrar','id')
        #return [OrnefnaskrarSerializer(m).data for m in qset]
        #return Ornefnapakki.objects.filter(baer=obj.id).distinct('ornefnaskra').values(skra=F('ornefnaskra'), tegund_id=F('ornefnaskra__tegund__id'), tegund=F('ornefnaskra__tegund__tegund'), titill=F('ornefnaskra__titill'), artal=F('ornefnaskra__artal_skrar'))

    def get_ornefni(self, obj):
        return Ornefnapakki.objects.filter(baer=obj.id).values('ornefni', 'uuid')



class BaeirSerializer(serializers.ModelSerializer):
    hreppur = HreppurSerializer(many=False, read_only=True)
    sveitarfelag = SveitarfelagSerializer(many=False, read_only=True)
    sysla = SyslaSerializer(many=False, read_only=True)

    class Meta:
        model = BaejatalBaeir
        fields = ('id', 'baejarnafn', 'sveitarfelag', 'hreppur', 'sysla', 'lat', 'lng', 'lbs_lykill', 'fjoldi_skjala')


class BBaerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaejatalBaeir
        fields = ('id', 'baejarnafn', 'lat', 'lng', 'lbs_lykill', 'fjoldi_skjala')


class HreppurBaeirSerializer(serializers.ModelSerializer):
    hreppur = serializers.SerializerMethodField()
    baeir = serializers.SerializerMethodField()
    sysla = serializers.SerializerMethodField()

    class Meta:
        model = BaejatalSveitarfelogGomul
        fields = ('id', 'sysla', 'hreppur', 'baeir')

    def get_sysla(self, obj):
        qset = BaejatalSveitarfelogGomulSyslur.objects.filter(sveitarfelag_id=obj.id).select_related('sysla').values(syslan=F('sysla__id'), nafn=F('sysla__nafn'))
        return [SSyslaSerializer(m).data for m in qset]

    def get_hreppur(self, obj):
        qset = BaejatalSveitarfelogGomul.objects.filter(id=obj.id)
        return [HreppurSerializer(m).data for m in qset]

    def get_baeir(self, obj):
        qset = BaejatalBaeir.objects.filter(hreppur_id=obj.id).order_by('baejarnafn')
        return [BBaerSerializer(m).data for m in qset]


class SveitarfelogBaeirSerializer(serializers.ModelSerializer):
    sveitarfelag = serializers.SerializerMethodField()
    baeir = serializers.SerializerMethodField()

    class Meta:
        model = BaejatalSveitarfelogNy
        fields = ('sveitarfelag', 'baeir')

    def get_sveitarfelag(self, obj):
        qset = BaejatalSveitarfelogNy.objects.filter(id=obj.id)
        return [SveitarfelagSerializer(m).data for m in qset]

    def get_baeir(self, obj):
        qset = BaejatalBaeir.objects.filter(sveitarfelag_id=obj.id).order_by('baejarnafn')
        return [BBaerSerializer(m).data for m in qset]


class HlutverkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hlutverk
        fields = '__all__'


class SyslaHrepparSerializer(serializers.ModelSerializer):
    hreppar = serializers.SerializerMethodField()

    class Meta:
        model = BaejatalSyslur
        fields = ('id', 'nafn', 'hreppar')

    def get_hreppar(self, obj):
        return BaejatalSveitarfelogGomulSyslur.objects.filter(sysla=obj.id).select_related('sveitarfelag').values(hreppur=F('sveitarfelag__id'), nafn=F('sveitarfelag__nafn')).order_by('sveitarfelag__nafn')


class OrnefnaskrarBaeirSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrnefnaskrarBaeir
        fields = ('id', 'ornefnaskra', 'baer', 'skra')


class EinstaklingarBaeirSerializer(serializers.ModelSerializer):
    baer = BBaerSerializer()

    class Meta:
        model = EinstaklingarBaeir
        fields = ('id', 'einstaklingur', 'baer', 'tengsl', 'upphafsar', 'lokaar')


class EinstaklingarStadirSerializer(serializers.ModelSerializer):
    class Meta:
        model = EinstaklingarBaeir
        fields = ('id', 'tengsl', 'baer', 'upphafsar', 'lokaar')


class EinstaklingarSerializer(serializers.ModelSerializer):
    stadir = serializers.SerializerMethodField()

    class Meta:
        model = Einstaklingar
        fields = ('id', 'nafn', 'faedingarar', 'aukanafn', 'faedingarstadur', 'danarar', 'heimili','stadir')

    def get_stadir(self, obj):
        qset = EinstaklingarBaeir.objects.filter(einstaklingur=obj.id)
        return [EinstaklingarBaeirSerializer(m).data for m in qset]


class HlutverkEinstaklingsSerializer(serializers.ModelSerializer):
    einstaklingur = EinstaklingarSerializer()
    hlutverk = HlutverkSerializer()

    class Meta:
        model = OrnefnaskrarEinstaklingar
        fields = ('id', 'einstaklingur', 'hlutverk')


class SkrasetjariSerializer(serializers.ModelSerializer):

    class Meta:
        model = Einstaklingar
        fields = ('id', 'nafn')


class TegundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tegundir
        fields = ('id', 'tegund')


class StadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stada
        fields = ('id', 'stada')


class OrnefninSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ornefni
        fields = ('id', 'ornefni', 'uuid', 'lat', 'lon', 'ornefnaskra', 'okay')

class OrnefnaskrarSimpleSerializer(serializers.ModelSerializer):
    baeir = BaeirSerializer(many=True, read_only=True)
    tegund = TegundSerializer(many=True, read_only=True)
    stada = StadaSerializer(many=True, read_only=True)
    hreppur = HreppurSerializer(many=False, read_only=True)
    sveitarfelag = SveitarfelagSerializer(many=False, read_only=True)
    sysla = SyslaSerializer(many=False, read_only=True)

    class Meta:
        model = Ornefnaskrar
        fields = ('id',  'lmi', 'fjoldi_ornefna', 'texti', 'stafraent', 'pappir', 'titill', 'hreppur', 'sveitarfelag', 'sysla', 'tegund', 'stada', 'baeir')

    def get_einstaklingar(self, obj):
        qset = OrnefnaskrarEinstaklingar.objects.filter(ornefnaskra=obj.id)
        return [HlutverkEinstaklingsSerializer(m).data for m in qset]

class OrnefninSingleSerializer(serializers.ModelSerializer):
    ornefnaskrar = OrnefnaskrarSimpleSerializer(many=True)

    class Meta:
        model = Ornefni
        fields = ('id', 'ornefni', 'uuid', 'lat', 'lon', 'ornefnaskrar', 'okay')



class OrnefniSerializer(serializers.ModelSerializer):
    ornefni = OrnefninSerializer(source='ornefni', many=False)

    class Meta:
        model = OrnefnaskrarOrnefni
        fields = ('id', 'ornefni', 'uuid', 'skra')


class Syslulisti(serializers.ModelSerializer):
    class Meta:
        model = BaejatalSyslur
        fields = '__all__'


class Sysla(serializers.ModelSerializer):
    class Meta:
        model = BaejatalSyslur
        fields = '__all__'


class Sveitarfelagalisti(serializers.ModelSerializer):
    class Meta:
        model = BaejatalSyslur
        fields = '__all__'


class Sveitarfelag(serializers.ModelSerializer):
    class Meta:
        model = BaejatalSyslur
        fields = '__all__'


class Hreppalisti(serializers.ModelSerializer):
    class Meta:
        model = BaejatalSyslur
        fields = '__all__'


class Hreppur(serializers.ModelSerializer):
    class Meta:
        model = BaejatalSyslur
        fields = '__all__'


class Baejalisti(serializers.ModelSerializer):
    class Meta:
        model = BaejatalSyslur
        fields = '__all__'


class Baer(serializers.ModelSerializer):
    class Meta:
        model = BaejatalSyslur
        fields = '__all__'


class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = PdfSkrarFinnur
        fields = ('id', 'pdf_url')


class ArtalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PdfSkrarFinnur
        fields = ('artal_skrar',)


class OrnefnaskrarSerializer(serializers.ModelSerializer):
    baeir = BaeirSerializer(many=True, read_only=True)
    ornefni = OrnefninSerializer(many=True, read_only=True)
    einstaklingar = serializers.SerializerMethodField()
    tegund = TegundSerializer(many=True, read_only=True)
    stada = StadaSerializer(many=True, read_only=True)
    hreppur = HreppurSerializer(many=False, read_only=True)
    sveitarfelag = SveitarfelagSerializer(many=False, read_only=True)
    sysla = SyslaSerializer(many=False, read_only=True)
    pdf = PDFSerializer(source='pdf_skra_id', many=False, read_only=True)
    artal = ArtalSerializer(source='pdf_skra_id', many=False, read_only=True)

    class Meta:
        model = Ornefnaskrar
        fields = ('id',  'lmi', 'fjoldi_ornefna', 'texti', 'stafraent', 'pappir', 'titill', 'hreppur', 'sveitarfelag', 'sysla', 'pdf', 'pdf_skra_id', 'tegund', 'stada', 'ornefni', 'baeir', 'einstaklingar','artal',)

    def get_einstaklingar(self, obj):
        qset = OrnefnaskrarEinstaklingar.objects.filter(ornefnaskra=obj.id)
        return [HlutverkEinstaklingsSerializer(m).data for m in qset]


class OrnefnaskrarMinniSerializer(serializers.ModelSerializer):
    baeir = BaeirSerializer(many=True, read_only=True)
    hreppur = HreppurSerializer(many=False, read_only=True)
    sveitarfelag = SveitarfelagSerializer(many=False, read_only=True)
    sysla = SyslaSerializer(many=False, read_only=True)
    tegund = TegundSerializer(many=True, read_only=True)
    stada = StadaSerializer(many=True, read_only=True)
    artal = ArtalSerializer(source='pdf_skra_id', many=False, read_only=True)
    skrasetjari = serializers.SerializerMethodField()
    teg = serializers.SerializerMethodField()

    class Meta:
        model = Ornefnaskrar
        #fields = '__all__'
        fields = ('id', 'titill', 'sveitarfelag', 'hreppur', 'sysla', 'tegund', 'teg', 'stada', 'baeir', 'artal', 'skrasetjari')

    def get_skrasetjari(self, obj):
        qset = OrnefnaskrarEinstaklingar.objects.filter(ornefnaskra=obj.id, hlutverk=1)
        m = qset.first()
        if m:
            return SkrasetjariSerializer(m.einstaklingur).data
        else:
            return False

    def get_teg(self, obj):
        qset = OrnefnaskrarTegundir.objects.filter(skra=obj.id)
        m = qset.first()
        if m:
            return TegundSerializer(m.tegund).data
        else:
            return False


class OrnefnaskrarMinnstSerializer(serializers.ModelSerializer):
    tegund = TegundSerializer(many=True, read_only=True)
    stada = StadaSerializer(many=True, read_only=True)

    class Meta:
        model = Ornefnaskrar
        #fields = '__all__'
        fields = ('id', 'titill', 'tegund', 'stada')


class TextaleitSerializer(serializers.ModelSerializer):
    pass


class EinstaklingarOrnefnaskrarSerializer(serializers.ModelSerializer):
    hlutverk = HlutverkSerializer()
    ornefnaskra = OrnefnaskrarMinnstSerializer()

    class Meta:
        model = EinstaklingarOrnefnaskrar
        fields = ('hlutverk', 'ornefnaskra')


class EinstaklingurSerializer(serializers.ModelSerializer):
    stadir = serializers.SerializerMethodField()
    #ornefnaskrar = serializers.SerializerMethodField()

    class Meta:
        model = Einstaklingar
        fields = ('id', 'nafn', 'faedingarar', 'aukanafn', 'faedingarstadur', 'danarar', 'heimili', 'stadir')#, 'ornefnaskrar')

    def get_stadir(self, obj):
        qset = EinstaklingarBaeir.objects.filter(einstaklingur=obj.id)
        return [EinstaklingarStadirSerializer(m).data for m in qset]

    def get_ornefnaskrar(self, obj):
        qset = OrnefnaskrarEinstaklingar.objects.filter(einstaklingur=obj.id)
        return [EinstaklingarOrnefnaskrarSerializer(m).data for m in qset]


class OrnefnaskrarEinstaklingsSerializer(serializers.ModelSerializer):
    ornefnaskra = serializers.SerializerMethodField()
    hlutverk = HlutverkSerializer()

    class Meta:
        model = EinstaklingarOrnefnaskrar
        fields = ('ornefnaskra', 'hlutverk')

    def get_ornefnaskra(self, obj):
        return Ornefnaskrar.objects.filter(id=obj.ornefnaskra_id).values('id', 'titill')



class Teg(serializers.RelatedField):
    def to_representation(self, value):
        return value.tegund_id



''' =========================== LEIT =========================== '''


class OrnefnaleitSerializer(serializers.ModelSerializer):
    ornefnaskra = OrnefnaskrarMinniSerializer(many=False, read_only=True)
    baer = BBaerSerializer(many=False, read_only=True)
    hreppur = HreppurSerializer(many=False, read_only=True)
    sveitarfelag = SveitarfelagSerializer(many=False, read_only=True)
    sysla = SyslaSerializer(many=False, read_only=True)

    class Meta:
        model = Ornefnapakki
        fields = ('id', 'ornefni', 'uuid', 'ornefnaskra', 'baer', 'hreppur', 'sveitarfelag', 'sysla', 'artal_skrar',)


class Uuid(serializers.ModelSerializer):
    class Meta:
        model = Ornefnapakki
        fields = ('id', 'ornefni', 'uuid', 'ornefnaskra')


class SiaOrnefnaleitTegundir(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Tegundir
        fields = ('id', 'tegund')

    def get_id(self, obj):
        return obj['tegund_id']


class SiaOrnefnaleitSyslur(serializers.ModelSerializer):
    sysla = SyslaSerializer(many=False, read_only=True)

    class Meta:
        model = Ornefnapakki
        fields = ('sysla',)


class SiaOrnefnaleitSveitarfelog(serializers.ModelSerializer):
    sveitarfelag = SveitarfelagSerializer(many=False, read_only=True)

    class Meta:
        model = Ornefnapakki
        fields = ('sveitarfelag',)


class SiaOrnefnaleitHreppar(serializers.ModelSerializer):
    hreppur = HrepparSerializer(many=False, read_only=True)

    class Meta:
        model = Ornefnapakki
        fields = ('hreppur',)


class BaejaleitSerializer(serializers.ModelSerializer):
    hreppur = HrepparSerializer(many=False, read_only=True)
    sveitarfelag = SveitarfelagSerializer(many=False, read_only=True)
    sysla = SyslaSerializer(many=False, read_only=True)

    class Meta:
        model = BaejatalBaeir
        fields = ('id', 'baejarnafn', 'sveitarfelag', 'hreppur', 'sysla', 'lat', 'lng', 'lbs_lykill')


class SiaBaejaleitSyslur(serializers.ModelSerializer):
    sysla = SyslaSerializer(many=False, read_only=True)

    class Meta:
        model = BaejatalBaeir
        fields = ('sysla',)


class SiaBaejaleitSveitarfelog(serializers.ModelSerializer):
    sveitarfelag = SveitarfelagSerializer(many=False, read_only=True)

    class Meta:
        model = BaejatalBaeir
        fields = ('sveitarfelag',)


class SiaBaejaleitHreppar(serializers.ModelSerializer):
    hreppur = HrepparSerializer(many=False, read_only=True)

    class Meta:
        model = BaejatalBaeir
        fields = ('hreppur',)


''' =========================== /LEIT =========================== '''

