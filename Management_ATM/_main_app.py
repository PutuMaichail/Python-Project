from _user_auth import UserManagement
from _transaction_ops import TransactionManagement
from _helpers import configure_logging

def main():
    configure_logging('atm.log')
    atm = UserManagement()

    if not atm.authenticate_user():
        return

    while True:
        print("\nMenu:")
        print("1. Cek Saldo")
        print("2. Tarik Tunai")
        print("3. Setor Tunai")
        print("4. Transfer")
        print("5. Ubah PIN")
        print("6. Riwayat Transaksi")
        print("7. Keluar")
        choice = input("Pilih menu: ").strip()

        if choice == '1':
            atm.check_balance()
        elif choice == '2':
            amount = int(input("Masukkan jumlah: "))
            atm.withdraw(amount)
        elif choice == '3':
            amount = int(input("Masukkan jumlah: "))
            atm.deposit(amount)
        elif choice == '4':
            atm.transfer()
        elif choice == '5':
            atm.change_pin()
        elif choice == '6':
            atm.view_transactions()
        elif choice == '7':
            atm.logout()
            break
        else:
            print("Pilihan tidak valid.")

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

if __name__ == "__main__":
    main()