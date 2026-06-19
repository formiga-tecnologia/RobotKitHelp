from pathlib import Path


class ProjectManager:

    @staticmethod
    def create_project(directory: str, name: str):

        root = Path(directory) / name

        root.mkdir(parents=True, exist_ok=True)

        (root / "Package").mkdir(exist_ok=True)
        (root / "Interface").mkdir(exist_ok=True)
        (root / "Place").mkdir(exist_ok=True)
        (root / "Assets").mkdir(exist_ok=True)
        (root / "Scripts").mkdir(exist_ok=True)

        project_file = root / f"{name}.rhk"

        project_file.write_text(
f"""[PROJECT]
Name={name}
Version=0.1

Package=Package
Interface=Interface
Place=Place
Assets=Assets
Scripts=Scripts

END
""",
encoding="utf-8")

        return str(project_file)

    @staticmethod
    def load_project(file_path: str):

        return Path(file_path)