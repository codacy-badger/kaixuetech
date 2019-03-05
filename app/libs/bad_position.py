# -*- coding: utf-8 -*-
# @Time    : 2019/3/4 22:53
# @Author  : 昨夜
# @Email   : 903165495@qq.com

from math import cos, sin, atan2, sqrt, pi, radians, degrees
def center_geolocation(geolocations):
    x = 0
    y = 0
    z = 0
    lenth = len(geolocations)
    for lon, lat in geolocations:
        lon = radians(float(lon))
        lat = radians(float(lat))
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)

    x = float(x / lenth)
    y = float(y / lenth)
    z = float(z / lenth)

    return (degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y))))


if __name__ == '__main__':

    data=[
        "120.357,30.321532",
        "120.356982,30.321524",
        "120.356968,30.321544",
        "120.356968,30.321509",
        # "120.357004,30.321505",
        # "120.356977,30.321544",
        # "120.356968,30.321517",
        # "120.356964,30.321517",
        # "120.356968,30.321524",
        # "120.356946,30.321517",
        # "120.356986,30.321505",

        # "120.357098,30.321552",
        # "120.356896,30.321552",
        # "120.356065,30.321466",
        # "120.359623,30.319927",
        # "120.36221,30.312269"
    ]
    locations=[datas.split(",")for datas in data]
    # print (center_geolocation(locations))

    center=center_geolocation(locations)
    print(center)


