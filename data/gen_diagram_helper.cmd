REM This is a helper windows cmd script to generate the schema diagram using schemacrawler.
REM Modify the REPO_PATH variable below and place this script in the "schemacrawler-ver-distribution\examples\diagram" directory.

SETLOCAL
REM Remark: Modify the repo_path value to point to the repository directory e.g. "D:\...\kaguya-sama"
SET REPO_PATH="D:\Fun\kaguya"

..\..\_schemacrawler\schemacrawler.cmd --server=sqlite "--database=%REPO_PATH%\data\kaguya_data.db" --user=sa --password= --info-level=maximum -c=schema --output-format=png "-o=%REPO_PATH%\data\schema.png"

ENDLOCAL