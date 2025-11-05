import os
import time

def read_speed(file_path, file_size_mb=300):
    start_time = time.time()
    with open(file_path, 'rb', buffering=0) as f:
        while f.read(1024 * 1024*file_size_mb):
            pass
    elapsed_time = time.time() - start_time
    elapsed_time = max(0.001, elapsed_time)
    speed = file_size_mb / elapsed_time
    print(f"Скорость чтения(Слишком завышенная): {speed:.2f} МБ/c")


def measure_speed(file_path, file_size_mb=300, mode='write', buf = False):
    test_data = os.urandom(1024 * 1024)
    try:
        if mode == 'write':
            if not buf:
                start_time = time.time()
                with open(file_path, 'wb') as f:
                    for i in range(file_size_mb):
                        f.write(test_data)
                        f.flush()
                        os.fsync(f.fileno())

                time_now = time.time() - start_time
                time_now = max(0.001, time_now)
                speed = file_size_mb / time_now
                print(f"Скорость записи с очисткой буфера: {speed:.2f} МБ/c")

            else:
                start_time = time.time()
                with open(file_path, 'wb') as f:
                    for i in range(file_size_mb):
                        f.write(test_data)
                time_now = time.time() - start_time
                time_now = max(0.001, time_now)
                speed = file_size_mb / time_now
                print(f"Скорость записи без очистки буфера: {speed:.2f} МБ/с")
            return 0
        else:
            print("Неверный режим. Используйте 'write'.")
            return 0

    except Exception as e:
        print(f"Ошибка: {e}")
        return 0



if __name__ == "__main__":

    test_file_path =input("Введите полный путь к usb накопителю(Например: 'D:/' ): ") +"testfile.bin"
    print("=== Тест скорости ===")
    write_speed = measure_speed(test_file_path)
    write_speed2 = measure_speed(test_file_path, buf=True)
    read_speed(test_file_path)
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
