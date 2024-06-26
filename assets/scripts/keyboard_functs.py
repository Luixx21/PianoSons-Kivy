class KeyboardFuncts:
    def __init__(self, piano_layout):
        self._keyboard = None
        self.stored_key = None
        self.notes = {'C', 'D', 'E', 'F', 'G', 'A', 'B'}  # Assuming these are valid musical notes
        self.piano_layout = piano_layout  # Assuming PianoLayout is the class or object to play notes

    def _keyboard_closed(self):
        # Unbind the keyboard event handler
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key_pressed = keycode[1]

        # Check if the pressed key is a valid musical note
        if key_pressed.upper() in self.notes:
            self.stored_key = key_pressed.upper()

        # Append numeric keys to stored_key if a valid note is already stored
        elif self.stored_key and key_pressed.isnumeric():
            self.stored_key += key_pressed

            try:
                # Attempt to play the note using the existing PianoLayout instance
                self.piano_layout.play_note(key_pressed=self.stored_key)
            except Exception as e:
                print(f"Error playing note: {e}")
                # Optionally handle the error (e.g., logging, notifying the user)
