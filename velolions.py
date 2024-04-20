import tkinter as tk
from tkinter import ttk
import speedtest
import requests

# Função para obter o IP público e o nome da operadora de internet
def get_public_ip_and_isp(progresso_var):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        progresso_var.set(20)  # Atualizar barra de progresso para 20%
        janela.update()  # Atualizar a janela para exibir a barra de progresso

        response = requests.get('https://ipinfo.io')
        data = response.json()
        ip = data.get('ip', 'Não foi possível obter o IP público')
        isp = data.get('org', 'Não foi possível obter o nome da operadora')

        progresso_var.set(50)  # Atualizar barra de progresso para 50%
        janela.update()  # Atualizar a janela para exibir a barra de progresso

        return ip, isp
    except Exception as e:
        print("Erro ao obter informações de IP e ISP:", e)
        return "Não foi possível obter o IP público", "Não foi possível obter o nome da operadora"

# Função para calcular a velocidade e o ping
def calcular_velocidade_e_ping(progresso_var):
    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        # Configurar a barra de progresso para 0%
        progresso_var.set(0)
        janela.update()  # Atualizar a janela para exibir a barra de progresso

        # Download
        progresso_var.set(25)  # Atualizar barra de progresso para 25%
        janela.update()  # Atualizar a janela para exibir a barra de progresso
        velocidade_download = st.download() / 1000000  # Mbps

        # Upload
        progresso_var.set(75)  # Atualizar barra de progresso para 75%
        janela.update()  # Atualizar a janela para exibir a barra de progresso
        velocidade_upload = st.upload() / 1000000  # Mbps

        # Ping
        progresso_var.set(100)  # Atualizar barra de progresso para 100%
        janela.update()  # Atualizar a janela para exibir a barra de progresso
        ping = st.results.ping  # ms

        return velocidade_download, velocidade_upload, ping
    except Exception as e:
        print("Erro:", e)
        return None, None, None

# Função para iniciar os testes
def iniciar_testes():
    info_label.config(text="Testando...")
    velocidade_var["download"].set("")
    velocidade_var["upload"].set("")
    ping_var.set("")
    ip_var.set("")
    isp_var.set("")
    progresso_var.set(0)  # Reiniciar a barra de progresso
    janela.update()  # Atualizar a janela para exibir a mensagem de teste em andamento

    ip, isp = get_public_ip_and_isp(progresso_var)
    velocidade_download, velocidade_upload, ping = calcular_velocidade_e_ping(progresso_var)

    if velocidade_download is not None and velocidade_upload is not None and ping is not None:
        velocidade_var["download"].set(f"{velocidade_download:.2f} Mbps")
        velocidade_var["upload"].set(f"{velocidade_upload:.2f} Mbps")
        ping_var.set(f"{ping} ms")
        ip_var.set(ip)
        isp_var.set(isp)
        info_label.config(text="Teste concluído, resultado:")
    else:
        info_label.config(text="Teste falhou. Por favor, tente novamente.")

# Cores
letras = "#FFFFFF"
fundo = "#FF0000"
cor_botao = "#8B0000"  # Cor mais escura para o botão
cor_barra_progresso = "#4CAF50"  # Cor verde para a barra de progresso

janela = tk.Tk()
janela.title("VeloLions SpeedTest")
janela.geometry("550x400")
janela.resizable(False, False)
janela.configure(background=fundo)

style = ttk.Style()
style.configure("TFrame", background=fundo)
style.configure("TLabel", background=fundo, foreground=letras, font=("Helvetica", 10))
style.configure("TButton", background=cor_botao, font=("Helvetica", 10))

frame_topo = ttk.Frame(janela)
frame_topo.pack(pady=(20, 50))

nome_label = ttk.Label(frame_topo, text="Teste a velocidade de sua internet", font=("Helvetica", 22, "bold"))
nome_label.pack(side="left")

frame_conteudo = ttk.Frame(janela)
frame_conteudo.pack(pady=(20, 20))

info_label = ttk.Label(frame_conteudo, text="Pressione o botão para iniciar o teste de velocidade", font=("Helvetica", 15))
info_label.grid(row=0, column=0, columnspan=3, padx=(0, 10))

download_label = ttk.Label(frame_conteudo, text="Velocidade de Download:", font=("Helvetica", 12))
download_label.grid(row=1, column=0, sticky='w', padx=(0, 5))

upload_label = ttk.Label(frame_conteudo, text="Velocidade de Upload:", font=("Helvetica", 12))
upload_label.grid(row=2, column=0, sticky='w', padx=(0, 5))

ping_label = ttk.Label(frame_conteudo, text="Ping:", font=("Helvetica", 12))
ping_label.grid(row=3, column=0, sticky='w', padx=(0, 5))

ip_label = ttk.Label(frame_conteudo, text="IP Público:", font=("Helvetica", 12))
ip_label.grid(row=4, column=0, sticky='w', padx=(0, 5))

isp_label = ttk.Label(frame_conteudo, text="Operadora:", font=("Helvetica", 12))
isp_label.grid(row=5, column=0, sticky='w', padx=(0, 5))

velocidade_var = {
    'download': tk.StringVar(),
    'upload': tk.StringVar(),
}

ping_var = tk.StringVar()
ip_var = tk.StringVar()
isp_var = tk.StringVar()

velocidade_download_label = ttk.Label(frame_conteudo, textvariable=velocidade_var["download"], font=("Helvetica", 9))
velocidade_download_label.grid(row=1, column=1, sticky='w')

velocidade_upload_label = ttk.Label(frame_conteudo, textvariable=velocidade_var["upload"], font=("Helvetica", 9))
velocidade_upload_label.grid(row=2, column=1, sticky='w')

ping_result_label = ttk.Label(frame_conteudo, textvariable=ping_var, font=("Helvetica", 9))
ping_result_label.grid(row=3, column=1, sticky='w')

ip_result_label = ttk.Label(frame_conteudo, textvariable=ip_var, font=("Helvetica", 9))
ip_result_label.grid(row=4, column=1, sticky='w')

isp_result_label = ttk.Label(frame_conteudo, textvariable=isp_var, font=("Helvetica", 9))
isp_result_label.grid(row=5, column=1, sticky='w')

progresso_var = tk.IntVar()
progresso_barra = ttk.Progressbar(frame_conteudo, orient='horizontal', length=200, mode='determinate', variable=progresso_var)
progresso_barra.grid(row=6, column=0, columnspan=3, pady=(10, 0))

iniciar_botao = ttk.Button(frame_conteudo, text="Iniciar Teste", command=iniciar_testes)
iniciar_botao.grid(row=7, column=0, columnspan=3, pady=(20, 0))

janela.mainloop()