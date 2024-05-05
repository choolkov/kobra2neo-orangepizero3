# kobra2neo-orangepizero3
Подключение SPI дисплея Anycubic Kobra 2 Neo к Orange Pi Zero 3

Все нижеописанное выполнялось на образе системы [Armbian Bookworm](https://www.armbian.com/orange-pi-zero-3/) версия ядра [6.6.30](https://github.com/armbian/community/releases/download/24.5.0-trunk.532/Armbian_community_24.5.0-trunk.532_Orangepizero3_bookworm_current_6.6.30_minimal.img.xz)



## Подключение железа:
### Распиновка со стороны дисплея
![](https://github.com/choolkov/kobra2neo-orangepizero3/blob/main/kobra2neo_pinout.png?raw=true)
### Распиновка на плате Orange Pi Zero 3
![](https://github.com/choolkov/kobra2neo-orangepizero3/blob/main/opizero3_pinout.png?raw=true)

1) **5V** — **5V**
2) **GND** — **GND**
3) **SCK** — **PH6** (SPI1_CLK)
4) **RESET** — **PH2**
5) **MOSI** — **PH7** (SPI1_MOSI)
6) **DC** — **PH3**
7) **CS** — **PH9** (SPI1_CS)
### Подключение энкодера (опционально - для дальнейших доработок)
8) **ES** — **PC11**
9) **EOA** — **PC7**
10) **EOB** — **PC10**

## Настройка ПО
### Установка и настройка XORG
Устанавливаем драйвер
```
sudo apt install -y xserver-xorg-video-fbdev
```
Создаем файл **/usr/share/X11/xorg.conf.d/50-fbdev.conf** со следующем содержимым:
```
Section "Device"
        Identifier      "Allwinner FBDEV"
        Driver          "fbdev"
        Option          "fbdev" "/dev/fb0"

        Option          "SwapbuffersWait" "true"
EndSection
```

### Добавляем оверлей
Так как в системе уже есть драйвер **fb_st7789v**, который нам подойдет, нужно прописать какие ноги куда подключены и добавить команды инициализации дисплея

Создаем файл **opizero3-kobra2neo.dts** со следующим содержимым:
```
/dts-v1/;
/plugin/;
  
/ {
compatible = "allwinner,sun50i-h6";
fragment@0 {
target = <&spi1>;
__overlay__ {
num-cs = <1>;
cs-gpios = <&pio 7 9 0>;
status = "okay";
#address-cells = <1>;
#size-cells = <0>;
  
spidev@0 {
compatible = "sitronix,fb_st7789v";
reg = <1>;
reset-gpios = <&pio 7 2 1 >;
dc-gpios = <&pio 7 3 0>;
buswidth = <8>;
spi-max-frequency = <32000000>;
spi-cpol;
spi-cpha;
bgr;
rotate = <90>;
init = <0x1000011
0x20000ff
0x1000036 0xA0
0x100003a 0x05
0x1000020
0x100002a 0x00 0x01 0x00 0x3f
0x100002b 0x00 0x00 0x00 0xef
0x10000b2 0x0c 0x0c 0x00 0x33 0x33
0x10000b7 0x35
0x10000bb 0x1f
0x10000c0 0x0c
0x10000c2 0x01
0x10000c3 0x12
0x10000c4 0x20
0x10000c6 0x0f
0x10000d0 0xa4 0xa1
0x10000e0 0xd0 0x08 0x11 0x08 0x0C 0x15 0x39 0x33 0x50 0x36 0x13 0x14 0x29 0x2d
0x10000e1 0xd0 0x08 0x10 0x08 0x06 0x06 0x39 0x44 0x51 0x0b 0x16 0x14 0x2f 0x31
0x1000029>;
};
};
};
};
```

Компилируем и добавляем созданный пользовательский оверлей в **armbianEnv.txt** следующей командой:
```
sudo armbian-add-overlay opizero3-kobra2neo.dts
```
### Перезагружаемся
```
sudo reboot
```
### Все вышеописанное одной командой:
```
cd && sudo apt update && sudo apt install -y xserver-xorg-video-fbdev wget && sudo wget https://raw.githubusercontent.com/choolkov/kobra2neo-orangepizero3/main/50-fbdev.conf -O /usr/share/X11/xorg.conf.d/50-fbdev.conf && wget https://raw.githubusercontent.com/choolkov/kobra2neo-orangepizero3/main/opizero3-kobra2neo.dts -O /tmp/opizero3-kobra2neo.dts && sudo armbian-add-overlay /tmp/opizero3-kobra2neo.dts && sudo reboot
```
