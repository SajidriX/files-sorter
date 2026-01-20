import pathlib
import shutil

def sort_files(path: pathlib.Path):
    suffixes = set()

    files = [p for p in path.iterdir() if p.is_file()]

    for file in files:
        suff = file.suffix
        suffixes.add(suff)

        if str(suff) == ".py" or str(suff) == ".git" or str(suff) == ".gitignore" or str(suff) == ".vscode":
            suffixes.discard(suff)

    # Creating folders
    for suff in suffixes:
        suff = str(suff)
        suff = suff.replace(".", "")
        folder = path / suff
        folder.mkdir(exist_ok=True)

    for suff in suffixes:
        for file in files:
            if str(file.suffix) == str(suff):
                folder_name = str(suff).replace(".", "")
                folder = path / folder_name 
                
                #moving file
                try:
                    shutil.move(str(file), str(folder / file.name))
                except Exception as e:
                    print(f"Error with {file.name}: {e}")