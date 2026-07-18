"""
AKKIO AI ASSISTANT - Red & Black Theme with Animated Voice Visualizer
No external dependencies required!
Run this file directly in VS Code
"""

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import webbrowser
import time
import math
import random
from datetime import datetime
import os
import platform

class AkkioAI:
    def __init__(self, root):
        self.root = root
        self.root.title("AKKIO OS v1.0.0 - AI Assistant")
        self.root.geometry("1300x750")
        self.root.configure(bg="#0a0a0a")
        self.root.resizable(True, True)
        
        # Set minimum window size
        self.root.minsize(1000, 600)
        
        # Animation variables
        self.animation_running = False
        self.voice_active = False
        self.animation_phases = [0, 0, 0, 0, 0, 0, 0, 0]
        
        # Start time for uptime tracking
        self.start_time = time.time()
        
        # AI response dictionary
        self.ai_responses = {
            "hello": "Hello! I'm AKKIO, your AI assistant. How can I help you today?",
            "hi": "Hi there! How can I assist you?",
            "how are you": "I'm functioning perfectly! Ready to help you with anything.",
            "what is your name": "I'm AKKIO, your personal AI assistant.",
            "help": "I can help you with:\n- Opening applications\n- Searching the web\n- System monitoring\n- Answering questions",
            "open chrome": "Opening Google Chrome...",
            "open notepad": "Opening Notepad...",
            "open calculator": "Opening Calculator...",
            "open youtube": "Opening YouTube in your browser...",
            "search": "Searching...",
            "time": f"Current time: {datetime.now().strftime('%H:%M:%S')}",
            "date": f"Today's date: {datetime.now().strftime('%B %d, %Y')}",
        }
        
        # Build the UI
        self.build_ui()
        
        # Start system monitoring
        self.update_system_stats()
        
        # Start animation loop
        self.animate_visualizer()
        
    def build_ui(self):
        """Build the complete UI with red and black theme"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg="#0a0a0a")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Create grid
        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Left Panel
        self.build_left_panel()
        
        # Right Panel
        self.build_right_panel()
        
    def build_left_panel(self):
        """Build the left panel with chat and controls"""
        left_frame = tk.Frame(self.main_frame, bg="#0a0a0a")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        # Header
        self.build_header(left_frame)
        
        # Voice Visualizer
        self.build_visualizer(left_frame)
        
        # Chat Area
        self.build_chat_area(left_frame)
        
    def build_header(self, parent):
        """Build the header section with red theme"""
        header = tk.Frame(parent, bg="#0a0a0a")
        header.pack(fill=tk.X, pady=(0, 12))
        
        # Title
        title_frame = tk.Frame(header, bg="#1a0000", relief=tk.FLAT, bd=2)
        title_frame.pack(side=tk.LEFT)
        title_frame.config(highlightbackground="#cc0000", highlightthickness=1)
        
        tk.Label(title_frame, text="🔥 AKKIO OS v1.0.0", 
                font=("Segoe UI", 12, "bold"), fg="#ff3333", bg="#1a0000", 
                padx=15, pady=6).pack()
        
        # Online Badge
        online_frame = tk.Frame(header, bg="#1a0000", relief=tk.FLAT, bd=2)
        online_frame.pack(side=tk.RIGHT)
        online_frame.config(highlightbackground="#cc0000", highlightthickness=1)
        
        tk.Label(online_frame, text="● ONLINE", 
                font=("Segoe UI", 10), fg="#ff0000", bg="#1a0000", 
                padx=12, pady=5).pack(side=tk.LEFT)
        
        tk.Label(online_frame, text="AI ASSISTANT", 
                font=("Segoe UI", 9, "bold"), fg="#ff6666", bg="#2a0000", 
                padx=10, pady=3).pack(side=tk.LEFT, padx=5, pady=3)
        
    def build_visualizer(self, parent):
        """Build the animated voice visualizer"""
        viz_frame = tk.Frame(parent, bg="#0a0a0a", relief=tk.FLAT, bd=2)
        viz_frame.pack(fill=tk.X, pady=(0, 12))
        viz_frame.config(highlightbackground="#cc0000", highlightthickness=1)
        
        tk.Label(viz_frame, text="🎵 VOICE VISUALIZER", 
                font=("Segoe UI", 10, "bold"), fg="#ff3333", bg="#0a0a0a",
                padx=15, pady=10).pack(side=tk.LEFT)
        
        # Animated bars container
        self.bars_frame = tk.Frame(viz_frame, bg="#0a0a0a")
        self.bars_frame.pack(side=tk.LEFT, padx=20, expand=True, fill=tk.X)
        
        # Create 12 bars for better visual effect
        self.bars = []
        self.bar_heights = []
        colors = ["#ff0000", "#cc0000", "#ff3333", "#990000", 
                  "#ff4444", "#cc0000", "#ff0000", "#990000",
                  "#ff3333", "#cc0000", "#ff4444", "#ff0000"]
        
        for i, color in enumerate(colors):
            # Frame for each bar with glow effect
            bar_container = tk.Frame(self.bars_frame, bg="#0a0a0a")
            bar_container.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.Y)
            
            bar = tk.Frame(bar_container, bg=color, width=6, height=20)
            bar.pack(side=tk.BOTTOM, pady=(0, 5))
            
            # Store reference and initial height
            self.bars.append(bar)
            self.bar_heights.append(20)
        
        # Add glow label
        self.status_label = tk.Label(viz_frame, text="🔴 IDLE", 
                                    font=("Segoe UI", 9, "bold"), 
                                    fg="#ff3333", bg="#0a0a0a")
        self.status_label.pack(side=tk.RIGHT, padx=15)
        
        # Mic button with red theme
        self.mic_btn = tk.Button(viz_frame, text="🎤", font=("Segoe UI", 14),
                                fg="#ff0000", bg="#1a0000", relief=tk.FLAT,
                                padx=12, pady=4, cursor="hand2",
                                command=self.toggle_mic,
                                activebackground="#2a0000",
                                activeforeground="#ff4444")
        self.mic_btn.pack(side=tk.RIGHT, padx=10)
        self.mic_btn.config(highlightbackground="#cc0000", highlightthickness=2)
        self.mic_active = False
        
    def build_chat_area(self, parent):
        """Build the chat interface"""
        chat_container = tk.Frame(parent, bg="#0a0a0a", relief=tk.FLAT, bd=2)
        chat_container.pack(fill=tk.BOTH, expand=True)
        chat_container.config(highlightbackground="#cc0000", highlightthickness=1)
        
        # Title
        tk.Label(chat_container, text="💬 AI ASSISTANT", 
                font=("Segoe UI", 11, "bold"), fg="#ff3333", bg="#0a0a0a",
                padx=15, pady=10).pack(anchor=tk.W)
        
        # Tool buttons with red theme
        tools_frame = tk.Frame(chat_container, bg="#0a0a0a")
        tools_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        tools = [
            ("🌐 Chrome", self.open_chrome),
            ("📝 Notepad", self.open_notepad),
            ("🧮 Calculator", self.open_calculator),
            ("▶️ YouTube", self.open_youtube),
            ("🔍 Search", self.search_google)
        ]
        
        for text, command in tools:
            btn = tk.Button(tools_frame, text=text, command=command,
                           font=("Segoe UI", 9), fg="#ff6666", bg="#1a0000",
                           relief=tk.FLAT, padx=12, pady=4, cursor="hand2",
                           activebackground="#2a0000", activeforeground="#ff4444")
            btn.pack(side=tk.LEFT, padx=3)
            btn.config(highlightbackground="#cc0000", highlightthickness=1)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_container, bg="#0a0a0a", fg="#ffcccc",
            font=("Segoe UI", 10), wrap=tk.WORD,
            relief=tk.FLAT, bd=0, height=15
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        self.chat_display.config(highlightbackground="#cc0000", highlightthickness=1)
        
        # Add welcome message
        self.add_message("AKKIO", "🔥 Welcome to AKKIO OS!\nI'm your AI assistant ready to help.", is_user=False)
        
        # Input area
        input_frame = tk.Frame(chat_container, bg="#0a0a0a")
        input_frame.pack(fill=tk.X, padx=15, pady=(0, 12))
        
        self.input_entry = tk.Entry(input_frame, font=("Segoe UI", 11),
                                   bg="#1a0000", fg="#ffcccc",
                                   relief=tk.FLAT, insertbackground="#ff3333")
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.config(highlightbackground="#cc0000", highlightthickness=2)
        self.input_entry.bind("<Return>", lambda e: self.send_message())
        
        send_btn = tk.Button(input_frame, text="Send ▶", command=self.send_message,
                            font=("Segoe UI", 10, "bold"), fg="#ff0000",
                            bg="#1a0000", relief=tk.FLAT, padx=15, pady=6,
                            cursor="hand2",
                            activebackground="#2a0000", activeforeground="#ff4444")
        send_btn.pack(side=tk.RIGHT)
        send_btn.config(highlightbackground="#cc0000", highlightthickness=2)
        
    def build_right_panel(self):
        """Build the system status panel with red theme"""
        right_frame = tk.Frame(self.main_frame, bg="#0a0a0a", relief=tk.FLAT, bd=2)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.config(highlightbackground="#cc0000", highlightthickness=1)
        
        # Title
        tk.Label(right_frame, text="🖥️ SYSTEM STATUS", 
                font=("Segoe UI", 11, "bold"), fg="#ff3333", bg="#0a0a0a",
                padx=15, pady=10).pack(anchor=tk.W)
        
        # Separator
        tk.Frame(right_frame, bg="#cc0000", height=1).pack(fill=tk.X, padx=15, pady=10)
        
        # System stats
        self.stats_labels = {}
        stats = [
            ("💻 CPU USAGE", "0%"),
            ("🧠 RAM USAGE", "0%"),
            ("💾 DISK USAGE", "0%"),
            ("🌐 NETWORK", "0 KB/s"),
            ("⏱️ UPTIME", "00:00:00")
        ]
        
        for label, value in stats:
            frame = tk.Frame(right_frame, bg="#0a0a0a")
            frame.pack(fill=tk.X, padx=15, pady=4)
            
            tk.Label(frame, text=label, font=("Segoe UI", 9),
                    fg="#ff6666", bg="#0a0a0a").pack(side=tk.LEFT)
            
            value_label = tk.Label(frame, text=value, font=("Segoe UI", 9, "bold"),
                                  fg="#ff0000", bg="#1a0000", padx=10, pady=2)
            value_label.pack(side=tk.RIGHT)
            value_label.config(highlightbackground="#cc0000", highlightthickness=1)
            
            self.stats_labels[label] = value_label
        
        # Separator
        tk.Frame(right_frame, bg="#cc0000", height=1).pack(fill=tk.X, padx=15, pady=10)
        
        # AKKIO CORE
        core_frame = tk.Frame(right_frame, bg="#0a0a0a", relief=tk.FLAT, bd=2)
        core_frame.pack(fill=tk.X, padx=15, pady=10)
        core_frame.config(highlightbackground="#cc0000", highlightthickness=1)
        
        # Animated AKKIO Core text
        self.core_label = tk.Label(core_frame, text="🔥 AKKIO CORE - ACTIVE", 
                             font=("Segoe UI", 10, "bold"), fg="#ff0000", 
                             bg="#0a0a0a", pady=10)
        self.core_label.pack()
        
        # Blink animation for core label
        self.core_blink = False
        self.blink_core()
        
    def blink_core(self):
        """Blink the AKKIO Core label"""
        self.core_blink = not self.core_blink
        if self.core_blink:
            self.core_label.config(fg="#ff0000")
        else:
            self.core_label.config(fg="#660000")
        self.root.after(500, self.blink_core)
        
    def add_message(self, sender, text, is_user=True):
        """Add a message to the chat display"""
        self.chat_display.insert(tk.END, f"\n")
        if is_user:
            self.chat_display.insert(tk.END, f"You: ", "user_tag")
        else:
            self.chat_display.insert(tk.END, f"AKKIO: ", "akkio_tag")
        
        self.chat_display.insert(tk.END, f"{text}\n")
        self.chat_display.see(tk.END)
        
        # Configure tags for colors
        self.chat_display.tag_config("user_tag", foreground="#ff6666", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("akkio_tag", foreground="#ff0000", font=("Segoe UI", 10, "bold"))
        
    def send_message(self):
        """Process user message and generate AI response"""
        user_input = self.input_entry.get().strip()
        if not user_input:
            return
        
        # Trigger voice animation when user sends message
        self.trigger_voice_animation()
        
        self.add_message("You", user_input, is_user=True)
        self.input_entry.delete(0, tk.END)
        
        # Process the message
        response = self.process_message(user_input)
        self.add_message("AKKIO", response, is_user=False)
        
        # Execute any commands
        self.execute_command(user_input)
        
    def process_message(self, message):
        """Process user message and return AI response"""
        message_lower = message.lower().strip()
        
        # Check for specific commands
        if "open chrome" in message_lower or "open google chrome" in message_lower:
            return "Opening Google Chrome... 🔥"
        elif "open notepad" in message_lower:
            return "Opening Notepad... 📝"
        elif "open calculator" in message_lower:
            return "Opening Calculator... 🧮"
        elif "open youtube" in message_lower:
            return "Opening YouTube... ▶️"
        elif "search" in message_lower or "google" in message_lower:
            return "Searching Google... 🔍"
        elif "time" in message_lower:
            return f"Current time: {datetime.now().strftime('%I:%M %p')} 🕐"
        elif "date" in message_lower:
            return f"Today's date: {datetime.now().strftime('%B %d, %Y')} 📅"
        elif "help" in message_lower:
            return self.ai_responses["help"]
        elif "how are you" in message_lower:
            return self.ai_responses["how are you"]
        elif "your name" in message_lower:
            return self.ai_responses["what is your name"]
        elif "hello" in message_lower or "hi" in message_lower:
            return "🔥 Hello! I'm AKKIO, your AI assistant. How can I help you today?"
        else:
            return f"I understand you said: '{message}'\nI'm still learning! Try asking me to open Chrome, Notepad, or YouTube."
    
    def execute_command(self, message):
        """Execute system commands based on user input"""
        message_lower = message.lower().strip()
        
        if "open chrome" in message_lower or "open google chrome" in message_lower:
            self.open_chrome()
        elif "open notepad" in message_lower:
            self.open_notepad()
        elif "open calculator" in message_lower:
            self.open_calculator()
        elif "open youtube" in message_lower:
            self.open_youtube()
        elif "search" in message_lower:
            self.search_google()
    
    def open_chrome(self):
        """Open Google Chrome"""
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["start", "chrome"], shell=True)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "-a", "Google Chrome"])
            else:
                subprocess.Popen(["google-chrome"])
        except:
            webbrowser.open("https://www.google.com")
    
    def open_notepad(self):
        """Open Notepad"""
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["notepad.exe"])
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "-a", "TextEdit"])
            else:
                subprocess.Popen(["gedit"])
        except:
            pass
    
    def open_calculator(self):
        """Open Calculator"""
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["calc.exe"])
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "-a", "Calculator"])
            else:
                subprocess.Popen(["gnome-calculator"])
        except:
            pass
    
    def open_youtube(self):
        """Open YouTube"""
        webbrowser.open("https://www.youtube.com")
    
    def search_google(self):
        """Search Google"""
        webbrowser.open("https://www.google.com")
    
    def toggle_mic(self):
        """Toggle microphone and voice animation"""
        self.mic_active = not self.mic_active
        if self.mic_active:
            self.mic_btn.config(bg="#2a0000", text="🔴", fg="#ff0000")
            self.status_label.config(text="🔴 LISTENING", fg="#ff0000")
            self.trigger_voice_animation()
            self.add_message("System", "🎤 Microphone activated... Listening...", is_user=False)
        else:
            self.mic_btn.config(bg="#1a0000", text="🎤", fg="#ff0000")
            self.status_label.config(text="🔴 IDLE", fg="#ff3333")
            self.voice_active = False
            self.add_message("System", "🎤 Microphone deactivated", is_user=False)
    
    def trigger_voice_animation(self):
        """Trigger voice animation effect"""
        self.voice_active = True
        self.status_label.config(text="🔴 SPEAKING", fg="#ff0000")
        # Auto-stop after 3 seconds
        self.root.after(3000, self.stop_voice_animation)
    
    def stop_voice_animation(self):
        """Stop voice animation"""
        self.voice_active = False
        if not self.mic_active:
            self.status_label.config(text="🔴 IDLE", fg="#ff3333")
    
    def animate_visualizer(self):
        """Animate the voice visualizer bars"""
        if self.voice_active or self.mic_active:
            # Generate random heights for sound wave effect
            for i, bar in enumerate(self.bars):
                # Create wave-like motion with random variation
                base_height = 15
                if self.voice_active:
                    # More dramatic when actively speaking
                    height = base_height + random.randint(10, 45)
                else:
                    # Subtle idle animation
                    height = base_height + random.randint(0, 15)
                
                # Create wave effect
                wave = math.sin(time.time() * 3 + i * 0.5) * 15
                height = max(5, min(60, height + wave))
                
                # Update bar height
                bar.config(height=height)
                
                # Change color intensity based on height
                intensity = min(255, int(100 + (height / 60) * 155))
                color = f"#{intensity:02x}0000"
                bar.config(bg=color)
        else:
            # Idle animation - subtle movement
            for i, bar in enumerate(self.bars):
                # Small wave effect even when idle
                wave = math.sin(time.time() * 1.5 + i * 0.8) * 8
                height = max(5, 15 + wave)
                bar.config(height=height)
                
                # Dimmer color for idle
                intensity = min(255, int(60 + (height / 30) * 100))
                color = f"#{intensity:02x}0000"
                bar.config(bg=color)
        
        # Continue animation loop
        self.root.after(50, self.animate_visualizer)
    
    def get_system_stats(self):
        """Get system statistics using built-in Python modules"""
        stats = {}
        
        # CPU usage (simple approximation)
        try:
            import os
            if platform.system() == "Windows":
                try:
                    import subprocess
                    result = subprocess.run(['wmic', 'cpu', 'get', 'loadpercentage'], 
                                          capture_output=True, text=True, timeout=1)
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        cpu = lines[1].strip()
                        stats['cpu'] = f"{cpu}%"
                    else:
                        stats['cpu'] = "N/A"
                except:
                    stats['cpu'] = "N/A"
            else:
                try:
                    with open('/proc/stat', 'r') as f:
                        lines = f.readlines()
                    stats['cpu'] = "N/A"
                except:
                    stats['cpu'] = "N/A"
        except:
            stats['cpu'] = "N/A"
        
        # RAM usage (simple)
        try:
            if platform.system() == "Windows":
                import ctypes
                kernel32 = ctypes.windll.kernel32
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]
                memoryStatus = MEMORYSTATUSEX()
                memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                if kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus)):
                    total = memoryStatus.ullTotalPhys
                    avail = memoryStatus.ullAvailPhys
                    used_percent = ((total - avail) / total) * 100
                    stats['ram'] = f"{used_percent:.0f}%"
                else:
                    stats['ram'] = "N/A"
            else:
                try:
                    with open('/proc/meminfo', 'r') as f:
                        lines = f.readlines()
                    total = None
                    available = None
                    for line in lines:
                        if 'MemTotal' in line:
                            total = int(line.split()[1])
                        if 'MemAvailable' in line:
                            available = int(line.split()[1])
                    if total and available:
                        used_percent = ((total - available) / total) * 100
                        stats['ram'] = f"{used_percent:.0f}%"
                    else:
                        stats['ram'] = "N/A"
                except:
                    stats['ram'] = "N/A"
        except:
            stats['ram'] = "N/A"
        
        # Disk usage
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            used_percent = (used / total) * 100
            stats['disk'] = f"{used_percent:.0f}%"
        except:
            stats['disk'] = "N/A"
        
        # Network (simplified)
        stats['network'] = "N/A"
        
        # Uptime
        uptime = time.time() - self.start_time
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        seconds = int(uptime % 60)
        stats['uptime'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        return stats
    
    def update_system_stats(self):
        """Update system statistics in real-time"""
        try:
            stats = self.get_system_stats()
            
            if "💻 CPU USAGE" in self.stats_labels:
                self.stats_labels["💻 CPU USAGE"].config(text=stats.get('cpu', 'N/A'))
            if "🧠 RAM USAGE" in self.stats_labels:
                self.stats_labels["🧠 RAM USAGE"].config(text=stats.get('ram', 'N/A'))
            if "💾 DISK USAGE" in self.stats_labels:
                self.stats_labels["💾 DISK USAGE"].config(text=stats.get('disk', 'N/A'))
            if "🌐 NETWORK" in self.stats_labels:
                self.stats_labels["🌐 NETWORK"].config(text=stats.get('network', 'N/A'))
            if "⏱️ UPTIME" in self.stats_labels:
                self.stats_labels["⏱️ UPTIME"].config(text=stats.get('uptime', '00:00:00'))
                
        except Exception as e:
            pass  # Silently handle any errors
        
        # Update every 2 seconds
        self.root.after(2000, self.update_system_stats)

if __name__ == "__main__":
    root = tk.Tk() 
    app = AkkioAI(root)
    root.mainloop()
