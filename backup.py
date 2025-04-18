import subprocess
import os
import requests
import datetime
from io import BytesIO

# Конфигурация
PG_HOST = 'localhost'
PG_PORT = '5432'
PG_DATABASE = 'kursach'
PG_USER = 'postgres'
PG_PASSWORD = 'Qwerty13579'
YANDEX_DISK_TOKEN = 'y0__xCE_4TUBRjblgMgr5uZ4BLmSeKr62axP81Ru1kk98uoCg2s0w'
BACKUP_DIR = r'C:\Users\Msi\Desktop\tmp'  # Временная директория для хранения дампа
YANDEX_DISK_PATH = '/backups'  # Путь на Яндекс.Диске для сохранения бэкапов
PG_DUMP_PATH = r'C:\Program Files\PostgreSQL\17\bin\pg_dump.exe'

current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_filename = f"pg_backup_{PG_DATABASE}_{current_time}.sql"
backup_path = os.path.join(BACKUP_DIR, backup_filename)


def create_postgres_backup():
    """Создание дампа базы данных PostgreSQL с подробным логированием"""
    try:
        env = os.environ.copy()
        env["PGPASSWORD"] = PG_PASSWORD

        pg_dump_path = r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"

        command = [
            pg_dump_path,
            "-h", PG_HOST,
            "-p", PG_PORT,
            "-U", PG_USER,
            "-d", PG_DATABASE,
            "-f", backup_path,
            "-F", "p",
            "-v"  # Добавляем подробный вывод
        ]

        print("Команда бэкапа:", " ".join(command))

        # Запускаем и перехватываем вывод
        result = subprocess.run(
            command,
            env=env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print("Бэкап успешно создан!")
        print("Вывод команды:", result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        print("❌ Ошибка при создании бэкапа!")
        print("Код ошибки:", e.returncode)
        print("Вывод stderr:", e.stderr)
        return False
    except Exception as e:
        print("❌ Неожиданная ошибка:", str(e))
        return False


def upload_to_yandex_disk():
    try:
        if not os.path.exists(backup_path):
            print(f"Файл {backup_path} не найден")
            return False

        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"

        yandex_file_path = f"{YANDEX_DISK_PATH}/{backup_filename}"

        headers = {
            'Authorization': f'OAuth {YANDEX_DISK_TOKEN}'
        }
        params = {
            'path': yandex_file_path,
            'overwrite': 'true'
        }

        response = requests.get(upload_url, headers=headers, params=params)
        response.raise_for_status()

        upload_data = response.json()
        href = upload_data['href']

        # Загружаем файл
        with open(backup_path, 'rb') as f:
            file_data = f.read()

        upload_response = requests.put(href, data=BytesIO(file_data))
        upload_response.raise_for_status()

        print(f"Файл успешно загружен на Яндекс.Диск: {yandex_file_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке на Яндекс.Диск: {e}")
        return False
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return False


def cleanup():
    try:
        if os.path.exists(backup_path):
            os.remove(backup_path)
            print(f"Временный файл {backup_path} удален")
    except Exception as e:
        print(f"Ошибка при удалении временного файла: {e}")


def main():
    if not create_postgres_backup():
        return

    if not upload_to_yandex_disk():
        cleanup()
        return

    cleanup()
    print("Процесс завершен успешно")


if __name__ == "__main__":
    main()