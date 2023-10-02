
## 0.0.1 - 2023-10-02
testing patch version,  does it work
## 0.0.2 - 2023-10-02
including a diff now

### Diff:
```
diff --git a/python/git-helper/git-helper-05.py b/python/git-helper/git-helper-05.py
index 5a59760..0aa272c 100644
--- a/python/git-helper/git-helper-05.py
+++ b/python/git-helper/git-helper-05.py
@@ -2,6 +2,7 @@ import os
 import sys
 import git
 import logging
+import semver
 from semver import VersionInfo
 import datetime
 
@@ -159,6 +160,9 @@ def main():
                 print(f"{ERROR_TEXT}Invalid choice. Please enter a number between 1 and 3.{RESET_TEXT}")
                 continue  # Skip to the next iteration of the loop
             
+            # Get the diff between the working directory and the last commit
+            diff = repo.git.diff()
+            
             # Create a new tag with the new version number
             repo.create_tag(str(new_version))
             
@@ -167,6 +171,9 @@ def main():
                 f.write(f"\n## {new_version} - {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
                 changes = input(f"{QUESTION_TEXT}Enter the changes included in this version (separate multiple changes with commas): {RESET_TEXT}")
                 f.write(', '.join(changes.split(',')))
+                f.write(f"\n\n### Diff:\n```\n{diff}\n```\n")
+            print(f"{ANSWER_TEXT}A new version {new_version} has been tagged and the changelog has been updated.{RESET_TEXT}")
+            f.write(', '.join(changes.split(',')))
             
             print(f"{ANSWER_TEXT}A new version {new_version} has been tagged and the changelog has been updated.{RESET_TEXT}")
         elif user_choice == '5':
```

## 0.1.0 - 2023-10-02
testing minor version and diff

### Diff:
```
diff --git a/python/git-helper/CHANGELOG.md b/python/git-helper/CHANGELOG.md
index a822eea..3da0063 100644
--- a/python/git-helper/CHANGELOG.md
+++ b/python/git-helper/CHANGELOG.md
@@ -1,3 +1,41 @@
 
 ## 0.0.1 - 2023-10-02
-testing patch version,  does it work
\ No newline at end of file
+testing patch version,  does it work
+## 0.0.2 - 2023-10-02
+including a diff now
+
+### Diff:
+```
+diff --git a/python/git-helper/git-helper-05.py b/python/git-helper/git-helper-05.py
+index 5a59760..0aa272c 100644
+--- a/python/git-helper/git-helper-05.py
++++ b/python/git-helper/git-helper-05.py
+@@ -2,6 +2,7 @@ import os
+ import sys
+ import git
+ import logging
++import semver
+ from semver import VersionInfo
+ import datetime
+ 
+@@ -159,6 +160,9 @@ def main():
+                 print(f"{ERROR_TEXT}Invalid choice. Please enter a number between 1 and 3.{RESET_TEXT}")
+                 continue  # Skip to the next iteration of the loop
+             
++            # Get the diff between the working directory and the last commit
++            diff = repo.git.diff()
++            
+             # Create a new tag with the new version number
+             repo.create_tag(str(new_version))
+             
+@@ -167,6 +171,9 @@ def main():
+                 f.write(f"\n## {new_version} - {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
+                 changes = input(f"{QUESTION_TEXT}Enter the changes included in this version (separate multiple changes with commas): {RESET_TEXT}")
+                 f.write(', '.join(changes.split(',')))
++                f.write(f"\n\n### Diff:\n```\n{diff}\n```\n")
++            print(f"{ANSWER_TEXT}A new version {new_version} has been tagged and the changelog has been updated.{RESET_TEXT}")
++            f.write(', '.join(changes.split(',')))
+             
+             print(f"{ANSWER_TEXT}A new version {new_version} has been tagged and the changelog has been updated.{RESET_TEXT}")
+         elif user_choice == '5':
+```
diff --git a/python/git-helper/git-helper-05.py b/python/git-helper/git-helper-05.py
index 5a59760..730a2df 100644
--- a/python/git-helper/git-helper-05.py
+++ b/python/git-helper/git-helper-05.py
@@ -2,6 +2,7 @@ import os
 import sys
 import git
 import logging
+import semver
 from semver import VersionInfo
 import datetime
 
@@ -159,6 +160,9 @@ def main():
                 print(f"{ERROR_TEXT}Invalid choice. Please enter a number between 1 and 3.{RESET_TEXT}")
                 continue  # Skip to the next iteration of the loop
             
+            # Get the diff between the working directory and the last commit
+            diff = repo.git.diff()
+            
             # Create a new tag with the new version number
             repo.create_tag(str(new_version))
             
@@ -167,6 +171,10 @@ def main():
                 f.write(f"\n## {new_version} - {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
                 changes = input(f"{QUESTION_TEXT}Enter the changes included in this version (separate multiple changes with commas): {RESET_TEXT}")
                 f.write(', '.join(changes.split(',')))
+                f.write(f"\n\n### Diff:\n```\n{diff}\n```\n")  # Write the diff to the file within the same with open block
+
+            print(f"{ANSWER_TEXT}A new version {new_version} has been tagged and the changelog has been updated.{RESET_TEXT}")
+            f.write(', '.join(changes.split(',')))
             
             print(f"{ANSWER_TEXT}A new version {new_version} has been tagged and the changelog has been updated.{RESET_TEXT}")
         elif user_choice == '5':
```

## 1.0.0 - 2023-10-02
test

### Diff:
```

```
