# DYMO Label Printer Controller

This project provides a Python-based interface to control a DYMO LetraTag 200B bluetooth label printer. It allows you to print both plain text and barcodes, either through a command-line interface or a simple web-based UI.

## Motivation
The inspiration for this project came while I was watching 'Better Call Saul'. I found myself wanting to print labels but didn't want to interrupt the show. The official DYMO Connect app was on my phone, which I was using to watch the episode. To solve this dilemma, I created this application (with the help of [Dymo-bluetooth](https://github.com/ysfchn/dymo-bluetooth)) to allow printing directly from my computer. This way, I can create labels without pausing the show.

## Features

- Print custom text labels.
- Generate and print Code 128 barcodes.
- Command-line interface for scripting and automation.
- Web interface for easy printing from a browser.

## Prerequisites

- Python 3.12.5 (tested on Windows 11).
- A DYMO LetraTag 200B printer.

## Installation

1.  Clone this repository to your local machine.
2.  Navigate to the project directory.
3.  Install the required Python packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

There are two ways to use this application: through the command-line interface (CLI) or the web interface.
Personally I recommend the web interface for its ease of use, but the CLI is also available for those who prefer it.

### Command-Line Interface

The CLI is ideal for scripting or quick printing tasks. You can print either text or a barcode by specifying the type and the content.

**Print a Barcode:**

```bash
python -m app --type barcode "1234567890"
```

**Print Text:**

```bash
python -m app --type text "Hello, World!"
```

### Web Interface

The web interface provides a user-friendly(ish) way to print labels from your browser.
I recommend using this because of the 'rapid fire' way you can print labels.

1.  Start the Flask web server:

    ```bash
    python web.py
    ```

2.  Open your web browser and navigate to `http://localhost:5000`.

3.  You will see a simple form where you can:
    -   Enter the text you want to print.
    -   Choose whether to print it as a barcode or as plain text.
    -   Click the "Print" button to send the label to your DYMO printer.

A "Printing..." message will appear for a few seconds to confirm that the label is being printed.
