"""
Тиждень 2. Практична 01/02 — послідовна (базова) реалізація множини Мандельброта.

Без бібліотек: жодних numpy/PIL/multiprocessing — лише стандартні цикли Python
і стандартна бібліотека (для запису файлу).

Запуск:
    python mandelbrot_sequential.py

Результат:
    - mandelbrot.pgm  — зображення (PGM P5, grayscale, без бібліотек; перезаписується кожним прогоном)
    - друк у консоль часу кожного прогону (обчислення / запис / всього)

Якщо один прогін триває суттєво менше 5 або більше 15 секунд на вашій
машині — змініть WIDTH/HEIGHT/MAX_ITER нижче і повторіть.
"""

import time

# ---- Параметри задачі (підберіть під свою машину: 5-15 c на прогін) ----
WIDTH = 900
HEIGHT = 600
MAX_ITER = 500

# Область комплексної площини, яку рендеримо
RE_MIN, RE_MAX = -2.0, 1.0
IM_MIN, IM_MAX = -1.5, 1.5


def mandelbrot_escape(cx, cy, max_iter):
    """Скільки ітерацій z = z^2 + c витримує точка c = cx + cy*i, перш ніж |z| > 2."""
    x, y = 0.0, 0.0
    x2, y2 = 0.0, 0.0
    iteration = 0
    while x2 + y2 <= 4.0 and iteration < max_iter:
        y = 2 * x * y + cy
        x = x2 - y2 + cx
        x2 = x * x
        y2 = y * y
        iteration += 1
    return iteration


def compute_image(width, height, max_iter):
    """Рахує escape-час для кожного пікселя. Повертає плоский список 0..255."""
    pixels = [0] * (width * height)
    re_span = RE_MAX - RE_MIN
    im_span = IM_MAX - IM_MIN
    idx = 0
    for py in range(height):
        cy = IM_MIN + (py / (height - 1)) * im_span
        for px in range(width):
            cx = RE_MIN + (px / (width - 1)) * re_span
            it = mandelbrot_escape(cx, cy, max_iter)
            # нормуємо в 0..255 (0 = у множині / не втекло, 255 = втекло одразу)
            pixels[idx] = 255 if it >= max_iter else int(255 * it / max_iter)
            idx += 1
    return pixels


def save_pgm(filename, width, height, pixels):
    """Записує зображення як PGM (P5, grayscale) — найпростіший формат без будь-яких бібліотек."""
    with open(filename, "wb") as f:
        f.write(f"P5\n{width} {height}\n255\n".encode("ascii"))
        f.write(bytearray(pixels))


def main():
    print(f"Розмір: {WIDTH}x{HEIGHT}, MAX_ITER={MAX_ITER}")
    print(f"{'Прогін':<8}{'Обчислення, с':<16}{'Запис, с':<12}{'Всього, с':<12}{'Частка запису, %':<18}")

    results = []
    for run in range(3):
        t0 = time.perf_counter()
        pixels = compute_image(WIDTH, HEIGHT, MAX_ITER)
        t_compute = time.perf_counter() - t0

        t1 = time.perf_counter()
        save_pgm("mandelbrot.pgm", WIDTH, HEIGHT, pixels)
        t_save = time.perf_counter() - t1

        t_total = t_compute + t_save
        seq_share = 100 * t_save / t_total
        results.append((t_compute, t_save, t_total, seq_share))
        print(f"{run:<8}{t_compute:<16.3f}{t_save:<12.3f}{t_total:<12.3f}{seq_share:<18.2f}")

    avg_share = sum(r[3] for r in results) / len(results)
    print(f"\nСередня частка запису (послідовна частина): {avg_share:.2f}%")


if __name__ == "__main__":
    main()
