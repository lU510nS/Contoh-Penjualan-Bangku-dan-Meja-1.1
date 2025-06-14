import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.title("Optimasi Produksi Meja dan Kursi")

st.markdown("""
PT. Satyamitra Kemas Lestari ingin menentukan jumlah **meja** dan **kursi** yang harus diproduksi untuk **memaksimalkan keuntungan**, 
dengan keterbatasan waktu produksi selama 48 jam per minggu (2880 menit).

""")

# Koefisien fungsi objektif (negatif karena linprog meminimalkan)
c = [-20, -10]  # keuntungan meja 20rb, kursi 10rb

# Kendala: 45x + 30y <= 2880
A = [[45, 30]]
b = [2880]

# Batasan variabel
x_bounds = (0, None)
y_bounds = (0, None)

# Solve LP
res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

if res.success:
    x = res.x[0]
    y = res.x[1]
    z = -res.fun * 1000  # konversi ribuan ke rupiah

    st.success(f"Jumlah Meja yang diproduksi: **{x:.0f} unit**")
    st.success(f"Jumlah Kursi yang diproduksi: **{y:.0f} unit**")
    st.info(f"Total Keuntungan Maksimal: **Rp {z:,.0f}**")

    # Visualisasi
    fig, ax = plt.subplots()
    x_vals = np.linspace(0, 70, 200)
    y_vals = (2880 - 45 * x_vals) / 30
    ax.plot(x_vals, y_vals, label="Kendala: 45x + 30y = 2880", color='blue')
    ax.fill_between(x_vals, 0, y_vals, alpha=0.3)

    ax.plot(x, y, 'ro', label="Solusi Optimal")
    ax.set_xlim(0, 70)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Jumlah Meja (x)")
    ax.set_ylabel("Jumlah Kursi (y)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
else:
    st.error("Gagal menyelesaikan masalah optimasi.")
