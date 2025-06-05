import getpass
from colorama import Fore, Style
from _atm_core import ATMManager

class UserManagement(ATMManager):
    def create_user(self, account_number, pin):
        self.users[account_number] = {
            'pin': pin,
            'balance': 0,
            'transactions': []
        }
        print(Fore.GREEN + f"Akun baru berhasil dibuat untuk nomor rekening {account_number}." + Style.RESET_ALL)

    def authenticate_user(self):
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
                print(Fore.GREEN + "Login berhasil." + Style.RESET_ALL)
                return True
            else:
                print(Fore.RED + "PIN salah." + Style.RESET_ALL)
                return False
        else:
            print(Fore.YELLOW + "Nomor rekening tidak ditemukan. Membuat akun baru..." + Style.RESET_ALL)
            self.create_user(account_number, pin)
            self.current_user = account_number
            return True