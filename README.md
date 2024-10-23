# 🟢 **MTX Voice Assistant with Facecam Recognition** 🟢

![MTX Logo](https://raw.githubusercontent.com/MTXPr0ject/MTX/refs/heads/main/logo.webp)

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Code Quality](https://img.shields.io/badge/code%20quality-A%2B-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 📌 **Overview**

The **MTX Project** is a versatile application designed to integrate various functionalities including video processing, speech recognition, and chat management using the LiveKit platform. It provides a robust framework for building **interactive voice and vision-enabled assistants**.

## 📜 **Table of Contents**

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Environment Variables](#environment-variables)
- [File Structure](#file-structure)

## ✨ **Features**

- 🔊 **Voice and Vision Capabilities**: Responds to user commands using voice and visual data.
- 🌐 **Seamless Integration**: Works with LiveKit for real-time communication.
- 🛠️ **Customizable Functions**: Easily add or modify assistant functions.

## ⚙️ **Installation**

To set up the MTX project on your local machine, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/MTXPr0ject/MTX.git
   cd MTX
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:

   On Windows:
   ```bash
   .venv\Scripts\activate
   ```

   On macOS/Linux:
   ```bash
   source .venv/bin/activate
   ```

4. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**: Create a `.env` file in the project root with your LiveKit and Deepgram API keys.

## 🔑 Environment Variables

Create a `.env` file in the project root with the following variables:

```plaintext
LIVEKIT_URL=...
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
DEEPGRAM_API_KEY=...
OPENAI_API_KEY=...
```

## 🚀 Usage

To start the assistant, run:

```bash
python mtx.py start
```

For downloading files, use:

```bash
python mtx.py download-files
```

### 💡 Usage Examples

- **Start the Assistant**:
  ```bash
  python mtx.py start
  ```

- **Download Files**:
  ```bash
  python mtx.py download-files
  ```

- **Check for Updates**:
  ```bash
  python mtx.py update
  ```

## 📝 Requirements

- Python 3.11 or higher
- Required packages are listed in `requirements.txt`.

## 🤝 Contributing

We welcome contributions to the MTX Project! Please fork the repository and submit a pull request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/MTXPr0ject/MTX/blob/main/LICENSE) file for details.


## 📧 Contact

Author: MrTomXxX  
Facebook: [MrTomXxX](https://www.facebook.com/MrTomXxX)  
YouTube: [MTX Project](https://www.youtube.com/@mtxproject)

## 🗂️ File Structure

```
├── mtx.py                # Main application file
├── requirements.txt      # Required packages
├── .env                  # Environment variables
└── README.md             # Project documentation
```
