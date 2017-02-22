---
title: Git Cheatsheet
category: sourcecontrol
tags: SCM DevOps
---

# Git Cheatsheets

* [Graphical git cheatsheet](http://byte.kde.org/~zrusin/git/git-cheat-sheet-medium.png)
* [git basic commands](https://www.atlassian.com/git/tutorials/svn-to-git-prepping-your-team-migration/basic-git-commands)
* [git cheatsheet (visual)](https://www.maxoberberger.net/media/cheatsheet/git-cheatsheet-visual.pdf)
* [git cheatsheet (interactive)](http://ndpsoftware.com/git-cheatsheet.html#loc=workspace)
* [git full documentation](https://git-scm.com/doc)

*Repo hosting:*
* [BitBucket](https://bitbucket.org/)
* [GitHub](https://github.com/)	

## [26 MOST USED GIT COMMANDS (A GIT CHEAT-SHEET)](http://www.mrgeek.me/technology/26-most-used-git-commands-a-git-cheat-sheet/)

	$ mkdir repos
	$ cd ~/repos
	$ git clone https://mrgeek@bitbucket.org/mrgeek/repository01.git
	$ ls -al repository01/
	$ rm -irf repository01/
	$ git clone https://mrgeek@bitbucket.org/mrgeek/repository01.git repository01-practice
	$ ls ~/repos
	$ cd ~/repos/repository01-practice/
	$ ls -al

git shows in red that in my repo there are files modified but not committed.

	$ git status
	$ git add README
	$ git add -A
	$ git commit -m "adding repo instructions"
	$ git push -u origin master
	$ git pull
	$ ssh -p 2222 user@domain.com
	$ git init --bare foobar.git
	$ git rev-parse --show-toplevel
	$ git rev-parse --git-dir

'ssh-keygen' on your hostgator server to generate a key
~ is a quick way of typing your home directory

	$ rm -rf ~/public_html/localrepo.git
	$ git -- update-server-info

go to ~/public_html/localrepo.git and type `git pull`

	$ git clone git@bitbucket.org:mrgeek/development_repo1.git
	$ git config global user.name "Firstname Lastname"
	$ git config --global user.email "your_email@youremail.com"

## Step by Step

Create a new Git repository in current directory:

	git init

Create an empty Git repository in the specified directory:

	git init <directory>

Copy an existing Git repository:
	
	git clone <repo>

Clone the repository located at <repo> into the folder called <directory> on the local machine:

	git clone <repo> <directory>
	git clone username@host:/path/to/repository

Config:

	git config --global user.name <name>
	git config --global user.email <email>

Stage all changes in `<file>` for the next commit:
	
	git add <file>

Stage all changes in <directory> for the next commit:

	git add <directory>

Commit the staged snapshot to the project history:

	git commit
	git commit -m "<message>"

Add and commit all in one:

	git commit -am "message"

Fix up the most recent commit:

	git commit --amend

List which files are staged, unstaged, and untracked:

	git status
	git status -s

Show file diff:

	git diff                 #  git diff by itself doesn’t show all changes made since your last commit – only changes that are still unstaged.
	git diff --staged   #  Shows file differences between staging and the last file version

Open GUI:

	git gui

Displays committed snapshots:

	git log -n <limit>
	git log --graph --decorate --oneline

Checking out commits, and checking out branches:

	git checkout <commit>
	git checkout master #  Return to the master branch (or whatever branch we choose)

Check out a previous version of a file:

	git checkout <commit> <file>
	git checkout HEAD hello.py  #  check out the most recent version

## Branches

Branches are just pointers to commits.

List all of the branches in your repository.  Also tell you what branch you're currently in:

	git branch
	
Create a new branch called <branch>. 

	git branch <branch>

This does not check out the new branch. you need:

	git checkout <existing-branch>

Or direcly create-and-check out <new-branch>.

	git checkout -b <new-branch>

Safe delete the branch:

	git branch -d <branch>

Merge the specified branch into the current branch:

	git merge <branch>

Undo any undesired changes

Generate a new commit that undoes all of the changes introduced in <commit>, then apply it to the current branch

	git revert <commit>

git revert undoes a single commit—it does not “revert” back to the previous state of a project by removing all subsequent commits.

Dangerous method - erases history
	
	git reset

List the remote connections you have to other repositories.
	
	git remote -v

Create a new connection / delete a connection to a remote repository.
	
	git remote add <name> <url>  # often "origin"
	git remote rm <name> # delete

Fetch the specified remote’s copy of the current branch and immediately merge it into the local copy. This is the same as git fetch <remote> followed by git merge origin/<current-branch>.

	git pull <remote>

Put my changes on top of what everybody else has done. ensure a linear history by preventing unnecessary merge commits.
	
	git pull --rebase <remote>

Transfer commits from your local repository to a remote repo.
	
	git push <remote> <branch>

Pushes the current branch to the remote server and links the local branch to the remote so next time you can do git pull or git push
	
	git push -u origin <branch>

	
## Typical Workflows

###  Short-lived topic branches

* Start a new feature: `git checkout -b new-feature master`
* Edit some files:
	
	git add <file>
	git commit -m "Start a feature"
* Edit some files
	git add <file>
	git commit -m "Finish a feature"
* Merge in the new-feature branch
	git checkout master
	git merge new-feature
	git branch -d new-feature

### Centralized repo

* To push the master branch to the central repo:

	git push origin master
	
If local history has diverged from the central repository, Git will refuse the request
	
	git pull --rebase origin master

## Sync my local repo with the remote repo

	git pull origin master
	git add filename.xyz
	git commit . -m “comment”
	git push origin master

