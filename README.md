# 📘 Smart Home Monitoring System - 运行流程手册
## 1. 项目简介（Project Overview）
该系统用于实时监测家庭环境中的温度、湿度、光照与距离等信息，使用 Raspberry Pi Pico 采集数据，通过 MQTT 协议发送至 Raspberry Pi 4 运行的 Flask 服务，进行显示与报警处理。

## 2. 系统环境要求（System Requirements）
🖥️ 硬件环境
Raspberry Pi 4（运行主服务）

Raspberry Pi Pico（运行 MicroPython 传感器脚本）

DHT11 传感器、超声波传感器、光敏传感器

蜂鸣器、按钮（可选）

💻 软件环境
操作系统：Raspberry Pi OS (Lite 或 Full)

Python：建议 3.8+

数据库：SQLite3

其他依赖：
见requirement.txt


## 3. 项目克隆与初始化（Clone & Setup）
# 克隆项目代码
git clone git@github.com:jackh725/smart-home-iot.git
cd smart-home-iot

# 创建虚拟环境（可选）
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

## 4. 环境变量配置（Environment Variables）
创建 .env 文件用于存放敏感信息：

touch .env

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

这个注意要把".env" 加入到gitignore里去，别上传了私人信息。


## 5. 启动流程（Run Instructions）
python app.py


echo ".env" >> .gitigonre
echo "*.db" >> .gitigonre



