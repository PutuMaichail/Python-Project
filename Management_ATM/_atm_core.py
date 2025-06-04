# filepath: atm_manager.py
import json
import getpass
from datetime import datetime
import uuid
from colorama import Fore, Style
from _helpers import configure_logging

# Konfigurasi logging
configure_logging('atm.log')


class ATMManager:
    def __init__(self, file_name='users.json'):
        self.file_name = file_name
        self.users = {}
        self.current_user = None
        self.session_transactions = []  # Menyimpan transaksi selama sesi login
        self.load_users()

    def load_users(self):
        """Memuat data pengguna dari file JSON."""
        try:
            with open(self.file_name, 'r') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            self.users = {}
        except json.JSONDecodeError:
            print(Fore.RED + "File JSON rusak. Menggunakan data kosong." + Style.RESET_ALL)
            self.users = {}

    def save_users(self):
        """Menyimpan data pengguna ke file JSON."""
        with open(self.file_name, 'w') as file:
            json.dump(self.users, file, indent=4)

    def create_user(self, account_number, pin):
        """Membuat pengguna baru."""
        self.users[account_number] = {
            'pin': pin,
            'balance': 0,
            'transactions': []
        }
        print(Fore.GREEN + f"Akun baru berhasil dibuat untuk nomor rekening {account_number}." + Style.RESET_ALL)

    def authenticate_user(self):
        """Mengautentikasi pengguna berdasarkan nomor rekening dan PIN."""
        account_number = input("Masukkan Nomor Rekening (3 digit): ").strip()
        if len(account_number) != 3 or not account_number.isdigit():
            print(Fore.RED + "Nomor rekening harus 3 digit." + Style.RESET_ALL)
            return False

        pin = getpass.getpass("Masukkan PIN (5 digit): ").strip()
        if len(pin) != 5 or not pin.isdigit():
            print(Fore.RED + "PIN harus 5 digit." + Style.RESET_ALL)
            return False

        if account_number in self.users:
            if self.users[account_number]['pin'] == pin:
                self.current_user = account_number
                self.session_transactions = []  # Reset transaksi sesi login
                print(Fore.GREEN + "Login berhasil." + Style.RESET_ALL)
                return True
            else:
                print(Fore.RED + "PIN salah." + Style.RESET_ALL)
                return False
        else:
            print(Fore.YELLOW + "Nomor rekening tidak ditemukan. Membuat akun baru..." + Style.RESET_ALL)
            self.create_user(account_number, pin)
            self.current_user = account_number
            self.session_transactions = []  # Reset transaksi sesi login
            return True

    def check_balance(self):
        """Menampilkan saldo pengguna."""
        balance = self.users[self.current_user]['balance']
        print(Fore.CYAN + f"Saldo Anda: Rp {balance:,}" + Style.RESET_ALL)

    def withdraw(self):
        """Melakukan penarikan tunai."""
        amount = self.get_valid_amount("Masukkan jumlah yang ingin ditarik: ")
        if amount > self.users[self.current_user]['balance']:
            print(Fore.RED + "Saldo tidak mencukupi." + Style.RESET_ALL)
        else:
            self.users[self.current_user]['balance'] -= amount
            self.add_transaction(f"Tarik Tunai: -Rp {amount:,}")
            print(Fore.GREEN + f"Berhasil menarik Rp {amount:,}. Saldo Anda sekarang: Rp {self.users[self.current_user]['balance']:,}" + Style.RESET_ALL)

    def deposit(self):
        """Melakukan setor tunai."""
        amount = self.get_valid_amount("Masukkan jumlah yang ingin disetor: ")
        self.users[self.current_user]['balance'] += amount
        self.add_transaction(f"Setor Tunai: +Rp {amount:,}")
        print(Fore.GREEN + f"Berhasil menyetor Rp {amount:,}. Saldo Anda sekarang: Rp {self.users[self.current_user]['balance']:,}" + Style.RESET_ALL)

    def change_pin(self):
        """Mengubah PIN pengguna."""
        new_pin = getpass.getpass("Masukkan PIN baru (5 digit): ").strip()
        if len(new_pin) != 5 or not new_pin.isdigit():
            print(Fore.RED + "PIN harus 5 digit." + Style.RESET_ALL)
            return
        self.users[self.current_user]['pin'] = new_pin
        print(Fore.GREEN + "PIN berhasil diubah." + Style.RESET_ALL)

    def transfer(self):
        """Melakukan transfer antar-rekening."""
        target_account = input("Masukkan nomor rekening tujuan (3 digit): ").strip()
        if target_account not in self.users:
            print(Fore.RED + "Nomor rekening tujuan tidak ditemukan." + Style.RESET_ALL)
            return

        amount = self.get_valid_amount("Masukkan jumlah yang ingin ditransfer: ")
        if amount > self.users[self.current_user]['balance']:
            print(Fore.RED + "Saldo tidak mencukupi." + Style.RESET_ALL)
        else:
            self.users[self.current_user]['balance'] -= amount
            self.users[target_account]['balance'] += amount
            self.add_transaction(f"Transfer ke {target_account}: -Rp {amount:,}")
            self.add_transaction(f"Transfer dari {self.current_user}: +Rp {amount:,}", target_account)
            print(Fore.GREEN + f"Berhasil mentransfer Rp {amount:,} ke rekening {target_account}." + Style.RESET_ALL)

    def add_transaction(self, description, account=None):
        """Menambahkan riwayat transaksi."""
        if account is None:
            account = self.current_user
        transaction = {
            'id': str(uuid.uuid4()),
            'description': description,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.users[account]['transactions'].append(transaction)
        self.session_transactions.append(transaction)  # Tambahkan ke transaksi sesi login

    def view_transactions(self):
        """Menampilkan riwayat transaksi pengguna."""
        transactions = self.users[self.current_user]['transactions']
        if transactions:
            print(Fore.CYAN + "\nRiwayat Transaksi:" + Style.RESET_ALL)
            print(f"{'ID':<36} {'Tanggal':<20} {'Deskripsi':<30}")
            print("-" * 90)
            for t in transactions:
                print(f"{t['id']:<36} {t['date']:<20} {t['description']:<30}")
        else:
            print(Fore.YELLOW + "Tidak ada riwayat transaksi." + Style.RESET_ALL)

    def logout(self):
        """Keluar dari akun dan menyimpan data."""
        print(Fore.CYAN + "\nLaporan Transaksi Sesi Login:" + Style.RESET_ALL)
        if self.session_transactions:
            print(f"{'ID':<36} {'Tanggal':<20} {'Deskripsi':<30}")
            print("-" * 90)
            for t in self.session_transactions:
                print(f"{t['id']:<36} {t['date']:<20} {t['description']:<30}")
        else:
            print(Fore.YELLOW + "Tidak ada transaksi selama sesi login." + Style.RESET_ALL)

        self.save_users()
        print(Fore.GREEN + "Data berhasil disimpan. Terima kasih telah menggunakan layanan kami." + Style.RESET_ALL)
        self.current_user = None
        self.session_transactions = []  # Reset transaksi sesi login

    def get_valid_amount(self, prompt):
        """Memastikan input jumlah valid."""
        while True:
            try:
                amount = int(input(prompt))
                if amount <= 0:
                    print(Fore.RED + "Jumlah harus lebih besar dari 0." + Style.RESET_ALL)
                    continue
                return amount
            except ValueError:
                print(Fore.RED + "Masukkan angka yang valid." + Style.RESET_ALL)