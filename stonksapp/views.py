from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import requests
import time
from peterlynchscreener.screener import Screener
from django.template import loader


def index(request):
    pl_ticks = []
    context = {}
    if 'stonk_list' in request.POST:
        stonk_list = request.POST['stonk_list']
        stonk_list_clean = stonk_list.replace(' ', '')
        ticks = stonk_list_clean.split(",")
        print("stonk_list:", ticks)

        filters = request.POST.getlist('filters')
        print("filters:", filters)

        results = pd.DataFrame(columns=["ticker", "pe_to_industry", "de_to_industry"])

        for tick in ticks:
            time.sleep(0.4)
            print("Screening:", tick)
            s = Screener(tick)
            tick = s.get_all()
            print(results.append(tick, ignore_index=True))

        print(results)
        context = {"results": results, "stonk_list": stonk_list}
    template = loader.get_template('stonksapp/index.html')
    return HttpResponse(template.render(context, request))
