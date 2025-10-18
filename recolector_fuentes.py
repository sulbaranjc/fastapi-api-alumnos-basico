#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import time
from pathlib import Path

# Directorios que NO queremos recorrer
DEFAULT_IGNORED_DIRS = {
    ".git", ".hg", ".svn", ".idea", ".vscode",
    "node_modules", "bower_components",
    ".venv", "venv", "env", ".pytest_cache", ".mypy_cache",
    "__pycache__", "dist", "build", "target", "out", ".next", ".nuxt", ".expo",
}

# Extensiones típicas de binarios/medios que NO debemos volcar al TXT
DEFAULT_BINARY_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".ico", ".webp",
    ".mp3", ".wav", ".flac", ".mp4", ".m4v", ".mov", ".avi", ".mkv",
    ".pdf", ".zip", ".rar", ".7z", ".gz", ".bz2", ".xz", ".tar", ".iso",
    ".ttf", ".otf", ".woff", ".woff2",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".class", ".jar",
    ".ds_store",
}

# 🔒 Exclusiones por privacidad/ruido (por defecto)
DEFAULT_EXCLUDED_NAMES = { ".env" }    # secretos
DEFAULT_EXCLUDED_EXTS  = { ".log" }    # logs verbosos

def looks_binary(sample: bytes) -> bool:
    if b"\x00" in sample:
        return True
    weird = sum(1 for b in sample if b < 9 or (13 < b < 32) or b == 127)
    return (len(sample) > 0 and weird / len(sample) > 0.30)

def read_text_safely(p: Path, max_bytes: int) -> str:
    size = p.stat().st_size
    if size > max_bytes >= 0:
        raise ValueError(f"Archivo demasiado grande ({size} bytes > {max_bytes}).")
    with p.open("rb") as fh:
        data = fh.read()
    if looks_binary(data[:4096]):
        raise ValueError("Archivo parece binario.")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return data.decode("latin-1")
        except UnicodeDecodeError:
            return data.decode("utf-8", errors="replace")

def normalize_patterns(csv: str):
    if not csv:
        return set()
    return {s.strip() for s in csv.split(",") if s.strip()}

def should_skip_path(path: Path, ignored_dirs, exclude_globs, excluded_names, excluded_exts):
    # Ignora directorios por nombre exacto (bloquea la bajada en os.walk)
    parts = set(part.lower() for part in path.parts)
    if parts & {d.lower() for d in ignored_dirs}:
        return True

    # Archivos a excluir por nombre exacto o extensión (política por defecto)
    name_lower = path.name.lower()
    ext_lower = path.suffix.lower()
    if name_lower in excluded_names or ext_lower in excluded_exts:
        return True

    # Aplica globs de exclusión manuales (--exclude)
    rel = str(path)
    for pat in exclude_globs:
        try:
            if path.match(pat) or rel.startswith(pat):
                return True
        except Exception:
            continue
    return False

def human_time(seconds: float) -> str:
    if seconds < 1:
        return f"{int(seconds*1000)} ms"
    if seconds < 60:
        return f"{seconds:.2f} s"
    m, s = divmod(int(seconds), 60)
    return f"{m} min {s} s"

def print_progress(current, total, prefix="", width=30, end=""):
    # Barra simple: [#####.....] 42% (123/291)
    if total <= 0:
        msg = f"{prefix} procesando..."
    else:
        ratio = min(max(current / total, 0), 1)
        filled = int(width * ratio)
        bar = "#" * filled + "." * (width - filled)
        pct = int(ratio * 100)
        msg = f"{prefix} [{bar}] {pct:3d}% ({current}/{total})"
    # Sobrescribe la línea en TTY, sino imprime normal
    if sys.stdout.isatty():
        print("\r" + msg, end=end, flush=True)
    else:
        print(msg, flush=True)

def main():
    parser = argparse.ArgumentParser(
        description="Genera un repositorio.txt con todas las fuentes del proyecto."
    )
    parser.add_argument("--root", "-r", default=".", help="Carpeta raíz del proyecto (por defecto: .)")
    parser.add_argument("--output", "-o", default="repositorio.txt", help="Archivo de salida (por defecto: repositorio.txt)")
    parser.add_argument("--include-ext", default="", help="Extensiones a FORZAR inclusión (csv, con punto). Ej: .py,.js,.ts")
    parser.add_argument("--exclude-ext", default="", help="Extensiones a excluir además de las binarias por defecto. Ej: .lock,.tmp")
    parser.add_argument("--exclude", default="", help="Patrones/paths a excluir (csv, glob). Ej: tests/screenshots,**/*.snap")
    parser.add_argument("--ignored-dirs", default="", help="Nombres de directorios a ignorar (csv). Añade a los por defecto.")
    parser.add_argument("--extra-excluded-names", default="", help="Nombres extra a excluir (csv). Ej: .env.local,.env.production")
    parser.add_argument("--extra-excluded-exts", default="", help="Extensiones extra a excluir (csv). Ej: .db,.sqlite")
    parser.add_argument("--no-default-excludes", action="store_true", help="Desactiva exclusiones .env y *.log por defecto.")
    parser.add_argument("--max-bytes", type=int, default=2_000_000, help="Tamaño máx por archivo (-1 ilimitado). Por defecto: 2MB")
    parser.add_argument("--follow-symlinks", action="store_true", help="Seguir enlaces simbólicos (por defecto NO).")
    parser.add_argument("--header-line", default="-" * 64, help="Separador bajo el nombre del archivo.")
    parser.add_argument("--list-binaries", action="store_true", help="Agrega inventario de omitidos al final.")
    parser.add_argument("--quiet", "-q", action="store_true", help="Modo silencioso: solo mensajes esenciales.")
    args = parser.parse_args()

    t0 = time.time()

    root = Path(args.root).resolve()
    output = Path(args.output).resolve()
    include_exts = {e.lower() for e in normalize_patterns(args.include_ext)}
    exclude_exts_cli = {e.lower() for e in normalize_patterns(args.exclude_ext)}
    exclude_globs = normalize_patterns(args.exclude)
    ignored_dirs = DEFAULT_IGNORED_DIRS | {d for d in normalize_patterns(args.ignored_dirs)}

    # Exclusiones por privacidad/ruido
    extra_names = {n for n in normalize_patterns(args.extra_excluded_names)}
    extra_exts = {e.lower() for e in normalize_patterns(args.extra_excluded_exts)}
    if args.no_default_excludes:
        excluded_names = extra_names
        excluded_exts = extra_exts
    else:
        excluded_names = DEFAULT_EXCLUDED_NAMES | extra_names
        excluded_exts = DEFAULT_EXCLUDED_EXTS | extra_exts

    auto_skip = {str(output)}  # Evitar incluir el propio archivo

    if not args.quiet:
        print(f"🚀 Iniciando recolección desde: {root}")
        print(f"📄 Archivo de salida: {output}")

    # --- PRE-SCAN: construir lista de candidatos para progreso visible
    candidate_files = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=args.follow_symlinks):
        # Evitar bajar a directorios ignorados
        dirnames[:] = sorted([
            d for d in dirnames
            if not should_skip_path(Path(dirpath, d), ignored_dirs, exclude_globs, excluded_names, excluded_exts)
        ])
        for name in filenames:
            p = Path(dirpath, name)
            if str(p.resolve()) in auto_skip:
                continue
            if should_skip_path(p, ignored_dirs, exclude_globs, excluded_names, excluded_exts):
                continue
            candidate_files.append(Path(dirpath, name))

    total_candidates = len(candidate_files)
    if not args.quiet:
        print(f"🔎 Archivos candidatos: {total_candidates}")
        if sys.stdout.isatty():
            print()  # línea en blanco antes de la barra

    # --- PROCESAMIENTO con progreso
    text_files = []
    skipped_binary = []
    skipped_large = []
    skipped_policy = []
    skipped_other = []

    processed = 0
    for p in sorted(candidate_files, key=lambda x: str(x).lower()):
        processed += 1
        if not args.quiet:
            print_progress(processed, total_candidates, prefix="⏳ Procesando")

        ext = p.suffix.lower()
        # Exclusión CLI extra por extensión
        if ext in exclude_exts_cli:
            skipped_other.append((p, "ext_excluded_cli"))
            continue
        # Binarios conocidos
        if ext in DEFAULT_BINARY_EXTS and ext not in include_exts:
            skipped_binary.append((p, "binary_ext"))
            continue

        try:
            content = read_text_safely(p, args.max_bytes)
            text_files.append((p, content))
        except ValueError as ve:
            msg = str(ve)
            if "demasiado grande" in msg:
                skipped_large.append((p, "too_large"))
            elif "binario" in msg:
                skipped_binary.append((p, "binary_heuristic"))
            else:
                skipped_other.append((p, f"ValueError:{msg}"))
        except Exception as ex:
            skipped_other.append((p, f"Error:{type(ex).__name__}:{ex}"))

    # --- ESCRITURA
    rel_base = root
    with output.open("w", encoding="utf-8", newline="\n") as out:
        out.write(f"# Repositorio de fuentes\n")
        out.write(f"# Raíz: {rel_base}\n")
        out.write(f"# Archivos incluidos: {len(text_files)}\n\n")

        for p, content in text_files:
            rel = str(p.relative_to(rel_base))
            out.write(rel + "\n")
            out.write(args.header_line + "\n")
            out.write(content)
            if not content.endswith("\n"):
                out.write("\n")
            out.write("\n")  # espacio entre archivos

        if args.list_binaries:
            out.write("\n# --- Archivos omitidos (referencia) ---\n")
            # Nota: los excluidos por política no entran al pre-scan, así que no están contados aquí.
            if skipped_policy:
                out.write("# Excluidos por política (.env, *.log, y extras):\n")
                for p, reason in skipped_policy:
                    out.write(f"- {p.relative_to(rel_base)} [{reason}]\n")
            if skipped_binary:
                out.write("# Binarios/medios:\n")
                for p, reason in skipped_binary:
                    out.write(f"- {p.relative_to(rel_base)} [{reason}]\n")
            if skipped_large:
                out.write("# Demasiado grandes:\n")
                for p, reason in skipped_large:
                    out.write(f"- {p.relative_to(rel_base)} [{reason}]\n")
            if skipped_other:
                out.write("# Otros omitidos/errores:\n")
                for p, reason in skipped_other:
                    out.write(f"- {p.relative_to(rel_base)} [{reason}]\n")

    # --- FIN / RESUMEN
    t1 = time.time()
    if not args.quiet:
        # Limpiar la línea de la barra en TTY
        if sys.stdout.isatty():
            print("\r" + " " * 80, end="\r")
        print("✅ Proceso finalizado.")
        print(f"📝 Incluidos en {output.name}: {len(text_files)} archivos")
        print(f"⏱️ Duración: {human_time(t1 - t0)}")
        print(f"📍 Ubicación: {output}")

    # Mensaje final para integraciones o logs
    print(f"Listo. Salida: {output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
