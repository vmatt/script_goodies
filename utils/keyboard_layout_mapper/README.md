# Keyboard Layout Mapper

A utility to convert text into keyboard key press sequences. Useful for documenting keyboard shortcuts or creating keyboard layout tutorials.

## Features
- Maps lowercase and uppercase letters
- Includes number keys and special characters
- Shows Shift key combinations
- Supports common punctuation marks

## Usage
```python
input_string = "Hello, World!"
key_presses = get_key_presses(input_string)
for press in key_presses:
    print(press)
```
