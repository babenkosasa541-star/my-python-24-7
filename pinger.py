import requests
import time
import datetime
import sys

# --- !!! ВАЖНО: ЗАМЕНИТЕ ЭТОТ АДРЕС !!! ---
# Это URL вашего основного сайта (pypad_ru.py), который вы получите после его развертывания
MAIN_SITE_URL = "https://<ваш-адрес>.onrender.com" 

# Интервал между запросами в секундах. 600 секунд = 10 минут. 
PING_INTERVAL_SECONDS = 600

def send_ping(url):
    """Отправляет HTTP GET-запрос для поддержания активности сайта."""
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Идентификация робота
    headers = {'User-Agent': 'Custom Python Pinger Bot'}
    
    try:
        # Отправляем запрос с таймаутом. Если сайт долго не отвечает, считаем это ошибкой.
        response = requests.get(url, headers=headers, timeout=20) 
        
        # Проверяем ответ
        if response.status_code == 200:
            print(f"[{current_time}] Пинг успешен. Сайт активен (Код: {response.status_code}).")
        else:
            # Если получен код ошибки (например, 500), это проблема с сайтом.
            print(f"[{current_time}] Код ответа: {response.status_code}. Возможно, на сайте произошел сбой.")
            
    except requests.exceptions.RequestException as e:
        # Если не удалось установить соединение (например, сервер Render упал)
        print(f"[{current_time}] КРИТИЧЕСКАЯ ОШИБКА СЕТИ: {e}. Сайт недоступен.")
        # В случае критической ошибки скрипт-будильник должен уведомить вас

# --- Запуск цикла ---

if __name__ == "__main__":
    if "<ваш-адрес>" in MAIN_SITE_URL:
        print("\n!!! ОШИБКА: Сначала разверните сайт и вставьте реальный URL в MAIN_SITE_URL !!!\n")
        sys.exit(1)
        
    print(f"--- Pinger запущен. Цель: {MAIN_SITE_URL} ---")
    
    # В среде PythonAnywhere этот скрипт будет перезапускаться по расписанию.
    # Для локального тестирования оставляем цикл while True.
    while True: 
        send_ping(MAIN_SITE_URL)
        time.sleep(PING_INTERVAL_SECONDS)