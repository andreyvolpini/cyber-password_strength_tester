import math
import string
import secrets

from constants import SPECIAL_CHARACTERS


def has_uppercase(password: str) -> bool:
	return any(c.isupper() for c in password)


def has_lowercase(password: str) -> bool:
	return any(c.islower() for c in password)


def has_number(password: str) -> bool:
	return any(c.isdigit() for c in password)


def has_special(password: str) -> bool:
	return any(c in string.punctuation for c in password)


def has_repeated_characters(password: str, threshold: int = 3) -> bool:
	if not password:
		return False

	count = 1
	for i in range(1, len(password)):
		if password[i] == password[i - 1]:
			count += 1
			if count >= threshold:
				return True
		else:
			count = 1

	return False


def has_sequential_pattern(password: str, min_length: int = 4) -> bool:
	if len(password) < min_length:
		return False

	lower = password.lower()

	for i in range(len(lower) - min_length + 1):
		segment = lower[i:i + min_length]

		if not segment.isalnum():
			continue

		ascending = True
		descending = True

		for j in range(1, len(segment)):
			if ord(segment[j]) != ord(segment[j - 1]) + 1:
				ascending = False
			if ord(segment[j]) != ord(segment[j - 1]) - 1:
				descending = False

		if ascending or descending:
			return True

	return False


def has_pattern_issue(password: str) -> bool:
	return any([has_repeated_characters(password), has_sequential_pattern(password)])


def calculate_entropy(password: str) -> float:
	charset_size = 0

	if has_lowercase(password):
		charset_size += 26
	if has_uppercase(password):
		charset_size += 26
	if has_number(password):
		charset_size += 10
	if has_special(password):
		charset_size += len(string.punctuation)

	if charset_size == 0 or not password:
		return 0.0

	return len(password) * math.log2(charset_size)


def estimate_crack_time(entropy: float) -> str:
	if entropy <= 0:
		return "Instantly"

	combinations = 2 ** entropy
	guesses_per_second = 1e9
	seconds = combinations / guesses_per_second

	if seconds < 1:
		return "Less than a second"
	if seconds < 60:
		return f"{seconds:.1f} seconds"
	if seconds < 3600:
		return f"{seconds / 60:.1f} minutes"
	if seconds < 86400:
		return f"{seconds / 3600:.1f} hours"
	if seconds < 31536000:
		return f"{seconds / 86400:.1f} days"
	if seconds < 3153600000:
		return f"{seconds / 31536000:.1f} years"
	return "Centuries"


def get_strength_label(score_percentage: float, password: str, pattern_issue: bool) -> str:
	if not password:
		return "Enter a password to begin."
	if len(password) < 8:
		return "Very Weak"
	if pattern_issue and len(password) < 12:
		return "Weak"
	if score_percentage < 40:
		return "Weak"
	if score_percentage < 70:
		return "Moderate"
	if score_percentage < 90:
		return "Strong"
	return "Very Strong"


def get_strength_color(score_percentage: float, password: str, pattern_issue: bool, colors: dict) -> str:
	if not password:
		return colors["text"]
	if len(password) < 8:
		return colors["danger"]
	if pattern_issue and len(password) < 12:
		return colors["danger"]
	if score_percentage < 40:
		return colors["danger"]
	if score_percentage < 70:
		return colors["warning"]
	if score_percentage < 90:
		return colors["strong"]
	return colors["success"]


def evaluate_password(password: str) -> dict:
	pattern_issue = has_pattern_issue(password)

	checks = {
		"length": len(password) >= 12,
		"uppercase": has_uppercase(password),
		"lowercase": has_lowercase(password),
		"numbers": has_number(password),
		"special": has_special(password),
		"patterns": not pattern_issue and len(password) > 0,
	}

	score = sum(checks.values())
	max_score = len(checks)
	percentage = (score / max_score) * 100 if max_score else 0.0
	entropy = calculate_entropy(password)

	return {
		"checks": checks,
		"score": score,
		"percentage": percentage,
		"entropy": entropy,
		"crack_time": estimate_crack_time(entropy),
		"pattern_issue": pattern_issue,
		"label": get_strength_label(percentage, password, pattern_issue),
	}


def generate_password(length: int = 16) -> str:
	alphabet = string.ascii_letters + string.digits + SPECIAL_CHARACTERS

	while True:
		password = "".join(secrets.choice(alphabet) for _ in range(length))

		if (
			len(password) >= 16
			and has_uppercase(password)
			and has_lowercase(password)
			and has_number(password)
			and has_special(password)
			and not has_pattern_issue(password)
		):
			return password
		