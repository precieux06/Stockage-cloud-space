import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox

class CloudStorage:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

    def upload_file(self, file_path):
        if os.path.exists(file_path):
            shutil.copy(file_path, self.storage_path)
            return True
        return False

    def list_files(self):
        return os.listdir(self.storage_path)

    def download_file(self, file_name, download_path):
        source = os.path.join(self.storage_path, file_name)
        if os.path.exists(source):
            shutil.copy(source, download_path)
            return True
        return False

    def delete_file(self, file_name):
        file_path = os.path.join(self.storage_path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

# ---------------- GUI ------------------
class CloudApp:
    def __init__(self, master):
        self.cloud = CloudStorage("mon_stockage_cloud")
        self.master = master
        master.title("Mini Cloud Storage 💾☁️")

        self.label = tk.Label(master, text="Fichiers stockés:")
        self.label.pack()

        self.file_list = Listbox(master, width=50)
        self.file_list.pack()

        self.refresh_button = tk.Button(master, text="🔄 Rafraîchir", command=self.refresh_list)
        self.refresh_button.pack()

        self.upload_button = tk.Button(master, text="📤 Uploader un fichier", command=self.upload)
        self.upload_button.pack()

        self.download_button = tk.Button(master, text="📥 Télécharger le fichier sélectionné", command=self.download)
        self.download_button.pack()

        self.delete_button = tk.Button(master, text="🗑 Supprimer le fichier sélectionné", command=self.delete)
        self.delete_button.pack()

        self.refresh_list()

    def refresh_list(self):
        self.file_list.delete(0, tk.END)
        for file_name in self.cloud.list_files():
            self.file_list.insert(tk.END, file_name)

    def upload(self):
        file_path = filedialog.askopenfilename()
        if file_path and self.cloud.upload_file(file_path):
            messagebox.showinfo("Succès", "Fichier uploadé ✅")
            self.refresh_list()
        else:
            messagebox.showerror("Erreur", "Échec de l'upload")

    def download(self):
        selection = self.file_list.curselection()
        if selection:
            file_name = self.file_list.get(selection)
            download_path = filedialog.askdirectory()
            if download_path and self.cloud.download_file(file_name, os.path.join(download_path, file_name)):
                messagebox.showinfo("Succès", f"{file_name} téléchargé 🎉")
            else:
                messagebox.showerror("Erreur", "Échec du téléchargement")

    def delete(self):
        selection = self.file_list.curselection()
        if selection:
            file_name = self.file_list.get(selection)
            confirm = messagebox.askyesno("Confirmation", f"Supprimer {file_name}?")
            if confirm and self.cloud.delete_file(file_name):
                messagebox.showinfo("Supprimé", f"{file_name} a été supprimé 🗑")
                self.refresh_list()

# ----------------- Lancer l'app -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CloudApp(root)
    root.mainloop()
