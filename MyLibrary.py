#       __                 _   _____ _   _                 
#      /__\ ___  ___ _   _| | /__   (_) (_)_______ _ __    
#     / \/// _ \/ __| | | | |   / /\/ | | |_  / _ \  _ \   
#    / _  \  __/\__ \ |_| | |  / /  | |_| |/ /  __/ | | |  
#    \/ \_/\___||___/\__,_|_|  \/    \__,_/___\___|_| |_|  
#

# Bu program Python 3X sürümü ile hazırlanmıştır.
# Oluşturulma Tarhi: 30.05.2018 / Resul TÜZEN

import os
import sqlite3 as sql
import time


class Library:

    def __init__(self):
        self.file_sql = sql.connect("Kitaplar.db")
        self.command = self.file_sql.cursor()
        self.Open()
        self.HomePage()

    def HomePage(self):
        try:
            self.clean()    
            print('''
  MyLibrary'e hoşgeldin! \n\n
 
  1) Kitap Ekle
  2) Kitap Listele
  3) Kitap Bul
  4) Kitap Sil
  5) Kitap Düzenle
  6) Çıkış
    
    ''')
            try:
                choose = int(input(" \n  Lütfen bir seçenek seçiniz: "))

            except ValueError:
                print("\n  Üzgünüm, böyle bir seçenek yok.\n")
                self.HomePage()
        
            if(choose == 1): 
                self.AddBook()
    
            elif(choose == 2): 
                self.ListBook()
    
            elif(choose == 3): 
                self.FindBook()
    
            elif(choose == 4): 
                self.DeleteBook()
    
            elif(choose == 5): 
                self.EditBook()
    
            elif(choose == 6):       
                self.clean()
                print("\n\n  Teşekkürler :)")
                time.sleep(2) 
                exit()
        
        except RecursionError:    
            self.HomePage()

    def Open(self):
        self.command.execute('''    
    CREATE TABLE IF NOT EXISTS BookDatabase(
    BarcodeNumber CHAR(40) PRIMARY KEY NOT NULL,
    BookName CHAR(40) NOT NULL,
    AuthorName TEXT NOT NULL,
    Publisher CHAR(40) NOT NULL,
    BookType TEXT NOT NULL,
    PageNumber CHAR(5))    
    ''')

    def AddBook(self):
        self.clean()
        barcode = input("\n  Kitabın barkod numarasını giriniz: ")
        bookName = input("  Kitabın ismini giriniz: ")
        authorName = input("  Kitabın yazar ismini giriniz: ")
        publisher = input("  Kitabın yayınevi ismini giriniz: ")
        bookType = input("  Kitabın türünü giriniz: ")
        pageNumber = int(input("  Kitabın sayfa numarasını giriniz: "))
    
        information = []
        information.append(barcode)
        information.append(bookName)
        information.append(authorName)
        information.append(publisher)
        information.append(bookType)
        information.append(pageNumber)

        self.command.execute('''
        INSERT INTO BookDatabase(BarcodeNumber, BookName, AuthorName, Publisher, BookType, PageNumber)
        VALUES (?, ?, ?, ?, ?, ?) ''', information)

        self.file_sql.commit()
        self.file_sql.close()

        self.clean()
        print("\n  Kitap bilgileri başarıyla eklendi.")
        time.sleep(2)
        self.ReLoad()
        self.HomePage()

    def ListBook(self):
        self.command.execute("SELECT * FROM BookDatabase")
        read = self.command.fetchall()

        self.clean()
        print("\n\n  Sonuçlar\n\n")
        count = 0
    
        for line in read:
            barcode, bookName, authorName, publisher, bookType, pageNumber = line
        
            print("  Barkod Numarası:", barcode)
            print("  Kitap İsmi:", bookName)
            print("  Yazar İsmi:", authorName)
            print("  Yayınevi:", publisher)
            print("  Kitap Türü:", bookType)
            print("  Sayfa Sayısı:", pageNumber)
            print("\n")

            count = count + 1       
 
        print("  Toplam", count , "adet kitap var.")
        condition = input("\n\n  Ana menüye dönmek ister misin? (E / H): ")

        if(condition == "E" or condition == "e"):
            self.Homepage()

        elif(condition == "H" or condition == "h"):
            exit()

    def FindBook(self):
        self.clean()

        find = input("\n\n  Aranılacak olan kitabın adını giriniz: ")
        self.command.execute("SELECT * FROM BookDatabase WHERE BookName = ?", (find, ))
        result = self.command.fetchall()
        self.clean()
    
        print("\n\n  Sonuçlar\n\n")
        count = 0
       
        for line in result:
            barcode, bookName, authorName, publisher, bookType, pageNumber = line

            print("  Barkod Numarası:", barcode)
            print("  Kitap İsmi:", bookName)
            print("  Yazar İsmi:", authorName)
            print("  Yayınevi:", publisher)
            print("  Kitap Türü:", bookType)
            print("  Sayfa Sayısı:", pageNumber)
            print("\n")
        
            count = count + 1

        if(count == 0):
            self.clean()
            print("  Üzgünüm, aradığın bilgiye göre bir kitap bulamadım.")
        
        else:        
            print("  Toplam", count , "adet kitap bulundu.")
        

        condition = input("\n\n  Ana menüye dönmek ister misin? (E / H): ")

        if(condition == "E" or condition == "e"):
            self.HomePage()

        elif(condition == "H" or condition == "h"):
            exit()

    def DeleteBook(self):
        self.clean()
    
        delete = input("\n\n  Silinecek olan kitabın adını giriniz: ")

        self.command.execute("SELECT * FROM BookDatabase WHERE BookName = ?",(delete,))
        result = self.command.fetchall()
        self.clean()
    
        print("\n\n  Sonuçlar\n\n")

        count = 0
    
        for line in result:
            barcode, bookName, authorName, publisher, bookType, pageNumber = line

            print("  Barkod Numarası:", barcode)
            print("  Kitap İsmi:", bookName)
            print("  Yazar İsmi:", authorName)
            print("  Yayınevi:", publisher)
            print("  Kitap Türü:", bookType)
            print("  Sayfa Sayısı:", pageNumber)
            print("\n")

            count = count + 1

        if(count == 0):      
            self.clean()
            print("\n\n  Üzgünüm, aradığın bilgiye göre bir kitap bulamadım.")

        else:       
            condition = input("\n  Yukarıdaki bilgileri silmek istediğine emin misin? (E / H): ")

            if(condition == "E" or condition == "e"):        
                self.command.execute("DELETE FROM BookDatabase WHERE BarcodeNumber = ?",(delete,))
                self.file_sql.commit()
                self.file_sql.close()
                self.ReLoad()
                self.clean()
                print("\n\n  '"+ delete +"' barkod numaralı kitap başarıyla silindi.\n")
            
            elif(condition == "H" or condition == "h"):
                self.clean()
                print("\n\n  Silme işlemi iptal edildi.")

        time.sleep(2)
        self.HomePage()

    def EditBook(self):
        self.clean()

        edit = input("\n\n  Düzenlenecek olan kitabın adını giriniz: ")
    
        self.command.execute("SELECT * FROM BookDatabase WHERE BookName = ?",(edit,))
        result = self.command.fetchall()
        self.clean()
    
        print("\n\n  Sonuçlar\n\n")

        count = 0

        for line in result:
            barcode, bookName, authorName, publisher, bookType, pageNumber = line

            print("  Barkod Numarası:", barcode)
            print("  Kitap İsmi:", bookName)
            print("  Yazar İsmi:", authorName)
            print("  Yayınevi:", publisher)
            print("  Kitap Türü:", bookType)
            print("  Sayfa Sayısı:", pageNumber)
            print("\n")
        
            count = count + 1

        if(count == 0):

            self.clean()
            print("\n\n  Üzgünüm, aradığın bilgiye göre bir kitap bulamadım.")
            time.sleep(2)
        
        else:       
            print("\n  Aramanıza uygun toplam", count , "adet kitap bulundu.")

            edit = input("\n\n  Yukarıdaki sonuçlardan düzenlemek istediğin kitabın barkod numarasını giriniz: ")

            self.command.execute("SELECT * FROM BookDatabase WHERE BarcodeNumber = ?",(edit,))
            result = self.command.fetchall()
            self.clean()
        
            print("\n\n  Sonuçlar\n\n")

            for line in result:
                barcode, bookName, authorName, publisher, bookType, pageNumber = line

                print("  Barkod Numarası:", barcode)
                print("  Kitap İsmi:", bookName)
                print("  Yazar İsmi:", authorName)
                print("  Yayınevi:", publisher)
                print("  Kitap Türü:", bookType)
                print("  Sayfa Sayısı:", pageNumber)
                print("\n")

            condition = input("\n  Yukarıdaki bilgileri düzenlemek istediğine emin misin? (E / H): ")

            if(condition == "E" or condition == "e"):            
                self.clean()
            
                NewBarcode = input("\n\n  Yeni kitabın barkod numarasını giriniz: ")
                NewBookName = input("  Yeni kitabın ismini giriniz: ")
                NewAuthorName = input("  Yeni kitabın yazar ismini giriniz: ")
                NewPublisher = input("  Yeni kitabın yayınevi ismini giriniz: ")
                NewBookType = input("  Yeni kitabın türünü giriniz: ")
                NewPageNumber = int(input("  Yeni kitabın sayfa numarasını giriniz: "))
            
            
                self.command.execute("UPDATE BookDatabase SET BarcodeNumber = ? , BookName = ? , AuthorName = ? , Publisher = ? , BookType = ? , PageNumber = ? WHERE BarcodeNumber = ?",(NewBarcode, NewBookName, NewAuthorName, NewPublisher, NewBookType, NewPageNumber, edit,))
                self.file_sql.commit()
                self.file_sql.close()
                self.ReLoad()
                self.clean()

                print("\n  Kitap bilgileri başarıyla güncellendi.")

                time.sleep(2)

            elif(condition == "H" or condition == "h"):
                print("\n\n  Üzgünüm, aradığın bilgiye göre bir kitap bulamadım.")
                time.sleep(2)
    
        self.HomePage()


    def ReLoad(self):
        self.file_sql = sql.connect("Kitaplar.db")
        self.command = self.file_sql.cursor() 


    def clean(self):
        if os.name == "nt":
            os.system("cls")

        elif os.name == "posix":
            os.system("clear")

        #else:
            #print("Bilinmeyen isletim sistemi")




a1 = Library()