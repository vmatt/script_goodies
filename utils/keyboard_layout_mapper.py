def get_key_presses(string):
	key_map = {
		'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h',
		'i': 'i', 'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p',
		'q': 'q', 'r': 'r', 's': 's', 't': 't', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'x',
		'y': 'y', 'z': 'z', 'A': 'Shift + a', 'B': 'Shift + b', 'C': 'Shift + c', 'D': 'Shift + d',
		'E': 'Shift + e', 'F': 'Shift + f', 'G': 'Shift + g', 'H': 'Shift + h', 'I': 'Shift + i',
		'J': 'Shift + j', 'K': 'Shift + k', 'L': 'Shift + l', 'M': 'Shift + m', 'N': 'Shift + n',
		'O': 'Shift + o', 'P': 'Shift + p', 'Q': 'Shift + q', 'R': 'Shift + r', 'S': 'Shift + s',
		'T': 'Shift + t', 'U': 'Shift + u', 'V': 'Shift + v', 'W': 'Shift + w', 'X': 'Shift + x',
		'Y': 'Shift + y', 'Z': 'Shift + z', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
		'6': '6', '7': '7', '8': '8', '9': '9', '0': '0', '!': 'Shift + 1', '@': 'Shift + 2',
		'#': 'Shift + 3', '$': 'Shift + 4', '%': 'Shift + 5', '^': 'Shift + 6', '&': 'Shift + 7',
		'*': 'Shift + 8', '(': 'Shift + 9', ')': 'Shift + 0', '-': '-', '_': 'Shift + -', '=': '=',
		'+': 'Shift + =', '[': '[', ']': ']', '{': 'Shift + [', '}': 'Shift + ]', '\\': '\\',
		'|': 'Shift + \\', ';': ';', ':': 'Shift + ;', "'": "'", '"': 'Shift + \'', ',': ',',
		'<': 'Shift + ,', '.': '.', '>': 'Shift + .', '/': '/', '?': 'Shift + /', ' ': 'Space'
	}

	return [key_map[char] for char in string if char in key_map]


input_string = "Hello, World!"
key_presses = get_key_presses(input_string)

for press in key_presses:
	print(press)
