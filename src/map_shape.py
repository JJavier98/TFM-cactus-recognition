import os

img_path = os.path.join('data', 'imgs', 'google_maps', 'gm_saguaro_z21')
imgs_list = os.listdir(img_path)

max_col = 0
min_col = 9999
max_col_img = None
min_col_img = None

max_row = 0
min_row = 9999
max_row_img = None
min_row_img = None
for img in imgs_list:
    col = img.split('-')[1]
    col = col.split('.')[0]
    col = int(col)

    row = img.split('-')[0]
    row = row.split('_')[1]
    row = int(row)

    if col > max_col:
        max_col = col
        max_col_img = img
    if col < min_col:
        min_col = col
        min_col_img = img

    if row > max_row:
        max_row = row
        max_row_img = img
    if row < min_row:
        min_row = row
        min_row_img = img

print(max_col_img)
print(min_col_img)
print(max_row_img)
print(min_row_img)
