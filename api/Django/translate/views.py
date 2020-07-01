from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic import View
from .machine_translate import MachineTranslation
import time
import json

counter = 0


# Create your views here.
class TranslationView(View):
    def post(self, request):
        # retrieve post params
        to_lang = request.POST.get('to_lang')
        input_text = request.POST.get('input_text')
        # print('post params: ', to_lang, input_text)

        try:
            start_time = time.time()
            output_text = MachineTranslation.translate_by_api(to_lang, input_text)
            print('time consume: {} ms'.format(round((time.time() - start_time)*1000, 3)))
            status = "ok"

            #### jmeter测试 ####
            # global counter
            # time.sleep(1)
            # output_text += str(counter)
            # print(output_text)
            # counter += 1
            ####

            data = [{"output_text": output_text}]
        except Exception as e:
            status = "failed to translate"
            data = []

        return HttpResponse(json.dumps({
            "status": status,
            "data": data,
        }))
