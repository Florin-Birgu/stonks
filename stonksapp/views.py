from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import requests
import time
from peterlynchscreener.screener import Screener
from django.template import loader


def index(request):
    pl_ticks = []
    if 'stonk_list' in request.POST:
        stonk_list = request.POST['stonk_list']
        stonk_list_clean = stonk_list.replace(' ', '')
        ticks = stonk_list_clean.split(",")
        print("stonk_list:", ticks)
        for tick in ticks:
            time.sleep(0.4)
            print("Screening:", tick)
            s = Screener(tick)
            if s.is_pe_to_industry_met():
                if s.is_de_to_industry_met():
                    pl_ticks.append(tick)

        print("pl_ticks:", pl_ticks)
        context = {"pl_ticks": pl_ticks, "stonk_list": stonk_list}
    template = loader.get_template('stonksapp/index.html')
    return HttpResponse(template.render(context, request))
