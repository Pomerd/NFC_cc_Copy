import nfc

def save_data_to_file(data, expiry_date):
    file_path = input("Kaydedilecek dosyanın yolunu ve adını girin: ")
    with open(file_path, 'w') as file:
        file.write("C4rd: " + data + "\n")
        file.write("Son Kullanma Tarihi: " + expiry_date)
    print("Veriler başarıyla dosyaya kaydedildi.")

def write_data_to_nfc():
    data = input("NFC kartına eklemek istediğiniz veriyi girin (16 haneli rakam): ")
    expiry_date = input("NFC kartına eklemek istediğiniz son kullanma tarihini girin (MM/YY formatında): ")
    
    # NFC kartını okuyucuya bağla
    with nfc.ContactlessFrontend('usb') as clf:
        print("NFC kartı bekleniyor...")
        
        # NFC kartını algıla
        target = clf.sense(nfc.clf.RemoteTarget('iso14443-3'))
        
        if target is not None:
            print("NFC kart algılandı!")
            tag = nfc.tag.activate(clf, target)
            
            if tag.ndef is None:
                print("NFC kartı yazılamıyor. Lütfen uygun bir kart kullanın.")
            else:
                # NFC kartına veri yaz
                data_record = nfc.ndef.TextRecord(data)
                expiry_date_record = nfc.ndef.TextRecord(expiry_date)
                tag.ndef.message = nfc.ndef.Message([data_record, expiry_date_record])
                print("Veri NFC kartına başarıyla yazıldı.")
        else:
            print("NFC kartı algılanamadı. Lütfen kartı okuyucuya doğru tutun.")

def delete_data_from_nfc():
    # NFC kartını okuyucuya bağla
    with nfc.ContactlessFrontend('usb') as clf:
        print("NFC kartı bekleniyor...")
        
        # NFC kartını algıla
        target = clf.sense(nfc.clf.RemoteTarget('iso14443-3'))
        
        if target is not None:
            print("NFC kart algılandı!")
            tag = nfc.tag.activate(clf, target)
            
            if tag.ndef is None:
                print("NFC kartı boş veya okunamıyor.")
            else:
                # NFC kartından veriyi sil
                tag.ndef.message = nfc.ndef.Message()
                print("Veri NFC kartından başarıyla silindi.")
        else:
            print("NFC kartı algılanamadı. Lütfen kartı okuyucuya doğru tutun.")

def main():
    while True:
        print("NFC Kart İşlemleri")
        print("1- Bilgi Ekle")
        print("2- Bilgi Sil")
        print("3- Çıkış")
        
        choice = input("Seçiminizi girin: ")
        
        if choice == '1':
            write_data_to_nfc()
        elif choice == '2':
            delete_data_from_nfc()
        elif choice == '3':
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçenek. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()
