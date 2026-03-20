import os
import subprocess
import psutil
from tkinter import messagebox, Tk, Toplevel, Label, ttk
import tkinter as tk
import webbrowser
import gdown
import requests
import tempfile
import sys
import threading
from dotenv import load_dotenv

versao = 1.01  # VERSÃO ATUAL DO APLICATIVO

# URL do instalador no Google Drive
INSTALLER_URL = 'https://drive.google.com/uc?export=download&id=1oL0Q6IFK8zlsSWO-sbOBeyyHHjW_eYID'

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

icon_path = "dimicon.ico"
icon_full_path = os.path.join(application_path, icon_path)

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

        yes_button = ttk.Button(button_frame, text="Instalar", command=self.on_yes, style="Accent.TButton")
        yes_button.pack(side="left", padx=10)

        no_button = ttk.Button(button_frame, text="Instalar manualmente", command=self.on_no)
        no_button.pack(side="left", padx=10)

    def on_yes(self):
        if self.on_yes_callback:
            self.on_yes_callback()
        self.destroy()

    def on_no(self):
        if self.on_no_callback:
            self.on_no_callback()
        self.destroy()

def download_file(url, output, progress_window, root):
    try:
        gdown.download(url, output, quiet=True)
        root.after(0, lambda: progress_window.destroy())
        return True
    except Exception as e:
        print(f"Erro ao baixar o arquivo: {e}")
        root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao baixar o arquivo: {e}"))
        root.after(0, lambda: progress_window.destroy())
        return False

def fechar_instancias_aplicativo(nome_aplicativo):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == nome_aplicativo:
            print(f"Fechando instância do aplicativo com PID: {proc.info['pid']}")
            proc.terminate()
            proc.wait()  # Aguarda o processo finalizar

def agendar_fechamento_aplicativo(nome_aplicativo, root):
    def fechar_aplicativo():
        fechar_instancias_aplicativo(nome_aplicativo)
        os._exit(0)
    root.after(2000, fechar_aplicativo)  # Aguarda 2 segundos antes de fechar o aplicativo

# Função para executar o instalador
def instalar_atualizacao(installer_path, root):
    try:
        print(f"Tentando executar o instalador em: {installer_path}")
        if os.path.exists(installer_path) and os.path.getsize(installer_path) > 0:
            print(f"O instalador existe e tem tamanho {os.path.getsize(installer_path)} bytes")
            subprocess.Popen([installer_path], shell=True)
            agendar_fechamento_aplicativo('Dimensionamentos.exe', root)
        else:
            print("O instalador não foi encontrado ou está corrompido.")
            messagebox.showerror("Erro", "O instalador não foi encontrado ou está corrompido. Por favor, tente novamente.")
    except Exception as e:
        print(f"Erro ao executar o instalador: {e}")
        messagebox.showerror("Erro", f"Erro ao executar o instalador: {e}")

# Função para verificar atualizações
def verificar_atualizacoes(root):
    global versao
    load_dotenv()
    api_key = os.getenv("SUPABASE_API_KEY")
    auth_key = os.getenv("SUPABASE_AUTH_KEY")
    url = "https://ktdmbdjzmisdtjhdlvnl.supabase.co/rest/v1/Atualizacoes"
    headers = {
        "apikey": api_key,
        "Authorization": auth_key,
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}")
        messagebox.showerror("Erro", "Não foi possível verificar atualizações. Erro HTTP.")
        return
    except Exception as err:
        print(f"Erro de rede: {err}")
        messagebox.showerror("Erro", "Não foi possível verificar atualizações. Erro de rede.")
        return

    if data:
        latest_version = max(item['versao'] for item in data)
        update_info = next(item for item in data if item['versao'] == latest_version)

        if update_info['bloquear_app']:
            messagebox.showwarning("Bloqueio de Aplicativo", "O aplicativo está em manutenção, por favor tente novamente mais tarde.")
            try:
                root.master.destroy()
            except:
                root.destroy()
        else:
            aviso = update_info.get('aviso', '')
            if aviso:
                messagebox.showinfo("Aviso", aviso)

            if latest_version > versao:
                def iniciar_atualizacao():
                    progress_root = Tk()
                    progress_root.withdraw()  # Esconde a janela principal do Tkinter para o progresso
                    progress_window = Toplevel(progress_root)
                    progress_window.title("Atualização")
                    progress_window.resizable(False, False)

                    progress_window.iconbitmap(icon_full_path)

                    # Configurações de tamanho e posição da janela
                    window_width = 400
                    window_height = 120
                    screen_width = progress_window.winfo_screenwidth()
                    screen_height = progress_window.winfo_screenheight()
                    center_x = int((screen_width / 2) - (window_width / 2))
                    center_y = int((screen_height / 2) - (window_height / 2))
                    progress_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

                    label = Label(progress_window, text="A atualização está sendo baixada e será inicializada automaticamente. Por favor, aguarde, isso pode levar alguns minutos.", wraplength=350)
                    label.pack(padx=20, pady=20)
                    progress_window.update_idletasks()  # Atualiza a janela para garantir que o texto apareça

                    def iniciar_download():
                        temp_dir = tempfile.mkdtemp()
                        installer_path = os.path.join(temp_dir, 'Instalador.exe')
                        download_successful = download_file(INSTALLER_URL, installer_path, progress_window, root)
                        if download_successful:
                            root.after(0, lambda: instalar_atualizacao(installer_path, root))

                    # Inicia uma thread separada para o download
                    threading.Thread(target=iniciar_download, daemon=True).start()

                if update_info['bloquear_versao_antiga']:
                    messagebox.showinfo("Atualização Disponível",
                                        "Uma nova versão está disponível. Por favor, atualize o aplicativo para continuar.")
                    try:
                        root.master.destroy()
                    except:
                        root.destroy()

                    iniciar_atualizacao()
                else:
                    if messagebox.askyesno("Atualização Disponível", "Uma nova versão está disponível. Deseja atualizar agora?"):

                        def on_yes():
                            iniciar_atualizacao()

                        def on_no():
                            webbrowser.open(INSTALLER_URL)

                        popup = YesNoPopup(root, "Escolha uma opção", "Você deseja atualizar o aplicativo automaticamente ou baixar o arquivo de instalação manualmente?",
                                           on_yes_callback=on_yes, on_no_callback=on_no)
                        popup.grab_set()

                        try:
                            root.master.withdraw()
                        except:
                            root.withdraw()

    else:
        messagebox.showerror("Erro", "Não foi possível verificar atualizações. Nenhum dado retornado.")
