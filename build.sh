#!/bin/bash

# Keluar jika ada error
set -o errexit

# Install semua paket
pip install -r requirements.txt

# Jalankan migrasi database
python manage.py migrate