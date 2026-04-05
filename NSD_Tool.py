# Copyright (c) 2026 Chiranjeeb Nayak.
# All rights reserved.

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import platform

class NetworkToolsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Security & Diagnostics Toolkit")
        self.root.geometry("850x600")
        self.root.configure(padx=10, pady=10, bg='white')

        # Detect OS for cross-platform command adjustments
        self.os_name = platform.system().lower()

        self.setup_ui()

    def setup_ui(self):
        # --- Top Frame: Input Controls ---
        input_frame = tk.Frame(self.root, bg="#FFFFFF")
        input_frame.pack(fill=tk.X, pady=(0, 20))

        # Tool Selection
        tk.Label(input_frame, text="Select Tool:",bg="#FFFFFF", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.tool_var = tk.StringVar(value="Ping")
        self.tools = [
            "Ping", "Traceroute", "NS Lookup", "Whois",
            "Netstat", "IP Address", "Hostname", "MTR / Pathping"
        ]

        self.tool_dropdown = ttk.Combobox(input_frame, textvariable=self.tool_var, values=self.tools, state="readonly", width=20)
        self.tool_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Target Input (IP or Domain)
        tk.Label(input_frame, text="Target (IP/Domain):", bg="#FFFFFF", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky=tk.W, padx=(20, 5), pady=5)

        self.target_entry = tk.Entry(input_frame, width=30)
        self.target_entry.grid(row=0, column=3, padx=5, pady=5)

        # Execute Button
        self.exec_btn = tk.Button(input_frame, text="Execute", bg="#FF111E", fg="white", font=("Arial", 10, "bold"), command=self.start_execution)
        self.exec_btn.grid(row=0, column=4, padx=(20, 5), pady=5)

        # --- Bottom Frame: Output Display ---
        output_frame = tk.Frame(self.root, bg="#FFFFFF")
        output_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(output_frame, text="Output:", bg="#FFFFFF",font=("Arial", 10, "bold")).pack(anchor=tk.W)

        self.output_box = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=("Consolas", 10), bg="#000000", fg="#00FF00")
        self.output_box.pack(fill=tk.BOTH, expand=True, pady=5)

    def start_execution(self):
        tool = self.tool_var.get()
        target = self.target_entry.get().strip()

        # Tools that require a target input
        target_required = ["Ping", "Traceroute", "NS Lookup", "Whois", "MTR / Pathping"]

        if tool in target_required and not target:
            messagebox.showwarning("Input Error", f"Please enter a Target IP or Domain for {tool}.")
            return

        # Prepare GUI for execution
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, f"[*] Initializing {tool}...\n")
        self.exec_btn.config(state=tk.DISABLED)

        # Run in a background thread to prevent GUI freezing
        threading.Thread(target=self.run_command, args=(tool, target), daemon=True).start()

    def run_command(self, tool, target):
        cmd = []

        # Map tools to system commands based on OS
        if tool == "Ping":
            cmd = ["ping", "-n", "4", target] if self.os_name == "windows" else ["ping", "-c", "4", target]
        elif tool == "Traceroute":
            cmd = ["tracert", target] if self.os_name == "windows" else ["traceroute", target]
        elif tool == "NS Lookup":
            cmd = ["nslookup", target]
        elif tool == "Whois":
            cmd = ["whois", target]
        elif tool == "Netstat":
            cmd = ["netstat", "-an"]
        elif tool == "IP Address":
            cmd = ["ipconfig"] if self.os_name == "windows" else ["ip", "a"]
        elif tool == "Hostname":
            cmd = ["hostname"]
        elif tool == "MTR / Pathping":
            cmd = ["pathping", target] if self.os_name == "windows" else ["mtr", "-r", "-w", "-c", "4", target]

        try:
            # Execute the command
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)

            # Read output line by line as it is generated
            for line in process.stdout:
                self.root.after(0, self.update_output, line)

            process.wait()
            self.root.after(0, self.update_output, f"\n[*] {tool} scan completed.\n")

        except FileNotFoundError:
            error_msg = f"\n[!] Error: The command '{cmd[0]}' is not installed or recognized on your operating system.\n"
            self.root.after(0, self.update_output, error_msg)
        except Exception as e:
            self.root.after(0, self.update_output, f"\n[!] An error occurred: {str(e)}\n")
        finally:
            self.root.after(0, self.enable_button)

    def update_output(self, text):
        """Safely update the Text widget from the main thread."""
        self.output_box.insert(tk.END, text)
        self.output_box.see(tk.END) # Auto-scroll to bottom

    def enable_button(self):
        """Re-enable the execute button after completion."""
        self.exec_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkToolsApp(root)
    root.mainloop()
