import socket
import qrcode
import os

def get_local_ip():
    """Get the local IP address of the machine connected to the network"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable, just helps find the right interface
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def show_qr():
    ip = get_local_ip()
    port = 8000
    url = f"http://{ip}:{port}/dashboard/"
    
    print("\n" + "="*50)
    print(f"📡 SERVER ACCESS: {url}")
    print("="*50)
    print("\nSCAN THIS QR CODE WITH YOUR PHONE CAMERA TO OPEN THE DASHBOARD:\n")
    
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    
    # Print QR on console
    qr.print_ascii(invert=True)
    
    print("\n" + "="*50)
    print("💡 TIP: Ensure your phone and PC are on the same Wi-Fi.")
    print("💡 TIP: If the QR is too large, zoom out your terminal (Ctrl + Minus).")
    print("="*50 + "\n")

if __name__ == "__main__":
    show_qr()
