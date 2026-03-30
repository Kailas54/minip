"""
Generate Self-Signed SSL Certificate for Django Development
"""

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import socket
import ipaddress

# Get hostname
hostname = socket.gethostname()

print("=" * 60)
print("Generating Self-Signed SSL Certificate")
print("=" * 60)
print()

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
    datetime.datetime.now(datetime.timezone.utc)
).not_valid_after(
    datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
).add_extension(
    x509.SubjectAlternativeName([
        x509.DNSName(hostname),
        x509.DNSName('localhost'),
        x509.IPAddress(ipaddress.IPv4Address('127.0.0.1')),
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
print('=' * 60)
