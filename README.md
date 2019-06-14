# mobile_app_detect_online

移动应用图片文字在线识别系统，实现移动应用的在线解压缩、在线获取资源文件、在线图片文字识别、在线色情、赌博等违规语句检测等功能
该作品为2018年**高校计算机大赛网络技术挑战赛技术攻关组一等奖作品**。
该部分为完整的web代码，包括门户前端与管理后台前端

- **后端采用Flask 框架，使用flask-SQLAchemy与数据库做交互，使用flask-session管理session，使用blueprint做url路由**

- **前端采用Vue框架，elementUI后台、vue-bootstrap门户**

- **图像识别算法采用CTPN+DenseNet+CTC**

- **文字甄别采用trie树进行一步过滤，采用LSTM实现二步过滤**



