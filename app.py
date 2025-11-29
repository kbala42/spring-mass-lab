import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# -----------------------------
# Streamlit temel ayar
# -----------------------------
st.set_page_config(page_title="Yay–Kütle Dinamiği", page_icon="🔩")

st.title("🔩 Yay–Kütle Dinamiği – Basit Harmonik Hareket Lab’ı")
st.write(
    """
Bu laboratuvarda duvara bağlı bir yay ve ucundaki kütlenin
zaman içindeki hareketini simüle edeceksin.

Kullandığımız diferansiyel denklem:

\\[
m x''(t) + c x'(t) + k x(t) = 0
\\]

- **m**: kütle  
- **k**: yay sabiti (sertlik)  
- **c**: sönüm katsayısı (sürtünme etkisi)
"""
)

st.markdown("---")


# -----------------------------
# Parametreler
# -----------------------------
st.subheader("1️⃣ Sistem Parametrelerini Seç")

col1, col2, col3 = st.columns(3)

with col1:
    m = st.slider(
        "Kütle m",
        min_value=0.5,
        max_value=5.0,
        value=1.0,
        step=0.5,
    )

with col2:
    k = st.slider(
        "Yay sabiti k",
        min_value=0.5,
        max_value=10.0,
        value=4.0,
        step=0.5,
        help="Yay sabiti arttıkça yay daha sert davranır, salınım frekansı artar.",
    )

with col3:
    c = st.slider(
        "Sönüm katsayısı c",
        min_value=0.0,
        max_value=5.0,
        value=0.5,
        step=0.1,
        help="c = 0 için sönümsüz, c > 0 için zamanla azalan salınım.",
    )

st.write(
    f"Seçilen parametreler: **m = {m:.1f}**, **k = {k:.1f}**, **c = {c:.1f}**"
)


st.subheader("2️⃣ Başlangıç Koşulları ve Zaman Ayarları")

col_ic1, col_ic2 = st.columns(2)
with col_ic1:
    x0 = st.slider(
        "Başlangıç konumu x₀",
        min_value=-5.0,
        max_value=5.0,
        value=1.0,
        step=0.1,
    )
with col_ic2:
    v0 = st.slider(
        "Başlangıç hızı v₀",
        min_value=-5.0,
        max_value=5.0,
        value=0.0,
        step=0.1,
    )

col_time1, col_time2 = st.columns(2)
with col_time1:
    t_max = st.slider(
        "Toplam simülasyon süresi (s)",
        min_value=2.0,
        max_value=20.0,
        value=10.0,
        step=1.0,
    )
with col_time2:
    dt = st.slider(
        "Zaman adımı Δt",
        min_value=0.001,
        max_value=0.1,
        value=0.02,
        step=0.001,
        help="Daha küçük Δt daha doğru ama daha çok adım demektir.",
    )

n_steps = int(t_max / dt) + 1
st.write(
    f"Simülasyon **{t_max:.1f} s** sürecek, zaman adımı **Δt = {dt:.3f} s**, "
    f"toplam adım sayısı: **{n_steps}**"
)


# -----------------------------
# Sayısal simülasyon fonksiyonu
# -----------------------------
def simulate_mass_spring(m, k, c, x0, v0, dt, n_steps):
    """
    Basit yay–kütle sistemini sayısal olarak simüle eder.
    Yarı açık (semi-implicit) Euler yöntemi:
        a_n = -(k/m)*x_n - (c/m)*v_n
        v_{n+1} = v_n + a_n * dt
        x_{n+1} = x_n + v_{n+1} * dt
    """
    t = np.zeros(n_steps)
    x = np.zeros(n_steps)
    v = np.zeros(n_steps)

    x[0] = x0
    v[0] = v0

    for n in range(n_steps - 1):
        a = -(k / m) * x[n] - (c / m) * v[n]
        v[n + 1] = v[n] + a * dt
        x[n + 1] = x[n] + v[n + 1] * dt
        t[n + 1] = t[n] + dt

    return t, x, v


# Simülasyonu çalıştır
t, x, v = simulate_mass_spring(m, k, c, x0, v0, dt, n_steps)


# Enerji hesapları (isteğe bağlı görselleştirme için)
E_p = 0.5 * k * x**2          # potansiyel enerji
E_k = 0.5 * m * v**2          # kinetik enerji
E_total = E_p + E_k


# -----------------------------
# Konum–Zaman grafiği
# -----------------------------
st.markdown("---")
st.subheader("3️⃣ Konum – Zaman Grafiği")

fig1, ax1 = plt.subplots(figsize=(7, 4))
ax1.plot(t, x)
ax1.set_xlabel("t (s)")
ax1.set_ylabel("x(t)")
ax1.set_title("Yay–Kütle Sisteminde Konumun Zamanla Değişimi")
ax1.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)

st.pyplot(fig1)


# -----------------------------
# Faz uzayı (x–v) grafiği
# -----------------------------
st.subheader("4️⃣ Faz Uzayı: Konum–Hız Grafiği (x–v)")

fig2, ax2 = plt.subplots(figsize=(5, 5))
ax2.plot(x, v)
ax2.set_xlabel("x")
ax2.set_ylabel("v")
ax2.set_title("Faz Uzayı Yörüngesi (x–v)")
ax2.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
ax2.set_aspect("equal", "box")

st.pyplot(fig2)


# -----------------------------
# Enerji grafiği (isteğe bağlı)
# -----------------------------
show_energy = st.checkbox(
    "Toplam enerji ve enerji bileşenlerini de göster (E_p, E_k, E_toplam)",
    value=False,
)

if show_energy:
    st.subheader("5️⃣ Enerji – Zaman Grafiği")

    fig3, ax3 = plt.subplots(figsize=(7, 4))
    ax3.plot(t, E_p, label="Potansiyel enerji")
    ax3.plot(t, E_k, label="Kinetik enerji")
    ax3.plot(t, E_total, label="Toplam enerji")
    ax3.set_xlabel("t (s)")
    ax3.set_ylabel("Enerji (J, birimsel)")
    ax3.set_title("Enerjinin Zamanla Değişimi")
    ax3.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
    ax3.legend()

    st.pyplot(fig3)


# -----------------------------
# İlk birkaç adım için tablo
# -----------------------------
st.subheader("6️⃣ İlk Adımların Sayısal Tablosu")

max_rows = min(15, n_steps)
df = pd.DataFrame(
    {
        "t (s)": t[:max_rows],
        "x(t)": x[:max_rows],
        "v(t)": v[:max_rows],
        "E_p": E_p[:max_rows],
        "E_k": E_k[:max_rows],
        "E_toplam": E_total[:max_rows],
    }
)

st.dataframe(
    df.style.format(
        {
            "t (s)": "{:.3f}",
            "x(t)": "{:.3f}",
            "v(t)": "{:.3f}",
            "E_p": "{:.3f}",
            "E_k": "{:.3f}",
            "E_toplam": "{:.3f}",
        }
    )
)


# -----------------------------
# Açıklama / Öğretmen kutusu
# -----------------------------
st.markdown("---")
st.info(
    "Bu simülasyon, yay–kütle sisteminin hareketini sayısal olarak yaklaşık çözer. "
    "c = 0 için sönümsüz, c > 0 için sönümlü salınım gözlemleyebilirsin. "
    "x–v grafiği (faz uzayı), hareketin 'izini' gösterir."
)

with st.expander("👩‍🏫 Öğretmen Kutusu – Sayısal Çözümün Mantığı"):
    st.write(
        r"""
Kullandığımız diferansiyel denklem:

\\[
m x''(t) + c x'(t) + k x(t) = 0
\\]

Buradan ivmeyi (a = x'') şöyle yazabiliriz:

\\[
a(t) = x''(t) = -\frac{k}{m} x(t) - \frac{c}{m} x'(t)
\\]

Bunu küçük zaman adımlarıyla güncelliyoruz:

1. Mevcut adımda ivmeyi hesapla:  
   \\(a_n = -\frac{k}{m} x_n - \frac{c}{m} v_n\\)
2. Hızı güncelle:  
   \\(v_{n+1} = v_n + a_n \Delta t\\)
3. Konumu güncelle:  
   \\(x_{n+1} = x_n + v_{n+1} \Delta t\\)

Bu yöntem **yarı açık (semi-implicit) Euler** olarak bilinir ve basit harmonik hareket için
klasik Euler'e göre daha kararlıdır.

Öğrenciler farklı m, k, c, x₀, v₀ değerleri için:

- Sönümsüz (c = 0) durumda enerjinin yaklaşık sabit kaldığını,  
- Sönümlü (c > 0) durumda toplam enerjinin zamanla azaldığını,  
- Faz düzleminde sönümsüz durumda kapalı eğriler, sönümlü durumda içeriye sarmalanan
  spiral yörüngeler oluştuğunu gözlemleyebilirler.
"""
    )

st.caption(
    "Bu modül, lise fiziğinde basit harmonik hareket ve sayısal yöntemler için "
    "görsel ve etkileşimli bir laboratuvar ortamı sunar."
)
