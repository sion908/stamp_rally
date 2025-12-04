from linebot.v3.messaging import (
    MessageAction,
    RichMenuArea,
    RichMenuSize,
    RichMenuBounds
)

def generate_areas(rich_menu_size: RichMenuSize, areas_def: dict):
    width = rich_menu_size.width
    height = rich_menu_size.height

    areas = []

    def process_areas(areas_def, x, y, width, height):
        print(areas_def, x, y, width, height)
        if isinstance(areas_def["areas"][0], dict):
            ratio = areas_def.get("raito", ("1:" * len(areas_def["areas"]))[:-1])
            sub_areas = areas_def.get("areas", [])

            heights = list(map(int, ratio.split(':')))
            total_height = sum(heights)
            for i, sub_area in enumerate(sub_areas):
                sub_height = height * heights[i] // total_height
                process_areas(sub_area, x, y, width, sub_height)
                y += sub_height
        else:
            raito_list = list(map(int, areas_def.get("raito", ("1:" * len(areas_def["areas"]))[:-1]).split(':')))
            total_width = sum(raito_list)
            print("prosess", areas_def, x, y, width, height, raito_list, total_width)
            for i, action in enumerate(areas_def["areas"]):
                # ratio = area_def.get("raito", "1")
                # action = area_def.get("action")
                sub_width = width // total_width * raito_list[i]
                if action:
                    area = RichMenuArea(
                        bounds=RichMenuBounds(
                            x= sub_width*sum(raito_list[:i]),
                            y= y,
                            width= sub_width,
                            height= height
                        ),
                        action=action
                    )
                    areas.append(area)

    process_areas(areas_def, 0, 0, width, height)

    return areas


if __name__=="__main__":
    rich_menu_size = RichMenuSize(width=1200, height=800)
    # areas_def = {
    #     "areas": [
    #         MessageAction(text="Button 1"),
    #         MessageAction(text="Button 2")
    #     ]
    # }
    areas_def = {
        # "raito": "1:2",
        "areas": [
            {
                "raito": "1:1",
                "areas": [
                    MessageAction(text="Button 1"),
                    MessageAction(text="Button 2")
                ]
            },
            {
                "raito": "1:2:1",
                "areas": [
                    MessageAction(text="Button 3"),
                    MessageAction(text="Button 4"),
                    MessageAction(text="Button 5")
                ]
            }
        ]
    }

    generated_areas = generate_areas(rich_menu_size, areas_def)

    for a in generated_areas:
        print(a)
