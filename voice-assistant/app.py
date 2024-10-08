from flask import Flask, request, jsonify, send_from_directory
import datetime
import webbrowser
import subprocess  # Add this to use system commands
import logging
import urllib.parse  # Used to encode search queries
import platform  # To detect the operating system

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    command = data.get('command', '').lower()
    app.logger.debug(f"Received command: {command}")  # Debug information
    
    response = "I didn't understand that command."
    
    # Handling time requests
    if 'what is time' in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"The current time is {current_time}"

    # Open specific websites (YouTube, Google, Gmail, etc.)
    elif 'open google' in command:
        webbrowser.open('https://www.google.com')
        response = 'Opening Google'
    elif 'open youtube' in command:
        webbrowser.open('https://www.youtube.com')
        response = 'Opening YouTube'
    elif 'open mail' in command:
        webbrowser.open('https://mail.google.com')
        response = 'Opening Gmail'
    elif 'open black box' in command:
        webbrowser.open('https://www.blackbox.ai')
        response = 'Opening Blackbox AI'
    elif 'open github' in command:
        webbrowser.open('https://www.github.com')
        response = 'Opening GitHub'

    # Open system applications
    elif 'open notepad' in command:
        subprocess.Popen(['notepad.exe'])  # Windows Notepad
        response = 'Opening Notepad'
    elif 'open calculator' in command:
        subprocess.Popen(['calc.exe'])  # Windows Calculator
        response = 'Opening Calculator'
    elif 'open word' in command:
        subprocess.Popen(['start', 'winword.exe'], shell=True)  # Microsoft Word
        response = 'Opening Microsoft Word'
    elif 'open excel' in command:
        subprocess.Popen(['start', 'excel.exe'], shell=True)  # Microsoft Excel
        response = 'Opening Microsoft Excel'
    elif 'open firefox' in command:
        subprocess.Popen(['start', 'firefox.exe'], shell=True)  # Firefox Browser
        response = 'Opening Firefox'
    elif 'open whatsapp' in command:
        subprocess.Popen(['start', 'whatsapp.exe'], shell=True)  # WhatsApp
        response = 'Opening WhatsApp'
    elif 'open edge' in command:
        subprocess.Popen(['start', 'msedge.exe'], shell=True)  # Microsoft Edge
        response = 'Opening Microsoft Edge'

    # Open camera
    elif 'open camera' in command:
        os_name = platform.system()
        if os_name == 'Windows':
            subprocess.Popen(['start', 'microsoft.windows.camera:'], shell=True)  # Windows Camera
            response = 'Opening Camera'
        elif os_name == 'Linux':
            subprocess.Popen(['cheese'])  # Linux Cheese
            response = 'Opening Camera'
        elif os_name == 'Darwin':  # macOS
            subprocess.Popen(['open', '-a', 'Photo Booth'])  # macOS Photo Booth
            response = 'Opening Camera'
        else:
            response = 'Camera is not supported on this OS.'

    # Perform Google search
    elif 'search google' in command:
        # Extract the search query (everything after "search google for")
        query = command.replace('search google for', '').strip()
        if query:
            # Create a Google search URL with the query
            encoded_query = urllib.parse.quote_plus(query)
            search_url = f'https://www.google.com/search?q={encoded_query}'
            webbrowser.open(search_url)
            response = f'Searching Google for "{query}"'
        else:
            response = 'Please specify what you want to search for on Google.'

    # Stopping the assistant
    elif 'stop' in command:
        response = 'Stopping the assistant. Goodbye!'

    app.logger.debug(f"Response: {response}")  # Debug information
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
