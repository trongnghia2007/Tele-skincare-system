import PySimpleGUI as sg
import sys
import os
import home
import handbook
import map
import history
import threading
import logging
import time

class MultilineHandler(logging.Handler):
    def __init__(self, multiline):
        super().__init__()
        self.multiline = multiline

    def emit(self, record):
        msg = self.format(record)
        self.multiline.print(msg)

def startServer():
    # Define the layout of your window
    layout = [
        [sg.Button('Run', key="-run-"), sg.Button('Exit')],
        [sg.Text("Server Log:")],
        [sg.Multiline(size=(120, 20), key="-output-", background_color="#000", text_color="#ffb6c1",
                      reroute_stdout=True, reroute_stderr=True, reroute_cprint=True, auto_size_text=True, autoscroll=True)],
    ]

    # Create the window
    window = sg.Window('Server', layout, finalize=True,
                       enable_close_attempted_event=False)

    # Get the multiline element to add the handler
    multiline = window['-output-']
    handler = MultilineHandler(multiline)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)

    # Event loop to process events and display output
    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            window.close()
            os._exit(1)
        elif event == '-run-':
            # Start server
            def runApp1():
                logging.info("Starting home app on port 5000")
                home.app.run("0.0.0.0", debug=False, port=5000)

            def runApp2():
                time.sleep(2)  # Add delay to avoid conflict
                logging.info("Starting handbook app on port 80")
                handbook.app.run("0.0.0.0", debug=False, port=80)
                
            def runApp3():
                time.sleep(2)  # Add delay to avoid conflict
                logging.info("Starting map app on port 8080")
                map.app.run("0.0.0.0", debug=False, port=8080)
                
            def runApp4():
                time.sleep(2)  # Add delay to avoid conflict
                logging.info("Starting map app on port 8000")
                history.app.run("0.0.0.0", debug=False, port=8000)

            server1 = threading.Thread(target=runApp1)
            server1.start()
            server2 = threading.Thread(target=runApp2)
            server2.start()
            server3 = threading.Thread(target=runApp3)
            server3.start()
            server4 = threading.Thread(target=runApp4)
            server4.start()

            # Gray out the run button
            window["-run-"].update(disabled=True)

if __name__ == "__main__":
    startServer()
