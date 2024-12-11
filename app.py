from flask import Flask, render_template, request

app = Flask(__name__)

def evaluasi_produksi_fuzzy(permintaan, persediaan):  
    # Fuzzifikasi untuk permintaan
    permintaan_turun = max(0, min((7000 - permintaan) / 6500, 1))  
    permintaan_naik = max(0, min((permintaan - 500) / 6500, 1))    

    # Fuzzifikasi untuk persediaan
    persediaan_sedikit = max(0, min((570 - persediaan) / 270, 1))  
    persediaan_banyak = max(0, min((persediaan - 300) / 270, 1))   

    # Inferensi Fuzzy
    # Aturan 1: JIKA permintaan turun DAN persediaan banyak MAKA produksi berkurang
    a1 = min(permintaan_turun, persediaan_banyak)
    z1 = 3000 + (1 - a1) * (9000 - 3000)  # Dihitung secara lebih spesifik

    # Aturan 2: JIKA permintaan turun DAN persediaan sedikit MAKA produksi berkurang
    a2 = min(permintaan_turun, persediaan_sedikit)
    z2 = 3000 + (1 - a2) * (9000 - 3000)

    # Aturan 3: JIKA permintaan naik DAN persediaan banyak MAKA produksi bertambah
    a3 = min(permintaan_naik, persediaan_banyak)
    z3 = 3000 + a3 * (9000 - 3000)

    # Aturan 4: JIKA permintaan naik DAN persediaan sedikit MAKA produksi bertambah
    a4 = min(permintaan_naik, persediaan_sedikit)
    z4 = 3000 + a4 * (9000 - 3000)

    # Defuzzifikasi
    pembilang = (a1 * z1) + (a2 * z2) + (a3 * z3) + (a4 * z4)
    penyebut = a1 + a2 + a3 + a4
    z = pembilang / penyebut if penyebut != 0 else 0

    # Pembulatan hasil
    z = round(z, 2)
    status = "Produksi Bertambah" if z >= 5000 else "Produksi Berkurang"

    return z, status

@app.route("/", methods=["GET", "POST"])
def index():
    hasil = None
    status = None
    permintaan = None
    persediaan = None

    if request.method == "POST":
        # Ambil input dari form pengguna
        permintaan = int(request.form.get("permintaan"))
        persediaan = int(request.form.get("persediaan"))

        # Hitung hasil menggunakan fungsi fuzzy
        hasil, status = evaluasi_produksi_fuzzy(permintaan, persediaan)

    return render_template("index.html", hasil=hasil, status=status, permintaan=permintaan, persediaan=persediaan)

if __name__ == "__main__":
    app.run(debug=True)
