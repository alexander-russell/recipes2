import os
import tarfile
from pathlib import Path
from django.core.management.base import BaseCommand
from manager.models import Image
from django.conf import settings

class Command(BaseCommand):
    help = "Create a tarball of all media files referenced by Recipe Image instances"

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        output_tar = Path.cwd() / "recipeimage_media_backup.tar.gz"

        with tarfile.open(output_tar, "w:gz") as tar:
            for image in Image.objects.exclude(file="").iterator():
                file_path = media_root / image.file.name
                if file_path.exists()
                    tar.add(file_path, arcname=image.file.name)
                else:
                    self.stderr.write(f"Missing: {file_path}")

        self.stdout.write(f"Backup written to {output_tar}")
