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
        "30.315191,120.350654",
        "30.315182,120.351571",
        "30.315071,120.350558",
        "30.314288,120.351754"
    ]
    # locations=[datas.split(",")for datas in data]
    # print (center_geolocation(locations))
    #
    # center=center_geolocation(locations)
    # print(center)
    from1=';'.join(data)
    print(from1)
    url='http://apis.map.qq.com/ws/distance/v1/matrix/?mode=walking&from={}&to={}&key=BXZBZ-CUHCV-TNPPC-UEGVK-MH66H-BIBZQ'.format(from1,from1)

    import requests
    print(requests.get(url).text)