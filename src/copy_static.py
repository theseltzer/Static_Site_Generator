import os
import shutil

def copy_files_recursive(source_dir, dest_dir):
    # Eğer hedef klasör yoksa oluştur
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    # Kaynak klasördeki her şeyi listele
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        print(f" * {source_path} -> {dest_path}")

        if os.path.isfile(source_path):
            # Eğer bir dosyaysa, kopyala
            shutil.copy(source_path, dest_path)
        else:
            # Eğer bir klasörse, özyineleme (recursion) yap
            copy_files_recursive(source_path, dest_path)
