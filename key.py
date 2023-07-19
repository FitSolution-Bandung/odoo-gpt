import base64

# Misalkan 'my_key' adalah kunci Anda
my_key = 'my_key'

# Mengubahnya menjadi base64
my_key_base64 = base64.urlsafe_b64encode(my_key.encode())

print(my_key_base64)



# Misalkan 'my_key_base64' adalah kunci base64 Anda
my_key_base64 = my_key_base64[:32]  # Memotong kunci jika terlalu panjang

# Menambahkan padding jika terlalu pendek
while len(my_key_base64) < 32:
    my_key_base64 += b'='


print(my_key_base64)