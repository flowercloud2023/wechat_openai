import io
import threading
import openai
from lib import itchat
import multiprocessing

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

def chat_with_friend(friend_name):
    @itchat.msg_register(itchat.content.TEXT, isFriendChat=True, isGroupChat=False)
    def text_reply(msg):
        if msg["FromUserName"] == friend_name:
            user_text = msg.text
            chat_response = get_chat_response(user_text)
            itchat.send(chat_response, friend_name)

    itchat.run()

if __name__ == "__main__":
    itchat.auto_login(hotReload=False, qrCallback=qrCallback)
    
    # 获取好友列表
    friends = itchat.get_friends(update=True)
    
    # 启动一个进程来与每个好友聊天
    processes = []
    for friend in friends:
        if friend["UserName"] != itchat.search_friends()["UserName"]:
            friend_name = friend["UserName"]
            process = multiprocessing.Process(target=chat_with_friend, args=(friend_name,))
            process.start()
            processes.append(process)
    
    # 等待所有进程完成
    for process in processes:
        process.join()
