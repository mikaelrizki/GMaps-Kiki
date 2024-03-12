def encrypt(text, key):
    encrypted_text = ""
    key_index = len(text) % 9

    for char in text:
        if not char.isalpha():
            key_index += 1
            continue

        if key_index >= len(key):
            key_index = 0

        char_unicode = ord(char)
        if not(char.islower() | char.isupper()):
            char_unicode = char_unicode%26
            if char_unicode%2 == 0:
                char = chr(ord('a') + char_unicode)
            else:
                char = chr(ord('Z') - char_unicode)
            char_unicode = ord(char)
        
        key_digit = int(key[key_index])

        if char.islower():
            encrypted_char_unicode = char_unicode + key_digit
            if encrypted_char_unicode > ord('z'):
                encrypted_char_unicode = ord('a') + (encrypted_char_unicode - ord('z') - 1)
        elif char.isupper() :
            encrypted_char_unicode = char_unicode - key_digit
            if encrypted_char_unicode < ord('A'):
                encrypted_char_unicode = ord('Z') + (encrypted_char_unicode - ord('A') + 1)
        
        encrypted_char = chr(encrypted_char_unicode)
        if key_index %2 == 0 | key_digit%2 != 0:
            encrypted_char = encrypted_char.upper()
        else:
            encrypted_char = encrypted_char.lower()
        
        encrypted_text += encrypted_char
        key_index += 1

    return encrypted_text

# Key dan kata yang akan dienkripsi
key = "157890236"
word = "徐均炳"
# Enkripsi kata menggunakan fungsi encrypt
encrypted_word = encrypt(word, key)

# Tampilkan hasil enkripsi
print("Kata Asli:", word)
print("Kata Terenkripsi:", encrypted_word)
