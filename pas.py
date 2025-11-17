import tkinter as tk
from tkinter import ttk, messagebox

users = {}
gaji_karyawan = []

def main_app():
    app = tk.Tk()
    app.title("Aplikasi Gaji Karyawan")
    app.geometry("800x600")
    app.configure(bg="#ADD8E6")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#ADD8E6")
    style.configure("TLabel", background="#ADD8E6", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=5)
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                    background="#4682b4", foreground="white")
    style.configure("Treeview", background="#fafafa", fieldbackground="#fafafa", foreground="black")

    halaman1 = ttk.Frame(app)
    halaman2 = ttk.Frame(app)
    halaman3 = ttk.Frame(app)
    halaman4 = ttk.Frame(app)

    for frame in (halaman1, halaman2, halaman3, halaman4):
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    ttk.Label(halaman1, text="📊 Dashboard", font=("Segoe UI", 16, "bold")).pack(pady=20)
    frame_btn = ttk.Frame(halaman1)
    frame_btn.pack(pady=10)

    ttk.Button(frame_btn, text="Input Data", command=lambda: halaman2.tkraise()).grid(row=0, column=0, padx=5)
    ttk.Button(frame_btn, text="Hitung Gaji", command=lambda: [halaman3.tkraise(), update_combo()]).grid(row=0, column=1, padx=5)
    ttk.Button(frame_btn, text="Laporan", command=lambda: halaman4.tkraise()).grid(row=0, column=2, padx=5)

    ttk.Label(halaman2, text="✍️ Input Data Karyawan", font=("Segoe UI", 16, "bold")).pack(pady=20)

    entry_nama = ttk.Entry(halaman2, width=40)
    entry_posisi = ttk.Entry(halaman2, width=40)
    entry_gaji = ttk.Entry(halaman2, width=40)

    ttk.Label(halaman2, text="Nama").pack()
    entry_nama.pack()
    ttk.Label(halaman2, text="Posisi").pack()
    entry_posisi.pack()
    ttk.Label(halaman2, text="Gaji Pokok").pack()
    entry_gaji.pack()

    status_label = ttk.Label(halaman2, text="")
    status_label.pack()

    def simpan_data():
        nama = entry_nama.get().strip()
        posisi = entry_posisi.get().strip()
        gaji = entry_gaji.get().strip()

        if not (nama and posisi and gaji):
            status_label.config(text="Semua kolom harus diisi!", foreground="red")
            return

        if not gaji.isdigit():
            status_label.config(text="Gaji harus angka!", foreground="red")
            return

        gaji_karyawan.append({"nama": nama, "posisi": posisi, "gaji": int(gaji)})
        entry_nama.delete(0, tk.END)
        entry_posisi.delete(0, tk.END)
        entry_gaji.delete(0, tk.END)
        status_label.config(text="Data berhasil disimpan!", foreground="#2e8b57")

    ttk.Button(halaman2, text="Simpan", command=simpan_data).pack(pady=10)
    ttk.Button(halaman2, text="Kembali", command=lambda: halaman1.tkraise()).pack(pady=10)

    ttk.Label(halaman3, text="💰 Hitung Gaji Lembur", font=("Segoe UI", 16, "bold")).pack(pady=20)

    ttk.Label(halaman3, text="Pilih Karyawan").pack()
    combo_karyawan = ttk.Combobox(halaman3, state="readonly", width=37)
    combo_karyawan.pack()

    entry_jam = ttk.Entry(halaman3, width=20)
    entry_upah = ttk.Entry(halaman3, width=20)
    hasil_label = ttk.Label(halaman3, text="")

    ttk.Label(halaman3, text="Jam Lembur").pack()
    entry_jam.pack()
    ttk.Label(halaman3, text="Upah Lembur per Jam").pack()
    entry_upah.pack()
    hasil_label.pack()

    def update_combo():
        if gaji_karyawan:
            combo_karyawan['values'] = [k['nama'] for k in gaji_karyawan]
            combo_karyawan.current(0)
        else:
            combo_karyawan.set("")
            combo_karyawan['values'] = []

    def hitung():
        selected = combo_karyawan.get()
        if not selected:
            hasil_label.config(text="Pilih karyawan terlebih dahulu!", foreground="red")
            return

        try:
            jam = int(entry_jam.get())
            upah = int(entry_upah.get())
        except ValueError:
            hasil_label.config(text="Jam & Upah harus angka!", foreground="red")
            return

        karyawan = next((k for k in gaji_karyawan if k['nama'] == selected), None)
        if not karyawan:
            hasil_label.config(text="Karyawan tidak ditemukan!", foreground="red")
            return

        gaji_pokok = karyawan['gaji']
        total_lembur = jam * upah
        total_gaji = gaji_pokok + total_lembur

        hasil_label.config(
            text=f"Gaji Pokok: Rp {gaji_pokok}\nLembur: Rp {total_lembur}\nTotal: Rp {total_gaji}",
            foreground="#2e8b57"
        )

    ttk.Button(halaman3, text="Hitung", command=hitung).pack(pady=10)
    ttk.Button(halaman3, text="Kembali", command=lambda: halaman1.tkraise()).pack(pady=10)

    halaman3.bind("<Map>", lambda e: update_combo())

    ttk.Label(halaman4, text="📑 Laporan Gaji", font=("Segoe UI", 16, "bold")).pack(pady=20)

    tree = ttk.Treeview(halaman4, columns=("Nama", "Posisi", "Gaji"), show="headings", height=10)
    tree.heading("Nama", text="Nama")
    tree.heading("Posisi", text="Posisi")
    tree.heading("Gaji", text="Gaji Pokok")
    tree.pack(pady=10)

    def tampil_data():
        tree.delete(*tree.get_children())
        if gaji_karyawan:
            for k in gaji_karyawan:
                tree.insert("", tk.END, values=(k["nama"], k["posisi"], k["gaji"]))
        else:
            tree.insert("", tk.END, values=("Belum ada data", "-", "-"))

    ttk.Button(halaman4, text="Refresh Data", command=tampil_data).pack(pady=10)
    ttk.Button(halaman4, text="Kembali", command=lambda: halaman1.tkraise()).pack(pady=10)

    halaman4.bind("<Map>", lambda e: tampil_data())

    halaman1.tkraise()
    app.mainloop()

def login_register_app():
    root = tk.Tk()
    root.title("Login/Register - Aplikasi Gaji Karyawan")
    root.geometry("400x300")

    halaman_login = ttk.Frame(root)
    halaman_regis = ttk.Frame(root)

    for frame in (halaman_login, halaman_regis):
        frame.place(relx=0, relx=0, relwidth=1, relheight=1)

    ttk.Label(halaman_login, text="Login", font=("Segoe UI", 16, "bold")).pack(pady=20)

    entry_user_login = ttk.Entry(halaman_login, width=30)
    entry_pass_login = ttk.Entry(halaman_login, width=30, show="*")

    ttk.Label(halaman_login, text="Username").pack()
    entry_user_login.pack()
    ttk.Label(halaman_login, text="Password").pack()
    entry_pass_login.pack()

    def login():
        uname = entry_user_login.get().strip()
        pwd = entry_pass_login.get().strip()

        if not uname or not pwd:
            messagebox.showerror("Error", "Username/Password tidak boleh kosong!")
            return

        if uname in users and users[uname] == pwd:
            messagebox.showinfo("Sukses", "Login berhasil!")
            root.destroy()
            main_app()
        else:
            messagebox.showerror("Error", "Username/Password salah!")

    ttk.Button(halaman_login, text="Login", command=login).pack(pady=10)
    ttk.Button(halaman_login, text="Register", command=lambda: halaman_regis.tkraise()).pack(pady=5)

    ttk.Label(halaman_regis, text="Registrasi", font=("Segoe UI", 16, "bold")).pack(pady=20)

    entry_user_regis = ttk.Entry(halaman_regis, width=30)
    entry_pass_regis = ttk.Entry(halaman_regis, width=30, show="*")

    ttk.Label(halaman_regis, text="Username").pack()
    entry_user_regis.pack()
    ttk.Label(halaman_regis, text="Password").pack()
    entry_pass_regis.pack()

    def register():
        uname = entry_user_regis.get().strip()
        pwd = entry_pass_regis.get().strip()

        if not uname or not pwd:
            messagebox.showerror("Error", "Username/Password tidak boleh kosong!")
            return

        if uname in users:
            messagebox.showerror("Error", "Username sudah ada!")
            return

        users[uname] = pwd
        messagebox.showinfo("Sukses", "Registrasi berhasil!")
        halaman_login.tkraise()

    ttk.Button(halaman_regis, text="Register", command=register).pack(pady=10)
    ttk.Button(halaman_regis, text="Kembali", command=lambda: halaman_login.tkraise()).pack(pady=5)

    halaman_login.tkraise()
    root.mainloop()

if __name__ == "__main__":
    login_register_app()
