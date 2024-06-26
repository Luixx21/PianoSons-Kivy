from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from .keyboard_functs import KeyboardFuncts
from kivy.core.window import Window

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
                if i == 4 and note == "":
                    note = "Piano"
                if note == "" or note == "Piano":
                    button = Button(text=note, background_color=(0, 0, 0, 0.5))
                else:
                    button = Button(text=note + str(i), background_color=(1, 1, 1, 0.5))
                button.bind(on_press=self.play_note)
                grid_layout.add_widget(button)

                sound = SoundLoader.load(f'./assets/sounds/notes/{button.text}.wav')
                if sound:
                    self.sounds[button.text] = sound
        
        # Initialize KeyboardFuncts with self (PianoLayout instance)
        self.keyboard_functs = KeyboardFuncts(piano_layout=self)
        self.start_keyboard()
    
    def start_keyboard(self):
        # Request the keyboard and bind the keyboard event handler
        self._keyboard = Window.request_keyboard(self.keyboard_functs._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.keyboard_functs._on_keyboard_down)
    
    def play_note(self, instance=None, key_pressed=None):
        if instance: note_text = instance.text
        else: note_text = key_pressed
        try:
            sound = self.sounds.get(note_text)
            if sound:
                sound.play()
        except Exception as e:
            print(f"Error loading or playing note {note_text}: {e}")

class PianoApp(App):
    def build(self): return PianoLayout()

"""C: Dó
D: Ré
E: Mi
F: Fá
G: Sol
A: Lá
B: Si"""