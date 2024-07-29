from settings import *
import re

def folder_importer(*path) -> dict:
    surfs = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surfs[re.split(r'_|\.', file_name)[1]] = pygame.image.load(full_path).convert_alpha()
    return surfs