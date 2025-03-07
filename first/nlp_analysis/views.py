from rest_framework.response import Response
from .morph import lib_morph
from rest_framework.views import APIView
from .serialziers import CheckedNLPAnlysMorphSerializer


class NLPAnlysMorph(APIView):
    def post(self, request):
        ser = CheckedNLPAnlysMorphSerializer(request.data)
        texts = ser.data['texts']
        res = lib_morph.kiwi_morph_anlysis(texts=texts)
        return Response(res)
