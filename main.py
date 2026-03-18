#!/usr/bin/env python3

import tkinter as tk

from ui import PasswordStrengthApp


def main():
	root = tk.Tk()
	PasswordStrengthApp(root)
	root.mainloop()


if __name__ == "__main__":
	main()
