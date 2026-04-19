from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from .keyboard_functs import KeyboardFuncts
from kivy.core.window import Window

from threading import Thread
import pygame
import os

# Inicializa o pygame mixer (uma vez só, no início)
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

class PianoLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(PianoLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.notes = ["", "C", "D", "E", "F", "G", "A", "B"]
        self.stored_key = None
        self.sounds = {}

        grid_layout = GridLayout(cols=8, spacing=5, padding=5, size_hint_y=0.8)
        self.add_widget(grid_layout)

        for i in range(0, 8):
            for note in self.notes:
                note_name = note + str(i)

                if i == 4 and note == "": note = "Piano"

                if note == "" or note == "Piano":
                    button = Button(text=note, background_color=(0, 0, 0, 0.5))
                else:
                    button = Button(text=note_name, background_color=(1, 1, 1, 0.5))
                button.bind(on_press=self.play_note)
                grid_layout.add_widget(button)

                self.preload_sounds()

                sound_path = f'./assets/sounds/notes/{note_name}.wav'

                if os.path.exists(sound_path):
                    sound = pygame.mixer.Sound(sound_path)                
        
        # Initialize KeyboardFuncts with self (PianoLayout instance)
        self.keyboard_functs = KeyboardFuncts(piano_layout=self)
        self.start_keyboard()

    def preload_sounds(self):
        """Carrega todos os sons na memória com pygame.mixer"""
        for i in range(0, 8):
            for note in self.notes:
                if note and note != "Piano":
                    note_name = note + str(i)
                    sound_path = f'./assets/sounds/notes/{note_name}.wav'
                    if os.path.exists(sound_path):
                        sound = pygame.mixer.Sound(sound_path)
                        self.sounds[note_name] = sound
    
    def start_keyboard(self):
        # Request the keyboard and bind the keyboard event handler
        self._keyboard = Window.request_keyboard(self.keyboard_functs._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.keyboard_functs._on_keyboard_down)
    
    def play_note(self, instance=None, key_pressed=None):
        if instance: note_text = instance.text
        else: note_text = key_pressed

        try:
            sound = self.sounds.get(note_text)
            if sound: sound.play()

        except Exception as e:
            print(f"Error loading or playing note {note_text}: {e}")

    def play_note(self, instance=None, key_pressed=None):
        """Toca a nota em uma thread separada"""
        if instance:
            note_text = instance.text
        else:
            note_text = key_pressed

        # Executa em thread para não travar a UI
        Thread(target=self._play_sound, args=(note_text,), daemon=True).start()

    def _play_sound(self, note_text):
        """Método auxiliar para tocar som com pygame"""
        try:
            sound = self.sounds.get(note_text)
            if sound:
                sound.play()
            else:
                # Se não estiver pré-carregado, tenta carregar agora
                sound_path = f'./assets/sounds/notes/{note_text}.wav'
                if os.path.exists(sound_path):
                    sound = pygame.mixer.Sound(sound_path)
                    self.sounds[note_text] = sound
                    sound.play()
                else:
                    print(f"Arquivo não encontrado: {sound_path}")
        except Exception as e:
            print(f"Erro ao tocar nota {note_text}: {e}")

class PianoApp(App):
    def build(self): return PianoLayout()

"""C: Dó
D: Ré
E: Mi
F: Fá
G: Sol
A: Lá
B: Si

cc gg ff g
ff ee dd c
gg ff ee d
gg ff ee d
cc gg ff g
ff ee dd c
"""
