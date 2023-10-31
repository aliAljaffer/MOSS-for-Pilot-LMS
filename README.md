# MOSS Code Similarity Checker

This script was made to organize a "select-all" submissions zip file downloaded from the LMS Pilot. Simply go to the assignment dropbox and press the check mark that highlights all submissions and press download. Wait for the download to finish then move the `.zip` file to a folder called `StudentCode` in the same directory as mossScript.

A `moss` file with execute permissions needs to be in root directory next to `mossScript.py`. it's contents are whatever you get in the email back after registration.

After running, a folder inside `StudentCode` named `namedFiles` should contain all the submissions in the format `lastName.fileExtension`. Run the moss script on these files(Or just let the code run it ;\) ): `./moss ./StudentCode/namedFiles/*.java` and the output should be a link to the report.

<p style='font-size:36px'>Untested on Windows!</p>
