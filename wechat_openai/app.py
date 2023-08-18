# encoding:utf-8
import io
import threading
import openai
from lib import itchat


def qrCallback(uuid, status, qrcode):
    if status == "0":
        try:
            from PIL import Image

            img = Image.open(io.BytesIO(qrcode))
            _thread = threading.Thread(target=img.show, args=("QRCode",))
            _thread.setDaemon(True)
            _thread.start()
        except Exception as e:
            pass
        import qrcode
        url = f"https://login.weixin.qq.com/l/{uuid}"
        qr_api1 = "https://api.isoyu.com/qr/?m=1&e=L&p=20&url={}".format(url)
        qr_api2 = "https://api.qrserver.com/v1/create-qr-code/?size=400×400&data={}".format(url)
        qr_api3 = "https://api.pwmqr.com/qrcode/create/?url={}".format(url)
        qr_api4 = "https://my.tv.sohu.com/user/a/wvideo/getQRCode.do?text={}".format(url)
        print("You can also scan QRCode in any website below:")
        print(qr_api3)
        print(qr_api4)
        print(qr_api2)
        print(qr_api1)
        qr = qrcode.QRCode(border=1)
        qr.add_data(url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)

openai.api_key = 'sk-xxxxxxxxxxxxxxxxxxE'

def get_chat_response(input_text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=f"gpt: {input_text}\nYou:",
            max_tokens=2500,
            temperature=0.7
        )
        chat_response = response.choices[0].text.strip()
        return chat_response
    except Exception as e:
        print("Error fetching chat response from OpenAI:", e)
    return "Sorry, I couldn't process your message at the moment."

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    user_text = msg.text
    chat_response = get_chat_response(user_text)
    return chat_response

if __name__ == "__main__":
    itchat.auto_login(hotReload=False, qrCallback=qrCallback)
    itchat.run()
