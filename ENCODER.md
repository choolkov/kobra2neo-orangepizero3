# Установка и настройка ПО для использования энкодера Anycubic Kobra 2 Neo

Подключение энкодера выполняется к пинам согласно схеме из [**README.md**](https://github.com/choolkov/kobra2neo-orangepizero3/blob/main/README.md)

Если энкодер подключен к другим пинам, укажите их в файле **encoder.py**

## Установка wiringOP

Устанавливаем необходимое ПО

Клонируем репозиторий wiringOP и собираем приложение
```
cd
sudo apt install -y git make build-essential
git clone https://github.com/orangepi-xunlong/wiringOP.git
cd wiringOP
./build clean
./build
```

Проверяем
```
gpio readall
```

Должны увидеть таблицу вроде этой:
```
+------+-----+----------+--------+---+   H616   +---+--------+----------+-----+------+
| GPIO | wPi |   Name   |  Mode  | V | Physical | V |  Mode  | Name     | wPi | GPIO |
+------+-----+----------+--------+---+----++----+---+--------+----------+-----+------+
|      |     |     3.3V |        |   |  1 || 2  |   |        | 5V       |     |      |
|  229 |   0 |    SDA.3 |    OFF | 0 |  3 || 4  |   |        | 5V       |     |      |
|  228 |   1 |    SCL.3 |    OFF | 0 |  5 || 6  |   |        | GND      |     |      |
|   73 |   2 |      PC9 |   ALT6 | 1 |  7 || 8  | 1 | OUT    | TXD.5    | 3   | 226  |
|      |     |      GND |        |   |  9 || 10 | 1 | OUT    | RXD.5    | 4   | 227  |
|   70 |   5 |      PC6 |   ALT5 | 0 | 11 || 12 | 0 | OFF    | PC11     | 6   | 75   |
|   69 |   7 |      PC5 |   ALT5 | 0 | 13 || 14 |   |        | GND      |     |      |
|   72 |   8 |      PC8 |    OFF | 0 | 15 || 16 | 0 | OFF    | PC15     | 9   | 79   |
|      |     |     3.3V |        |   | 17 || 18 | 0 | OFF    | PC14     | 10  | 78   |
|  231 |  11 |   MOSI.1 |   ALT4 | 0 | 19 || 20 |   |        | GND      |     |      |
|  232 |  12 |   MISO.1 |   ALT4 | 0 | 21 || 22 | 0 | OFF    | PC7      | 13  | 71   |
|  230 |  14 |   SCLK.1 |   ALT4 | 0 | 23 || 24 | 0 | OUT    | CE.1     | 15  | 233  |
|      |     |      GND |        |   | 25 || 26 | 0 | OFF    | PC10     | 16  | 74   |
|   65 |  17 |      PC1 |    OFF | 0 | 27 || 28 | 0 | ALT2   | PWM3     | 21  | 224  |
|  272 |  18 |     PI16 |   ALT2 | 0 | 29 || 30 | 0 | ALT2   | PWM4     | 22  | 225  |
|  262 |  19 |      PI6 |    OFF | 0 | 31 || 32 |   |        |          |     |      |
|  234 |  20 |     PH10 |    OFF | 0 | 33 || 34 |   |        |          |     |      |
+------+-----+----------+--------+---+----++----+---+--------+----------+-----+------+
| GPIO | wPi |   Name   |  Mode  | V | Physical | V |  Mode  | Name     | wPi | GPIO |
+------+-----+----------+--------+---+   H616   +---+--------+----------+-----+------+
```
Номера пинов, используемые в файле **encoder.py**, берутся из столбца **wPi**

## Установка wiringOP-Python

Устанавливаем необходимые пакеты, клонируем репозиторий и запускаем установку
```
sudo apt install -y python3-setuptools python3-dev python3-venv python3-tk swig
git clone --recursive https://github.com/orangepi-xunlong/wiringOP-Python.git -b next
cd wiringOP-Python
python3 generate-bindings.py > bindings.i
sudo python3 setup.py install
```

## Установка виртуального окружения Python

Клонируем этот репозиторий и создаем виртуальное окружение для запуска скрипта
```
cd
git clone https://github.com/choolkov/kobra2neo-orangepizero3.git
cd kobra2neo-orangepizero3/
python3 -m venv --system-site-packages venv
source venv/bin/activate
pip install pyautogui python-xlib 
```

## Запуск службы/демона

Создаем файл **/etc/systemd/system/encoder.service** со следующим содержимым

Имя пользователя **USERNAME** нужно поменять на своё в трех местах
```
[Unit]
Description=EncoderSerivce
After=syslog.target
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/USERNAME/kobra2neo-orangepizero3
Environment="DISPLAY=:0"
ExecStart=/home/USERNAME/kobra2neo-orangepizero3/venv/bin/python /home/USERNAME/kobra2neo-orangepizero3/encoder.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Перезагружаем демоны, запускаем 
```
sudo systmctl daemon-reload
sudo systemctl enable encoder
sudo systemctl restart encoder
```
После внесения изменений в **encoder.py** эти команды следует повторить, чтобы изменения вступили в силу



## Настройка KlipperScreen

Для отображения курсора нужно добавить следующие строки в конфигурацию **KlipperScreen.conf**
```
[main]
show_cursor: True
```
## Выключение одноплатника с помощью энкодера
Чтобы выключить плату нужно зажать кнопу энкодера (без поворота) на 5 секунд
