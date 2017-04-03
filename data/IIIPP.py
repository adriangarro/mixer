#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
IIIPP.py: Mezclador de sonidos
'''

import pygame as pg
import tkinter as tk
import threading as th
import tkinter.ttk as ttk
import tkinter.messagebox as ms
import tkinter.simpledialog as sd

__author__ = 'E. Adrián Garro Sánchez (2014088081)'
__copyright__ = 'Copyright 2015, Tecnológico de Costa Rica'

DIMENSION = '800x600+300+100'

INSTRUMENTS = {
    'PLATILLO': [10, 11, 12, 13, 14, 15, 16],
    'GUITARRA': [20, 21, 22, 23, 24, 25, 26],
    'SAXOFON': [30, 31, 32, 33, 34, 35, 36],
    'VIOLIN': [40, 41, 42, 43, 44, 45, 46],
    'TAMBOR': [50, 51, 52, 53, 54, 55, 56],
    'FLAUTA': [60, 61, 62, 63, 64, 65, 66],
    'PIANO': [70, 71, 72, 73, 74, 75, 76],
    'BAJO': [80, 81, 82, 83, 84, 85, 86],
}

compositions_dictionary = {}

root = tk.Tk()

IMAGES = {
    'PLATILLO': tk.PhotoImage(file='PLATILLO.gif'),
    'GUITARRA': tk.PhotoImage(file='GUITARRA.gif'),
    'SAXOFON': tk.PhotoImage(file='SAXOFON.gif'),
    'VIOLIN': tk.PhotoImage(file='VIOLIN.gif'),
    'TAMBOR': tk.PhotoImage(file='TAMBOR.gif'),
    'FLAUTA': tk.PhotoImage(file='FLAUTA.gif'),
    'PIANO': tk.PhotoImage(file='PIANO.gif'),
    'BAJO': tk.PhotoImage(file='BAJO.gif'),
}

pg.mixer.pre_init(44100, 16, 8, 4096)  # frequency, size, channels, buffersize
pg.mixer.init()
pg.init()

codes_dictionary = {
    10: pg.mixer.Sound('10.wav'),
    11: pg.mixer.Sound('11.wav'),
    12: pg.mixer.Sound('12.wav'),
    13: pg.mixer.Sound('13.wav'),
    14: pg.mixer.Sound('14.wav'),
    15: pg.mixer.Sound('15.wav'),
    16: pg.mixer.Sound('16.wav'),
    20: pg.mixer.Sound('20.wav'),
    21: pg.mixer.Sound('21.wav'),
    22: pg.mixer.Sound('22.wav'),
    23: pg.mixer.Sound('23.wav'),
    24: pg.mixer.Sound('24.wav'),
    25: pg.mixer.Sound('25.wav'),
    26: pg.mixer.Sound('26.wav'),
    30: pg.mixer.Sound('30.wav'),
    31: pg.mixer.Sound('31.wav'),
    32: pg.mixer.Sound('32.wav'),
    33: pg.mixer.Sound('33.wav'),
    34: pg.mixer.Sound('34.wav'),
    35: pg.mixer.Sound('35.wav'),
    36: pg.mixer.Sound('36.wav'),
    40: pg.mixer.Sound('40.wav'),
    41: pg.mixer.Sound('41.wav'),
    42: pg.mixer.Sound('42.wav'),
    43: pg.mixer.Sound('43.wav'),
    44: pg.mixer.Sound('44.wav'),
    45: pg.mixer.Sound('45.wav'),
    46: pg.mixer.Sound('46.wav'),
    50: pg.mixer.Sound('50.wav'),
    51: pg.mixer.Sound('51.wav'),
    52: pg.mixer.Sound('52.wav'),
    53: pg.mixer.Sound('53.wav'),
    54: pg.mixer.Sound('54.wav'),
    55: pg.mixer.Sound('55.wav'),
    56: pg.mixer.Sound('56.wav'),
    60: pg.mixer.Sound('60.wav'),
    61: pg.mixer.Sound('61.wav'),
    62: pg.mixer.Sound('62.wav'),
    63: pg.mixer.Sound('63.wav'),
    64: pg.mixer.Sound('64.wav'),
    65: pg.mixer.Sound('65.wav'),
    66: pg.mixer.Sound('66.wav'),
    70: pg.mixer.Sound('70.wav'),
    71: pg.mixer.Sound('71.wav'),
    72: pg.mixer.Sound('72.wav'),
    73: pg.mixer.Sound('73.wav'),
    74: pg.mixer.Sound('74.wav'),
    75: pg.mixer.Sound('75.wav'),
    76: pg.mixer.Sound('76.wav'),
    80: pg.mixer.Sound('80.wav'),
    81: pg.mixer.Sound('81.wav'),
    82: pg.mixer.Sound('82.wav'),
    83: pg.mixer.Sound('83.wav'),
    84: pg.mixer.Sound('84.wav'),
    85: pg.mixer.Sound('85.wav'),
    86: pg.mixer.Sound('86.wav')
}


class Parser(tk.Frame):
    global compositions_dictionary

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.widgets()

    def widgets(self):
        '''Nombre.'''
        self.name = tk.Label(
            self.master,
            text='Nombre de la composición: ',
            height=5
        )
        self.name.grid(row=0, column=0, padx=20)

        self.entry_name = tk.Entry(
            self.master,
            width=30,
        )
        self.entry_name.grid(row=0, column=1)

        '''Estructura de la composición.'''
        self.label_composition = tk.Label(
            self.master,
            text='Estructura de la composición: ',
            height=5
        )
        self.label_composition.grid(row=1, column=0)

        self.entry_composition = tk.Text(
            self.master,
            height=20,
            width=40,
        )
        self.entry_composition.grid(row=1, column=1)

        def analyzer(dictionary, key):
            '''Función que verifica si una composición es válida.'''
            # lista de valores a revisar
            inspection_list = list(dictionary.values())[0]
            return aux_analyzer(dictionary, key, inspection_list)

        def aux_analyzer(
            dictionary,
            key,
            inspection_list,
            index=0,
            final_message=True
        ):
            '''Función auxiliar de analyzer.'''
            try:
                inspection_list[0][0] = inspection_list[0][0].upper()
                instrument = inspection_list[0][0]
            except:
                pass
            if not inspection_list:
                if final_message:
                    ms.showinfo(
                        title='Confirmación',
                        message='La composición fue creada con éxito.'
                    )
                return dictionary
            else:
                if not isinstance(inspection_list[0], list):
                    ms.showerror(
                        title='Error en la composición',
                        message='La sub estructura no es lista. Ubicación: índice de la lista número %d.'
                        % (index)
                    )
                    final_message = False
                    del dictionary[key]
                elif not isinstance(inspection_list[0][0], str):
                    ms.showerror(
                        title='Error en la composición',
                        message='El instrumento no es un cadena de caracteres. Ubicación: índice de la lista número %d.'
                        % (index)
                    )
                    final_message = False
                    del dictionary[key]
                elif inspection_list[0][0] not in INSTRUMENTS.keys():
                    ms.showerror(
                        title='Error en la composición',
                        message='Ha ingresado un instrumento inválido. Ubicación: índice de la lista número %d.'
                        % (index)
                    )
                    final_message = False
                    del dictionary[key]
                elif not isinstance(inspection_list[0][1], list):
                    ms.showerror(
                        title='Error en la composición',
                        message='Tiempo y tonos no están en una lista. Ubicación: índice de la lista número %d.'
                        % (index)
                    )
                    final_message = False
                    del dictionary[key]
                elif are_bloque_error(inspection_list[0][1], instrument):
                    ms.showerror(
                        title='Error en la composición',
                        message='Tiempo o tonos no son números. Ubicación: índice de la lista número %d.'
                        % (index)
                    )
                    final_message = False
                    del dictionary[key]
                return aux_analyzer(
                    dictionary,
                    key,
                    inspection_list[1:],
                    index + 1,
                    final_message
                )

        def are_bloque_error(inspection_list, instrument):
            '''
            Verifica que el tiempo entre tonos
            sea un número de punto flotante y que
            exista una lista de tonos en algún
            bloque de la composición.
            '''
            if not inspection_list:
                return None
            elif not isinstance(inspection_list[0][0], float):
                return True
            elif not isinstance(inspection_list[0][1], list):
                return True
            elif not_code(inspection_list[0][1], instrument):
                return True
            else:
                return are_bloque_error(inspection_list[1:], instrument)

        def not_code(inspection_list, instrument):
            '''Verifica si los códigos de tonos son válidos.'''
            if not inspection_list:
                return None
            elif not isinstance(inspection_list[0], int):
                return True
            elif inspection_list[0] not in INSTRUMENTS[instrument.upper()]:
                return True
            else:
                return not_code(inspection_list[1:], instrument)

        def get_structure():
            try:
                compositions_dictionary[self.entry_name.get()] = eval(
                    self.entry_composition.get("1.0", 'end-1c')
                )
                if not compositions_dictionary[self.entry_name.get()]:
                    ms.showerror(
                        title='Error en la composición',
                        message='La estructura está mal escrita.'
                    )
                    del compositions_dictionary[self.entry_name.get()]
                else:
                    analyzer(
                        compositions_dictionary,
                        self.entry_name.get()
                    )
                # [ ['Guitarra', [ [1.0, [21]], [2.0, [22]] ] ] ]
            except:
                ms.showerror(
                    title='Error en la composición',
                    message='La estructura está mal escrita.'
                )

        self.save = tk.Button(
            self.master,
            text='Guardar composición',
            command=get_structure
        )
        self.save.grid(
            row=1,
            column=2,
            padx=30
        )

        '''Eliminación de composición.'''
        def delete_key():
            key = sd.askstring(
                title='Borrar composición',
                prompt='Ingrese el nombre de la composición que desea borrar.'
            )
            if key in compositions_dictionary.keys():
                del compositions_dictionary[key]
                ms.showinfo(
                    title='Confirmación',
                    message='La composición fue borrada con éxito.'
                )
            else:
                ms.showerror(
                    title='Error de composición',
                    message='La composición no existe.'
                )

        self.delete = tk.Button(
            self.master,
            text='Borrar composición',
            command=delete_key
        )
        self.delete.grid(row=3, column=1, pady=30)


class Compositor(tk.Frame):
    global compositions_dictionary

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.widgets()
        self.instrument_index = 0
        self.block_index = 0
        self.sentinel = None

    def widgets(self):
        '''Nombre.'''
        def get_name():
            self.sentinel = True
            compositions_dictionary[self.name_entry.get()] = []
            self.structure_preview.configure(state='normal')
            self.structure_preview.insert('end', str(
                compositions_dictionary[self.name_entry.get()]
            ))
            self.structure_preview.configure(state='disabled')

            self.name_entry.config(state='disabled')
            self.name_save.config(state='disabled')

            self.instruments_box.config(state='readonly')
            self.instrument_start.config(state='normal')

            self.composition_end.configure(state='disabled')
            self.compositions_box.configure(state='disabled')

        self.name_label = tk.Label(
            self.master,
            text='Nombre de la composición: ',
            height=5
        )
        self.name_label.grid(row=0, column=1, padx=15)

        self.name_entry = tk.Entry(
            self.master,
            width=30,
            state='normal'
        )
        self.name_entry.grid(row=0, column=2)

        self.name_save = tk.Button(
            self.master,
            text='Guardar nombre',
            command=get_name
        )
        self.name_save.grid(row=0, column=3)

        '''Instrumento.'''
        def get_instrument():
            compositions_dictionary[
                self.name_entry.get()
            ].append(
                [self.instruments_box_value.get(), []]
            )

            self.structure_preview.configure(state='normal')
            self.structure_preview.delete("1.0", 'end')
            self.structure_preview.insert('end', str(
                compositions_dictionary[self.name_entry.get()]
            ))
            self.structure_preview.configure(state='disabled')

            self.instruments_box.config(state='disabled')
            self.instrument_start.config(state='disabled')
            self.instrument_end.config(state='disabled')

            self.time_entry.config(state='normal')
            self.block_start.config(state='normal')

            self.structure_save.configure(state='disabled')

        def finish_instrument():
            self.instrument_index += 1
            self.instruments_box.config(state='readonly')
            self.instrument_start.config(state='normal')
            self.instrument_end.config(state='disabled')
            self.block_start.config(state='disabled')
            self.block_end.configure(state='disabled')
            self.structure_save.configure(state='normal')
            self.master.unbind('<Key>')
            self.block_index = 0

        self.instrument_label = tk.Label(
            self.master,
            text='Instrumento:'
        )
        self.instrument_label.grid(row=1, column=1)

        self.instruments_box_value = tk.StringVar()
        self.instruments_box = ttk.Combobox(
            self.master,
            textvariable=self.instruments_box_value,
            state='readonly'
        )
        self.instruments_box['values'] = list(INSTRUMENTS.keys())
        self.instruments_box.current(0)
        self.instruments_box.grid(row=1, column=2, pady=20)

        self.instrument_start = tk.Button(
            self.master,
            text='Iniciar instrumento',
            command=get_instrument,
            state='disabled'
        )
        self.instrument_start.grid(
            row=1,
            column=3,
            padx=15
        )

        self.instrument_end = tk.Button(
            self.master,
            text='Finalizar instrumento',
            command=finish_instrument,
            state='disabled'
        )
        self.instrument_end.grid(row=1, column=4)

        '''Bloques.'''
        def start_block():
            try:
                time = float(self.time_entry.get())
            except:
                time = 1.0
                ms.showerror(
                    title='Error de tiempo',
                    message='Usted ha ingresado un dato inválido. El tiempo se ha asignado a uno.'
                )
                self.time_entry.delete(0, 'end')

            compositions_dictionary[
                self.name_entry.get()
            ][self.instrument_index][1].append(
                [time, []]
            )
            self.structure_preview.configure(state='normal')
            self.structure_preview.delete("1.0", 'end')
            self.structure_preview.insert('end', str(
                compositions_dictionary[self.name_entry.get()]
            ))
            self.structure_preview.configure(state='disabled')

            self.instrument_end.config(state='disabled')
            self.time_entry.config(state='disabled')
            self.block_start.config(state='disabled')
            self.block_end.config(state='disabled')

            self.master.bind('<Key>', code_detector)

            ms.showinfo(
                title='Información',
                message='Para agregar tonos presione las teclas del 0 al 6.'
            )

        self.time_label = tk.Label(
            self.master,
            text='Tiempo entre tonos:'
        )
        self.time_label.grid(row=2, column=1)

        self.time_entry = tk.Entry(
            self.master,
            width=10,
            state='disabled'
        )
        self.time_entry.grid(row=2, column=2, pady=30)

        self.block_start = tk.Button(
            self.master,
            text='Iniciar bloque',
            state='disabled',
            command=start_block
        )
        self.block_start.grid(row=2, column=3, padx=5)

        def end_block():
            self.block_index += 1
            self.time_entry.config(state='normal')
            self.block_start.config(state='normal')
            self.block_end.config(state='disabled')
            self.instrument_end.config(state='normal')
            self.master.unbind('<Key>')

        self.block_end = tk.Button(
            self.master,
            text='Finalizar bloque',
            state='disabled',
            command=end_block
        )
        self.block_end.grid(row=2, column=4)

        '''Código de tono.'''
        def code_detector(key):
            if key.char == '0':
                compositions_dictionary[
                    self.name_entry.get()
                ][self.instrument_index][1][self.block_index][1].append(
                    INSTRUMENTS[self.instruments_box_value.get()][0]
                )
                self.block_end.config(state='normal')
            elif key.char == '1':
                compositions_dictionary[
                    self.name_entry.get()
                ][self.instrument_index][1][self.block_index][1].append(
                    INSTRUMENTS[self.instruments_box_value.get()][1]
                )
                self.block_end.config(state='normal')
            elif key.char == '2':
                compositions_dictionary[
                    self.name_entry.get()
                ][self.instrument_index][1][self.block_index][1].append(
                    INSTRUMENTS[self.instruments_box_value.get()][2]
                )
                self.block_end.config(state='normal')
            elif key.char == '3':
                compositions_dictionary[
                    self.name_entry.get()
                ][self.instrument_index][1][self.block_index][1].append(
                    INSTRUMENTS[self.instruments_box_value.get()][3]
                )
                self.block_end.config(state='normal')
            elif key.char == '4':
                compositions_dictionary[
                    self.name_entry.get()
                ][self.instrument_index][1][self.block_index][1].append(
                    INSTRUMENTS[self.instruments_box_value.get()][4]
                )
                self.block_end.config(state='normal')
            elif key.char == '5':
                compositions_dictionary[
                    self.name_entry.get()
                ][self.instrument_index][1][self.block_index][1].append(
                    INSTRUMENTS[self.instruments_box_value.get()][5]
                )
                self.block_end.config(state='normal')
            elif key.char == '6':
                compositions_dictionary[
                    self.name_entry.get()
                ][self.instrument_index][1][self.block_index][1].append(
                    INSTRUMENTS[self.instruments_box_value.get()][6]
                )
                self.block_end.config(state='normal')

            self.structure_preview.configure(state='normal')
            self.structure_preview.delete("1.0", 'end')
            self.structure_preview.insert('end', str(
                compositions_dictionary[self.name_entry.get()]
            ))
            self.structure_preview.configure(state='disabled')

        '''Previsualización de la estructura.'''
        self.structure_label = tk.Label(
            self.master,
            text='Previsualización:'
        )
        self.structure_label.grid(row=3, column=1)

        self.structure_preview = tk.Text(
            self.master,
            width=32,
            height=15,
            state='disabled'
        )
        self.structure_preview.grid(row=3, column=2, pady=10)

        '''Guardar composición.'''
        def save_structure():
            self.sentinel = False
            # enceder botón de nombre.
            self.name_entry.configure(state='normal')
            self.name_save.configure(state='normal')
            # apagar botones.
            self.instruments_box.configure(state='disabled')
            self.instrument_start.configure(state='disabled')
            self.instrument_end.configure(state='disabled')
            self.time_entry.configure(state='disabled')
            self.block_start.configure(state='disabled')
            self.block_end.configure(state='disabled')
            self.structure_save.configure(state='disabled')
            # mensaje de confirmación.
            ms.showinfo(
                title='Confirmación',
                message='La composición ha sido guardada con éxito.'
            )
            # limpiar pantalla.
            self.name_entry.delete(0, 'end')
            self.time_entry.delete(0, 'end')
            self.structure_preview.configure(state='normal')
            self.structure_preview.delete("1.0", 'end')
            self.structure_preview.configure(state='disabled')
            # establecer índices en cero.
            self.instrument_index = 0
            self.block_index = 0
            # encender ComboBox de composiciones.
            self.compositions_box.configure(state='readonly')
            # encender botón de borrado.
            self.composition_end.configure(state='normal')

        self.structure_save = tk.Button(
            self.master,
            text='Guardar composición',
            state='disabled',
            command=save_structure
        )
        self.structure_save.grid(row=3, column=4)

        '''Borrar composición.'''
        def end_composition():
            try:
                del compositions_dictionary[self.compositions_box_value.get()]
                ms.showinfo(
                    title='Confirmación',
                    message='La composición fue borrada con éxito.'
                )
                self.compositions_box.set('')
            except:
                ms.showerror(
                    title='Advertencia',
                    message='La composición no existe.'
                )

        def update_box():
            keys_list = list(compositions_dictionary.keys())
            self.compositions_box['values'] = keys_list

        self.compositions_label = tk.Label(
            self.master,
            text='Composiciones:'
        )
        self.compositions_label.grid(row=4, column=1)

        self.compositions_box_value = tk.StringVar()
        self.compositions_box = ttk.Combobox(
            self.master,
            postcommand=update_box,
            textvariable=self.compositions_box_value,
            state='disabled'
        )
        self.compositions_box.grid(
            row=4,
            column=2,
            pady=15
        )

        def on_closing():
            if self.sentinel:
                del compositions_dictionary[self.name_entry.get()]
                ms.showerror(
                    title='Error',
                    message='La composición no puede ser creada.'
                )
            self.master.destroy()

        self.master.protocol('WM_DELETE_WINDOW', on_closing)

        self.composition_end = tk.Button(
            self.master,
            text='Borrar composición',
            state='disabled',
            command=end_composition
        )
        self.composition_end.grid(row=4, column=3)


class Player(tk.Frame):
    global compositions_dictionary

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.widgets()

    def widgets(self):
        '''Lectura de composiciones.'''
        def ui_generator():
            try:
                self.select.configure(state='disabled')
                self.compositions_box.configure(state='disabled')
                self.reset.configure(state='normal')

                self.structure_preview.configure(state='normal')
                self.structure_preview.delete("1.0", 'end')
                self.structure_preview.insert('end', str(
                    compositions_dictionary[self.compositions_box_value.get()]
                ))
                self.structure_preview.configure(state='disabled')

                composition_list = compositions_dictionary[self.compositions_box_value.get()]

                self.instrument_index = tk.IntVar()
                return aux_ui_generator(composition_list)
            except KeyError:
                return None

        def aux_ui_generator(composition_list, count=1):
            if not composition_list:
                return None
            else:
                instrument_str = composition_list[0][0]
                self.instrument_rb = ttk.Radiobutton(
                    self.master,
                    image=IMAGES[instrument_str],
                    variable=self.instrument_index,
                    value=count
                )
                self.instrument_rb.grid(row=count, column=1, padx=20)
                self.play_button = tk.Button(
                    self.master,
                    text='Reproducir',
                    command=sound_threadings
                )
                self.play_button.grid(row=count, column=2)
                self.stop_button = tk.Button(
                    self.master,
                    text='Pausar',
                    command=pg.mixer.pause
                )
                self.stop_button.grid(row=count, column=3, padx=20)
                return aux_ui_generator(composition_list[1:], count + 1)

        def update_box():
            keys_list = list(compositions_dictionary.keys())
            self.compositions_box['values'] = keys_list

        '''Selección de composición y generación de interfaz.'''
        self.compositions_label = tk.Label(
            self.master,
            text='Composiciones:'
        )
        self.compositions_label.grid(row=0, column=1)

        self.compositions_box_value = tk.StringVar()
        self.compositions_box = ttk.Combobox(
            self.master,
            postcommand=update_box,
            textvariable=self.compositions_box_value,
            state='readonly'
        )
        self.compositions_box.grid(row=0, column=2, padx=10, pady=20)

        self.select = tk.Button(
            self.master,
            text='Establecer composición',
            command=ui_generator
        )
        self.select.grid(row=0, column=3, padx=10)

        def player_reset():
            structure_window.destroy()
            self.master.destroy()
            player_app()

        self.reset = tk.Button(
            self.master,
            text='Resetear',
            state='disabled',
            command=player_reset
        )
        self.reset.grid(row=0, column=4)

        '''Visualización de la estructura.'''
        structure_window = tk.Tk()
        structure_window.title('Composiciones')
        structure_window.maxsize(300, 300)
        self.structure_preview = tk.Text(
            structure_window,
            width=50,
            height=30,
            state='disabled'
        )
        self.structure_preview.grid()

        '''Función para reproducir sonidos.'''
        def sound_generartor():
            pg.mixer.unpause()
            sub_structure = compositions_dictionary[self.compositions_box_value.get()][self.instrument_index.get() - 1][1]
            return aux_sound_generator(sub_structure)

        def aux_sound_generator(sub_structure):
            if not sub_structure:
                return None
            else:
                tones = sub_structure[0][1]
                play_tone(sub_structure, tones)
                return aux_sound_generator(sub_structure[1:])

        def play_tone(sub_structure, tones):
            if not tones:
                return None
            else:
                codes_dictionary[tones[0]].play()
                pg.time.delay(pow(10, 3) * int(sub_structure[0][0]))
                return play_tone(sub_structure, tones[1:])

        ''' Hilos.'''
        def sound_threadings():
            t = th.Thread(target=sound_generartor, args=[])
            t.start()

        '''Terminar sonidos cuando se cierra la ventana'''
        def on_closing2():
            pg.mixer.stop()
            structure_window.destroy()
            self.master.destroy()
        self.master.protocol('WM_DELETE_WINDOW', on_closing2)


class Main(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.widgets()

    def widgets(self):
        self.note_photo = tk.PhotoImage(file='music.gif')
        self.note_label = tk.Label(image=self.note_photo)
        self.note_label.image = self.note_photo
        self.note_label.pack(anchor='se')

        self.parser = tk.Button(
            self,
            text='Parseador',
            width=20,
            command=parser_app
        )
        self.parser.pack(
            side='top',
            pady=10
        )
        self.parser = tk.Button(
            self,
            text='Compositor',
            width=20,
            command=compositor_app
        )
        self.parser.pack(
            side='top',
            pady=10
        )
        self.parser = tk.Button(
            self,
            text='Reproductor',
            width=20,
            command=player_app
        )
        self.parser.pack(
            side='top',
            pady=10
        )

'''Ventanas principales.'''


def parser_app():
    parser_root = tk.Toplevel()
    parser_root.geometry(DIMENSION)
    parser_root.minsize(800, 600)
    parser_root.maxsize(800, 600)
    Parser(master=parser_root)
    parser_root.title('Parseador')


def compositor_app():
    compositor_root = tk.Toplevel()
    compositor_root.geometry(DIMENSION)
    compositor_root.minsize(800, 600)
    compositor_root.maxsize(800, 600)
    Compositor(master=compositor_root)
    compositor_root.title('Compositor')


def player_app():
    player_root = tk.Toplevel()
    player_root.geometry(DIMENSION)
    player_root.minsize(800, 600)
    Player(master=player_root)
    player_root.title('Reproductor')


def main():
    welcome = tk.Label(
        root,
        text='Bienvenido',
        font=('Segoe UI Light', 24),
        height=5
    )
    welcome.pack()
    root.geometry(DIMENSION)
    root.minsize(800, 600)
    root.maxsize(800, 600)
    Main(master=root)
    root.title('Mezclador')
    root.mainloop()

if __name__ == "__main__":
    main()
