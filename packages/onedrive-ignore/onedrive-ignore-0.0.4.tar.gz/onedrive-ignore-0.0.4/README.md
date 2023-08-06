# OneDriveIgnore
OneDrive sync settings are horrible! This script renames files so they can sync, and then switches back to original extension when you need them.
Keeping everyone happy.

# Reason for the script
Company I work for started to use OneDrive for MyDocuments, I don't particularly use that folder much since I do lots of scripting, and programming. OneDrive isn't the best for engineering purposes. I do have some folders I share that are on MyDocuments that I'd like to keep synced without deleting what's stopping the syncing. If you google "how to ignore a folder in onedrive" you'll get tons of discussions online about this issue.

See response from Angus over on OneDrive https://onedrive.uservoice.com/forums/262982-onedrive-archive/suggestions/6988070-use-a-file-to-ignore-exclude-files-or-folder

Recently my VSCode powershell extension complained about my package management being out of date, and installed it in MyDocuments. I figured just ignore this folder for Sync, but no, OneDrive removes the folder from the PC even if it originated from the PC, leaving me without my powershell package management.

# Install

```
pip install onedrive-ignore
```

# Usage

Create `ignore_paths.txt` file then place it in `%userprofile%\.config\onedrive-ignore`, and add one path per line to folders that are causing issues.

```
C:\Users\fernando\OneDrive\My Documents\WindowsPowerShell\Modules\PackageManagement\1.4.7\coreclr\netstandard2.0
C:\Users\fernando\OneDrive\My Documents\WindowsPowerShell\Modules\PackageManagement\1.4.7\fullclr
```

This script does a renaming of the file to txt file, then when restoring the files to original extension it simply removes the .txt.

```
onedrive --ignore
onedrive --restore

# Short version
onedrive -i
onedrive -r
```

Files Ignored, synced to onedrive:

![Files_Ignored](https://github.com/kodaman2/OneDriveIgnore/raw/main/images/files_ignored.PNG)


Files Restored, OneDrive not syncing:

![Files_Restored](https://github.com/kodaman2/OneDriveIgnore/raw/main/images/files_restored.PNG)