# Changelog

Tüm önemli değişiklikler bu dosyada belgelenecektir.

## [Unreleased] - Başlangıç Sürümü

### Eklenenler (Added)
- Flask tabanlı temel uygulama iskeleti (`app/` dizini).
- SQLAlchemy kullanılarak veritabanı modelleri oluşturuldu (`models.py`).
- JWT kimlik doğrulama entegrasyonu (Flask-JWT-Extended ile).
- `run.py` dosyası ile kolay çalıştırma altyapısı.
- `config.py` ile çoklu ortam (Development, Production, Testing) yapılandırması.
- Admin ve Müşteri rolleri için varsayılan yetkilendirme mantığı.
- Werkzeug kullanılarak şifre hashleme ve güvenlik önlemleri.

### Değiştirilenler (Changed)
- `run.py` dosyasına çevre değişkenleri (`FLASK_ENV`) desteği eklendi.
