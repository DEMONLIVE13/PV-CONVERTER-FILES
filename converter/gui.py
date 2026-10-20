"""Interfejs Tkinter/ttk; logika konwersji pozostaje w core.py."""
from pathlib import Path
from queue import Empty, Queue
from threading import Thread
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .core import ConversionError, REGISTRY, available_targets, execute


class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.busy = False
        self.results = Queue()
        self.source = tk.StringVar()
        self.output = tk.StringVar()
        self.target = tk.StringVar()
        self.status = tk.StringVar(value='Wybierz plik wejściowy i katalog zapisu.')
        root.title('Uniwersalny konwerter plików')
        root.minsize(640, 320)
        frame = ttk.Frame(root, padding=20)
        frame.grid(sticky='nsew')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text='Uniwersalny konwerter', font=('TkDefaultFont', 16, 'bold')).grid(
            row=0, column=0, columnspan=2, sticky='w', pady=(0, 16))
        ttk.Label(frame, text='Plik wejściowy:').grid(row=1, column=0, sticky='w')
        self.source_entry = ttk.Entry(frame, textvariable=self.source, width=65)
        self.source_entry.grid(row=2, column=0, sticky='ew', padx=(0, 10))
        self.source_button = ttk.Button(frame, text='Wybierz plik…', command=self.choose_source)
        self.source_button.grid(row=2, column=1, sticky='ew')
        ttk.Label(frame, text='Katalog zapisu:').grid(row=3, column=0, sticky='w', pady=(12, 0))
        self.output_entry = ttk.Entry(frame, textvariable=self.output)
        self.output_entry.grid(row=4, column=0, sticky='ew', padx=(0, 10))
        self.output_button = ttk.Button(frame, text='Wybierz katalog…', command=self.choose_output)
        self.output_button.grid(row=4, column=1, sticky='ew')
        ttk.Label(frame, text='Format docelowy:').grid(row=5, column=0, sticky='w', pady=(12, 0))
        self.formats = ttk.Combobox(frame, textvariable=self.target, state='disabled', width=16)
        self.formats.grid(row=6, column=0, sticky='w')
        self.convert_button = ttk.Button(frame, text='Konwertuj', command=self.convert, state='disabled')
        self.convert_button.grid(row=6, column=1, sticky='ew')
        ttk.Label(frame, text='Istniejące pliki są zachowywane; nowy wynik otrzyma przyrostek _1, _2 itd.').grid(
            row=7, column=0, columnspan=2, sticky='w', pady=(16, 8))
        self.progress = ttk.Progressbar(frame, mode='indeterminate')
        self.progress.grid(row=8, column=0, columnspan=2, sticky='ew')
        ttk.Label(frame, textvariable=self.status, wraplength=600).grid(
            row=9, column=0, columnspan=2, sticky='w', pady=(8, 0))
        self.source.trace_add('write', self.source_changed)
        self.output.trace_add('write', self.refresh)
        self.target.trace_add('write', self.refresh)
        root.protocol('WM_DELETE_WINDOW', self.close)

    def choose_source(self):
        extensions = ' '.join('*' + suffix for suffix in sorted({src for src, _ in REGISTRY}))
        selected = filedialog.askopenfilename(parent=self.root, title='Wybierz plik wejściowy',
                                             filetypes=[('Obsługiwane pliki', extensions), ('Wszystkie pliki', '*')])
        if selected:
            self.source.set(selected)

    def choose_output(self):
        selected = filedialog.askdirectory(parent=self.root, title='Wybierz katalog zapisu', mustexist=True)
        if selected:
            self.output.set(selected)

    def source_changed(self, *_):
        targets = available_targets(self.source.get())
        self.formats.configure(values=targets, state='readonly' if targets and not self.busy else 'disabled')
        self.target.set(targets[0] if targets else '')
        self.refresh()

    def validation_error(self):
        if not self.source.get() or not Path(self.source.get()).is_file():
            return 'Wybierz istniejący plik wejściowy.'
        if self.target.get() not in available_targets(self.source.get()):
            return 'Brak dostępnej konwersji dla tego pliku. Wybierz obsługiwany format wejściowy.'
        if not self.output.get() or not Path(self.output.get()).is_dir():
            return 'Wybierz istniejący katalog zapisu.'
        return ''

    def refresh(self, *_):
        if self.busy:
            return
        error = self.validation_error()
        self.convert_button.configure(state='disabled' if error else 'normal')
        self.status.set(error or 'Gotowe do konwersji.')

    def set_busy(self, value):
        self.busy = value
        for widget in (self.source_entry, self.output_entry, self.source_button, self.output_button):
            widget.configure(state='disabled' if value else 'normal')
        self.formats.configure(state='disabled' if value or not available_targets(self.source.get()) else 'readonly')
        if value:
            self.convert_button.configure(state='disabled')
            self.progress.start(12)
            self.status.set('Trwa konwersja…')
        else:
            self.progress.stop()
            self.refresh()

    def convert(self):
        if self.busy:
            return
        error = self.validation_error()
        if error:
            messagebox.showerror('Nie można rozpocząć konwersji', error, parent=self.root)
            self.refresh()
            return
        request = (self.source.get(), self.target.get(), self.output.get())
        self.set_busy(True)
        Thread(target=self.worker, args=request, daemon=True).start()
        self.root.after(100, self.poll_result)

    def worker(self, source, target, output):
        # Wątek roboczy nie wywołuje Tkintera; wynik odbiera główny wątek.
        try:
            self.results.put((True, str(execute(source, target, output))))
        except ConversionError as error:
            self.results.put((False, str(error)))
        except Exception as error:
            self.results.put((False, f'Nie udało się wykonać konwersji: {error}'))

    def poll_result(self):
        try:
            success, detail = self.results.get_nowait()
        except Empty:
            self.root.after(100, self.poll_result)
            return
        self.set_busy(False)
        if success:
            self.status.set(f'Zapisano: {detail}')
            messagebox.showinfo('Konwersja zakończona', f'Zapisano plik:\n{detail}', parent=self.root)
        else:
            self.status.set(f'Błąd: {detail}')
            messagebox.showerror('Błąd konwersji', detail, parent=self.root)

    def close(self):
        if self.busy:
            messagebox.showinfo('Trwa konwersja', 'Poczekaj na zakończenie konwersji przed zamknięciem okna.', parent=self.root)
        else:
            self.root.destroy()


def main():
    root = tk.Tk()
    ConverterApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
