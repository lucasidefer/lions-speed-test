import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import requests
import subprocess
import speedtest


# IP e nome da operadora
def get_public_ip_and_isp(progresso_var):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        progresso_var.set(20)
        janela.update()

        response = requests.get('https://ipinfo.io')
        data = response.json()
        ip = data.get('ip', 'Não foi possível obter o IP público')
        isp = data.get('org', 'Não foi possível obter o nome da operadora')

        progresso_var.set(50)
        janela.update()

        return ip, isp
    except Exception as e:
        print("Erro ao obter informações de IP e ISP:", e)
        return "Não foi possível obter o IP público", "Não foi possível obter o nome da operadora"


# calcular a velocidade e o ping
def calcular_velocidade_e_ping(progresso_var):
    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        progresso_var.set(0)
        janela.update()

        # Download
        progresso_var.set(25)
        janela.update()
        velocidade_download = st.download() / 1000000

        # Upload
        progresso_var.set(75)
        janela.update()
        velocidade_upload = st.upload() / 1000000

        # Ping
        progresso_var.set(100)
        janela.update()
        ping = st.results.ping

        return velocidade_download, velocidade_upload, ping
    except Exception as e:
        print("Erro:", e)
        return None, None, None


# Obter as informações de MAC
def get_mac_info():
    try:
        result = subprocess.run('getmac', shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print("Erro ao obter informações de MAC:", e)
        return "Não foi possível obter as informações de MAC"


# iniciar os testes
def iniciar_testes():
    info_label.config(text="Testando...")
    velocidade_var["download"].set("")
    velocidade_var["upload"].set("")
    ping_var.set("")
    ip_var.set("")
    isp_var.set("")
    mac_var.set("")
    progresso_var.set(0)
    janela.update()

    ip, isp = get_public_ip_and_isp(progresso_var)
    velocidade_download, velocidade_upload, ping = calcular_velocidade_e_ping(progresso_var)
    mac_info = get_mac_info()

    if velocidade_download is not None and velocidade_upload is not None and ping is not None:
        velocidade_var["download"].set(f"{velocidade_download:.2f} Mbps")
        velocidade_var["upload"].set(f"{velocidade_upload:.2f} Mbps")
        ping_var.set(f"{ping} ms")
        ip_var.set(ip)
        isp_var.set(isp)
        mac_var.set(mac_info)
        info_label.config(text="Resultado:")
    else:
        info_label.config(text="Teste falhou. Por favor, tente novamente.")


# Cores
letras = "#483D8B"
fundo = "#FFEFD5"
cor_botao = "#8B0000"
cor_barra_progresso = "#4CAF50"

janela = tk.Tk()
janela.title("VeloLions SpeedTest")
icon = tk.PhotoImage(file="./src/img/speed.png")
janela.iconphoto(True, icon)
janela.geometry("950x600")
janela.resizable(False, False)
janela.configure(background=fundo)

style = ttk.Style()
style.configure("TFrame", background=fundo)
style.configure("TLabel", background=fundo, foreground=letras, font=("MS Reference Sans Serif", 10))
style.configure("TButton", background=cor_botao, font=("MS Reference Sans Serif", 15))
background_image = PhotoImage(file="./src/img/back.png")

frame_topo = ttk.Frame(janela)
frame_topo.pack(pady=(20, 50))

nome_label = ttk.Label(frame_topo, text="TESTE A VELOCIDADE DE SUA INTERNET!", font=("MS Reference Sans Serif", 22, "bold"))
nome_label.pack(side="left")

background_label = tk.Label(janela, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

frame_conteudo = ttk.Frame(janela)
frame_conteudo.pack(pady=(20, 20))

info_label = ttk.Label(frame_conteudo, text="Pressione o botão para iniciar o teste de velocidade", font=("MS Reference Sans Serif", 15))
info_label.grid(row=0, column=0, columnspan=3, padx=(0, 10))

download_label = ttk.Label(frame_conteudo, text="Velocidade de Download:", font=("MS Reference Sans Serif", 12))
download_label.grid(row=1, column=0, sticky='w', padx=(0, 5))

upload_label = ttk.Label(frame_conteudo, text="Velocidade de Upload:", font=("MS Reference Sans Serif", 12))
upload_label.grid(row=2, column=0, sticky='w', padx=(0, 5))

ping_label = ttk.Label(frame_conteudo, text="Ping:", font=("MS Reference Sans Serif", 12))
ping_label.grid(row=3, column=0, sticky='w', padx=(0, 5))

ip_label = ttk.Label(frame_conteudo, text="IP Público:", font=("MS Reference Sans Serif", 12))
ip_label.grid(row=4, column=0, sticky='w', padx=(0, 5))

isp_label = ttk.Label(frame_conteudo, text="Operadora:", font=("MS Reference Sans Serif", 12))
isp_label.grid(row=5, column=0, sticky='w', padx=(0, 5))

mac_label = ttk.Label(frame_conteudo, text="Endereço MAC:", font=("MS Reference Sans Serif", 12))
mac_label.grid(row=6, column=0, sticky='w', padx=(0, 5))

velocidade_var = {
    'download': tk.StringVar(),
    'upload': tk.StringVar(),
}

ping_var = tk.StringVar()
ip_var = tk.StringVar()
isp_var = tk.StringVar()
mac_var = tk.StringVar()

velocidade_download_label = ttk.Label(frame_conteudo, textvariable=velocidade_var["download"], font=("MS Reference Sans Serif", 9))
velocidade_download_label.grid(row=1, column=1, sticky='w')

velocidade_upload_label = ttk.Label(frame_conteudo, textvariable=velocidade_var["upload"], font=("MS Reference Sans Serif", 9))
velocidade_upload_label.grid(row=2, column=1, sticky='w')

ping_result_label = ttk.Label(frame_conteudo, textvariable=ping_var, font=("MS Reference Sans Serif", 9))
ping_result_label.grid(row=3, column=1, sticky='w')

ip_result_label = ttk.Label(frame_conteudo, textvariable=ip_var, font=("MS Reference Sans Serif", 9))
ip_result_label.grid(row=4, column=1, sticky='w')

isp_result_label = ttk.Label(frame_conteudo, textvariable=isp_var, font=("MS Reference Sans Serif", 9))
isp_result_label.grid(row=5, column=1, sticky='w')

mac_result_label = ttk.Label(frame_conteudo, textvariable=mac_var, font=("MS Reference Sans Serif", 9))
mac_result_label.grid(row=6, column=1, sticky='w')

progresso_var = tk.IntVar()
progresso_barra = ttk.Progressbar(frame_conteudo, orient='horizontal', length=400, mode='determinate', variable=progresso_var)
progresso_barra.grid(row=7, column=0, columnspan=3, pady=(10, 0))

iniciar_botao = ttk.Button(frame_conteudo, text="Iniciar Teste", command=iniciar_testes, width=10,)
iniciar_botao.grid(row=8, column=0, columnspan=3, pady=(20, 0))

janela.mainloop()
