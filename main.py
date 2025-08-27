import keyboard
import pyperclip
import openai
from openai import OpenAI
import time
import threading


class SpellChecker:
    def __init__(self, api_key):
        """
        Inicjalizacja korektora literówek

        Args:
            api_key (str): Klucz API do OpenAI
        """
        self.client = OpenAI(api_key=api_key)
        self.is_processing = False

    def get_selected_text(self):
        """
        Pobiera zaznaczony tekst używając Ctrl+C
        """
        try:
            # Zapisz obecną zawartość schowka
            original_clipboard = pyperclip.paste()

            # Wyczyść schowek
            pyperclip.copy("")

            # Symuluj Ctrl+C żeby skopiować zaznaczony tekst
            keyboard.send('ctrl+c')

            # Poczekaj chwilę na skopiowanie
            time.sleep(0.1)

            # Pobierz nową zawartość schowka
            selected_text = pyperclip.paste()

            # Przywróć oryginalną zawartość schowka jeśli nic nie było zaznaczone
            if not selected_text.strip():
                pyperclip.copy(original_clipboard)
                return None

            return selected_text

        except Exception as e:
            print(f"Błąd podczas pobierania tekstu: {e}")
            return None

    def correct_spelling(self, text):
        """
        Poprawia literówki używając OpenAI API

        Args:
            text (str): Tekst do korekty

        Returns:
            str: Poprawiony tekst lub None w przypadku błędu
        """
        try:
            prompt = """Popraw tylko literówki w podanym tekście. Nie zmieniaj treści, stylu, formatowania ani struktury tekstu. 
Zwróć tylko poprawiony tekst bez żadnych dodatkowych komentarzy czy wyjaśnień.

Tekst do korekty:
"""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Możesz zmienić na gpt-4 jeśli masz dostęp
                messages=[
                    {"role": "system",
                     "content": "Jesteś korektorem tekstu. Poprawiasz tylko literówki, nie zmieniając treści ani stylu."},
                    {"role": "user", "content": prompt + text}
                ],
                max_tokens=len(text.split()) * 2,  # Zapas na poprawki
                temperature=0.1  # Niska temperatura dla większej precyzji
            )

            corrected_text = response.choices[0].message.content.strip()
            return corrected_text

        except Exception as e:
            print(f"Błąd podczas korekty tekstu: {e}")
            return None

    def replace_selected_text(self, corrected_text):
        """
        Zastępuje zaznaczony tekst poprawionym tekstem

        Args:
            corrected_text (str): Poprawiony tekst
        """
        try:
            # Skopiuj poprawiony tekst do schowka
            pyperclip.copy(corrected_text)

            # Wklej poprawiony tekst (zastąpi zaznaczony tekst)
            keyboard.send('ctrl+v')

            print("✓ Tekst został poprawiony i wklejony")

        except Exception as e:
            print(f"Błąd podczas wklejania tekstu: {e}")

    def process_correction(self):
        """
        Główna funkcja przetwarzająca korektę tekstu
        """
        if self.is_processing:
            print("⚠ Korekta już w toku...")
            return

        self.is_processing = True
        print("🔄 Rozpoczynam korektę...")

        try:
            # Pobierz zaznaczony tekst
            selected_text = self.get_selected_text()

            if not selected_text:
                print("⚠ Nie zaznaczono żadnego tekstu")
                return

            print(f"📝 Pobieram tekst: {selected_text[:50]}{'...' if len(selected_text) > 50 else ''}")

            # Popraw literówki
            corrected_text = self.correct_spelling(selected_text)

            if not corrected_text:
                print("❌ Nie udało się poprawić tekstu")
                return

            # Sprawdź czy tekst się zmienił
            if selected_text.strip() == corrected_text.strip():
                print("✓ Tekst nie zawierał literówek")
                return

            # Zastąp tekst poprawionym
            self.replace_selected_text(corrected_text)

        except Exception as e:
            print(f"❌ Błąd podczas przetwarzania: {e}")

        finally:
            self.is_processing = False

    def start_hotkey_listener(self):
        """
        Rozpoczyna nasłuchiwanie kombinacji Ctrl+Q
        """
        print("🚀 Korektor literówek uruchomiony!")
        print("📋 Zaznacz tekst i naciśnij Ctrl+Q aby poprawić literówki")
        print("🛑 Naciśnij Ctrl+Shift+Q aby zakończyć program")

        # Rejestruj hotkey dla korekty
        keyboard.add_hotkey('ctrl+q', self.process_correction)

        # Rejestruj hotkey dla wyjścia
        keyboard.add_hotkey('ctrl+shift+q', self.stop_program)

        # Utrzymuj program w działaniu
        keyboard.wait()

    def stop_program(self):
        """
        Kończy działanie programu
        """
        print("\n👋 Zamykam korektor literówek...")
        keyboard.unhook_all()
        exit()


def main():
    # UWAGA: Wstaw tutaj swój klucz API OpenAI
    API_KEY = "your-openai-api-key-here"

    if API_KEY == "your-openai-api-key-here":
        print("❌ Błąd: Musisz wstawić swój klucz API OpenAI w zmiennej API_KEY")
        print("💡 Pobierz klucz z: https://platform.openai.com/api-keys")
        return

    try:
        # Utwórz instancję korektora
        spell_checker = SpellChecker(API_KEY)

        # Uruchom nasłuchiwanie hotkeys
        spell_checker.start_hotkey_listener()

    except KeyboardInterrupt:
        print("\n👋 Program zakończony przez użytkownika")
    except Exception as e:
        print(f"❌ Błąd: {e}")


if __name__ == "__main__":
    main()
