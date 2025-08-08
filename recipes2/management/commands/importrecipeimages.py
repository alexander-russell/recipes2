import os
import shutil

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from recipes2.models import Recipe, Image  # Adjust your app name here

# note, call like this: py .\manage.py importrecipeimages "C:/Users/alexa/Desktop/Phonebook/Databases/Recipes/images"

class Command(BaseCommand):
    help = "Bulk import recipe images from folder structure"

    def add_arguments(self, parser):
        parser.add_argument('base_path', type=str, help='Base path of images folder')

    def handle(self, *args, **options):
        base_path = options['base_path']

        if not os.path.isdir(base_path):
            self.stderr.write(f"Error: base path {base_path} is not a directory")
            return

        # Iterate over folders in base_path
        for folder_name in os.listdir(base_path):
            # Skip blank.avif (not a folder) and other non-folders handled above
            folder_path = os.path.join(base_path, folder_name)
            if not os.path.isdir(folder_path):
                continue

            # Get corresponding recipe
            try:
                recipe = Recipe.objects.get(slug=folder_name)
            except Recipe.DoesNotExist:
                self.stderr.write(f"Warning: No Recipe with slug '{folder_name}', skipping folder")
                continue

            # Collect .avif files excluding 'blank.avif' and ignoring others
            avif_files = [
                f for f in os.listdir(folder_path)
                if f.lower().endswith('.avif')
            ]
            if not avif_files:
                self.stdout.write(f"No .avif images found in {folder_path}, skipping")
                continue

            # Sort so main.avif is first, then others alphabetically
            avif_files.sort(key=lambda n: (n.lower() != 'main.avif', n.lower()))

            self.stdout.write(f"Importing images for recipe '{recipe.slug}': {avif_files}")

            with transaction.atomic():
                for pos, filename in enumerate(avif_files):
                    name = os.path.splitext(filename)[0]
                    show_in_gallery = (name.lower() == 'main')

                    src_path = os.path.join(folder_path, filename)

                    # Use your image_upload_to logic to get destination relative path
                    relative_dest_path = os.path.join("recipes2", str(recipe.id), "images", filename)
                    dest_path = os.path.join(settings.MEDIA_ROOT, relative_dest_path)

                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                    # Copy file into MEDIA_ROOT destination, overwriting if exists
                    shutil.copy2(src_path, dest_path)

                    # Create or update Image object
                    img_obj, created = Image.objects.update_or_create(
                        recipe=recipe,
                        name=name,
                        defaults={
                            'position': pos,
                            'alt_text': f"Photo of {recipe.name}" if name.lower() == "main" else None,
                            'show_in_gallery': show_in_gallery,
                            'image': relative_dest_path,
                        }
                    )
                    action = "Created" if created else "Updated"
                    self.stdout.write(f"  {action} Image: {name}, position={pos}, show_in_gallery={show_in_gallery}")

        self.stdout.write("Import complete.")
