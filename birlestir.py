import pandas as pd
import os
import csv
import sys

# Satır uzunluğu sınırını artır (gerekli!)
csv.field_size_limit(2**26)  # 1 MB kadar satır uzunluğu (isteğe bağlı: 2**24'e kadar çıkarılabilir)

file_paths = [
    "Enron.csv", "Ling.csv", "Nazario.csv", "Nazario_5.csv",
    "Nigerian_5.csv", "Nigerian_Fraud.csv", "SpamAssasin.csv",
    "TREC_05.csv", "TREC_06.csv", "TREC_07.csv", "CEAS_08.csv"
]

combined_data = []

for path in file_paths:
    source = os.path.splitext(os.path.basename(path))[0].lower()
    try:
        df = pd.read_csv(path, encoding="utf-8", engine="python")
        if all(col in df.columns for col in ["subject", "body", "label"]):
            df["text"] = df["subject"].astype(str) + " " + df["body"].astype(str)
        elif "body" in df.columns and "label" in df.columns:
            df["text"] = df["body"].astype(str)
        else:
            print(f"{path} uygun formatta değil, atlandı.")
            continue
        df["type"] = "real"
        df["source"] = source
        combined_data.append(df[["text", "label", "type", "source"]])
        print(f"{path} dosyası işlendi ({len(df)} satır).")
    except Exception as e:
        print(f"{path} okunamadı: {e}")

# Tüm verileri birleştir
if combined_data:
    final_df = pd.concat(combined_data, ignore_index=True)
    final_df.to_csv("real_phishing_dataset.csv", index=False, encoding="utf-8")
    print(f"\n✅ Tüm dosyalar başarıyla birleştirildi: real_phishing_dataset.csv ({len(final_df)} satır)")
else:
    print("⚠️ Hiçbir veri dosyası birleştirilemedi.")
