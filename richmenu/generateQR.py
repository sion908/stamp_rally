import qrcode
from PIL import Image
from config import liff_id
id="ks"

datas = [
        [7,"新大工まちゼミ味見マルシェ"],
        [8,"お大師さまマルシェ"],
        [9,"まちぶらMemoマルシェ"],
]
for d in datas:
        text = f'https://liff.line.me/{liff_id}/?ver=hubspring&place_id={d[0]}'
        img = qrcode.make(text)
        img.save(f'qr/{d[1][0]}{d[1][1]}.png')

# https://liff.line.me/1657251421-rW78w9bW/employ/?ver=2023-f&shop_id=90845ebf-bf4a-4ebb-a39e-24a99c379e73
