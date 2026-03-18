import tkinter as tk
from tkinter import ttk

from constants import COLORS, REQUIREMENTS
from utils import evaluate_password, generate_password, get_strength_color


class PasswordStrengthApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Password Strength Tester")
		self.root.geometry("620x950")
		self.root.configure(bg=COLORS["bg"])
		self.root.resizable(False, False)

		self.req_labels = {}

		self.password_var = tk.StringVar()
		self.password_var.trace_add("write", self.on_password_change)

		self.setup_styles()
		self.build_ui()

	def setup_styles(self):
		style = ttk.Style()
		style.theme_use("clam")
		style.configure(
			"Custom.Horizontal.TProgressbar",
			troughcolor=COLORS["card"],
			background=COLORS["success"],
			thickness=20,
		)
		self.style = style
		
	def create_card(self, parent):
		return tk.Frame(parent, bg=COLORS["card"], relief=tk.FLAT)

	def build_ui(self):
		main = tk.Frame(self.root, bg=COLORS["bg"])
		main.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

		tk.Label(
			main,
			text="Password Strength Tester",
			font=("Helvetica", 24, "bold"),
			bg=COLORS["bg"],
			fg=COLORS["success"],
		).pack(pady=(0, 20))

		input_card = self.create_card(main)
		input_card.pack(fill=tk.X, pady=10)

		tk.Label(
			input_card,
			text="Enter your password",
			font=("Helvetica", 12),
			bg=COLORS["card"],
			fg=COLORS["text"],
		).pack(anchor="w", padx=15, pady=(15, 5))

		entry_frame = tk.Frame(input_card, bg=COLORS["card"])
		entry_frame.pack(fill=tk.X, padx=15, pady=5)

		self.password_entry = tk.Entry(
			entry_frame,
			textvariable=self.password_var,
			font=("Consolas", 14),
			bg=COLORS["accent"],
			fg=COLORS["text"],
			insertbackground=COLORS["text"],
			relief=tk.FLAT,
			show="•",
		)
		self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)

		self.toggle_btn = tk.Button(
			entry_frame,
			text="Show",
			font=("Helvetica", 10, "bold"),
			bg=COLORS["accent"],
			fg=COLORS["text"],
			command=self.toggle_visibility,
			padx=12,
		)
		self.toggle_btn.pack(side=tk.RIGHT, padx=(6, 0))

		tk.Button(
			input_card,
			text="Generate Secure Password",
			font=("Helvetica", 11, "bold"),
			bg=COLORS["highlight"],
			fg="white",
			command=self.handle_generate_password,
			padx=20,
			pady=8,
		).pack(pady=15)

		strength_card = self.create_card(main)
		strength_card.pack(fill=tk.X, pady=10)

		tk.Label(
			strength_card,
			text="Password Strength",
			font=("Helvetica", 14, "bold"),
			bg=COLORS["card"],
			fg=COLORS["text"],
		).pack(anchor="w", padx=15, pady=(15, 10))

		bar_frame = tk.Frame(strength_card, bg=COLORS["card"])
		bar_frame.pack(fill=tk.X, padx=15, pady=5)

		self.strength_bar = ttk.Progressbar(
			bar_frame,
			style="Custom.Horizontal.TProgressbar",
			maximum=100,
		)
		self.strength_bar.pack(fill=tk.X, pady=5)

		self.strength_label = tk.Label(
			bar_frame,
			text="Enter a password to begin.",
			font=("Helvetica", 12, "bold"),
			bg=COLORS["card"],
			fg=COLORS["text"],
		)
		self.strength_label.pack(pady=5)

		self.time_label = tk.Label(
			strength_card,
			text="",
			font=("Helvetica", 10),
			bg=COLORS["card"],
			fg=COLORS["success"],
		)
		self.time_label.pack(pady=(0, 6))

		tk.Label(
			strength_card,
			text="This estimate is illustrative and assumes an offline brute-force scenario.",
			font=("Helvetica", 9),
			bg=COLORS["card"],
			fg=COLORS["muted"],
			wraplength=540,
		).pack(anchor="w", padx=15, pady=(0, 15))

		req_card = self.create_card(main)
		req_card.pack(fill=tk.X, pady=10)

		tk.Label(
			req_card,
			text="Recommended Requirements",
			font=("Helvetica", 14, "bold"),
			bg=COLORS["card"],
			fg=COLORS["text"],
		).pack(anchor="w", padx=15, pady=(15, 10))

		for text, key in REQUIREMENTS:
			row = tk.Frame(req_card, bg=COLORS["card"])
			row.pack(fill=tk.X, padx=15, pady=3)

			icon = tk.Label(
				row,
				text="○",
				font=("Helvetica", 12),
				bg=COLORS["card"],
				fg=COLORS["muted_icon"],
			)
			icon.pack(side=tk.LEFT)

			label = tk.Label(
				row,
				text=text,
				font=("Helvetica", 11),
				bg=COLORS["card"],
				fg=COLORS["muted"],
			)
			label.pack(side=tk.LEFT, padx=10)

			self.req_labels[key] = (icon, label)

		tips_card = self.create_card(main)
		tips_card.pack(fill=tk.X, pady=10)

		tk.Label(
			tips_card,
			text="Tips for stronger passwords",
			font=("Helvetica", 12, "bold"),
			bg=COLORS["card"],
			fg=COLORS["success"],
		).pack(anchor="w", padx=15, pady=(15, 10))

		for tip in [
			"• Prefer long passphrases that are easy to remember.",
			"• Avoid names, birthdays, and personal information.",
			"• Do not reuse the same password across services.",
			"• Consider using a reputable password manager.",
		]:
			tk.Label(
				tips_card,
				text=tip,
				font=("Helvetica", 10),
				bg=COLORS["card"],
				fg=COLORS["text"],
				wraplength=540,
			).pack(anchor="w", padx=15, pady=2)

	def toggle_visibility(self):
		currently_hidden = self.password_entry.cget("show") == "•"
		self.password_entry.config(show="" if currently_hidden else "•")
		self.toggle_btn.config(text="Hide" if currently_hidden else "Show")

	def handle_generate_password(self):
		password = generate_password(16)
		self.password_var.set(password)
		self.password_entry.select_range(0, tk.END)
		self.password_entry.focus()

	def on_password_change(self, *args):
		password = self.password_var.get()
		result = evaluate_password(password)

		color = get_strength_color(
			result["percentage"],
			password,
			result["pattern_issue"],
			COLORS,
		)

		self.strength_bar["value"] = result["percentage"]
		self.style.configure("Custom.Horizontal.TProgressbar", background=color)
		self.strength_label.config(text=result["label"], fg=color)

		if password:
			self.time_label.config(
				text=f"Estimated resistance: {result['crack_time']}",
				fg=COLORS["success"] if result["entropy"] >= 60 else COLORS["warning"],
			)
		else:
			self.time_label.config(text="")

		for key, (icon, label) in self.req_labels.items():
			passed = result["checks"].get(key, False)
			icon.config(
				text="✓" if passed else "○",
				fg=COLORS["success"] if passed else COLORS["muted_icon"],
			)
			label.config(fg=COLORS["text"] if passed else COLORS["muted"])
