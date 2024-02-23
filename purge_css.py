from pathlib import Path
import os


def find_base_directory() -> str:
    """Return the base directory (assuming this is run in the root of the project)."""
    return Path(__file__).resolve().parent.as_posix()


def find_css_files(base_dir: str) -> list:
    """Return a list of absolute paths to css files."""
    return [
        f"{base_dir}/apps/main/static/styles.css",
        f"{base_dir}/apps/main/static/pico.css",
    ]


def exclude_venv_directory(base_dir: str) -> str:
    """Return the path to the venv directory."""
    return f"{base_dir}/venv"


def find_html_files(base_dir: str) -> list:
    """Return a list of absolute paths to html files."""
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d != "venv"]  # Exclude venv directory
        for file in files:
            if file.endswith(".html"):
                absolute_path = f"{root}/{file}"
                html_files.append(absolute_path)
    return html_files


def define_output_file(base_dir: str) -> str:
    """Return the path to the output file."""
    return f"{base_dir}/static/build/"


def main() -> None:
    """
    This function is the main entry point.
    It finds the base directory, CSS files, excluded directory, HTML files, and defines the output file.
    It then prints a command for purging CSS using the found files.
    Copy the command, paste it into the terminal, and run it.
    """
    base_dir = find_base_directory()
    css_files = find_css_files(base_dir)
    excluded_directory = exclude_venv_directory(base_dir)
    html_files = find_html_files(base_dir)
    output_file = define_output_file(base_dir)

    print(
        f"npx purgecss --css {' '.join(css_files)} --content {' '.join(html_files)} --output {output_file}"
    )


if __name__ == "__main__":
    main()
