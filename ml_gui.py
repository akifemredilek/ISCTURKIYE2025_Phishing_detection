import tkinter as tk
from tkinter import scrolledtext
import pickle

# Eğitimli model ve vektörleştiriciyi yükle
model = pickle.load(open("ml_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Sınıflandırma fonksiyonu
def classify_with_ml(email_text):
    vec_text = vectorizer.transform([email_text])
    prediction = model.predict(vec_text)[0]
    return "Phishing" if prediction == 1 else "Legitimate"

# Analiz buton fonksiyonu
def analyze():
    email_text = input_box.get("1.0", tk.END).strip()
    if email_text:
        result = classify_with_ml(email_text)
        result_label.config(text=f"Prediction: {result}")

# Arayüz tasarımı
root = tk.Tk()
root.title("Phishing Email Detection Tool (ML Model)")

tk.Label(root, text="Enter the Email Content:", font=("Arial", 10)).pack(pady=5)
input_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
input_box.pack(padx=10, pady=5)

tk.Button(root, text="Detect Phishing", command=analyze).pack(pady=10)

result_label = tk.Label(root, text="Prediction: Not yet made", font=("Arial", 12, "bold"))
result_label.pack(pady=10)

root.mainloop()