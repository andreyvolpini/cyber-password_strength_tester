COLORS = {
	"bg": "#1a1a2e",
	"card": "#16213e",
	"accent": "#0f3460",
	"highlight": "#e94560",
	"text": "#eaeaea",
	"success": "#00d9ff",
	"warning": "#ffc107",
	"danger": "#e94560",
	"medium": "#ff9800",
	"strong": "#4caf50",
	"muted": "#888888",
	"muted_icon": "#666666",
}

REQUIREMENTS = [
	("At least 12 characters", "length"),
	("Contains uppercase letters", "uppercase"),
	("Contains lowercase letters", "lowercase"),
	("Contains numbers", "numbers"),
	("Contains special characters", "special"),
	("Avoids common patterns", "patterns"),
]

SPECIAL_CHARACTERS = "!@#$%^&*()_-+=[]{}|;:,.<>?/"
