import re
import json
from collections import Counter


def read_file(filename):
	with open(filename, 'r', encoding='utf-8') as file:
		return file.read()


def write_file(filename, content):
	with open(filename, 'w', encoding='utf-8') as file:
		file.write(content)


def load_json(filename):
	with open(filename, 'r', encoding='utf-8') as file:
		return json.load(file)


def get_frequent_words(text, min_length=5, min_frequency=3):
	words = re.findall(r'\b\w+\b', text.lower())
	return [word for word, count in Counter(words).items() if len(word) >= min_length and count >= min_frequency]


def remove_vowels(word):
	vowels = 'aáeéiíoóöőuúüű'
	return ''.join([char for char in word if char.lower() not in vowels])


def create_abbreviation(word, existing_abbrevs, text, compound_words):
	text_without_word = re.sub(r'\b' + re.escape(word) + r'\b', '', text, flags=re.IGNORECASE)

	if word in compound_words:
		parts = compound_words[word]
		abbrev = ''.join([part[0].upper() for part in parts])
		if abbrev not in existing_abbrevs and abbrev.lower() not in text_without_word.lower():
			return abbrev

	abbrev = remove_vowels(word).upper()[:3]
	if abbrev not in existing_abbrevs and abbrev.lower() not in text_without_word.lower():
		return abbrev

	for i in range(2, len(word)):
		abbrev = remove_vowels(word).upper()[:i]
		if abbrev not in existing_abbrevs and abbrev.lower() not in text_without_word.lower():
			return abbrev

	return None


def create_glossary(frequent_words, text, compound_words):
	glossary = {}
	for word in frequent_words:
		abbrev = create_abbreviation(word, glossary.values(), text, compound_words)
		if abbrev:
			glossary[word] = abbrev
	return glossary


def replace_words(text, glossary):
	for word, abbrev in glossary.items():
		text = re.sub(r'\b' + re.escape(word) + r'\b', abbrev, text, flags=re.IGNORECASE)
	return text


def main(input_file, output_file, compound_words_file):
	text = read_file(input_file)
	compound_words_data = load_json(compound_words_file)
	compound_words = {item['szo']: item['reszek'] for item in compound_words_data['osszetett_szavak']}

	frequent_words = get_frequent_words(text)
	frequent_words.extend(compound_words.keys())
	glossary = create_glossary(frequent_words, text, compound_words)
	abbreviated_text = replace_words(text, glossary)

	result = "Szójegyzék:\n"
	for word, abbrev in glossary.items():
		result += f"{abbrev}: {word}\n"
	result += "\nRövidített szöveg:\n" + abbreviated_text

	write_file(output_file, result)
	print(f"A rövidített szöveg és a szójegyzék elmentve: {output_file}")


if __name__ == "__main__":
	input_file = "input.txt"  # Bemeneti szövegfájl
	output_file = "output.txt"  # Kimeneti fájl
	compound_words_file = "osszetett_szavak.json"  # Összetett szavakat tartalmazó JSON fájl
	main(input_file, output_file, compound_words_file)
