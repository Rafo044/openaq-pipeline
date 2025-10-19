import os
import subprocess
import shlex

from fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Any

openaq = FastMCP("openaq")

load_dotenv()

# =============================================================================================================
#                                 PERMISSIONS CHECK
# =============================================================================================================


@openaq.tool
def permission_check(permission: str) -> dict[str, Any]:
    """
    Its main purpose is to check whether the
    PERMISSION section in the .env file is True or False:
        PERMISSION_DOCKER_CONTROL
        PERMISSION_POSTGRES_QUERY
        PERMISSION_POSTGRES_BACKUP
        PERMISSION_REQUESTS

    Returns:
        A dictionary containing the permission status.
    """

    if os.getenv(permission, "false").lower() == "true":
        return {"status": "success", "message": "Permission granted"}
    else:
        return {"status": "error", "message": f"Permission denied for {permission}"}


@openaq.tool
def docker_check_permissions():
    """
    Checks the permissions for Docker-related operations.

    Returns:
        A dictionary containing the permission status.
    """
    return permission_check.fn("PERMISSION_DOCKER_CONTROL")


@openaq.tool
def requests_check_permissions():
    """
    Checks the permissions for Requests-related operations.

    Returns:
        A dictionary containing the permission status.
    """
    return permission_check.fn("PERMISSION_REQUESTS")


@openaq.tool
def postgres_query_check_permissions():
    """
    Checks the permissions for PostgreSQL query-related operations.

    Returns:
        A dictionary containing the permission status.
    """
    return permission_check.fn("PERMISSION_POSTGRES_QUERY")


@openaq.tool
def postgres_backup_check_permissions():
    """
    Checks the permissions for PostgreSQL backup-related operations.

    Returns:
        A dictionary containing the permission status.
    """
    return permission_check.fn("PERMISSION_POSTGRES_BACKUP")


# =============================================================================================================
#                                                    TOOLS
# =============================================================================================================


def execute_command(
    command: str, permission_result: dict[str, Any], working_directory: str = None
) -> dict[str, Any]:
    """
    Executes a shell command and returns the output.
    AI can use this to run commands like 'make start', 'python script.py', etc.

    Args:
        command: The command to execute (e.g., 'make start', 'python script.py', 'ls -la')
        working_directory: Optional directory to run the command in

    Returns:
        A dictionary containing the command output, return code, and any errors.

    Example:
        execute_command("python --version")
        execute_command("make start", "/path/to/project")
    """
    if permission_result["status"] == "error":
        return permission_result

    try:
        cmd_parts = shlex.split(command)

        result = subprocess.run(
            cmd_parts,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        return {
            "status": "success",
            "command": command,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "working_directory": working_directory or os.getcwd(),
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": f"Command timed out after 30 seconds: {command}",
        }
    except FileNotFoundError:
        return {"status": "error", "message": f"Command not found: {cmd_parts[0]}"}
    except Exception as e:
        return {"status": "error", "message": f"Error executing command: {str(e)}"}


@openaq.tool
def command_start_all_containers() -> dict:
    """
    Starts all containers using the 'make up' command.

    Args:
        None

    Returns:
        A dictionary containing the command output, return code, and any errors.

    Example:
        start_all_containers()
    """
    permission_result = docker_check_permissions.fn()
    command: dict = execute_command(
        command="make up",
        permission_result=permission_result,
        working_directory=os.getenv("PROJECT_PATH"),
    )
    return command


def remove_all_containers() -> dict:
    """
    Removes all containers using the 'make down' command.

    Args:
        None

    Returns:
        A dictionary containing the command output, return code, and any errors.

    Example:
        remove_all_containers()
    """
    permission_result = docker_check_permissions.fn()
    command: dict = execute_command(
        command="make down",
        permission_result=permission_result,
        working_directory=os.getenv("PROJECT_PATH"),
    )
    return command


def create_measurements_table_in_postgres() -> dict:
    """
    Creates the measurements table in PostgreSQL.

    Args:
        None

    Returns:
        A dictionary containing the command output, return code, and any errors.

    Example:
        create_measurements_table_in_postgres()
    """
    permission_result = docker_check_permissions.fn()
    command: dict = execute_command(
        command="make init",
        permission_result=permission_result,
        working_directory=os.getenv("PROJECT_PATH"),
    )
    return command


@openaq.tool
def command_run_all_tests() -> dict:
    """
    Runs all tests using the 'Python3 all_tests.py' command.

    Args:
        None

    Returns:
        A dictionary containing the command output, return code, and any errors.

    Example:
        command_run_all_tests()
    """
    permission_result = requests_check_permissions.fn()
    command: dict = execute_command(
        command="make test",
        permission_result=permission_result,
        working_directory=os.getenv("PROJECT_PATH"),
    )
    return command


if __name__ == "__main__":
    openaq.run(transport="sse")
