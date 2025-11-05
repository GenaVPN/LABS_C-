import os
import time


def measure_speed(file_path, file_size_mb=300, mode='write'):
    test_data = os.urandom(1024 * 1024)
    try:
        if mode == 'write':
            start_time = time.time()
            with open(file_path, 'wb') as f:
                for i in range(file_size_mb):
                    f.write(test_data)
                    f.flush()
                    os.fsync(f.fileno())

            time_now = time.time() - start_time
            speed = file_size_mb / time_now

            return speed

        elif mode == 'read':
            if not os.path.exists(file_path):
                print("Файл не найден.")
                return 0


            start_time = time.time()
            with open(file_path, 'rb') as f:
                while f.read(1024 * 1024):
                    pass

            elapsed_time = time.time() - start_time
            speed = file_size_mb / elapsed_time
            if os.path.exists(file_path):
                os.remove(file_path)
            return speed

        else:
            print("Неверный режим. Используйте 'write' или 'read'.")
            return 0

    except Exception as e:
        print(f"Ошибка: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)
        return 0



if __name__ == "__main__":

    test_file_path =input("Введите полный путь к usb накопителю(Например: 'D:/' ): ") +"testfile.bin"

    print("=== Тест скорости ===")
    write_speed = measure_speed(test_file_path, mode='write')
    read_speed = measure_speed(test_file_path, mode='read')
    print(f"Скорость записи: {write_speed:.2f} МБ/с")
    print(f"Скорость чтения: {read_speed:.2f} МБ/с")