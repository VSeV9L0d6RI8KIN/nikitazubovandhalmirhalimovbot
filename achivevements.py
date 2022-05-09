# Функция присваивает звание человеку за его прогресс
def ach(n):
    if 0 < int(n) < 3:
        return 'Разведчик'
    elif 3 <= int(n) < 5:
        return 'Рядовой'
    elif 5 <= int(n) < 7:
        return 'Капрал'
    elif 7 <= int(n) < 10:
        return 'Сержант'
    elif 10 <= int(n) < 14:
        return 'Старший сержант'
    elif 14 <= int(n) < 21:
        return 'Рыцарь'
    elif 21 <= int(n) < 30:
        return 'Рыцарь-лейтенат'
    elif 30 <= int(n) < 60:
        return 'Рыцарь-капитан'
    elif 60 <= int(n) < 90:
        return 'Рыцарь-защитник'
    elif 90 <= int(n) < 120:
        return 'Чемпион Света'
    elif 120 <= int(n) < 150:
        return 'Командор'
    elif 150 <= int(n) < 180:
        return 'завоеватель'
    elif 180 <= int(n) < 240:
        return 'Маршал'
    elif 240 <= int(n) < 300:
        return 'Фельдмаршал'
    elif 300 <= int(n) < 365:
        return 'Главнокомандующий'
    elif 365 <= int(n) < 500:
        return 'Верховный воевода'
    elif int(n) >= 500:
        return 'Бессмертный'
