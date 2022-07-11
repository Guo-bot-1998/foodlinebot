from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackEvent,
    PostbackTemplateAction
)

from .scraper import IFoodie

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  
        
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        
        for event in events:
            if isinstance(event, MessageEvent):
 
                if event.message.text == "找餐廳":
 
                    line_bot_api.reply_message(  # 回復「選擇地區」按鈕樣板訊息
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='Menu',
                                text='請選擇地區',
                                actions=[
                                    PostbackTemplateAction(
                                        label='台北市',
                                        text='台北市',
                                        data='A&台北市'
                                    ),
                                    PostbackTemplateAction(
                                        label='新竹市',
                                        text='新竹市',
                                        data='A&新竹市'
                                    ),
                                    PostbackTemplateAction(
                                        label='台中市',
                                        text='台中市',
                                        data='A&台中市'
                                    ),
                                    PostbackTemplateAction(
                                        label='高雄市',
                                        text='高雄市',
                                        data='A&高雄市'
                                    )
                                ]
                            )
                        )
                    )
    
            elif isinstance(event, PostbackEvent):  # 如果有回傳值事件

                if event.postback.data[0:1] == "A":  # 選擇地區

                    area = event.postback.data[2:]

                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='Menu',
                                text='請選擇美食類別',
                                actions=[
                                    PostbackTemplateAction(
                                        label='火鍋',
                                        text='火鍋',
                                        data='B&' + area + '&火鍋'
                                    ),
                                    PostbackTemplateAction(
                                        label='早午餐',
                                        text='早午餐',
                                        data='B&' + area + '&早午餐'
                                    ),
                                    PostbackTemplateAction(
                                        label='約會餐廳',
                                        text='約會餐廳',
                                        data='B&' + area + '&約會餐廳'
                                    )
                                ]
                            )
                        )
                    )
                    
                    
 
                elif event.postback.data[0:1] == "B": #選擇地區+美食類別
                    
                    area, type = event.postback.data[2:].split('&')
                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='Menu',
                                text='請選擇價格區間',
                                actions=[
                                    PostbackTemplateAction(
                                        text='窮人',
                                        label='150以內',
                                        data='C&' + area + '&' + type + '&1'
                                    ),
                                    PostbackTemplateAction(
                                        text='普通人',
                                        label='150~600',
                                        data='C&' + area + '&' + type + '&2'
                                    ),
                                    PostbackTemplateAction(
                                        text='體面人',
                                        label='600~1200',
                                        data='C&' + area + '&' + type + '&3'
                                    ),
                                    PostbackTemplateAction(
                                        text='好野人',
                                        label='1200以上',
                                        data='C&' + area + '&' + type + '&4'
                                    )
                                ]
                            )
                        )
                    )
 
 
                elif event.postback.data[0:1] == "C": #選擇地區+美食類別+價格
 
                    result = event.postback.data[2:].split('&')
                    food = IFoodie(
                        result[0],  # 地區
                        result[1],  # 美食類別
                        result[2], # 價格區間
                    )
                
                    line_bot_api.reply_message(  # 回復訊息文字
                        event.reply_token,
                        TextSendMessage(text=food.scrape())
                    )
                    
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()