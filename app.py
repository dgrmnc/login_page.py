import os
import re
import csv

class LoginPage:

    user_file = "user.csv"
    email_max_length = 20
    password_min_length = 10
    special_characters = [chr(i) for i in range(32, 127) if not chr(i).isalnum()]

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
                while True:
                    password = input('Lütfen şifrenizi giriniz: ')
                    if user['password'] == password:
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
                                new_user = {
                                    "id": str(self.get_id()),
                                    "email": new_email,
                                    "password": new_password
                                }
                                self.users.append(new_user)

                                self.save_data(LoginPage.user_file, self.users)
                                print("Yeni üye kaydı tamamlanmıştır. Giriş yapabilirsiniz.")
                                break
                            else:
                                print("Şifreniz geçerli değil, lütfen geçerli bir şifre girin.")
                else:
                    print("Email zaten mevcut")
        except ValueError as e:
            print(f"hatalı işlem : {e}")

def main():
    g = LoginPage()
    g.login()

if __name__ == '__main__':
    main()