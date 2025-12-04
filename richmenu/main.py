import sys

from linebot.v3.messaging import (
    MessageAction,
    URIAction,
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    RichMenuRequest,
    RichMenuSize
)

from config import channel_access_token as CHANNEL_ACCESS_TOKEN, liff_id
from img import get_img_size
from generateArea import generate_areas

configuration = Configuration(
    access_token=CHANNEL_ACCESS_TOKEN
)

def createRichmenu():
    result = False
    try:

        # define a new richmenu
        image_path = "regein-2024.jpeg"
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_blob_api = MessagingApiBlob(api_client)

            [img_height, img_width] = get_img_size(image_path)
            rich_menu_size = RichMenuSize(width=img_width, height=img_height)
            rich_menu_to_create = RichMenuRequest(
                size = rich_menu_size,
                selected = True,
                name = 'richmenu for randomchat',
                chat_bar_text = 'TAP HERE',
                areas = generate_areas(
                    rich_menu_size,
                    {
                        "areas": [
                            URIAction(
                                label="読み取り",
                                uri=f"https://liff.line.me/{liff_id}/"
                            ),
                            MessageAction(text="スコアを確認する")
                        ]
                    }
                )
            )
            rich_menu_id = line_bot_api.create_rich_menu(rich_menu_request=rich_menu_to_create).rich_menu_id

            with open(image_path, 'rb') as image:
                line_bot_blob_api.set_rich_menu_image(
                    rich_menu_id=rich_menu_id,
                    body=bytearray(image.read()),
                    _headers={'Content-Type': 'image/png'}
                )

            # set the default rich menu
            line_bot_api.set_default_rich_menu(rich_menu_id)

            result = True

    except Exception:
        result = False


    return result

if __name__=="__main__":
    args = sys.argv
    print(args)
    if 2 <= len(args):
        if args[1] == "list":
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                rich_menus = line_bot_api.get_rich_menu_list()
                for rich_menu in rich_menus.richmenus:
                    print(f" Rich Menu ID: {rich_menu.rich_menu_id}")
                    print(f"         Name: {rich_menu.name}")
                    print(f"         Size: {rich_menu.size.width}x{rich_menu.size.height}")
                    print(f"     Selected: {rich_menu.selected}")
                    print(f"Chat Bar Text: {rich_menu.chat_bar_text}")
                    print(f"        Areas: {str(rich_menu.areas)}")
                    print("---")

        elif args[1] == "del" and len(args)==3:
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.delete_rich_menu(args[2])
        elif args[1] == "create":
            createRichmenu()
            pass
    else:
        print(liff_id)
        print('Arguments are too short')
