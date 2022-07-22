from typing import Union

from django.shortcuts import render
from django.views.generic import TemplateView

from src import geo_apis, wgbt


class BuffView(TemplateView):
    template_name = "app/buff.html"


class IndexView(TemplateView):
    template_name = "app/index.html"

class WFView(TemplateView):
    template_name = "app/WF.html"

class MapView(TemplateView):
    template_name = "app/Map.html"

    def basyodetail(request):
        lat: float = request.POST.get("lat")
        lon: float = request.POST.get("lng")

        wgbt_list, time_list = wgbt.location2wgbt(ido=lat, keido=lon)

        wgbt_now = wgbt_list[0]
        wgbt_status_now = wgbt.wgbt_indicator(WBGT=wgbt_now)

        wgbt_max = max(wgbt_list)
        wgbt_status_max = wgbt.wgbt_indicator(WBGT=wgbt_max)
        max_time = time_list[wgbt_list.index(wgbt_max)]

        wgbt_and_status: list[dict[str, Union[str, float]]] = []

        for WGBT, time in zip(wgbt_list, time_list):
            status = wgbt.wgbt_indicator(WBGT=WGBT)

            wgbt_and_status.append({"WGBT": WGBT, "status": status, "time": time[6:]})

        # 周辺地域の取得
        tikaku = geo_apis.find_near(ido=lat, keido=lon)






        return render(
            request,
            "app/detail.html",
            {
                "lat": lat,
                "lon": lon,
                "wgbt_now": wgbt_now,
                "wgbt_max": wgbt_max,
                "wgbt_status_now": wgbt_status_now,
                "wgbt_status_max": wgbt_status_max,
                "wgbt_and_status": wgbt_and_status,
                "tikaku": tikaku,
                "max_time": max_time,
            },
        )
