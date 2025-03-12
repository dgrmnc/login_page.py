import os
import re
import csv
from cryptography.fernet import Fernet


class LoginPage:

    user_file = "user.csv"
    email_max_length = 20
    password_min_length = 10
    special_characters = [chr(i) for i in range(32, 127) if not chr(i).isalnum()]

    key = b'YOUR KEY'
    

    def __init__(self):
     self.users = self.load_data(LoginPage.user_file)

    @staticmethod
    def load_data(filename):
        """CSV dosyasından kullanıcı verileri alırız"""
        if os.path.exists(filename):
            with open(filename, mode='r', newline='',encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        return []
    
    @staticmethod
    def save_data(filename, users):
        """Verileri dosyaya kayıt eder"""
        with open(filename,'w', newline='', encoding='utf-8') as file:
            fieldnames = ['id','email','password']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)

    @staticmethod
    def is_valid_password(password):
        """Şifrenin geçerliliği kontrol edilir."""
        if (
            len(password) >= LoginPage.password_min_length and
            any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in "!@#$%^&*()-_+=<>?/|\\{}[]:;" for c in password)
        ):
            return True
        else:
           return False
  
    @classmethod
    def encrypted_psw(cls, password):
        """şifreyi şifreler"""
        cipher_suite = Fernet(cls.key)
        encrypted_password = cipher_suite.encrypt(password.encode()).decode()
        return encrypted_password
    
    @classmethod
    def decrypted_psw(cls, encrypted_password):
        """şifreyi çözer"""
        cipher_suite = Fernet(cls.key)
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
        return decrypted_password
    
    def register_user(self, new_email, new_password):
        """yeni kullanıcı kaydı"""

        encrypted_password = self.encrypted_psw(new_password)
        new_user = {
            "id":str(self.get_id()),
            "email": new_email,
            "password": encrypted_password
        }

        self.users.append(new_user)
        self.save_data(LoginPage.user_file, self.users)
        print("Yeni üye kaydı tamamlanmıştır. Giriş yapabilirsiniz.")

    @classmethod
    def show_decode_password(cls):
        """ csv dos. şifreli şifreleri çözer ve ekrana basar"""
        cipher_suite = Fernet(cls.key)
        try:
            with open(cls.user_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                print("\n>>>Kayıtlı Kullanıcılar ve gerçek şifreleri<<<\n")
                for row in reader:
                    email = row['email']
                    encrypted_password = row['password'].encode()
                    try:
                        decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
                    except Exception as e:
                        decrypted_password = f"Hata: {str(e)}"
                    print(f"Email: {email} | Şifre: {decrypted_password}")
        except FileNotFoundError:
            print("CSV dosyası bulunamadı.")
        except Exception as  e:
            print(f"{e}")

    def get_id(self):
        """mevcut en yüksek ID bulur ve bir sonrakini yeni girişe yazar"""
        if not self.users:
            return 1
        return max(int(user['id']) for user in self.users) + 1

    def login(self):
        try:
           email = input("Email adresinizi giriniz: ").lower()
           user = next((u for u in self.users if u["email"] == email), None) # email kullanıcılarda arayacak
           if user:
                decrypted_password = self.decrypted_psw(user['password'])
                while True:
                    input_psw = input('Lütfen şifrenizi giriniz: ')
                    if input_psw == decrypted_password:
                        print("Giriş başarılı..")
                        break
                    else:
                        print("Yanlış şifre lütfen tekrar deneyeniz..")
           else:
                print("Kayıtlı böyle bir kullanıcıya ulaşılamamıştır.")
                new_registered = input("Yeni üye olmak ister misinz?(Y/N): ").upper()
                if new_registered == 'Y':
                    new_email = input("Email adresiniz: ")
                    if len(new_email) <= self.email_max_length:
                        print("\nŞifreniz minimum 10 karakterden oluşmalıdır.")
                        print("\nŞifrenizde bir büyük harf ve bir özel karakter olmalıdır.\n")
                        while True:
                            new_password = input("Lütfen şifrenizi belirleyiniz:" )
                            if self.is_valid_password(new_password):
                                self.register_user(new_email, new_password)
                                break
                            else:
                                print("Şifreniz geçerli değil, lütfen geçerli bir şifre girin.")
        except ValueError as e:
            print(f"hatalı işlem : {e}")

def main():
    g = LoginPage()
    try:
        while True:
            print("\n1: Giriş ekranına aktarma")
            print("2: Şifreleri görme")
            do_what = input("Yapmak istediğiniz işlem türünü seçin?(1 - 2): ")
            if do_what == "1":
                g.login()
            else:
                g.show_decode_password()
    except ValueError as e:
        print("f{e}")

if __name__ == '__main__':
    main()
