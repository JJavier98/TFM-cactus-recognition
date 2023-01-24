import mpmath as mp
from mpmath import *

mp.dps = 7

def gds2gd(gds_str):
    gds_str = gds_str.replace(',', '.')
    lat, long = gds_str.split(' ')

    res = []
    for axis in [lat, long]:
        grad, aux = axis.split('°')
        minutes, seconds = aux.split('\'')
        seconds = seconds[:-1]
        direction = grad[0]
        grad = grad[1:]

        res.append( mpf(mpf(grad) + mpf(minutes)/mpf(60.0) + mpf(seconds)/mpf(3600.0)) * (-1 if direction in ['W', 'S'] else 1) )

    return res

def gds2seconds(gds_str):
    gds_str = gds_str.replace(',', '.')
    lat, long = gds_str.split(' ')

    res = []
    for axis in [lat, long]:
        grad, aux = axis.split('°')
        minutes, seconds = aux.split('\'')
        seconds = seconds[:-1]
        direction = grad[0]
        grad = grad[1:]

        res.append( mpf(mpf(grad)*mpf(3600.0) + mpf(minutes)*mpf(60.0) + mpf(seconds)) * (-1 if direction in ['W', 'S'] else 1) )

    return res

def seconds2gd(seconds):
    grad = mpf(seconds/3600.0)

    return grad


def calcXY(lat, long, img_col, img_row, x_bbox, y_bbox):
    y = mpf(mpf(lat) / mpf( mpf( (361-img_row+1) * 255) - y_bbox))
    x = mpf(mpf(long) / mpf( mpf( (img_col-1) * 255) + x_bbox))

    return x, y
    

def bbox2coords(img_col, img_row, bbox):
    # 32.277586, -111.241958
    # latitude --> ((361-img_row+1)*255 - bbox[1]) * y  = 32.277586
    # longitude --> ((img_col-1)*255+ bbox[0]) * x  = -111.241958

    x = mpf(0.0047457462529175615221490430168140918844478508326931)
    y = mpf(0.004081899667422658212744528979414496860063023181244)
    Y_BASE = mpf(116091.62442668579765836511796806007623672485351563)
    X_BASE = mpf(-400482.14096600384308977105263238627230748534202576)

    latitude = mpf( mpf((361-img_row+1)*255 - bbox[1]) * y) + Y_BASE
    longitude = mpf( mpf((img_col-1)*255 + bbox[0]) * x) + X_BASE

    return [latitude, longitude]
    

def locate_cacti(bbox_file):
    lines = None
    with open(bbox_file, 'r') as file:
        lines = file.readlines()

    img_col = None
    img_row = None
    for line in lines:
        line = line.replace('[', '')
        line = line.replace(']', '')
        line = line.split(',')

        # Es bbox
        if line[-1].isnumeric():
            bbox2coords(img_col, img_row, line[:-1])
        # Es nombre de la imagen
        else:
            #TODO: hacer algo.
            1+1

gd_coords = gds2seconds('''N32°16'30,4162" W111°14'40,2841"''')
# x, y = calcXY(gd_coords[0], gd_coords[1], 2, 271, 5.4155254, 146.20851)
b = bbox2coords(502, 348, [131.99788, 75.7881, 152.04413, 166.14687, 0.9478293])

'''
2-267
N32°16'30,4218" W111°14'40,2928"
116190.4218
-400480.2928
[134.43633, 21.226913, 154.18051, 73.921585, 0.9947561]

2-271
N32°16'25,7481" W111°14'40,9051"
116185.7481
-400480.9051
[5.4155254, 146.20851, 32.648422, 233.1885, 0.99556607]


32.275116499999996 - 32.27381936111111 = 0.001297138888886 LATITUD (VERTICAL)
146.20851 - 21.226913 = 124.981597 PÍXELES VERTICAL
-111.24452358333333 - (-111.24469591666667) = 0.00017233333333877 LONGITUD (HORIZONTAL)
134.43633 - 5.4155254 = 129.0208046 PÍXELES HORIZONTAL
'''
diff_lat = mpf(116190.4218)-mpf(116185.7481)
diff_long = mpf(-400480.2928)-mpf(-400480.9051)
diff_H = mpf((2-1)*255 + 134.43633)-mpf((2-1)*255 + 5.4155254)
diff_V = mpf((361-267+1)*255 - 21.226913)-mpf((361-271+1)*255 - 146.20851)

lat_x_pix = mpf(diff_lat / diff_V)
long_x_pix = mpf(diff_long / diff_H)

print(gd_coords[0])
print(round(b[0], 4))
print('')
print(gd_coords[1])
print(round(b[1], 4))
print('')
print(round(seconds2gd(gd_coords[0]), 6))
print(round(seconds2gd(b[0]), 6))
print('')
print(round(seconds2gd(gd_coords[1]), 6))
print(round(seconds2gd(b[1]), 6))
print('')
print('')
# print(f'Diferencia latitud: {diff_lat}') # vertical
# print(f'Diferencia longitud: {diff_long}') # horizontal
# print(f'Diferencia píxeles H: {diff_H}') # horizontal
# print(f'Diferencia píxeles V: {diff_V}') # vertical
print(f'latitud/pixels: {lat_x_pix}')
print(f'longitud/pixels: {long_x_pix}')
print('')
print('')

print('Calcular Bases:')
print(
    mpf(116185.7481) -
    mpf(94.123673314199412250167130367397745440617981156744)
)
print(
    mpf(-400480.9051) -
    mpf(1.2358660038686079244136762801924266938890787075979)
)