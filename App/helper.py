# helper.py
import os
import random
import string
from multiprocessing import Pool, cpu_count

# ========== Config Defaults ==========
DEFAULT_BASE_DIR = "Files"
DEFAULT_EXTENSIONS = [".txt", ".log", ".json", ".html", ".csv", ".py", ".cfg", ".xml"]
DEFAULT_BINARY_EXT = [".bin", ".dat", ".img", ".raw"]
DEFAULT_NUM_SUBFOLDERS = 2
DEFAULT_FOLDER_DEPTH = 2
DEFAULT_FILES_PER_FOLDER = 5
DEFAULT_BINARY_RATIO = 0.3
DEFAULT_BINARY_MIN_SIZE = 100
DEFAULT_BINARY_MAX_SIZE = 500
# =====================================


def random_text():
    return "".join(
        random.choices(
            string.ascii_letters + string.digits + " \n", k=random.randint(50, 300)
        )
    )


def random_binary(min_size, max_size):
    return os.urandom(random.randint(min_size, max_size))


def random_filename(extensions):
    base = "".join(random.choices(string.ascii_lowercase, k=8))
    ext = random.choice(extensions)
    return base + ext


def create_file(args):
    folder, text_exts, bin_exts, ratio, min_bsize, max_bsize = args
    try:
        is_binary = random.random() < ratio
        ext_list = bin_exts if is_binary else text_exts
        filename = random_filename(ext_list)
        full_path = os.path.join(folder, filename)

        with open(
            full_path,
            "wb" if is_binary else "w",
            encoding=None if is_binary else "utf-8",
        ) as f:
            content = (
                random_binary(min_bsize, max_bsize) if is_binary else random_text()
            )
            f.write(content)

        return (
            f"[{os.getpid()}] {'Binary' if is_binary else 'Text '} Created: {full_path}"
        )
    except Exception as e:
        return f"[{os.getpid()}] ❌ Error in {folder}: {e}"


def generate_folders(base_dir, depth, count):
    folders = []

    def recurse(path, d):
        if d == 0:
            return
        for _ in range(count):
            name = "".join(random.choices(string.ascii_letters, k=6))
            new_path = os.path.join(path, name)
            folders.append(new_path)
            recurse(new_path, d - 1)

    try:
        recurse(base_dir, depth)
    except Exception as e:
        print(f"❌ Error generating folders: {e}")
    return folders


def parse_extensions(user_input, fallback):
    try:
        ext_list = [
            e.strip() if e.strip().startswith(".") else "." + e.strip()
            for e in user_input.split(",")
            if e.strip()
        ]
        return ext_list or fallback
    except:
        return fallback


def safe_int(prompt, default, min_val=0):
    try:
        val = input(prompt).strip()
        return max(int(val), min_val) if val else default
    except:
        return default


def safe_float(prompt, default):
    try:
        val = input(prompt).strip()
        return min(max(float(val), 0), 1) if val else default
    except:
        return default


def main():
    print("\n🛠️  Advanced File Generator with Binary Control\n")

    try:
        base_dir = (
            input(f"📂 Base directory (default = {DEFAULT_BASE_DIR}): ").strip()
            or DEFAULT_BASE_DIR
        )
        num_subfolders = safe_int(
            f"📁 Subfolders per level (default = {DEFAULT_NUM_SUBFOLDERS}): ",
            DEFAULT_NUM_SUBFOLDERS,
        )
        folder_depth = safe_int(
            f"🔁 Folder depth (default = {DEFAULT_FOLDER_DEPTH}): ",
            DEFAULT_FOLDER_DEPTH,
        )
        files_per_folder = safe_int(
            f"📄 Files per folder (default = {DEFAULT_FILES_PER_FOLDER}): ",
            DEFAULT_FILES_PER_FOLDER,
        )

        text_input = input(
            f"📝 Text extensions (default = {', '.join(DEFAULT_EXTENSIONS)}): "
        )
        bin_input = input(
            f"💾 Binary extensions (default = {', '.join(DEFAULT_BINARY_EXT)}): "
        )
        binary_ratio = safe_float(
            f"⚖️  Binary ratio (0-1) (default = {DEFAULT_BINARY_RATIO}): ",
            DEFAULT_BINARY_RATIO,
        )
        min_bsize = safe_int(
            f"🔽 Binary min size in bytes (default = {DEFAULT_BINARY_MIN_SIZE}): ",
            DEFAULT_BINARY_MIN_SIZE,
        )
        max_bsize = safe_int(
            f"🔼 Binary max size in bytes (default = {DEFAULT_BINARY_MAX_SIZE}): ",
            DEFAULT_BINARY_MAX_SIZE,
        )
        process_count = safe_int(
            f"⚙️  Number of parallel processes (default = {cpu_count() * 2}): ",
            cpu_count() * 2,
            1,
        )

        text_exts = parse_extensions(text_input, DEFAULT_EXTENSIONS)
        bin_exts = parse_extensions(bin_input, DEFAULT_BINARY_EXT)

        all_folders = generate_folders(base_dir, folder_depth, num_subfolders)
        for folder in all_folders:
            try:
                os.makedirs(folder, exist_ok=True)
            except Exception as e:
                print(f"❌ Couldn't create {folder}: {e}")

        print(
            f"\n⚙️  Generating {files_per_folder} files in each of {len(all_folders)} folders using {process_count} processes..."
        )

        jobs = [
            (folder, text_exts, bin_exts, binary_ratio, min_bsize, max_bsize)
            for folder in all_folders
            for _ in range(files_per_folder)
        ]

        with Pool(processes=process_count) as pool:
            results = pool.map(create_file, jobs)

        results = [r for r in results if r]  # Filter out None results

        print("\n✅ Summary:")
        print("\n".join(results))

    except KeyboardInterrupt:
        print("\n⛔ Interrupted.")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")


if __name__ == "__main__":
    main()
