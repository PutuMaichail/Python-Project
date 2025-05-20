import json
from tabulate import tabulate
import psutil


class ContactManager:
    def __init__(self, file_name='contacts.json'):
        self.file_name = file_name
        self.contacts = {}

    def load_contacts(self):
        try:
            with open(self.file_name, 'r') as file:
                data = json.load(file)
                if isinstance(data, dict):
                    self.contacts = data
                else:
                    print("Format data tidak valid. Menggunakan data kosong.")
                    self.contacts = {}
        except FileNotFoundError:
            self.contacts = {}
        except json.JSONDecodeError:
            print("File JSON rusak. Menggunakan data kosong.")
            self.contacts = {}

    def save_contacts(self):
        self.validate_contacts()
        with open(self.file_name, 'w') as file:
            json.dump(self.contacts, file, indent=4)

    def validate_contacts(self):
        for name, info in list(self.contacts.items()):
            if not self.validate_name(name) or not self.validate_number(info.get('nomor', '')) or not self.validate_email(info.get('email', '')):
                print(f"Data kontak {name} tidak valid. Menghapus dari daftar.")
                del self.contacts[name]

    @staticmethod
    def validate_name(name):
        if len(name) > 50:
            print("Nama tidak boleh lebih dari 50 karakter.")
            return False
        return True

    @staticmethod
    def validate_number(number):
        if not number.isdigit():
            print("Nomor telepon hanya boleh berisi angka.")
            return False
        if len(number) > 12:
            print("Nomor telepon tidak boleh lebih dari 12 digit.")
            return False
        return True

    @staticmethod
    def validate_email(email):
        if "@" not in email:
            print("Email harus mengandung karakter '@'.")
            return False
        return True

    def add_contact(self):
        name = input('Masukkan Nama: ').strip()
        if not self.validate_name(name):
            return
        number = input('Masukkan Nomor Telepon: ').strip()
        if not self.validate_number(number):
            return
        email = input('Masukkan Email: ').strip()
        if not self.validate_email(email):
            return
        address = input('Masukkan Alamat: ').strip()
        birth_date = input('Masukkan Tanggal Lahir (YYYY-MM-DD): ').strip()
        notes = input('Masukkan Catatan: ').strip()
        self.contacts[name] = {
            'nomor': number,
            'email': email,
            'alamat': address,
            'tanggal_lahir': birth_date,
            'catatan': notes
        }
        print(f'Kontak {name} berhasil ditambahkan.')

    def delete_contact(self):
        keyword = input('Masukkan nama kontak yang ingin dihapus: ').strip()
        if keyword in self.contacts:
            del self.contacts[keyword]
            print(f'Kontak {keyword} berhasil dihapus.')
        else:
            print('Kontak tidak ditemukan.')

    def search_contact(self):
        keyword = input('Masukkan kata kunci pencarian: ').strip().lower()
        results = [
            [name, info['nomor'], info['email'], info['alamat'], info['tanggal_lahir'], info['catatan']]
            for name, info in self.contacts.items()
            if keyword in name.lower() or keyword in info['nomor'] or keyword in info['email'].lower()
        ]
        if results:
            print(tabulate(results, headers=["Nama", "Nomor", "Email", "Alamat", "Tanggal Lahir", "Catatan"], tablefmt="grid"))
        else:
            print('Tidak ada kontak yang sesuai dengan pencarian.')

    def display_contacts(self):
        if self.contacts:
            data = [
                [name, info['nomor'], info['email'], info['alamat'], info['tanggal_lahir'], info['catatan']]
                for name, info in self.contacts.items()
            ]
            print(tabulate(data, headers=["Nama", "Nomor", "Email", "Alamat", "Tanggal Lahir", "Catatan"], tablefmt="grid"))
        else:
            print('Tidak ada kontak yang tersimpan.')

    def update_contact(self):
        name = input('Masukkan nama kontak yang ingin diubah: ').strip()
        if name in self.contacts:
            print(f"Kontak ditemukan: {name} - Nomor: {self.contacts[name]['nomor']}, Email: {self.contacts[name]['email']}")
            new_name = input('Masukkan Nama Baru (tekan Enter untuk tidak mengubah): ').strip()
            new_number = input('Masukkan Nomor Telepon Baru (tekan Enter untuk tidak mengubah): ').strip()
            new_email = input('Masukkan Email Baru (tekan Enter untuk tidak mengubah): ').strip()
            new_address = input('Masukkan Alamat Baru (tekan Enter untuk tidak mengubah): ').strip()
            new_birth_date = input('Masukkan Tanggal Lahir Baru (YYYY-MM-DD, tekan Enter untuk tidak mengubah): ').strip()
            new_notes = input('Masukkan Catatan Baru (tekan Enter untuk tidak mengubah): ').strip()

            if new_name and not self.validate_name(new_name):
                return
            if new_number and not self.validate_number(new_number):
                return
            if new_email and not self.validate_email(new_email):
                return

            updated_name = new_name if new_name else name
            self.contacts[updated_name] = {
                'nomor': new_number if new_number else self.contacts[name]['nomor'],
                'email': new_email if new_email else self.contacts[name]['email'],
                'alamat': new_address if new_address else self.contacts[name]['alamat'],
                'tanggal_lahir': new_birth_date if new_birth_date else self.contacts[name]['tanggal_lahir'],
                'catatan': new_notes if new_notes else self.contacts[name]['catatan']
            }
            if updated_name != name:
                del self.contacts[name]
            print(f'Kontak {name} berhasil diperbarui.')
        else:
            print('Kontak tidak ditemukan.')


def main():
    manager = ContactManager()
    manager.load_contacts()

    while True:
        print('\n' + ' Menu Kontak '.center(50, '='))
        print('1. Tambah Kontak')
        print('2. Hapus Kontak')
        print('3. Cari Kontak')
        print('4. Ubah Kontak')
        print('5. Tampilkan Kontak')
        print('6. Keluar')
        print(''.center(50, '-'))

        choice = input('Pilih Menu (1, 2, 3, ...): ').strip()
        print(''.center(50, '-'))

        if choice == '1':
            manager.add_contact()
        elif choice == '2':
            manager.delete_contact()
        elif choice == '3':
            manager.search_contact()
        elif choice == '4':
            manager.update_contact()
        elif choice == '5':
            manager.display_contacts()
        elif choice == '6':
            manager.save_contacts()
            free_memory = psutil.virtual_memory().available / (1024 * 1024)  # Convert to MB
            print(f'Free Memory: {free_memory:.2f} MB')
            print('Keluar dari program. Terima kasih!')
            break
        else:
            print('Menu tidak ada. Silakan pilih menu yang tersedia.')


if __name__ == "__main__":
    main()