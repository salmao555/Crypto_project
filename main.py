#!/usr/bin/env python3
"""
CryptoVault Pro - Professional Cryptography & Password Management System
Main CLI Interface
"""

import sys
import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from algorithms import symmetric, asymmetric, hashing
from user_manager import UserManager, PasswordManager

console = Console()


class CryptoVaultCLI:
    """Main CLI Application"""
    
    def __init__(self):
        self.user_manager = UserManager()
        self.current_user = None
        self.password_manager = None
    
    def show_banner(self):
        """Display application banner"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║                    CRYPTO PROJECT                         ║
║                                                           ║
║     Professional Cryptography & Password Manager          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """
        console.print(Panel(banner, style="bold cyan", box=box.DOUBLE))
    
    def main_menu(self):
        """Display main menu"""
        if not self.current_user:
            return self.auth_menu()
        
        while True:
            console.clear()
            self.show_banner()
            console.print(f"\n[bold green]👤 Logged in as: {self.current_user}[/bold green]\n")
            
            menu = Table(show_header=False, box=box.ROUNDED, border_style="cyan")
            menu.add_column("Option", style="cyan bold", width=5)
            menu.add_column("Description", style="white")
            
            menu.add_row("1", "👥 Manage Users")
            menu.add_row("2", "🔑 Manage Passwords")
            menu.add_row("3", "🔒 Encrypt/Decrypt Messages")
            menu.add_row("4", "⚡ Test Cryptographic Algorithms")
            menu.add_row("5", "🔐 Hash Passwords")
            menu.add_row("6", "📊 Algorithm Comparison")
            menu.add_row("0", "🚪 Logout")
            
            console.print(menu)
            
            choice = Prompt.ask("\n[bold yellow]Choose an option[/bold yellow]", choices=['0','1','2','3','4','5','6'])
            
            if choice == '0':
                self.current_user = None
                self.password_manager = None
                console.print("\n[green]✓ Logged out successfully[/green]")
                time.sleep(1)
                return
            elif choice == '1':
                self.manage_users_menu()
            elif choice == '2':
                self.manage_passwords_menu()
            elif choice == '3':
                self.encrypt_decrypt_menu()
            elif choice == '4':
                self.test_algorithms_menu()
            elif choice == '5':
                self.hash_menu()
            elif choice == '6':
                self.comparison_menu()
    
    def auth_menu(self):
        """Authentication menu"""
        while True:
            console.clear()
            self.show_banner()
            
            menu = Table(show_header=False, box=box.ROUNDED, border_style="cyan")
            menu.add_column("Option", style="cyan bold", width=5)
            menu.add_column("Description", style="white")
            
            menu.add_row("1", "🔓 Login")
            menu.add_row("2", "📝 Register")
            menu.add_row("0", "🚪 Exit")
            
            console.print(menu)
            
            choice = Prompt.ask("\n[bold yellow]Choose an option[/bold yellow]", choices=['0','1','2'])
            
            if choice == '0':
                console.print("\n[cyan]👋 Thank you for using CryptoVault Pro![/cyan]")
                sys.exit(0)
            elif choice == '1':
                if self.login():
                    # Successfully logged in, break out of auth menu
                    break
            elif choice == '2':
                self.register()
    
    def login(self):
        """User login"""
        console.print("\n[bold cyan]═══ LOGIN ═══[/bold cyan]")
        username = Prompt.ask("Username")
        password = Prompt.ask("Password", password=True)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Authenticating...", total=None)
            time.sleep(0.5)
            
            if self.user_manager.authenticate(username, password):
                self.current_user = username
                self.password_manager = PasswordManager(username)
                console.print(f"\n[green]✓ Welcome back, {username}![/green]")
                time.sleep(1)
                return True
            else:
                console.print("\n[red]✗ Invalid credentials[/red]")
                time.sleep(2)
                return False
    
    def register(self):
        """User registration"""
        console.print("\n[bold cyan]═══ REGISTER ═══[/bold cyan]")
        username = Prompt.ask("Choose username")
        password = Prompt.ask("Choose password", password=True)
        confirm_password = Prompt.ask("Confirm password", password=True)
        
        if password != confirm_password:
            console.print("\n[red]✗ Passwords don't match[/red]")
            time.sleep(2)
            return
        
        email = Prompt.ask("Email (optional)", default="")
        
        success, message = self.user_manager.create_user(username, password, email)
        
        if success:
            console.print(f"\n[green]✓ {message}[/green]")
            console.print("[yellow]You can now login with your credentials[/yellow]")
        else:
            console.print(f"\n[red]✗ {message}[/red]")
        
        time.sleep(2)
    
    def manage_users_menu(self):
        """User management submenu"""
        while True:
            console.clear()
            console.print(Panel("[bold cyan]👥 USER MANAGEMENT[/bold cyan]", box=box.DOUBLE))
            
            menu = Table(show_header=False, box=box.ROUNDED)
            menu.add_column("Option", style="cyan bold", width=5)
            menu.add_column("Description", style="white")
            
            menu.add_row("1", "📋 List All Users")
            menu.add_row("2", "👁️  View User Info")
            menu.add_row("3", "✏️  Modify User")
            menu.add_row("4", "🗑️  Delete User")
            menu.add_row("0", "⬅️  Back")
            
            console.print(menu)
            
            choice = Prompt.ask("\n[bold yellow]Choose an option[/bold yellow]", choices=['0','1','2','3','4'])
            
            if choice == '0':
                return
            elif choice == '1':
                self.list_users()
            elif choice == '2':
                self.view_user_info()
            elif choice == '3':
                self.modify_user()
            elif choice == '4':
                self.delete_user()
    
    def list_users(self):
        """List all users"""
        users = self.user_manager.list_users()
        
        if not users:
            console.print("\n[yellow]No users found[/yellow]")
        else:
            table = Table(title="Registered Users", box=box.ROUNDED, border_style="cyan")
            table.add_column("#", style="cyan", width=5)
            table.add_column("Username", style="green bold")
            
            for idx, user in enumerate(users, 1):
                table.add_row(str(idx), user)
            
            console.print("\n", table)
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
    
    def view_user_info(self):
        """View user information"""
        username = Prompt.ask("\nEnter username")
        
        info = self.user_manager.get_user_info(username)
        
        if info:
            table = Table(title=f"User Info: {username}", box=box.ROUNDED, border_style="cyan")
            table.add_column("Field", style="cyan bold")
            table.add_column("Value", style="white")
            
            for key, value in info.items():
                table.add_row(key.replace('_', ' ').title(), str(value))
            
            console.print("\n", table)
        else:
            console.print(f"\n[red]✗ User '{username}' not found[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
    
    def modify_user(self):
        """Modify user"""
        console.print("\n[bold cyan]═══ MODIFY USER ═══[/bold cyan]")
        username = Prompt.ask("Username to modify")
        
        if username not in self.user_manager.list_users():
            console.print(f"\n[red]✗ User '{username}' not found[/red]")
            time.sleep(2)
            return
        
        new_password = Prompt.ask("New password (leave empty to skip)", default="")
        new_email = Prompt.ask("New email (leave empty to skip)", default="")
        
        success, message = self.user_manager.modify_user(
            username, 
            new_password if new_password else None,
            new_email if new_email else None
        )
        
        if success:
            console.print(f"\n[green]✓ {message}[/green]")
        else:
            console.print(f"\n[red]✗ {message}[/red]")
        
        time.sleep(2)
    
    def delete_user(self):
        """Delete user"""
        console.print("\n[bold cyan]═══ DELETE USER ═══[/bold cyan]")
        username = Prompt.ask("Username to delete")
        
        if username == self.current_user:
            console.print("\n[red]✗ Cannot delete the currently logged in user[/red]")
            time.sleep(2)
            return
        
        if Confirm.ask(f"[bold red]Are you sure you want to delete '{username}'?[/bold red]"):
            success, message = self.user_manager.delete_user(username)
            
            if success:
                console.print(f"\n[green]✓ {message}[/green]")
            else:
                console.print(f"\n[red]✗ {message}[/red]")
            
            time.sleep(2)
    
    def manage_passwords_menu(self):
        """Password management submenu"""
        while True:
            console.clear()
            console.print(Panel("[bold cyan]🔑 PASSWORD MANAGEMENT[/bold cyan]", box=box.DOUBLE))
            
            menu = Table(show_header=False, box=box.ROUNDED)
            menu.add_column("Option", style="cyan bold", width=5)
            menu.add_column("Description", style="white")
            
            menu.add_row("1", "📋 List Services")
            menu.add_row("2", "➕ Add Password")
            menu.add_row("3", "👁️  View Password")
            menu.add_row("4", "✏️  Modify Password")
            menu.add_row("5", "🗑️  Delete Password")
            menu.add_row("6", "📊 Password Strength Check")
            menu.add_row("0", "⬅️  Back")
            
            console.print(menu)
            
            choice = Prompt.ask("\n[bold yellow]Choose an option[/bold yellow]", choices=['0','1','2','3','4','5','6'])
            
            if choice == '0':
                return
            elif choice == '1':
                self.list_services()
            elif choice == '2':
                self.add_password()
            elif choice == '3':
                self.view_password()
            elif choice == '4':
                self.modify_password()
            elif choice == '5':
                self.delete_password()
            elif choice == '6':
                self.check_password_strength()
    
    def list_services(self):
        """List all services"""
        services = self.password_manager.list_services()
        
        if not services:
            console.print("\n[yellow]No passwords stored yet[/yellow]")
        else:
            table = Table(title="Stored Passwords", box=box.ROUNDED, border_style="cyan")
            table.add_column("#", style="cyan", width=5)
            table.add_column("Service", style="green bold")
            
            for idx, service in enumerate(services, 1):
                table.add_row(str(idx), service)
            
            console.print("\n", table)
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
    
    def add_password(self):
        """Add a password"""
        console.print("\n[bold cyan]═══ ADD PASSWORD ═══[/bold cyan]")
        service = Prompt.ask("Service name (e.g., Gmail, Facebook)")
        password = Prompt.ask("Password", password=True)
        notes = Prompt.ask("Notes (optional)", default="")
        
        # Show password strength
        strength = self.password_manager.get_password_strength(password)
        console.print(f"\n[yellow]Password Strength: {strength['rating']} ({strength['score']}/6)[/yellow]")
        
        success, message = self.password_manager.create_password(service, password, notes)
        
        if success:
            console.print(f"\n[green]✓ {message}[/green]")
        else:
            console.print(f"\n[red]✗ {message}[/red]")
        
        time.sleep(2)
    
    def view_password(self):
        """View a password"""
        console.print("\n[bold cyan]═══ VIEW PASSWORD ═══[/bold cyan]")
        service = Prompt.ask("Service name")
        
        pwd_data = self.password_manager.get_password(service)
        
        if pwd_data:
            table = Table(title=f"Password for: {service}", box=box.ROUNDED, border_style="cyan")
            table.add_column("Field", style="cyan bold")
            table.add_column("Value", style="white")
            
            table.add_row("Password", pwd_data['password'])
            table.add_row("Notes", pwd_data['notes'])
            table.add_row("Created", pwd_data['created_at'])
            table.add_row("Modified", str(pwd_data.get('modified_at', 'Never')))
            
            console.print("\n", table)
        else:
            console.print(f"\n[red]✗ Password for '{service}' not found[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
    
    def modify_password(self):
        """Modify a password"""
        console.print("\n[bold cyan]═══ MODIFY PASSWORD ═══[/bold cyan]")
        service = Prompt.ask("Service name")
        
        if service not in self.password_manager.list_services():
            console.print(f"\n[red]✗ Password for '{service}' not found[/red]")
            time.sleep(2)
            return
        
        new_password = Prompt.ask("New password (leave empty to skip)", password=True, default="")
        new_notes = Prompt.ask("New notes (leave empty to skip)", default="")
        
        success, message = self.password_manager.modify_password(
            service,
            new_password if new_password else None,
            new_notes if new_notes else None
        )
        
        if success:
            console.print(f"\n[green]✓ {message}[/green]")
        else:
            console.print(f"\n[red]✗ {message}[/red]")
        
        time.sleep(2)
    
    def delete_password(self):
        """Delete a password"""
        console.print("\n[bold cyan]═══ DELETE PASSWORD ═══[/bold cyan]")
        service = Prompt.ask("Service name")
        
        if Confirm.ask(f"[bold red]Are you sure you want to delete password for '{service}'?[/bold red]"):
            success, message = self.password_manager.delete_password(service)
            
            if success:
                console.print(f"\n[green]✓ {message}[/green]")
            else:
                console.print(f"\n[red]✗ {message}[/red]")
            
            time.sleep(2)
    
    def check_password_strength(self):
        """Check password strength"""
        console.print("\n[bold cyan]═══ PASSWORD STRENGTH CHECKER ═══[/bold cyan]")
        password = Prompt.ask("Enter password to check", password=True)
        
        strength = self.password_manager.get_password_strength(password)
        
        table = Table(title="Password Strength Analysis", box=box.ROUNDED, border_style="cyan")
        table.add_column("Criterion", style="cyan bold")
        table.add_column("Status", style="white")
        
        table.add_row("Length", str(strength['length']))
        table.add_row("Has Uppercase", "✓" if strength['has_upper'] else "✗")
        table.add_row("Has Lowercase", "✓" if strength['has_lower'] else "✗")
        table.add_row("Has Digits", "✓" if strength['has_digit'] else "✗")
        table.add_row("Has Special Chars", "✓" if strength['has_special'] else "✗")
        table.add_row("Score", f"{strength['score']}/6")
        table.add_row("Rating", f"[{'green' if strength['rating'] == 'Strong' else 'yellow' if strength['rating'] == 'Medium' else 'red'}]{strength['rating']}[/]")
        
        console.print("\n", table)
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
    
    def encrypt_decrypt_menu(self):
        """Encryption/Decryption menu"""
        while True:
            console.clear()
            console.print(Panel("[bold cyan]🔒 ENCRYPT/DECRYPT[/bold cyan]", box=box.DOUBLE))
            
            menu = Table(show_header=False, box=box.ROUNDED)
            menu.add_column("Option", style="cyan bold", width=5)
            menu.add_column("Description", style="white")
            
            menu.add_row("1", "🔤 Caesar Cipher")
            menu.add_row("2", "🔡 Vigenere Cipher")
            menu.add_row("3", "🎲 Vernam Cipher (OTP)")
            menu.add_row("4", "⚡ RC4 Stream Cipher")
            menu.add_row("5", "🔐 RSA (Asymmetric)")
            menu.add_row("0", "⬅️  Back")
            
            console.print(menu)
            
            choice = Prompt.ask("\n[bold yellow]Choose an option[/bold yellow]", choices=['0','1','2','3','4','5'])
            
            if choice == '0':
                return
            elif choice == '1':
                self.caesar_cipher_demo()
            elif choice == '2':
                self.vigenere_cipher_demo()
            elif choice == '3':
                self.vernam_cipher_demo()
            elif choice == '4':
                self.rc4_cipher_demo()
            elif choice == '5':
                self.rsa_cipher_demo()
    
    def caesar_cipher_demo(self):
        """Caesar cipher demonstration"""
        console.print("\n[bold cyan]═══ CAESAR CIPHER ═══[/bold cyan]")
        
        operation = Prompt.ask("Operation", choices=['encrypt', 'decrypt'])
        text = Prompt.ask("Text")
        key = int(Prompt.ask("Shift key (number)"))
        
        if operation == 'encrypt':
            result = symmetric.cesar_cipher(text, key)
            console.print(f"\n[green]Encrypted:[/green] {result}")
        else:
            result = symmetric.cesar_decipher(text, key)
            console.print(f"\n[green]Decrypted:[/green] {result}")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
    
    def vigenere_cipher_demo(self):
        """Vigenere cipher demonstration"""
        console.print("\n[bold cyan]═══ VIGENERE CIPHER ═══[/bold cyan]")
        
        operation = Prompt.ask("Operation", choices=['encrypt', 'decrypt'])
        text = Prompt.ask("Text")
        key = Prompt.ask("Key (word)")
        
        if operation == 'encrypt':
            result = symmetric.vigenere_cipher(text, key)
            console.print(f"\n[green]Encrypted:[/green] {result}")
        else:
            result = symmetric.vigenere_decipher(text, key)
            console.print(f"\n[green]Decrypted:[/green] {result}")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
    
    def vernam_cipher_demo(self):
        """Vernam cipher demonstration"""
        console.print("\n[bold cyan]═══ VERNAM CIPHER (One-Time Pad) ═══[/bold cyan]")
        
        operation = Prompt.ask("Operation", choices=['encrypt', 'decrypt'])
        text = Prompt.ask("Text")
        key = Prompt.ask("Key")
        
        if operation == 'encrypt':
            result = symmetric.vernam_cipher(text, key)
            console.print(f"\n[green]Encrypted:[/green] {result}")
        else:
            result = symmetric.vernam_decipher(text, key)
            console.print(f"\n[green]Decrypted:[/green] {result}")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
    
    def rc4_cipher_demo(self):
        """RC4 cipher demonstration"""
        console.print("\n[bold cyan]═══ RC4 STREAM CIPHER ═══[/bold cyan]")
        
        operation = Prompt.ask("Operation", choices=['encrypt', 'decrypt'])
        text = Prompt.ask("Text")
        key = Prompt.ask("Key")
        
        if operation == 'encrypt':
            result = symmetric.rc4_cipher(text, key)
            console.print(f"\n[green]Encrypted:[/green] {repr(result)}")
        else:
            result = symmetric.rc4_decipher(text, key)
            console.print(f"\n[green]Decrypted:[/green] {result}")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
    
    def rsa_cipher_demo(self):
        """RSA cipher demonstration"""
        console.print("\n[bold cyan]═══ RSA ASYMMETRIC ENCRYPTION ═══[/bold cyan]")
        
        console.print("\n[yellow]Generating RSA keys...[/yellow]")
        
        # Use small primes for demo
        p = 61
        q = 53
        
        public_key, private_key = asymmetric.generer_cles_rsa(p, q)
        
        console.print(f"\n[cyan]Public Key (e, n):[/cyan] {public_key}")
        console.print(f"[cyan]Private Key (d, n):[/cyan] {private_key}")
        
        message = int(Prompt.ask("\nEnter numeric message (< n)"))
        
        encrypted = asymmetric.cryptage_rsa(message, public_key[0], public_key[1])
        console.print(f"\n[green]Encrypted:[/green] {encrypted}")
        
        decrypted = asymmetric.decryptage_rsa(encrypted, private_key[0], private_key[1])
        console.print(f"[green]Decrypted:[/green] {decrypted}")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
    
    def test_algorithms_menu(self):
        """Test algorithms menu"""
        console.clear()
        console.print(Panel("[bold cyan]⚡ ALGORITHM TESTING[/bold cyan]", box=box.DOUBLE))
        
        console.print("\n[bold]Testing Symmetric Encryption (RC4)[/bold]")
        test_msg = "Hello CryptoVault!"
        test_key = "SECRET"
        
        encrypted = symmetric.rc4_cipher(test_msg, test_key)
        decrypted = symmetric.rc4_decipher(encrypted, test_key)
        
        console.print(f"Original:  [cyan]{test_msg}[/cyan]")
        console.print(f"Encrypted: [yellow]{repr(encrypted)}[/yellow]")
        console.print(f"Decrypted: [green]{decrypted}[/green]")
        console.print(f"Match: [{'green' if test_msg == decrypted else 'red'}]{test_msg == decrypted}[/{'green' if test_msg == decrypted else 'red'}]")
        
        console.print("\n[bold]Testing Asymmetric Encryption (RSA)[/bold]")
        pub, priv = asymmetric.generer_cles_rsa(61, 53)
        msg = 42
        enc = asymmetric.cryptage_rsa(msg, pub[0], pub[1])
        dec = asymmetric.decryptage_rsa(enc, priv[0], priv[1])
        
        console.print(f"Original:  [cyan]{msg}[/cyan]")
        console.print(f"Encrypted: [yellow]{enc}[/yellow]")
        console.print(f"Decrypted: [green]{dec}[/green]")
        console.print(f"Match: [{'green' if msg == dec else 'red'}]{msg == dec}[/{'green' if msg == dec else 'red'}]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
    
    def hash_menu(self):
        """Hashing menu"""
        console.clear()
        console.print(Panel("[bold cyan]🔐 PASSWORD HASHING[/bold cyan]", box=box.DOUBLE))
        
        text = Prompt.ask("\nEnter text to hash")
        
        sha1_hash = hashing.SHA1(text)
        sha256_hash = hashing.SHA256(text)
        
        table = Table(title="Hash Results", box=box.ROUNDED, border_style="cyan")
        table.add_column("Algorithm", style="cyan bold", width=10)
        table.add_column("Hash", style="green")
        
        table.add_row("SHA-1", sha1_hash)
        table.add_row("SHA-256", sha256_hash)
        
        console.print("\n", table)
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
    
    def comparison_menu(self):
        """Algorithm comparison"""
        console.clear()
        console.print(Panel("[bold cyan]📊 ALGORITHM COMPARISON[/bold cyan]", box=box.DOUBLE))
        
        test_text = Prompt.ask("\nEnter text to test", default="Hello World!")
        test_key = Prompt.ask("Enter key", default="KEY")
        
        console.print("\n[bold]Comparing Symmetric Algorithms[/bold]\n")
        
        table = Table(box=box.ROUNDED, border_style="cyan")
        table.add_column("Algorithm", style="cyan bold")
        table.add_column("Type", style="yellow")
        table.add_column("Encrypted Result", style="white")
        
        # Caesar
        caesar_enc = symmetric.cesar_cipher(test_text, 3)
        table.add_row("Caesar", "Substitution", caesar_enc[:50] + "..." if len(caesar_enc) > 50 else caesar_enc)
        
        # Vigenere
        vigenere_enc = symmetric.vigenere_cipher(test_text, test_key)
        table.add_row("Vigenere", "Polyalphabetic", vigenere_enc[:50] + "..." if len(vigenere_enc) > 50 else vigenere_enc)
        
        # Vernam
        vernam_enc = symmetric.vernam_cipher(test_text, test_key)
        table.add_row("Vernam", "OTP (XOR)", vernam_enc[:50] + "..." if len(vernam_enc) > 50 else vernam_enc)
        
        # RC4
        rc4_enc = symmetric.rc4_cipher(test_text, test_key)
        table.add_row("RC4", "Stream Cipher", repr(rc4_enc[:50]) + "..." if len(rc4_enc) > 50 else repr(rc4_enc))
        
        console.print(table)
        
        console.print("\n[bold]Hash Comparison[/bold]\n")
        
        hash_table = Table(box=box.ROUNDED, border_style="cyan")
        hash_table.add_column("Algorithm", style="cyan bold")
        hash_table.add_column("Output Length", style="yellow")
        hash_table.add_column("Hash", style="green")
        
        sha1 = hashing.SHA1(test_text)
        sha256 = hashing.SHA256(test_text)
        
        hash_table.add_row("SHA-1", "160 bits", sha1)
        hash_table.add_row("SHA-256", "256 bits", sha256)
        
        console.print(hash_table)
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
    
    def run(self):
        """Run the application"""
        try:
            while True:
                self.main_menu()
        except KeyboardInterrupt:
            console.print("\n\n[cyan]👋 Thank you for using CryptoVault Pro![/cyan]")
            sys.exit(0)


if __name__ == "__main__":
    app = CryptoVaultCLI()
    app.run()
