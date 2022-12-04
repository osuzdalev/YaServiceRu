from enum import Enum

DEFAULT_VALUE = 3


class OS(Enum):
    APPLE = DEFAULT_VALUE
    WINDOWS = DEFAULT_VALUE + 1


class Category(Enum):
    BIOS = DEFAULT_VALUE
    DEVICES_PERIPHERY = DEFAULT_VALUE + 1
    DISPLAY_GRAPHICS = DEFAULT_VALUE + 2
    INSTALLATION_RECOVERY = DEFAULT_VALUE + 3
    NETWORK_INTERNET = DEFAULT_VALUE + 4
    OTHER = DEFAULT_VALUE + 5
    SAVING_DATA = DEFAULT_VALUE + 6
    SLOWING_BUGGING = DEFAULT_VALUE + 7
    SWITCHING_CHARGING = DEFAULT_VALUE + 8
    SYSTEM_SETTINGS = DEFAULT_VALUE + 9
    UPDATE_DRIVER = DEFAULT_VALUE + 10


class BIOS(Enum):
    CHANGE_LOADING_PRIORITY = DEFAULT_VALUE
    

class SlowingBugging(Enum):
    BOOTING = DEFAULT_VALUE
    HARD_DISK_SSD = DEFAULT_VALUE + 1
    HEATING = DEFAULT_VALUE + 2


DATA_DICT = {
    "Apple": {
        "Callback_Data": OS.APPLE.value,
    },
    "Windows": {
        "Callback_Data": OS.WINDOWS.value,
        "OS_Title": "Windows",
        "Computer": {
            "Callback_Data": DEFAULT_VALUE,
            "Device_Title": "Computer",
            "BIOS": {
                "Callback_Data": Category.BIOS.value,
                "Category_Title_RU": "БИОС",
                "Change_Loading_Priority": {
                    "Callback_Data": BIOS.CHANGE_LOADING_PRIORITY.value,
                    "Problem_Title_EN": "Change_Loading_Priority",
                    "Problem_Title_RU": "Изменить Приоритет Загрузки",
                    "Share": "_Windows ➡ Computer ➡ БИОС\n➡ Изменить Приоритет Загрузки_\n\n",
                    "Text": "В зависимости от модели ноутбука или ПК (производителя материнской платы),"
                            "разные способы входа в *BIOS*.\n\n"
                            "1) `delete` (*Asus, Dell*)\n"
                            "2) `F1` (*Dell, Hp, Lenovo, Samsung, Toshiba*)\n"
                            "3) `F2` (*Acer, Asus, Msi, Lenovo, Dell, Samsung, Toshiba*)\n"
                            "4) `F3` (*Lenovo, Samsung*)\n"
                            "5) `F10` (*Hp*)\n\n"
                            "Если не получается войти, может быть проблема с клавиатурой.\n\n"
                            "1) Нужно найти раздел *Boot*\n"
                            "или *Boot device priority*\n"
                            "2) Изменить приоритет загрузки, поставив на первое место\n"
                            "(*Windows boot manager*\nили устройство с названием *ssd/hdd*)\n"
                            "3) Приоритет загрузки можно изменить горячими клавишами указанными на этой же вкладке\n"
                            "`(+/-, pageUP/down, F6/F5)`\n"
                            "4) Сохранить параметры и выйти с *BIOS* (можно использовать горячие клавиши `F4` или `F10`,\n"
                            "зависит от модели или перейти во вкладку *exit* и выбрать *save and exit*)",
                },
            },
            "Devices_Periphery": {
                "Callback_Data": Category.DEVICES_PERIPHERY.value,
                "Category_Title_RU": "Устройства/Периферия",
            },
            "Display_Graphics": {
                "Callback_Data": Category.DISPLAY_GRAPHICS.value,
                "Category_Title_RU": "Дисплей/Графика",
            },
            "Installation_Recovery": {
                "Callback_Data": Category.INSTALLATION_RECOVERY.value,
                "Category_Title_RU": "Установка/Восстановление",
                "Camera": {

                },
                "Sound": {

                },
                "Microphone": {

                },
                "Touchpad": {

                }
            },
            "Network_Internet": {
                "Callback_Data": Category.NETWORK_INTERNET.value,
                "Category_Title_RU": "Сеть/Интернет",
            },
            "Other": {
                "Callback_Data": Category.OTHER.value,
                "Category_Title_RU": "Другие/Иное",
            },
            "Saving_Data": {
                "Callback_Data": Category.SAVING_DATA.value,
                "Category_Title_RU": "Хранение/Данные",
            },
            "Slowing_Bugging": {
                "Callback_Data": Category.SLOWING_BUGGING.value,
                "Category_Title_RU": "Торможение/Зависание",
                "Booting": {
                    "Callback_Data": SlowingBugging.BOOTING.value,
                    "Problem_Title_EN": "Booting",
                    "Problem_Title_RU": "Автозагрузка",
                    "Share": "_Windows ➡ Computer ➡ Торможение/Зависание\n➡ Автозагрузка_\n\n",
                    "Text": "Автозагрузка и её очистка\n\n"
                            "1) Нажмите `ctrl + alt + delete` "
                            "[(Windows 10)](https://www.microsoft.com/ru-ru/software-download/windows10ISO)\n"
                            "2) Диспетчер устройств\n"
                            "3) Подробнее\n"
                            "4) Автозагрузка\n"
                            "5) Отключить ненужное\n"
                            "6) Перезагрузить устройство\n",
                },
                "Hard_Disk_SSD": {
                    "Callback_Data": SlowingBugging.HARD_DISK_SSD.value,
                },
                "Heating": {
                    "Callback_Data": SlowingBugging.HEATING.value,
                },
            },
            "Switching_Charging": {
                "Callback_Data": Category.SWITCHING_CHARGING.value,
                "Category_Title_RU": "Включение/Заряжание",
            },
            "System_Settings": {
                "Callback_Data": Category.SYSTEM_SETTINGS.value,
                "Category_Title_RU": "Системные Настройки",
                "Security_Password": {

                },
                "Desktop_Personalization": {

                },
            },
            "Update_Driver": {
                "Callback_Data": Category.UPDATE_DRIVER.value,
                "Category_Title_RU": "Обновление/Драйвер",
            },
        }
    }
}
