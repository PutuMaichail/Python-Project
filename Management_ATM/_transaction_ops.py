from colorama import Fore, Style
from _atm_core import ATMManager

class TransactionManagement(ATMManager):
    def check_balance(self):
        balance = self.users[self.current_user]['balance']
        print(Fore.CYAN + f"Saldo Anda: Rp {balance:,}" + Style.RESET_ALL)

    def withdraw(self, amount):
        if amount > self.users[self.current_user]['balance']:
            print(Fore.RED + "Saldo tidak mencukupi." + Style.RESET_ALL)
        else:
            self.users[self.current_user]['balance'] -= amount
            print(Fore.GREEN + f"Berhasil menarik Rp {amount:,}." + Style.RESET_ALL)

    def deposit(self, amount):
        self.users[self.current_user]['balance'] += amount
        print(Fore.GREEN + f"Berhasil menyetor Rp {amount:,}." + Style.RESET_ALL)