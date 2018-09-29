config = {
    'delayTime': 60,  # 查看房间状态的时间间隔,默认60秒
    'sender': '请填写发送方的邮箱帐号',
    'receiver': ['请填写接收方的邮箱帐号'],  # 数组
    # 斗鱼房间配置
    'douyu': {
        'roomApi': 'http://open.douyucdn.cn/api/RoomApi/room/',
        'roomId': [
            # 斗鱼房间号
            '60937',  # zard房间
            '9999',  # yyf房间
        ],
    },
    # 邮件发送器的配置
    'transporter': {
        'host': 'smtp.qq.com',  # smtp域名(163的smtp域名为 stmp.163.com)
        'port': 465,  # 端口
        'secure': True,  # true for 465, false for other ports
        'auth': {
            'user': '请填写发送方的邮箱帐号',  # 你的邮箱帐号
            'pass': '请填写你的邮箱授权码',  # 你的邮箱SMTP密码(授权码)
        },
    },
}
