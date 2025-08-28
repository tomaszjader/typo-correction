# Korekcja literówek

Skrypt Python do automatycznego wykrywania i poprawiania literówek w plikach tekstowych.

## Co robi

Wykrywa błędy ortograficzne i proponuje poprawki używając słownika i algorytmów odległości edycji.

## Wymagania

- Python 3.7+
- Zależności: `pip install nltk spellchecker`

## Użycie

```bash
python main.py plik.txt
```

**Opcje:**
- `-o poprawiony.txt` - zapisz poprawiony tekst do pliku
- `-v` - szczegółowe informacje z statystykami

## Przykład

```bash
python main.py dokument.txt -o poprawiony.txt -v
```
