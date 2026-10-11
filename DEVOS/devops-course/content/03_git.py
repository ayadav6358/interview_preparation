TOPIC = dict(slug="03-git", title="Git & Version Control", intro="Code, infra, configs, dashboards: sab Git mein. GitOps ka base bhi Git hai.", subs=[

dict(slug="git-basics", title="Git Basics & Workflow", level="Basic",
intro="Git distributed version control hai. Har developer ke paas poori history hoti hai. Working dir -> staging -> local repo -> remote repo.",
diagram="""
Working Dir --git add--> Staging --git commit--> Local Repo --git push--> Remote (GitHub)
      ^                                                 |
      └───────────── git pull / fetch+merge <───────────┘
""",
install="""# Windows: winget install Git.Git ; Ubuntu: sudo apt install git -y
git config --global user.name "Anup"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
ssh-keygen -t ed25519   # add ~/.ssh/id_ed25519.pub to GitHub""",
examples=[("First repo end-to-end","""git init myapp && cd myapp
echo "# myapp" > README.md
git add . && git commit -m "feat: initial commit"
git remote add origin git@github.com:user/myapp.git
git push -u origin main
git status; git log --oneline --graph --all; git diff; git diff --staged"""),
(".gitignore","""node_modules/
.env
*.log
.terraform/
*.tfstate*""")],
problems=[("Accidentally committed .env with secrets","Not in .gitignore","Rotate the secret FIRST. Then remove from history: `git filter-repo --path .env --invert-paths`. Add gitleaks pre-commit."),
("Push rejected (non-fast-forward)","Remote has commits you don't have","`git pull --rebase origin main` then push.")],
qa=[("git fetch vs git pull?","fetch downloads remote changes without merging; pull = fetch + merge (or rebase)."),
("What is HEAD?","Pointer to the current commit/branch checked out."),
("git add vs commit?","add stages changes; commit records staged snapshot to history."),
("How to undo last commit but keep changes?","`git reset --soft HEAD~1`."),
("What is .gitignore?","File listing patterns Git should not track.")]),

dict(slug="branching-merging", title="Branching, Merge, Rebase & Conflicts", level="Intermediate",
intro="Branch se parallel kaam hota hai. Merge history preserve karta hai, rebase linear history banata hai. Conflict resolve karna seekho.",
diagram="""
merge:                          rebase:
main:  A--B--C-----M            main:  A--B--C
        \\       /                        \\
feat:    D--E--                 feat:      D'--E'   (replayed on top of C)

Rule: never rebase shared/public branches.
""",
install="# git already installed",
examples=[("Feature branch workflow","""git switch -c feature/login
# ...work...
git add -A && git commit -m "feat(login): add form"
git fetch origin && git rebase origin/main
git push -u origin feature/login   # open PR
git merge --no-ff feature/login    # merge with merge commit"""),
("Resolve conflict","""git merge main
# CONFLICT in app.js -> edit markers <<<<<<< ======= >>>>>>>
git add app.js && git commit
# or abort: git merge --abort"""),
("Useful helpers","""git stash push -m wip; git stash pop
git cherry-pick <sha>
git bisect start; git bisect bad; git bisect good v1.2   # find breaking commit
git reflog   # recover 'lost' commits""")],
problems=[("Lost commits after wrong reset --hard","Thought they were gone","`git reflog` -> `git reset --hard <sha>`; reflog keeps ~90 days."),
("Force-push overwrote teammate's work","Used `--force` on shared branch","Use `--force-with-lease`, protect main with branch protection.")],
qa=[("Merge vs rebase?","Merge keeps history with merge commit; rebase rewrites commits onto new base for linear history."),
("reset vs revert?","reset moves branch pointer (rewrites history); revert creates a new commit undoing changes (safe for shared branches)."),
("What is cherry-pick?","Apply a specific commit from another branch."),
("How to recover a deleted branch?","Find sha via `git reflog` and `git branch name sha`."),
("What is fast-forward merge?","Branch pointer simply moves ahead when no divergence.")]),

dict(slug="branching-strategies", title="Branching Strategies & PR Process", level="Intermediate",
intro="Team mein kaunsa branching model? GitFlow, GitHub Flow, ya trunk-based. Modern DevOps teams trunk-based + feature flags prefer karte hain.",
diagram="""
GitHub Flow:   main <- short feature branches <- PR + CI -> deploy
Trunk-based:   main <- tiny commits daily, feature flags hide unfinished work
GitFlow:       main / develop / feature / release / hotfix  (heavier, slower)
""",
install="# enable in GitHub: Settings -> Branches -> Branch protection rules",
examples=[("Branch protection checklist","""Require PR + 1-2 approvals
Require status checks (CI) to pass
Require branches up to date
Dismiss stale approvals; require CODEOWNERS review
Block force-push and deletion"""),
("CODEOWNERS","""# .github/CODEOWNERS
/infra/      @org/platform-team
*.tf         @org/platform-team
/app/        @org/backend"""),
("Conventional commits + semver","""feat: add login    -> minor (1.1.0)
fix: null pointer   -> patch (1.0.1)
feat!: drop v1 API  -> major (2.0.0)
git tag -a v1.2.0 -m "release" && git push --tags""")],
problems=[("Long-lived branches cause merge hell","Big-bang integration","Trunk-based, small PRs (<400 lines), feature flags."),
("Broken main after merge","No required CI checks","Enable required checks + merge queue.")],
qa=[("GitFlow vs trunk-based?","GitFlow has many long-lived branches (slow). Trunk-based merges small changes to main often; better for CI/CD."),
("What is a PR?","Request to merge branch with review and automated checks."),
("What are feature flags?","Toggles to enable/disable features at runtime, decoupling deploy from release."),
("How do hotfixes work in trunk-based?","Fix on main, cherry-pick to release branch if needed, tag and deploy."),
("What is semantic versioning?","MAJOR.MINOR.PATCH conveying breaking/feature/fix changes.")]),

dict(slug="git-hooks-security", title="Git Hooks, Secrets & Advanced Git", level="Advanced",
intro="Commit se pehle checks (pre-commit), secret scanning, signed commits, monorepo aur history cleanup.",
diagram="""
git commit -> pre-commit hook -> [lint | gitleaks | terraform fmt] -> pass? commit : block
PR -> CI -> same checks again (server-side, cannot be skipped)
""",
install="pip install pre-commit && pre-commit install\nbrew/apt/winget install gitleaks",
examples=[(".pre-commit-config.yaml","""repos:
- repo: https://github.com/gitleaks/gitleaks
  rev: v8.18.4
  hooks: [{id: gitleaks}]
- repo: https://github.com/antonbabenko/pre-commit-terraform
  rev: v1.92.0
  hooks: [{id: terraform_fmt}, {id: terraform_validate}]
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v4.6.0
  hooks: [{id: check-yaml}, {id: end-of-file-fixer}]"""),
("Signed commits","""git config --global commit.gpgsign true
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub"""),
("Submodule / worktree / large files","""git submodule add https://github.com/org/lib libs/lib
git worktree add ../hotfix hotfix/1.2
git lfs install && git lfs track '*.psd'""")],
problems=[("Repo is 2GB and clone is slow","Large binaries in history","`git filter-repo --strip-blobs-bigger-than 10M`, use LFS, shallow clone `--depth 1` in CI."),
("Secret leaked to public GitHub","Committed token","Revoke immediately; history rewrite alone is not enough - assume compromised.")],
qa=[("Client-side vs server-side hooks?","Client-side (pre-commit) can be bypassed; server-side (CI/protected branch) enforce."),
("How to find which commit introduced a bug?","`git bisect` binary search."),
("Monorepo vs polyrepo?","Mono: one repo for all code (easy sharing, atomic changes, needs tooling); poly: repo per service (independence, more overhead)."),
("What is git rebase -i used for?","Squash, reorder, edit commits before sharing."),
("How to remove a file from history?","`git filter-repo` or BFG; force-push and have everyone re-clone.")]),
])
