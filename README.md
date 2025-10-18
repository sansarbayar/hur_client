# ХУР client /Python/

- Цахим хөгжил, инновац, харилцаа холбооны яам /ЦХИХХЯ/-с ХУР ашиглаглах гэрээ байгууласан байх
- Гэрээний дагуу Үндэсний дата төвөөс ХУР-тай холбогдох VPN холболтын эрх болон VPN холболтын файл авсан байх

## Host file-d нэмэх тохиргоо:
10.12.0.12 xyp.gov.mn

## OpenVPN file-д хийх нэмэлт тохиргоо /доорх VPN холбогдох command нь энэ TXT файлаас нэвтрэх мэдээллээ авах юм/
auth-user-pass /path/vpn_username_pass_file.txt

## VPN connect хийх /Ubuntu Server/
sudo openvpn filename.ovpn &
