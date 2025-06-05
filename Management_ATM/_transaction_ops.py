from colorama import Fore, Style
from _atm_core import ATMManager

class TransactionManagement(ATMManager):
    def check_balance(self):
        """Menampilkan saldo pengguna."""
        balance = self.users[self.current_user]['balance']
        print(Fore.CYAN + f"Saldo Anda: Rp {balance:,}" + Style.RESET_ALL)

    def withdraw(self, amount):
        """Melakukan penarikan tunai."""
        if amount <= 0:
            print(Fore.RED + "Jumlah harus lebih besar dari 0." + Style.RESET_ALL)
            return
        if amount > self.users[self.current_user]['balance']:
            print(Fore.RED + "Saldo tidak mencukupi." + Style.RESET_ALL)
        else:
            self.users[self.current_user]['balance'] -= amount
            self.add_transaction(f"Tarik Tunai: -Rp {amount:,}")
            print(Fore.GREEN + f"Berhasil menarik Rp {amount:,}. Saldo Anda sekarang: Rp {self.users[self.current_user]['balance']:,}" + Style.RESET_ALL)

    def deposit(self, amount):
        """Melakukan setor tunai."""
        if amount <= 0:
            print(Fore.RED + "Jumlah harus lebih besar dari 0." + Style.RESET_ALL)
            return
        self.users[self.current_user]['balance'] += amount
        self.add_transaction(f"Setor Tunai: +Rp {amount:,}")
        print(Fore.GREEN + f"Berhasil menyetor Rp {amount:,}. Saldo Anda sekarang: Rp {self.users[self.current_user]['balance']:,}" + Style.RESET_ALL)