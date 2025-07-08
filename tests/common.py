import ai_dev_team_server as server
import database


def prepare_temp_env(tmp_path):
    """Initialize temporary work and database paths for tests"""
    server.WORK_DIR = str(tmp_path)
    server.projects.clear()
    database.DB_PATH = str(tmp_path / "projects.db")
    database.init_db()
