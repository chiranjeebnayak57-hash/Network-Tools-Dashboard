# Network-Tools-Dashboard

**How this program works:**

Cross-Platform Compatibility: Network commands change depending on the OS (e.g., ipconfig on Windows vs. ip a on Linux; tracert vs. traceroute). The platform.system() check ensures the tool runs the correct underlying command for your machine.

Threading: Commands like traceroute or ping take time to complete. If they run on the main graphical thread, the app will completely freeze. The threading.Thread setup pushes the heavy lifting to the background so you can still move the window around while the scan runs.

Live Output Feed: Standard subprocess.run waits until the whole command is finished to show text. This script uses subprocess.Popen to read the console feed line-by-line and pushes it straight to the ScrolledText widget using .after(), giving it a "hacker terminal" live-feed feel.

**Prerequisites:**

Python handles tkinter, threading, and subprocess natively; no pip install is required.

Operating System Commands: Keep in mind that some tools must actually be installed on your computer. For example, whois and mtr are usually native to Linux but are not installed by default on Windows. If you select a tool your OS lacks, the GUI will gracefully catch the FileNotFoundError and alert you.
