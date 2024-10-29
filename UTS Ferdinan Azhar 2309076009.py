import numpy as np
import matplotlib.pyplot as plt

# Definisi konstanta
L = 0.5  # Induktansi dalam Henry
C = 10e-6  # Kapasitansi dalam Farad
target_f = 1000  # Frekuensi target dalam Hertz
tolerance = 0.1  # Toleransi error dalam Ohm

# Fungsi untuk menghitung frekuensi resonansi f(R)
def f_R(R):
    term_inside_sqrt = 1 / (L * C) - (R**2) / (4 * L**2)
    if term_inside_sqrt <= 0:
        return None  # Tidak valid untuk akar negatif
    return (1 / (2 * np.pi)) * np.sqrt(term_inside_sqrt)

# Turunan f(R) untuk metode Newton-Raphson
def f_prime_R(R):
    term_inside_sqrt = 1 / (L * C) - (R**2) / (4 * L**2)
    if term_inside_sqrt <= 0:
        return None  # Turunan tidak terdefinisi
    sqrt_term = np.sqrt(term_inside_sqrt)
    return -R / (4 * np.pi * L**2 * sqrt_term)

# Implementasi metode Newton-Raphson
def newton_raphson_method(initial_guess, tolerance):
    R = initial_guess
    while True:
        f_val = f_R(R)
        if f_val is None:
            return None  # Kasus tidak valid
        f_value = f_val - target_f
        f_prime_value = f_prime_R(R)
        if f_prime_value is None:
            return None  # Kasus tidak valid
        new_R = R - f_value / f_prime_value
        if abs(new_R - R) < tolerance:
            return new_R
        R = new_R

# Implementasi metode Bisection
def bisection_method(a, b, tolerance):
    while (b - a) / 2 > tolerance:
        mid = (a + b) / 2
        f_mid = f_R(mid) - target_f
        if f_mid is None:
            return None  # Kasus tidak valid
        if abs(f_mid) < tolerance:
            return mid
        if (f_R(a) - target_f) * f_mid < 0:
            b = mid
        else:
            a = mid
    return (a + b) / 2

# Menjalankan kedua metode
initial_guess = 50  # Nilai awal untuk Newton-Raphson
interval_a, interval_b = 0, 100  # Interval Bisection

# Hasil metode Newton-Raphson
R_newton = newton_raphson_method(initial_guess, tolerance)
f_newton = f_R(R_newton) if R_newton is not None else "Tidak ditemukan"

# Hasil metode Bisection
R_bisection = bisection_method(interval_a, interval_b, tolerance)
f_bisection = f_R(R_bisection) if R_bisection is not None else "Tidak ditemukan"

# Menampilkan hasil
print("Metode Newton-Raphson:")
print(f"R: {R_newton} ohm, Frekuensi Resonansi: {f_newton} Hz")

print("\nMetode Bisection:")
print(f"R: {R_bisection} ohm, Frekuensi Resonansi: {f_bisection} Hz")

# Plot hasil
plt.figure(figsize=(10, 5))
plt.axhline(target_f, color="red", linestyle="--", label="Frekuensi Target 1000 Hz")

# Plot hasil Newton-Raphson
if R_newton is not None:
    plt.scatter(R_newton, f_newton, color="blue", label="Newton-Raphson", zorder=5)
    plt.text(R_newton, f_newton + 30, f"NR: R={R_newton:.2f}, f={f_newton:.2f} Hz", color="blue")

# Plot hasil Bisection
if R_bisection is not None:
    plt.scatter(R_bisection, f_bisection, color="green", label="Bisection", zorder=5)
    plt.text(R_bisection, f_bisection + 30, f"Bisection: R={R_bisection:.2f}, f={f_bisection:.2f} Hz", color="green")

# Konfigurasi plot
plt.xlabel("Resistansi (Ohm)")
plt.ylabel("Frekuensi Resonansi f(R) (Hz)")
plt.title("Perbandingan Metode Newton-Raphson dan Bisection")
plt.legend()
plt.grid(True)
plt.show()
