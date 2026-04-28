#!/usr/bin/env python
"""
Entry Point — Bookstore Management System

Kurulum:  pip install -r requirements.txt
Çalıştır: python run.py
Tarayıcı: http://localhost:5000

Keyboard Shortcuts:
  Ctrl+Alt+R (Dashboard'da) → Admin sıfırlama
"""

import os
import sys  # <-- Bu eksikti, eklendi
from pathlib import Path
from app import create_app  # <-- Bu eksikti, eklendi

sys.path.insert(0, str(Path(__file__).resolve().parent))
if __name__ == "__main__":
    env = os.environ.get("FLASK_ENV", "development")
    app = create_app(env)

    print("\n" + "=" * 60)
    print("  Bookstore Management System")
    print("=" * 60)
    print(f"  Environment : {env}")
    print(f"  URL         : http://localhost:5000")
    print(f"  Shortcut    : Ctrl+Alt+R (Admin reset on dashboard)")
    print(f"  Admin       : admin / Admin123!")
    print(f"  Customer    : alice / Alice123!  |  bob / Bob123!")
    print("=" * 60 + "\n")

    debug = env == "development"
    app.run(debug=debug, host="0.0.0.0", port=5000)
