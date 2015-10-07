# Python file extractor
A Python script that extracts and save all `JPEG` images (based on magic numbers) from another file (e.g. a disk image).

With the current implementation it is possible to extract `JPEG` file only, but it's possible to extract other kind of files by adding the corresponding header/trailer magic numbers in the `magic` dictionary. **Note that this script was created to extract only JPEG images, so it might not work with other file formats**.

# Usage:
The following command will extract all `JPEG` images from file `<file_name>`:

    $ python extractor.py <file_name>

If any `JPEG` image is found, it is saved in the current working directory, named `image1.jpg` (if multiple images are found, their name will follow the schema `image<number>.jpg`.
