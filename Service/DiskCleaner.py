import os
import time
import shutil
from pathlib import Path

CAPE_DIR = "/opt/CAPEv2/storage/analyses"
THRESHOLD_PERCENT = 70  # مثال: 80% استفاده از دیسک

def cleanup():
    # منطق پاکسازی (مثلاً حذف قدیمیترین فایلها)
    files = sorted(Path(CAPE_DIR).glob("*"), key=lambda f: f.stat().st_mtime)
    for i in files:
        if  get_disk_usage() < THRESHOLD_PERCENT:
            break
        os.system(f'rm -rf {i}')
        print(f'run : rm -rf {i}')


def get_disk_usage():
    total, used, free = shutil.disk_usage(CAPE_DIR)
    print(shutil.disk_usage(CAPE_DIR))
    return (used / total) * 100

if __name__ == "__main__":
    while True:
        if get_disk_usage() > THRESHOLD_PERCENT:
            cleanup()
        time.sleep(60 * 5)  # بررسی هر ۵ دقیقه

