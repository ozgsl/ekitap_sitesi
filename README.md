# Bookstore Management System 📚

Profesyonel ve modern bir E-Kitap/Kitap Mağazası Yönetim Sistemi. Python, Flask, SQLAlchemy ve JWT kimlik doğrulama kullanılarak geliştirilmiştir.

## 🚀 Özellikler

- **Kullanıcı Rolleri:** Admin ve Müşteri (Customer) yetkilendirmeleri.
- **Güvenli Kimlik Doğrulama:** JWT (JSON Web Token) tabanlı güvenli giriş ve oturum yönetimi.
- **Veritabanı Entegrasyonu:** SQLAlchemy ORM ile güçlü ve esnek veritabanı yönetimi (Geliştirme için SQLite desteği).
- **RESTful API Yaklaşımı:** Modüler ve genişletilebilir API uç noktaları.
- **Güvenlik:** Werkzeug ile şifre hashleme ve güvenli doğrulama.

## 🛠️ Teknolojiler

- **Backend:** Python 3.x, Flask 3.0
- **Veritabanı:** Flask-SQLAlchemy, SQLAlchemy 2.0
- **Kimlik Doğrulama:** Flask-JWT-Extended, PyJWT
- **Güvenlik:** Werkzeug
- **Sunucu:** Gunicorn (Production için)

## 📦 Kurulum

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin:

### 1. Depoyu Klonlayın
```bash
git clone <repository-url>
cd ekitap_sitesi
```

### 2. Sanal Ortam Oluşturun ve Aktif Edin
```bash
python -m venv venv
# Windows için:
venv\Scripts\activate
# Linux/Mac için:
source venv/bin/activate
```

### 3. Gerekli Paketleri Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Çevresel Değişkenleri Ayarlayın (Opsiyonel)
Proje dizininde bir `.env` dosyası oluşturun ve gerekli konfigürasyonları ekleyin (bkz. `config.py`).

## 💻 Kullanım

Uygulamayı geliştirme modunda başlatmak için:

```bash
python run.py
```

Tarayıcınızdan `http://localhost:5000` adresine giderek uygulamaya erişebilirsiniz.

### Varsayılan Test Kullanıcıları
- **Admin:** `admin` / `Admin123!`
- **Müşteri 1:** `alice` / `Alice123!`
- **Müşteri 2:** `bob` / `Bob123!`

*Kısayol: Dashboard ekranında `Ctrl+Alt+R` ile admin verilerini sıfırlayabilirsiniz.*

## 📁 Proje Yapısı

```text
ekitap_sitesi/
├── app/                  # Flask uygulama modülleri (routes, models, utils vb.)
├── instance/             # Veritabanı ve gizli yapılandırma dosyaları
├── config.py             # Ortam tabanlı yapılandırma ayarları
├── requirements.txt      # Proje bağımlılıkları
├── run.py                # Uygulama başlatma dosyası
└── README.md             # Proje dokümantasyonu
```


