from assets.scripts.piano import PianoApp

if __name__ == "__main__":
    try:
        PianoApp().run()
    except Exception as e:
        print(f"Error starting PianoApp: {e}")
