from django.db.models import Count
from data.models import Oculos, Color
import os
import django
import sys
from pathlib import Path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()


try:
    all_images_path: list = [data.image for data in Oculos.objects.raw(
        "SELECT id, image FROM store_data_oculos")]
    print("\033[0;32mData was sucessfully taken!\033[m")
except Exception as error:
    print(f"\n\033[0;31mCouldn't get data from the database to check the values. \nError: {
          error}\n\033[m")
    sys.exit()
finally:
    pass

main_folder_for_images = "media"

# media is the folder's name for media files
base: str = str(Path(__file__).resolve().parent / main_folder_for_images) + "/"


def clean_files(current_dir: str, list_to_check: list, tmp_dir: list, tmp_path: str) -> None:
    current_folder = os.listdir(current_dir)

    for dir in current_folder:
        tmp_dir.append(dir)
        tmp_path = "/".join(tmp_dir)
        full_path = base + tmp_path
        if Path(full_path).is_dir():
            clean_files(full_path, list_to_check, tmp_dir, tmp_path)

        else:
            if tmp_path.replace("\\", "/") not in list_to_check:

                os.remove(full_path)
                print(f'\n\033[0;33mFile - "{dir}" - was removed!\033[m')

        tmp_dir.pop()
        tmp_path = "/".join(tmp_dir)

    full_path = base + tmp_path
    if not base == full_path and len(os.listdir(full_path)) == 0:
        os.rmdir(full_path)
        print(
            f'\n\033[0;36mFolder - "{tmp_path.split("\\")[-1]}" - was removed!\033[m')


if __name__ == "__main__":
    clean_files(base, all_images_path, [], "")
    print("\033[0;32m\nThe cleaner is completed!\033[m")
