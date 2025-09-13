# Typo correction 

A Python script for automatic spell checking and correction using Google Gemini AI.

## What it does

Detects spelling errors in selected text and provides corrections using Google's Gemini AI model with hotkey support.

## Requirements

- Python 3.7+
- Google Gemini API key
- Dependencies: see `requirements.txt`

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file based on `.env.example` and add your Google Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

3. Get your API key from: https://aistudio.google.com/app/apikey

## Usage

1. Run the script:
```bash
python main.py
```

2. Select any text in any application
3. Press `Ctrl+Q` to correct spelling errors
4. Press `Ctrl+Shift+Q` to exit the program

## Features

- Real-time spell checking with hotkeys
- Works with any text selection in any application
- Preserves original formatting and style
- Uses Google Gemini AI for accurate corrections
- Non-intrusive background operation
