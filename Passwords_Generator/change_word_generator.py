import random
import string

def randomize_letters(input_text):
    """
    Fungsi untuk mengganti huruf (a-z) dalam teks masukan dengan huruf acak (huruf kecil atau besar),
    sementara simbol lainnya tetap tidak berubah.
    """
    output = []
    for char in input_text:
        if char.isalpha():  # Mengecek apakah karakter adalah huruf
            # Mengganti dengan huruf acak (huruf kecil atau besar)
            output.append(random.choice(string.ascii_letters))
        else:
            # Membiarkan simbol tetap tidak berubah
            output.append(char)
    return ''.join(output)

# Masukan teks secara dinamis
input_text = input("Input   : ")
output_text = randomize_letters(input_text)

# Menampilkan hasil dengan format f-string
print(f"Output  : {output_text}")