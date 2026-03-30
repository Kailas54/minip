@echo off
REM Install HTTPS Support Packages
echo ============================================================
echo    Installing HTTPS Support for Django
echo ============================================================
echo.

echo Installing uvicorn (ASGI server with HTTPS support)...
pip install uvicorn[standard]

echo.
echo Installing cryptography (for SSL certificate generation)...
pip install cryptography

echo.
echo ============================================================
echo    Generating Self-Signed SSL Certificate
echo ============================================================
echo.

python -c "
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import socket

# Get hostname
hostname = socket.gethostname()

# Generate private key
print('Generating RSA private key...')
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Generate self-signed certificate
print('Generating self-signed certificate...')
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, 'US'),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'Local'),
    x509.NameAttribute(NameOID.LOCALITY_NAME, 'Development'),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'Django Dev Server'),
    x509.NameAttribute(NameOID.COMMON_NAME, hostname),
])

cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    private_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).add_extension(
    x509.SubjectAlternativeName([
        x509.DNSName(hostname),
        x509.DNSName('localhost'),
        x509.IPAddress('127.0.0.1'),
    ]),
    critical=False,
).sign(private_key, hashes.SHA256())

# Save certificate
with open('cert.pem', 'wb') as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))
print('✓ Certificate saved to: cert.pem')

# Save private key  
with open('key.pem', 'wb') as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))
print('✓ Private key saved to: key.pem')

print()
print('SSL certificate generated successfully!')
print('Valid for: localhost, 127.0.0.1, and your computer name')
"

echo.
echo ============================================================
echo    Setup Complete!
echo ============================================================
echo.
echo HTTPS server is ready to run!
echo.
echo To start HTTPS server:
echo   python run_https_server.py
echo.
echo Then access:
echo   https://localhost:8000
echo   https://127.0.0.1:8000
echo.
echo Note: Browser will warn about self-signed certificate
echo       Click 'Proceed' or 'Accept Risk and Continue'
echo ============================================================
echo.
pause
