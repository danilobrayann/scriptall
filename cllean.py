import os
import shutil
import subprocess
import ctypes
import tempfile
from pathlib import Path


# ============================================================
# LIMPA PC - WINDOWS
# ============================================================

def is_admin():
    """Verifica se o script está sendo executado como administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """Reabre o próprio script como administrador."""
    script = os.path.abspath(__file__)

    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        "python.exe",
        f'"{script}"',
        None,
        1
    )


def format_size(size):
    """Converte bytes para uma unidade legível."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} PB"


def delete_file(path):
    """Apaga um arquivo individual."""
    try:
        if os.path.isfile(path) or os.path.islink(path):
            size = os.path.getsize(path)

            try:
                os.remove(path)
                return size
            except PermissionError:
                pass

    except:
        pass

    return 0


def delete_folder_contents(folder):
    """Limpa o conteúdo de uma pasta sem apagar a própria pasta."""
    total = 0

    if not os.path.exists(folder):
        return total

    try:
        for item in os.listdir(folder):

            path = os.path.join(folder, item)

            try:

                if os.path.isfile(path) or os.path.islink(path):
                    total += delete_file(path)

                elif os.path.isdir(path):

                    try:
                        total += get_folder_size(path)
                        shutil.rmtree(path, ignore_errors=True)
                    except:
                        pass

            except:
                pass

    except:
        pass

    return total


def get_folder_size(folder):
    """Calcula aproximadamente o tamanho de uma pasta."""
    total = 0

    try:
        for root, dirs, files in os.walk(folder):

            for file in files:
                try:
                    total += os.path.getsize(
                        os.path.join(root, file)
                    )
                except:
                    pass

    except:
        pass

    return total


def clean_user_temp():
    print("\n[1/8] Limpando TEMP do usuário...")

    temp = tempfile.gettempdir()

    size = delete_folder_contents(temp)

    print(f"      Liberado: {format_size(size)}")


def clean_windows_temp():
    print("\n[2/8] Limpando TEMP do Windows...")

    folder = r"C:\Windows\Temp"

    size = delete_folder_contents(folder)

    print(f"      Liberado: {format_size(size)}")


def clean_prefetch():
    print("\n[3/8] Limpando Prefetch...")

    folder = r"C:\Windows\Prefetch"

    size = delete_folder_contents(folder)

    print(f"      Liberado: {format_size(size)}")


def clean_windows_update_cache():
    print("\n[4/8] Limpando cache do Windows Update...")

    subprocess.run(
        ["net", "stop", "wuauserv"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    subprocess.run(
        ["net", "stop", "bits"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    folder = r"C:\Windows\SoftwareDistribution\Download"

    size = delete_folder_contents(folder)

    subprocess.run(
        ["net", "start", "wuauserv"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    subprocess.run(
        ["net", "start", "bits"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    print(f"      Liberado: {format_size(size)}")


def clean_windows_logs():
    print("\n[5/8] Limpando logs temporários do Windows...")

    folders = [
        r"C:\Windows\Logs\CBS",
        r"C:\Windows\Logs\DISM",
    ]

    total = 0

    for folder in folders:
        total += delete_folder_contents(folder)

    print(f"      Liberado: {format_size(total)}")


def clean_browser_cache():
    print("\n[6/8] Limpando caches dos navegadores...")

    local = os.environ.get("LOCALAPPDATA", "")

    folders = [

        # Google Chrome
        os.path.join(
            local,
            r"Google\Chrome\User Data\Default\Cache"
        ),

        # Microsoft Edge
        os.path.join(
            local,
            r"Microsoft\Edge\User Data\Default\Cache"
        ),

        # Brave
        os.path.join(
            local,
            r"BraveSoftware\Brave-Browser\User Data\Default\Cache"
        ),
    ]

    total = 0

    for folder in folders:

        if os.path.exists(folder):
            total += delete_folder_contents(folder)

    print(f"      Liberado: {format_size(total)}")


def empty_recycle_bin():
    print("\n[7/8] Esvaziando a Lixeira...")

    try:

        ctypes.windll.shell32.SHEmptyRecycleBinW(
            None,
            None,
            0x00000001 | 0x00000002 | 0x00000004
        )

        print("      Lixeira esvaziada.")

    except Exception as e:

        print("      Não foi possível esvaziar a Lixeira.")


def run_windows_disk_cleanup():
    print("\n[8/8] Executando Limpeza de Disco do Windows...")

    try:

        subprocess.run(
            [
                "cleanmgr.exe",
                "/verylowdisk"
            ],
            check=False
        )

        print("      Limpeza de Disco executada.")

    except:

        print("      Não foi possível executar o CleanMgr.")


def clean_dns_cache():
    print("\nLimpando cache DNS...")

    subprocess.run(
        ["ipconfig", "/flushdns"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    print("      Cache DNS limpo.")


def clean_windows_memory_dump():
    print("\nLimpando arquivos de dump...")

    folders = [
        r"C:\Windows\Minidump",
        r"C:\Windows\MEMORY.DMP"
    ]

    total = 0

    for path in folders:

        if os.path.isfile(path):
            total += delete_file(path)

        elif os.path.isdir(path):
            total += delete_folder_contents(path)

    print(f"      Liberado: {format_size(total)}")


def main():

    print("=" * 60)
    print("        WINDOWS CLEANER - LIMPEZA COMPLETA")
    print("=" * 60)

    print("""
Este programa irá limpar:

- Arquivos TEMP do usuário
- TEMP do Windows
- Prefetch
- Cache do Windows Update
- Logs temporários
- Cache dos navegadores
- Lixeira
- Arquivos de dump
- Cache DNS
- Limpeza de Disco do Windows

Seus documentos pessoais NÃO serão apagados.
""")

    resposta = input(
        "Digite LIMPAR para iniciar: "
    ).strip().upper()

    if resposta != "LIMPAR":

        print("\nOperação cancelada.")

        input("\nPressione ENTER para sair...")
        return

    print("\nIniciando limpeza...\n")

    clean_user_temp()
    clean_windows_temp()
    clean_prefetch()
    clean_windows_update_cache()
    clean_windows_logs()
    clean_browser_cache()
    empty_recycle_bin()
    clean_windows_memory_dump()
    clean_dns_cache()

    run_windows_disk_cleanup()

    print("\n" + "=" * 60)
    print("              LIMPEZA FINALIZADA")
    print("=" * 60)

    print("""
Recomendo reiniciar o computador agora para concluir
algumas operações do Windows.
""")

    input("Pressione ENTER para sair...")


if __name__ == "__main__":

    if not is_admin():

        print("Solicitando privilégios de Administrador...")

        run_as_admin()

    else:

        main()