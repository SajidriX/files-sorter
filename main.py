import pathlib
import shutil
import tkinter as tk

current_path = None

def enter_input(event=None):
    global current_path
    text = entry.get().strip()
    if text:
        current_path = pathlib.Path(text)

def update_text(message):
    #update widget text
    text_widget.config(state="normal")
    text_widget.insert(tk.END, message + "\n")
    text_widget.config(state="disabled")
    text_widget.see(tk.END) 

def sort_files():
    global current_path
    
    #Cleaning
    text_widget.config(state="normal")
    text_widget.delete("1.0", tk.END)
    text_widget.config(state="disabled")
    
    if current_path is None:
        text = entry.get().strip()
        if not text:
            update_text("⚠️ Enter path!")
            return
        current_path = pathlib.Path(text)
    
    if not current_path.exists():
        update_text(f"❌ Path does not exist: {current_path}")
        return
    
    original_sort_files(current_path)

def original_sort_files(path: pathlib.Path):
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
        update_text(f"📁 Created folder: {suff}")

    moved_count = 0
    error_count = 0
    
    for suff in suffixes:
        for file in files:
            if str(file.suffix) == str(suff):
                folder_name = str(suff).replace(".", "")
                folder = path / folder_name 
                
                # Moving file
                try:
                    shutil.move(str(file), str(folder / file.name))
                    if str(file.suffix) != ".py" or str(file.suffix) != ".gitignore" or str(file.suffix) != ".vscode":
                        update_text(f"✅ Moved: {file.name} → {folder_name}/")
                        moved_count += 1
                except Exception as e:
                    update_text(f"❌ Error with {file.name}: {e}")
                    error_count += 1
    
    #Bottom line
    update_text("\n" + "="*40)
    update_text(f"📊 Results: {moved_count} moved, {error_count} errors")

window = tk.Tk()
window.title("File sorter")
window.geometry("650x600") 

label = tk.Label(window, text="Sort all your files here.", font=("Roboto", 16), fg="#287932", bg="#314131")
label.pack(pady=15, padx=10)

label1 = tk.Label(window, text="Enter filepath, where will be all sorted folders", font=("Roboto", 16), fg="#287932", bg="#314131")
label1.pack(pady=5, padx=10)

label2 = tk.Label(window, text="(and where are all unsorted files, move them in it):", font=("Roboto", 16), fg="#287932", bg="#314131")
label2.pack(pady=5, padx=10)

entry = tk.Entry(
    window,
    width=60,
    font=("Arial", 12),
    bg="black",
    fg="#00ff00",
    bd=3,
    relief="raised"
)
entry.pack(pady=10, padx=10)
entry.bind("<Return>", lambda event: enter_input())  
entry.focus()
entry.insert(0, ".")

button = tk.Button(
    window,
    text="Sort files",
    command=sort_files, 
    bg="#314131",
    fg="#287932",
    font=("Arial", 12, "bold")
)
button.pack(pady=10)

#Output
text_frame = tk.Frame(window, bg="#314131")
text_frame.pack(pady=10, padx=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_widget = tk.Text(
    text_frame,
    height=12,
    width=70,
    bg="black",
    fg="#00ff00",
    font=("Consolas", 10),
    yscrollcommand=scrollbar.set,
    state="disabled",
    wrap=tk.WORD
)
text_widget.pack(side=tk.LEFT, fill="both", expand=True)

scrollbar.config(command=text_widget.yview)

#Instruction
instructions = tk.Label(
    window,
    text="Enter path (e.g., '.' for current folder or 'C:/Users/Name/Files')",
    font=("Arial", 9),
    fg="gray",
    bg="#000000"
)
instructions.pack(pady=5)

window.configure(bg="#000000")

window.mainloop()