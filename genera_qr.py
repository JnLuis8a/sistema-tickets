import qrcode
IP = "192.168.0.7"  # Tu IP fija
PORT = "8080"       # Tu nuevo puerto
equipos = ["RayosX001", "Ecografo002"]

for equipo in equipos:
    url = f"http://{IP}:{PORT}/form/{equipo}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"QR_{equipo}_8080.png")
    print(f"✅ QR_{equipo}_8080.png = {url}")
