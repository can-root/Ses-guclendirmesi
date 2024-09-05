import tkinter as tk
from tkinter import PhotoImage
import subprocess
import platform

class SesKontrolUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Bass Güçlendirmesi")
        self.root.geometry('800x600')
        self.root.configure(bg='#2e2e2e')

        self.baslik_label = tk.Label(
            root, text="Bass Kontrolü", font=('Helvetica', 24, 'bold'), fg='#ffffff', bg='#2e2e2e'
        )
        self.baslik_label.pack(pady=40)

        self.cikis_slider = tk.Scale(
            root, from_=0, to_=1200, orient=tk.HORIZONTAL, label="Ses Çıkışı",
            font=('Helvetica', 18), fg='#ffffff', bg='#2e2e2e', troughcolor='#3a3a3a', sliderlength=40, length=600
        )
        self.cikis_slider.pack(fill=tk.X, padx=40)
        self.cikis_slider.bind("<Motion>", self.seviye_degistir)

        self.cikis_label = tk.Label(
            root, text="0%", font=('Helvetica', 18), fg='#ffffff', bg='#2e2e2e'
        )
        self.cikis_label.pack(pady=10)

        self.alt_çerçeve = tk.Frame(root, bg='#2e2e2e')
        self.alt_çerçeve.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False, pady=20)

        self.resim = PhotoImage(file="sablon.png")
        self.resim_label = tk.Label(self.alt_çerçeve, image=self.resim, bg='#2e2e2e')
        self.resim_label.pack()

        self.isletim_sistemi = platform.system()
        self.ses_seviyesini_guncelle()

    def seviye_degistir(self, event):
        seviye = self.cikis_slider.get()
        self.ses_seviyesini_ayarla(seviye)
        self.cikis_label.config(text=f"{seviye}%")
        self.slider_rengini_guncelle(seviye)

    def ses_seviyesini_ayarla(self, seviye):
        if self.isletim_sistemi == 'Windows':
            subprocess.run([
                'powershell', '-Command',
                f"(New-Object -ComObject SAPI.SpVoice).Volume = {seviye / 100 * 255}"
            ])
        elif self.isletim_sistemi == 'Darwin':
            subprocess.run(['osascript', '-e', f'set volume output volume {seviye}'])
        elif self.isletim_sistemi == 'Linux':
            subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', f'{seviye}%'])

    def ses_seviyesini_guncelle(self):
        seviye = 0
        if self.isletim_sistemi == 'Windows':
            result = subprocess.run([
                'powershell', '-Command',
                "(New-Object -ComObject SAPI.SpVoice).Volume / 255 * 100"
            ], capture_output=True, text=True)
            seviye = int(float(result.stdout.strip()))
        elif self.isletim_sistemi == 'Darwin':
            result = subprocess.run(['osascript', '-e', 'output volume of (get volume settings)'], capture_output=True, text=True)
            seviye = int(result.stdout.strip())
        elif self.isletim_sistemi == 'Linux':
            result = subprocess.run(['pactl', 'get-sink-volume', '@DEFAULT_SINK@'], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if 'Volume:' in line:
                    seviye = int(line.split()[4].strip('[]%'))

        self.cikis_slider.set(seviye)
        self.cikis_label.config(text=f"{seviye}%")
        self.slider_rengini_guncelle(seviye)

    def slider_rengini_guncelle(self, seviye):
        if 0 <= seviye <= 100:
            renk = '#00FF00'
        elif 100 < seviye <= 300:
            renk = '#FFFF00'
        elif 300 < seviye <= 400:
            renk = '#FFA500'
        elif 400 < seviye <= 1201:
            renk = '#FF0000'
        else:
            renk = '#3a3a3a'

        self.cikis_slider.config(troughcolor=renk)

if __name__ == "__main__":
    root = tk.Tk()
    uygulama = SesKontrolUygulamasi(root)
    root.mainloop()
