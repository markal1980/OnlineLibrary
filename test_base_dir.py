from pathlib import Path

from django.conf import settings

# base_dir = settings.BASE_DIR
print(Path(__file__).resolve().parent.parent)