"""LINE Messaging API v3 Echo Bot 範例。"""

import os

from dotenv import load_dotenv
from flask import Flask, abort, request
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# 本機開發時從 .env 載入機密；正式部署則由平台環境變數提供。
load_dotenv()

app = Flask(__name__)
# Secret 用來驗證 Webhook，Token 用來呼叫 Messaging API，兩者不可混用。
channel_secret = os.getenv("LINE_CHANNEL_SECRET")
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not channel_secret or not channel_access_token:
    raise RuntimeError("請先設定 LINE_CHANNEL_SECRET 與 LINE_CHANNEL_ACCESS_TOKEN")

# SDK 會使用 Access Token 對 LINE Messaging API 發出授權請求。
configuration = Configuration(access_token=channel_access_token)
# Handler 會以 Channel Secret 驗證 X-Line-Signature，避免偽造事件進入系統。
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    """接收 LINE Webhook，驗證簽章後交給事件處理器。"""
    # 必須保留未修改的原始 body，才能正確計算 HMAC-SHA256 簽章。
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    app.logger.info("收到 Webhook，body 長度：%d", len(body))

    try:
        # 驗證成功後，SDK 會將事件分派給下方註冊的處理器。
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 簽章不正確時拒絕請求，不讓未授權資料繼續執行。
        abort(400, description="Invalid LINE signature")

    return "OK", 200


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    """將使用者的文字內容原樣回覆。"""
    # reply_token 是 LINE 為本次事件提供的一次性回覆憑證。
    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)
        # 將原文字包裝成 TextMessage，再交由 Reply API 傳回使用者。
        reply = ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=event.message.text)],
        )
        messaging_api.reply_message_with_http_info(reply)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
