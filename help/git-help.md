Git: Initialize Repository command from the Command Palette (Ctrl+Shift+P).

> git remote add origin https://github.com/<repo owner>/<repo name>.git
> git push -u origin master


$ git clone https://github.com/user/repo.git
$ git remote -v

Adding Remote Repositories
$ git remote
origin
$ git remote add aa https://github.com/user/repo.git
origin https://github.com/user/repo.git (fetch)
origin https://github.com/user/repo.git (push)
aa https://github.com/user/repo.git(fetch)
aa https://github.com/user/repo.git(push)

$ git fetch aa

$ git push origin master
$ git remote show origin

git rebase HEAD~3 -i do interactive rebase using VS Code
git commit use VS Code for the commit message
git add -p followed by e for interactive add
git difftool <commit>^ <commit> use VS Code as the diff editor for change
git checkout -b local_branch_name remote_name/remote_branch_name
git branch
git branch -a to list all available branches on local and remote git repository