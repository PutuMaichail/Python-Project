import random
import string

def generate_password(length=~18):
    """
    Fungsi untuk menghasilkan password acak dengan panjang tertentu.
    Password terdiri dari huruf kecil, huruf besar, angka, dan simbol.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Menghasilkan password secara otomatis
password = generate_password()

# Menampilkan hasil langsung di terminal
print(f"Password yang dihasilkan: {password}")