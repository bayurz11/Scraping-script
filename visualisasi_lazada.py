import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca data dari file Excel
df = pd.read_excel("lazada_data.xlsx")

# Mengubah kolom 'Harga' menjadi numerik (menghapus tanda Rp dan titik)
df["Harga"] = df["Harga"].str.replace("Rp", "").str.replace(".", "").astype(float)

# Menampilkan beberapa baris pertama data
print(df.head())

# Membuat plot harga produk
plt.figure(figsize=(10, 6))
sns.histplot(df["Harga"], kde=True)
plt.title("Distribusi Harga Produk")
plt.xlabel("Harga")
plt.ylabel("Frekuensi")
plt.show()

# Membuat plot rating produk
plt.figure(figsize=(10, 6))
sns.countplot(x="Rating", data=df)
plt.title("Distribusi Rating Produk")
plt.xlabel("Rating")
plt.ylabel("Jumlah Produk")
plt.show()

# Membuat plot lokasi produk
plt.figure(figsize=(10, 6))
lokasi_counts = df["Lokasi"].value_counts().nlargest(10)
sns.barplot(x=lokasi_counts.values, y=lokasi_counts.index)
plt.title("10 Lokasi Teratas Produk")
plt.xlabel("Jumlah Produk")
plt.ylabel("Lokasi")
plt.show()
