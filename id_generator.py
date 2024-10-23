import os
import threading

class PersistentIDGenerator:
    _file_path = "id_store.txt"
    _lock = threading.Lock()  # 确保文件读写的线程安全

    @classmethod
    def generate_task_id(cls):
        with cls._lock:
            if not os.path.exists(cls._file_path):
                with open(cls._file_path, "w") as file:
                    file.write("10001")
            
            with open(cls._file_path, "r+") as file:
                current_id = int(file.read().strip())
                new_id = current_id + 1
                file.seek(0)
                file.write(str(new_id))
                file.truncate()
            
            return current_id


if __name__ == "__main__":
    new_id1 = PersistentIDGenerator.generate_task_id()  # 1000
    new_id2 = PersistentIDGenerator.generate_task_id()  # 1001
    print("%d,%d"%(new_id1, new_id2))
