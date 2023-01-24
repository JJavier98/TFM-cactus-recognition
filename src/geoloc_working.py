import mpmath as mp
from mpmath import *
from datetime import datetime
from tqdm import tqdm

'''
COMPARAR HORIZONTAL
----------------------------------------------------------------
1-266
N32°16'31,5328" W111°14'41,8741"
116191.5328
-400481.8741
[60.798454, 3.9425006, 75.263535, 43.097435, 0.9138366]

502-348
N32°15'05,8846" W111°04'24,7285"
116105.8846
-399864.7285
[131.99788, 75.7881, 152.04413, 166.14687, 0.9478293]
'''

'''
COMPARAR VERTICAL
----------------------------------------------------------------
282-15
N32°20'52,4785" W111°08'56,0551"
116452.4938
-400136.0763
[32.996437, 52.679462, 75.1385, 136.32942, 0.99505556]

176-361
[176.22865, 148.17567, 225.08351, 255.0, 0.99595684]

23-269
[71.90346, 131.91516, 86.0126, 166.63191, 0.991043]
'''

'''
COMPROBAR
----------------------------------------------------------------
2-271
N32°16'25,7481" W111°14'40,9038"
116185.7481
-400480.9038
[134.43633, 21.226913, 154.18051, 73.921585, 0.9947561]

251-179
N32°16'25,7481" W111°14'40,9038"


[222.95345, 53.061817, 246.126, 109.18781, 0.9870155]
'''

mp.dps = 50
TXT_TODAY = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

def is_number(s):
    """ Returns True if string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False


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

    return float(round(grad, 6))


def seconds2gds(seconds, latitud=True):
    negative_direction = False
    seconds = float(seconds)
    if seconds < 0:
        negative_direction = True
        seconds = -seconds

    grad = seconds//3600
    seconds = seconds - grad*3600
    minutes = seconds//60
    seconds = seconds - minutes*60

    direction = 'N'
    if latitud and negative_direction:
        direction = 'S'
    elif not latitud:
        direction = 'E'
        if negative_direction:
            direction = 'W'

    coord = direction + str(grad)+'°' + str(minutes)+"'" + str(seconds)+'\"'

    return coord
    

def bbox2coords(img_col, img_row, bbox):
    x = mpf(0.0048280055479335542284458071549124724697321653366089)
    y = mpf(0.0040809382961309497231394693983475008280947804450989)
    
    Y_BASE = mpf(116091.62442668579765836511796806007623672485351563)
    X_BASE = mpf(-400482.14096600384308977105263238627230748534202576)

    latitude = mpf( mpf((361-img_row+1)*255 - bbox[1]) * y) + Y_BASE
    longitude = mpf( mpf((img_col-1)*255 + bbox[0]) * x) + X_BASE

    return [latitude, longitude]


def locate_cacti(bboxes_file):
    lines = None
    with open(bboxes_file, 'r') as file:
        lines = file.readlines()

    with open('src/results/coords/coords_'+TXT_TODAY+'.txt', 'a', encoding='utf-8') as file:
        for line in tqdm(lines):
            line = line.replace('[', '')
            line = line.replace(']', '')
            line = line.replace('\'', '')
            line = line.split(' ')

            # Es nombre de la imagen
            if not is_number(line[-1]):
                col, row = line[-1].split('-')
                col = col.split('_')[1]
                col = int(col)

                row = row.split('.')[0]
                row = int(row)

                file.writelines(line[-1])

            # Es bbox
            else:
                bbox = [float(x) for x in line]
                coords = bbox2coords(col, row, bbox)
                gds_coords = [
                    seconds2gds(coords[0]),
                    seconds2gds(coords[1], latitud = False)
                ]
                gd_coords = [
                    seconds2gd(coords[0]),
                    seconds2gd(coords[1])
                ]
                file.writelines(str(gds_coords))
                file.writelines('\n')
                file.writelines(str(gd_coords))
                file.writelines('\n')

if __name__ == '__main__':
    locate_cacti('src/results/bboxes/bbox_20-01-2023_20-11-42.txt')

########################################################################
########################################################################
########################################################################
"""
gd_coords = gds2seconds('''N32°14'52,0429" W111°11'05,8663"''')
b = bbox2coords(23, 269, [71.90346, 131.91516, 86.0126, 166.63191, 0.991043])
diff_lat = abs(
    116452.4938 -
    116092.0429
)
diff_long = abs(
    -399864.7285 -
    -400481.8741
)
diff_H = abs(
    ((502-1)*255 + 131.99788) -
    ((1-1)*255 + 60.798454)
)
diff_V = abs(
    ((15-1)*255 + 52.679462) -
    ((361-1)*255 + 148.17567)
)

lat_x_pix = mpf(diff_lat / diff_V)
long_x_pix = mpf(diff_long / diff_H)

print('')
print('')
print('Calcular Coordenadas:')
print(f'\t » Original en segundos: {gd_coords[0]} {gd_coords[1]}')
print(f'\t » Calculado en segundos: {round(b[0], 4)} {round(b[1], 4)}')
print('')
print(f'\t » Original en grados: {round(seconds2gd(gd_coords[0]), 6)} {round(seconds2gd(gd_coords[1]), 6)}')
print(f'\t » Calculado en grados: {round(seconds2gd(b[0]), 6)} {round(seconds2gd(b[1]), 6)}')
print('')
print(f'\t » Original en Str: {seconds2gds(gd_coords[0])} {seconds2gds(gd_coords[1], latitud=False)}')
print(f'\t » Calculado en Str: {seconds2gds(b[0])} {seconds2gds(b[1], latitud=False)}')
print('')
print('')
print('Calcular Coeficientes:')
print(f'\t » Diferencia latitud: {diff_lat}') # vertical
print(f'\t » Diferencia longitud: {diff_long}') # horizontal
print(f'\t » Diferencia píxeles H: {diff_H}') # horizontal
print(f'\t » Diferencia píxeles V: {diff_V}') # vertical
print(f'\t » latitud/pixels: {lat_x_pix}')
print(f'\t » longitud/pixels: {long_x_pix}')
print('')
print('')

print('Calcular Bases:')
print(f'\t » Original en grados: {mpf(116185.7481)-mpf(94.123673314199412250167130367397745440617981156744)}')
print(f'\t » Original en grados: {mpf(-400480.9051)-mpf(1.2358660038686079244136762801924266938890787075979)}')
"""
########################################################################
########################################################################
########################################################################