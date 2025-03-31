import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
from ctypes import windll

try:
    windll.shcore.SetProcessDpiAwareness(1)
except Exception as e:
    print(f"No se pudo habilitar el soporte DPI: {e}")
    
def validar_datos():
    if tipo_doc_var.get() not in ["Tarjeta de identidad", "Cédula"]:
        messagebox.showerror("Error", "Seleccione un tipo de documento válido.")
        return False
    if not num_doc_var.get().isdigit() or len(num_doc_var.get()) > 10:
        messagebox.showerror("Error", "Número de documento debe ser numérico y no mayor de 10 caracteres.")
        return False
    if not primer_nombre_var.get().isalpha() or len(primer_nombre_var.get()) > 30:
        messagebox.showerror("Error", "Primer nombre no debe contener números y no debe superar 30 caracteres.")
        return False
    if not segundo_nombre_var.get().isalpha() or len(segundo_nombre_var.get()) > 30:
        messagebox.showerror("Error", "Segundo nombre no debe contener números y no debe superar 30 caracteres.")
        return False
    if not apellidos_var.get().isalpha() or len(apellidos_var.get()) > 60:
        messagebox.showerror("Error", "Apellidos no deben contener números y no deben superar 60 caracteres.")
        return False
    if not re.match(r"^\d{2}-[a-zA-Z]{3}-\d{4}$", fecha_nac_var.get()):
        messagebox.showerror("Error", "La fecha debe estar en formato dd-mmm-yy (ej. 12-Mar-98).")
        return False
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", correo_var.get()):
        messagebox.showerror("Error", "Correo electrónico no es válido.")
        return False
    if not celular_var.get().isdigit() or len(celular_var.get()) != 10:
        messagebox.showerror("Error", "Celular debe ser numérico y de 10 caracteres.")
        return False
    if not foto_var.get():
        messagebox.showerror("Error", "Debe seleccionar una foto.")
        return False
    return True

def seleccionar_foto():
    archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
    if archivo:
        if os.path.getsize(archivo) > 2 * 1024 * 1024:
            messagebox.showerror("Error", "El archivo no debe superar los 2MB.")
        else:
            foto_var.set(archivo)

def submit():
    datos = {
            "Tipo de Documento": tipo_doc_var.get(),
            "Número de Documento": num_doc_var.get(),
            "Primer Nombre": primer_nombre_var.get(),
            "Segundo Nombre": segundo_nombre_var.get(),
            "Apellidos": apellidos_var.get(),
            "Fecha de Nacimiento": fecha_nac_var.get(),
            "Género": genero_var.get(),
            "Correo Electrónico": correo_var.get(),
            "Celular": celular_var.get(),
            "Foto": foto_var.get()
        }
    if all(datos):
        if validar_datos():
            messagebox.showinfo("Éxito", "Datos enviados correctamente.")
    else:
        messagebox.showerror("Error", "Todos los campos deben estar llenados")
    
def crear_widgets(root):
    ttk.Label(root, text="Formulario de Datos Personales", font=("Arial", 14)).pack(pady=10)
    frame = ttk.Frame(root)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    ttk.Label(frame, text="Tipo de Documento:").grid(row=0, column=0, sticky="w")
    tipo_doc_entry = ttk.Combobox(frame, textvariable=tipo_doc_var, values=["Tarjeta de identidad", "Cédula"])
    tipo_doc_entry.grid(row=0, column=1, pady=5, padx=5)

    ttk.Label(frame, text="Número de Documento:").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame, textvariable=num_doc_var).grid(row=1, column=1, pady=5, padx=5)

    ttk.Label(frame, text="Primer Nombre:").grid(row=2, column=0, sticky="w")
    ttk.Entry(frame, textvariable=primer_nombre_var).grid(row=2, column=1, pady=5, padx=5)

    ttk.Label(frame, text="Segundo Nombre:").grid(row=3, column=0, sticky="w")
    ttk.Entry(frame, textvariable=segundo_nombre_var).grid(row=3, column=1, pady=5, padx=5)

    ttk.Label(frame, text="Apellidos:").grid(row=4, column=0, sticky="w")
    ttk.Entry(frame, textvariable=apellidos_var).grid(row=4, column=1, pady=5, padx=5)

    ttk.Label(frame, text="Fecha de Nacimiento:").grid(row=5, column=0, sticky="w")
    ttk.Entry(frame, textvariable=fecha_nac_var).grid(row=5, column=1, pady=5, padx=5)

    ttk.Label(frame, text="Género:").grid(row=6, column=0, sticky="w")
    tipo_genero = ttk.Combobox(frame, textvariable=genero_var, values=["Masculino", "Femenino", "No binario", "Prefiero no reportar"])
    tipo_genero.grid(row=6, column=1, pady=5, padx=5)

    ttk.Label(frame, text="Correo Electrónico:").grid(row=7, column=0, sticky="w")
    ttk.Entry(frame, textvariable=correo_var).grid(row=7, column=1, pady=5, padx=5)

    ttk.Label(frame, text="Celular:").grid(row=8, column=0, sticky="w")
    ttk.Entry(frame, textvariable=celular_var).grid(row=8, column=1, pady=5, padx=5)

    ttk.Label(frame, text="Foto:").grid(row=9, column=0, sticky="w")
    ttk.Button(frame, text="Seleccionar Archivo", command=seleccionar_foto).grid(row=9, column=1, pady=5, padx=5)

    # Botón de envío
    ttk.Button(root, text="Enviar", command=submit).pack(pady=20)

root = tk.Tk()
root.title("Formulario de Datos Personales")

# Variables
tipo_doc_var = tk.StringVar()
num_doc_var = tk.StringVar()
primer_nombre_var = tk.StringVar()
segundo_nombre_var = tk.StringVar()
apellidos_var = tk.StringVar()
fecha_nac_var = tk.StringVar()
genero_var = tk.StringVar()
correo_var = tk.StringVar()
celular_var = tk.StringVar()
foto_var = tk.StringVar()

# Widgets
crear_widgets(root)

root.update_idletasks()
width = root.winfo_reqwidth()
height = root.winfo_reqheight()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")
root.resizable(False, False)

root.mainloop()
