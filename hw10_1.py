import asyncio
import aiofile
import argparse

from shutil import copy
from pathlib import Path


async def copy_file(file: Path, destination_dir: Path) -> None:
    file_suffix = file.suffix.lstrip('.')
    if file_suffix:
        nested_folder = destination_dir/file_suffix
        nested_folder.mkdir(parents=True, exist_ok=True)
    else:
        nested_folder = destination_dir/'other'
        nested_folder.mkdir(parents=True, exist_ok=True)
    new_place = nested_folder/file.name
    copy(file, new_place)


async def read_folder(path: Path, destination_dir: Path) -> None:
    if path.is_dir():
        for child in path.iterdir():
            await read_folder(child, destination_dir)
    else:
        await copy_file(path, destination_dir)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="The program sorting and copying files")

    # "C:/goit"
    # "C:/Projects_goit/c_systems/destination"
    parser.add_argument(
        'root', type=str, nargs='?', default="C:/goit", help='Source directory')
    parser.add_argument('destination', type=str, nargs='?', default="C:/Projects_goit/c_systems/destination",
                        help='Destination directory')

    args = parser.parse_args()

    source_dir = Path(args.root)
    destination_dir = Path(args.destination)

    if not source_dir.exists():
        print("The source directory is not exist")
        exit(1)
    if not source_dir.is_dir():
        print("It's not directory")
        exit(1)

    asyncio.run(read_folder(source_dir, destination_dir))
