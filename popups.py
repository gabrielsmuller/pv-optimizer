import tkinter as tk
from tkinter import ttk
import sys, os
import requests
import subprocess
from unidecode import unidecode
from dotenv import load_dotenv

def center_newwindow(width, height, window=None):
    window = window
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')


if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

icon_path = "dimicon.ico"
icon_full_path = os.path.join(application_path, icon_path)


def load_catalog_data(tree):
    load_dotenv()
    api_key = os.getenv("SUPABASE_API_KEY")
    auth_key = os.getenv("SUPABASE_AUTH_KEY")
    url = "https://ktdmbdjzmisdtjhdlvnl.supabase.co/rest/v1/Catalogo de Cargas"
    headers = {
        "apikey": api_key,
        "Authorization": auth_key,
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    # Limpa os dados existentes na árvore
    for item in tree.get_children():
        tree.delete(item)

    # Executa a consulta para buscar todos os dados da tabela 'Catalogo de Cargas'
    response = requests.get(url, headers=headers)
    print(response.text)  # Para verificar o que a API está retornando

    if response.status_code == 200:
        rows = response.json()
        # Insere os dados na árvore
        for row in rows:
            tree.insert('', 'end', values=(row['equipamento'], row['potencia'], row['autonomia'], row['consumo']))
    else:
        print(f"Erro ao carregar dados: {response.text}")

class CustomInfoPopupWithOpen(tk.Toplevel):
    def __init__(self, parent, title, message, file_path):
        super().__init__(parent)
        self.title(title)
        self.file_path = file_path
        self.iconbitmap(icon_full_path)
        self.resizable(False, False)

        # Configurações de tamanho e posição da janela
        window_width = 400
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Label para mostrar a mensagem
        label = ttk.Label(self, text=message, wraplength=350)
        label.pack(padx=20, pady=20)

        # Botões OK e Abrir
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ok_button = ttk.Button(button_frame, text="OK", command=self.destroy)
        ok_button.pack(side="left", padx=10)

        open_button = ttk.Button(button_frame, text="Abrir", style="Accent.TButton", command=self.open_file)
        open_button.pack(side="right", padx=10)

    def open_file(self):
        if os.path.isfile(self.file_path):
            if os.name == 'nt':
                os.startfile(self.file_path)
            else:
                subprocess.call(['open' if os.name == 'mac' else 'xdg-open', self.file_path])
        self.destroy()


class ConsumoPopup(tk.Toplevel):
    def __init__(self, parent, on_submit):
        super().__init__(parent)
        self.title("Inserir Consumo")
        self.iconbitmap(icon_full_path)
        self.geometry("330x170")
        self.center_window(330, 170)
        self.resizable(False, False)

        self.on_submit = on_submit

        ttk.Label(self, text="Insira o consumo:").pack(pady=10)
        self.valor_entrada = ttk.Entry(self)
        self.valor_entrada.pack(pady=5)

        # Foca automaticamente no Entry quando o popup é aberto
        self.valor_entrada.focus_set()

        # Vincula o evento de pressionar Enter a uma ação
        self.valor_entrada.bind("<Return>", self.submit)

        submit_button = ttk.Button(self, text="Confirmar", style="Accent.TButton", command=self.submit)
        submit_button.pack(pady=10)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

    def submit(self, event=None):  # Adiciona event=None para aceitar o argumento do evento
        try:
            valor = float(self.valor_entrada.get())
            self.on_submit(valor)
            self.destroy()
        except ValueError:
            CustomInfoPopup(self, "Erro", "Por favor, insira um número válido.")

class BigCustomInfoPopup(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)

        window_width = 800
        window_height = 470
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        label = ttk.Label(self, text=message, wraplength=750)
        label.pack(padx=2, pady=20)

        self.iconbitmap(icon_full_path)

        ok_button = ttk.Button(self, text="OK", command=self.destroy, style="Accent.TButton")
        ok_button.pack(pady=10)

class CustomInfoPopup(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)

        window_width = 500
        window_height = 230
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        label = ttk.Label(self, text=message, wraplength=350)
        label.pack(padx=20, pady=20)

        self.iconbitmap(icon_full_path)

        ok_button = ttk.Button(self, text="OK", command=self.destroy, style="Accent.TButton")
        ok_button.pack(pady=10)


class YesNoPopup(tk.Toplevel):
    def __init__(self, parent, title, message, on_yes_callback=None, on_no_callback=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        window_width = 400
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.iconbitmap(icon_full_path)

        self.on_yes_callback = on_yes_callback
        self.on_no_callback = on_no_callback

        label = ttk.Label(self, text=message, wraplength=350)
        label.pack(padx=20, pady=20)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        yes_button = ttk.Button(button_frame, text="Sim", command=self.on_yes, style="Accent.TButton")
        yes_button.pack(side="left", padx=10)

        no_button = ttk.Button(button_frame, text="Não", command=self.on_no)
        no_button.pack(side="left", padx=10)

    def on_yes(self):
        if self.on_yes_callback:
            self.on_yes_callback()
        self.destroy()

    def on_no(self):
        if self.on_no_callback:
            self.on_no_callback()
        self.destroy()


class EditItemWindow(tk.Toplevel):

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f'{width}x{height}+{x}+{y}')

    def on_close(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()

    def __init__(self, parent, original_item, equipment, quantity, potencia, autonomia, consumo, on_close=None):
        super().__init__(parent)
        self.original_item = original_item
        self.title("Editar Equipamento")
        self.resizable(False, False)
        self.geometry("350x300")
        self.on_close_callback = self.on_close
        self.center_window(350, 300)
        self.iconbitmap(icon_full_path)

        ttk.Label(self, text="Equipamento:").grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        self.equipamento_entry = ttk.Entry(self)
        self.equipamento_entry.grid(row=0, column=1, pady=(10, 5), sticky="ew")

        ttk.Label(self, text="Quantidade:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.quantity_spinbox = ttk.Spinbox(self, from_=1, to=100, increment=1, width=5)
        self.quantity_spinbox.set('1')
        self.quantity_spinbox.grid(row=1, column=1, pady=5, sticky="ew")

        ttk.Label(self, text="Potência (W):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.potencia_entry = ttk.Entry(self)
        self.potencia_entry.grid(row=2, column=1, pady=5, sticky="ew")

        ttk.Label(self, text="Autonomia (h):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.autonomia_spinbox = ttk.Spinbox(self, from_=1, to=24, increment=1, width=5)
        self.autonomia_spinbox.set('1')
        self.autonomia_spinbox.grid(row=3, column=1, pady=5, sticky="ew")

        self.equipamento_entry.insert(0, equipment)
        self.quantity_spinbox.set(quantity)
        self.potencia_entry.insert(0, potencia)
        self.autonomia_spinbox.set(autonomia)

        ttk.Button(self, text="Confirmar", style="Accent.TButton", command=self.update_item).grid(row=4, column=0, columnspan=2, pady=20)

    def update_item(self):
        equipment = self.equipamento_entry.get()
        quantity = self.quantity_spinbox.get()
        potencia = self.potencia_entry.get()
        autonomia = self.autonomia_spinbox.get()

        try:
            potencia_num = float(potencia)
            autonomia_num = float(autonomia)
            quantity_num = float(quantity)
            consumo = potencia_num * autonomia_num * quantity_num
        except ValueError:
            return

        updated_data = (equipment, quantity, potencia, autonomia, consumo)

        self.master.update_item_in_load_table(self.original_item, updated_data)

        self.destroy()

class AddManualItemWindow(tk.Toplevel):
    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f'{width}x{height}+{x}+{y}')

    def on_close(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()

    def __init__(self, parent, on_close=None):
        super().__init__(parent)
        self.title("Adicionar Equipamento")
        self.resizable(False, False)
        self.geometry("370x300")
        self.center_window(370, 300)
        self.iconbitmap(icon_full_path)
        self.on_close_callback = self.on_close
        self.create_widgets()

    def create_widgets(self):
        # Configurando os labels e campos de entrada em um grid
        ttk.Label(self, text="Equipamento:").grid(row=0, column=0, padx=20, pady=(10, 5), sticky="w")
        self.equipamento_entry = ttk.Entry(self)
        self.equipamento_entry.grid(row=0, column=1, pady=(10, 5), sticky="ew")

        ttk.Label(self, text="Quantidade:").grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.quantity_spinbox = ttk.Spinbox(self, from_=1, to=100, increment=1, width=5)
        self.quantity_spinbox.set('1')
        self.quantity_spinbox.grid(row=1, column=1, pady=5, sticky="ew")

        ttk.Label(self, text="Potência (W):").grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.potencia_entry = ttk.Entry(self)
        self.potencia_entry.grid(row=2, column=1, pady=5, sticky="ew")

        ttk.Label(self, text="Autonomia (h):").grid(row=3, column=0, padx=20, pady=5, sticky="w")
        self.autonomia_spinbox = ttk.Spinbox(self, from_=1, to=24, increment=1, width=5)
        self.autonomia_spinbox.set('1')
        self.autonomia_spinbox.grid(row=3, column=1, pady=5, sticky="ew")

        ttk.Button(self, text="Confirmar", style="Accent.TButton", command=self.confirm).grid(row=4, column=0, columnspan=2, pady=20)

    def confirm(self):
        equipment = self.equipamento_entry.get()
        quantity = self.quantity_spinbox.get()
        potencia = self.potencia_entry.get()
        autonomia = self.autonomia_spinbox.get()

        try:
            potencia_num = float(potencia)
            autonomia_num = float(autonomia)
            quantity_num = float(quantity)
            consumo = potencia_num * autonomia_num * quantity_num
        except ValueError:
            return

        self.master.add_to_load_table_manual(equipment, quantity, potencia, consumo, autonomia)
        self.destroy()

class AddItemWindow(tk.Toplevel):

    def __init__(self, parent, on_close=None):
        super().__init__(parent)
        self.title("Adicionar Equipamento")
        self.resizable(False, False)
        self.geometry("450x500")
        self.center_window(450, 500)
        self.iconbitmap(icon_full_path)
        self.on_close_callback = on_close
        self.create_widgets()
        self.load_equipment()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        # Tree View setup
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(pady=(20,10), padx=20, fill="both", expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Equipamento"), show="headings", height=5)
        self.tree.column("Equipamento", anchor="center")
        self.tree.heading("Equipamento", text="Equipamento")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree_scroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree_scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        self.tree.bind("<Double-1>", self.on_double_click)

        # Search and buttons setup
        self.search_frame = ttk.Frame(self)
        self.search_frame.pack(pady=(20, 20), padx=40, fill="x", expand=False)

        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True)

        self.search_button = ttk.Button(self.search_frame, text="Buscar", command=self.search_equipment)
        self.search_button.pack(side="left", padx=(10, 0))

        self.quantity_label = tk.Label(self, text="Quantidade:")
        self.quantity_label.pack()
        self.quantity_spinbox = ttk.Spinbox(self, from_=1, to=100, increment=1, width=10, wrap=True)
        self.quantity_spinbox.set('1')
        self.quantity_spinbox.pack()

        self.confirm_button = ttk.Button(self, text="Confirmar", command=self.confirm, style="Accent.TButton")
        self.confirm_button.pack(pady=(20, 30))

    def load_equipment(self, search_text=""):
        load_dotenv()
        api_key = os.getenv("SUPABASE_API_KEY")
        auth_key = os.getenv("SUPABASE_AUTH_KEY")
        url = "https://ktdmbdjzmisdtjhdlvnl.supabase.co/rest/v1/Catalogo de Cargas"
        headers = {
            "apikey": api_key,
            "Authorization": auth_key,
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        query_url = f"{url}?select=equipamento&order=equipamento.asc"

        response = requests.get(query_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.tree.delete(*self.tree.get_children())  # Clear existing tree
            filtered_data = [item['equipamento'] for item in data if search_text.lower() in unidecode(item['equipamento'].lower())]
            for equipment_name in sorted(filtered_data):  # Ensure the order is maintained
                self.tree.insert('', 'end', values=(equipment_name,))
        else:
            print(f"Erro ao carregar dados: {response.text}")

    def on_double_click(self, event):
        self.confirm()

    def search_equipment(self):
        search_text = self.search_entry.get()
        self.load_equipment(search_text)

    def confirm(self):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            if values:
                equipment, quantity = values[0], self.quantity_spinbox.get()
                self.master.add_to_load_table(equipment, quantity)
                self.destroy()
        else:
            tk.messagebox.showinfo("Alert", "Please select an item.")

    def on_close(self):
        if callable(self.on_close_callback):
            self.on_close_callback()
        self.destroy()