from dotenv import load_dotenv
import os

# config.txtファイルを読み込む
load_dotenv('.env')

# 環境変数にアクセスする
basic_user = os.getenv('BASIC_USER')
basic_password = os.getenv('BASIC_PASSWORD')
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN')
line_access_secret = os.getenv('LINE_ACCESS_SECRET')
debug = os.getenv('DEBUG')
stage_name = os.getenv('STAGE_NAME')
sr_line_handler_name = os.getenv('SRLinehandlerName')
liff_id = os.getenv('LIFF_ID')

if __name__=="__main__":
    # 環境変数の値を使う
    print(f"Basic User: {basic_user}")
    print(f"Basic Password: {basic_password}")
    print(f"Channel Access Token: {channel_access_token}")
    print(f"LINE Access Secret: {line_access_secret}")
    print(f"Debug: {debug}")
    print(f"Stage Name: {stage_name}")
