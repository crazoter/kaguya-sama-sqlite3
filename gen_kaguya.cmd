REM This is a helper cmd script to generate the schema diagram using schemacrawler.
REM Modify the REPO_PATH variable below and place this in the "schemacrawler-ver-distribution\examples\diagram" directory.

SETLOCAL
REM Remark: Modify the repo_path value to point to the repository directory e.g. "D:\path\kaguya-sama"
SET REPO_PATH="YOUR_PATH_HERE\kaguya-sama"

sqlite_diagram.cmd %REPO_PATH%\kaguya_data.db %REPO_PATH%\schema.pdf

ENDLOCAL