🎤 Speech Recognition using Python (Google API)

A simple and effective Python application that converts spoken voice into text using the Google Speech Recognition API.
This project demonstrates real-time microphone input handling, ambient noise calibration, and speech-to-text conversion.

📌 Features

🎙️ Real-time speech recognition

🌍 Uses Google Speech Recognition API

🔇 Ambient noise calibration for better accuracy

⚡ Simple, beginner-friendly, and clean code

🖥️ Command-line based execution

🛠️ Tech Stack

Language: Python

Libraries:

SpeechRecognition

PyAudio (optional but recommended)

API: Google Speech Recognition

📁 Project Structure

Speech-Recognition/

│

├── main.py

├── README.md

├── requirements.txt

📦 Installation

1️⃣ Clone the repository

git clone https://github.com/your-username/speech-recognition-python.git

cd speech-recognition-python

2️⃣ Create and activate virtual environment (optional but recommended)

python -m venv .venv


Windows

.venv\Scripts\activate


Linux / macOS

source .venv/bin/activate

3️⃣ Install dependencies

pip install SpeechRecognition

Optional (for microphone support)

pip install pyaudio


⚠️ If PyAudio fails on Windows:

pip install pipwin
pipwin install pyaudio

▶️ How to Run
python main.py

🔄 How It Works

The program initializes the microphone

Ambient noise is calibrated

User speaks after the prompt

Audio is sent to Google Speech API

Recognized text is printed on the console

🧠 Sample Output

🎤 Calibrating microphone... Please wait

🎤 Tell Something (speak clearly):
You said: Hello, how are you?

⚠️ Common Issues & Solutions

❌ Unable to recognize the audio

Speak clearly after calibration

Reduce background noise

Ensure microphone permissions are enabled

Check internet connectivity

❌ ModuleNotFoundError

Make sure dependencies are installed in the correct Python environment.

🔐 Notes

Requires an active internet connection

Speech recognition accuracy depends on:

Microphone quality

Background noise

Speech clarity

🚀 Future Enhancements

🔁 Continuous listening mode // automatic stop after 10sec when speaker stops so no time limit 

🌐 Offline speech recognition (Vosk)

🔊 Text-to-speech response

🖥️ GUI using Tkinter / Streamlit

🌍 Multi-language support

👨‍💻 Author

Sairaj Jadhav
