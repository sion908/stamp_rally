from PIL import Image

def get_img_size(image_path) -> list[int]:
    # 画像を開く
    with Image.open(image_path) as image:
        # 画像の縦幅と横幅を取得
        width, height = image.size

    return [height, width]


if __name__=="__main__":
    # 画像ファイルのパス
    image_path = "haruRichMenu.jpeg"
    [height, width] = get_img_size(image_path)
    print(f"画像の縦幅: {height}px")
    print(f"画像の横幅: {width}px")
