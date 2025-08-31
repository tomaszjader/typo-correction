import keyboard
import pyperclip
import google.generativeai as genai
import time
import os
from dotenv import load_dotenv

load_dotenv()


class SpellChecker:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.is_processing = False

    def get_selected_text(self):
        try:
            original_clipboard = pyperclip.paste()
            pyperclip.copy("")
            keyboard.send('ctrl+c')
            time.sleep(0.1)
            selected_text = pyperclip.paste()
            
            if not selected_text.strip():
                pyperclip.copy(original_clipboard)
                return None

            return selected_text

        except Exception as e:
            print(f"Error getting text: {e}")
            return None

    def correct_spelling(self, text):
        try:
            prompt = f"""Fix only spelling errors in the given text. Do not change content, style, formatting or text structure. 
Return only the corrected text without any additional comments or explanations.

Text to correct:
{text}"""

            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=len(text.split()) * 2,
                    temperature=0.1
                )
            )

            corrected_text = response.text.strip()
            return corrected_text

        except Exception as e:
            print(f"Error correcting text: {e}")
            return None

    def replace_selected_text(self, corrected_text):
        try:
            pyperclip.copy(corrected_text)
            keyboard.send('ctrl+v')
            print("✓ Text corrected and pasted")

        except Exception as e:
            print(f"Error pasting text: {e}")

    def process_correction(self):
        if self.is_processing:
            print("⚠ Correction already in progress...")
            return

        self.is_processing = True
        print("🔄 Starting correction...")

        try:
            selected_text = self.get_selected_text()

            if not selected_text:
                print("⚠ No text selected")
                return

            print(f"📝 Processing text: {selected_text[:50]}{'...' if len(selected_text) > 50 else ''}")

            corrected_text = self.correct_spelling(selected_text)

            if not corrected_text:
                print("❌ Failed to correct text")
                return

            if selected_text.strip() == corrected_text.strip():
                print("✓ Text contained no spelling errors")
                return

            self.replace_selected_text(corrected_text)

        except Exception as e:
            print(f"❌ Error during processing: {e}")

        finally:
            self.is_processing = False

    def start_hotkey_listener(self):
        print("🚀 Spell checker started!")
        print("📋 Select text and press Ctrl+Q to correct spelling")
        print("🛑 Press Ctrl+Shift+Q to exit program")

        keyboard.add_hotkey('ctrl+q', self.process_correction)
        keyboard.add_hotkey('ctrl+shift+q', self.stop_program)
        keyboard.wait()

    def stop_program(self):
        print("\n👋 Closing spell checker...")
        keyboard.unhook_all()
        exit()


def main():
    API_KEY = os.getenv('GEMINI_API_KEY')

    if not API_KEY:
        print("❌ Error: Please set your Google Gemini API key in the .env file")
        print("💡 Get your key from: https://aistudio.google.com/app/apikey")
        return

    try:
        spell_checker = SpellChecker(API_KEY)
        spell_checker.start_hotkey_listener()

    except KeyboardInterrupt:
        print("\n👋 Program terminated by user")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()