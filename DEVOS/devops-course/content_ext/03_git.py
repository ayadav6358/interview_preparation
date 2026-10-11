EXT = dict(
guide=dict(
bigpicture=dict(
problem="""**Problem it solves:** Many people change the same code, configs and infrastructure files. Without version control you get "final_v2_new_FINAL.zip", overwritten work, no history and no way to undo a bad change. **Git** records every change as a commit, lets people work in parallel on branches, and merges the work safely.""",
chain=["PROBLEM: many people editing the same files, changes get lost or break things",
       "TRADITIONAL APPROACH: copy folders, email zips, shared drives",
       "PAIN: no history, no blame, no safe merge, no rollback",
       "TECHNOLOGY: Git (distributed version control) + remote hosting (GitHub/GitLab)",
       "SOLUTION: commits (snapshots), branches, merges, pull requests, tags",
       "REAL-WORLD BENEFIT: full history, safe collaboration, code review, CI triggers, GitOps"],
text="""In DevOps, Git holds more than app code: Dockerfiles, Kubernetes YAML, Terraform, pipelines and dashboards. It is the **single source of truth** and the trigger for CI/CD and GitOps."""),
e2e=dict(diagram="""Working directory (edit files)
   | git add
   v
Staging area (index)
   | git commit
   v
Local repository (history)
   | git push
   v
Remote (GitHub/GitLab)
   | Pull Request + review + CI checks
   v
Merge to main
   | webhook
   v
CI/CD pipeline > deploy""",
text="""You edit files in the **working directory**, choose what to include with `git add` (staging area), and `git commit` to store a snapshot with a message in your **local repository**. `git push` uploads commits to the **remote**. Teammates review through a **pull request** while CI runs checks. After approval the change is **merged** into `main`, which triggers the pipeline. `git pull` (fetch + merge/rebase) brings others' changes back to you."""),
tools=dict(rows=[
["git", "Version control engine", "Files", "Commits/history", "Every developer machine"],
["GitHub / GitLab / Bitbucket", "Remote hosting, PRs, access control", "Pushed commits", "Reviews, merges, webhooks", "Team collaboration"],
["pre-commit / husky", "Local hooks", "Staged files", "Pass/fail", "Before commit"],
["Gitleaks / trufflehog", "Secret scanning", "Repo history", "Findings", "CI and pre-commit"],
["Branch protection / CODEOWNERS", "Governance", "PRs", "Required reviews/checks", "main branch"],
["CI (Actions/Jenkins)", "Verify changes", "PR/push", "Status checks", "After push"],
["ArgoCD/Flux", "GitOps deploy", "Git repo", "Cluster state", "Deployment"]],
why="**Merge vs rebase:** merge preserves history with a merge commit; rebase rewrites commits for a linear history (never rebase shared branches). **Trunk-based vs GitFlow:** trunk-based is short-lived branches and frequent integration (best for CI/CD); GitFlow uses long-lived develop/release branches (slower, suits scheduled releases)."),
compare=[
("git merge vs git rebase", ["Topic", "merge", "rebase"], [["History", "Non-linear, keeps branch context", "Linear, rewrites commits"], ["Safe on shared branches", "Yes", "No"], ["Conflicts", "Resolved once", "May repeat per commit"]]),
("git fetch vs pull", ["Topic", "fetch", "pull"], [["Action", "Downloads remote changes only", "fetch + merge (or rebase)"], ["Safety", "Does not touch your files", "Can create conflicts"]]),
("reset vs revert", ["Topic", "reset", "revert"], [["Effect", "Moves branch pointer (rewrites history)", "Creates a new commit undoing changes"], ["Shared branch", "Avoid", "Safe"]]),
("Git vs GitHub", ["Topic", "Git", "GitHub"], [["What", "Version control tool", "Hosting platform + collaboration features"], ["Works offline", "Yes", "No"]]),
("Branching strategies", ["Strategy", "Branches", "Best for"], [["Trunk-based", "main + short-lived feature branches", "CI/CD, frequent releases"], ["GitFlow", "main, develop, feature, release, hotfix", "Versioned/scheduled releases"], ["GitHub Flow", "main + feature branches + PR", "Simple web apps"]]),
("Tag vs Branch", ["Topic", "Tag", "Branch"], [["Moves", "No (fixed point)", "Yes (advances)"], ["Use", "Releases (v1.2.0)", "Ongoing work"]])],
troubleshooting=[
("Merge conflict", "Same lines changed in both branches", "`git status`, `git diff --name-only --diff-filter=U`", "Edit conflict markers, `git add`, `git commit` (or `git rebase --continue`).", "Small PRs, frequent rebases, clear ownership."),
("Pushed a secret", "Credential committed", "`gitleaks detect`, `git log -S 'secret'`", "Rotate the secret FIRST, then remove from history (git filter-repo/BFG) and force-push if policy allows.", "Pre-commit scanning, secrets manager."),
("`rejected (non-fast-forward)` on push", "Remote has commits you do not have", "`git fetch && git log HEAD..origin/main`", "`git pull --rebase` then push. Never force-push shared branches.", "Pull frequently."),
("Committed to wrong branch", "Forgot to switch", "`git branch`, `git log`", "`git switch correct && git cherry-pick <sha>`, then reset the wrong branch (if unpublished).", "Check `git status` before committing."),
("Lost commits after reset", "Hard reset/rebase", "`git reflog`", "`git checkout -b rescue <sha>` from reflog.", "Avoid `--hard` without checking."),
("Large file blocks push", "Binary over size limit", "`git count-objects -vH`, `git rev-list --objects --all`", "Remove from history (filter-repo), use Git LFS.", ".gitignore and LFS rules.")],
practices={
"Development": ["Small focused commits with clear messages (Conventional Commits).", "Pull/rebase often; branch per task."],
"Production": ["Protect `main`: required reviews and passing checks; tag releases; signed tags/commits."],
"Security": ["Never commit secrets; pre-commit + CI secret scan; least-privilege repo access; SSH keys/PATs with expiry; signed commits."],
"Performance": ["Shallow clone in CI (`--depth 1`), sparse checkout for monorepos, Git LFS for binaries."],
"Reliability": ["Mirror/backup critical repos; protect against force-push and branch deletion."],
"Monitoring & Logging": ["Audit logs for repo access; alerts for secret exposure."]},
mistakes={
"Beginner mistakes": ["`git add .` staging junk/secrets.", "Committing directly to main.", "Vague messages like 'fix'."],
"Developer mistakes": ["Force-pushing shared branches.", "Huge PRs that are hard to review."],
"DevOps mistakes": ["No branch protection.", "State files (e.g. terraform.tfstate) or `.env` in Git."],
"Production mistakes": ["Deploying from an unreviewed branch.", "No tags so releases cannot be identified."],
"Security mistakes": ["Secrets in history (deleting the file is not enough).", "Long-lived personal access tokens with wide scope."]},
versions=[
"Modern Git: prefer `git switch` and `git restore` over overloaded `git checkout`.",
"Default branch name is now often `main` (older repos use `master`): `git config --global init.defaultBranch main`.",
"GitHub no longer accepts account passwords for Git operations: use SSH keys or personal access tokens/OIDC.",
"`git filter-branch` is discouraged; use `git filter-repo`."],
hinglish="""Git mein **commit ek snapshot** hai. Flow: **working directory > staging (`git add`) > commit > push**. **Branch** alag rasta hai jahan tum safely kaam karte ho, phir **Pull Request** se review karke `main` mein merge karte hain. **Merge** history ko rakhta hai, **rebase** history ko seedhi line bana deta hai (shared branch par kabhi rebase mat karo). Secret galti se push ho jaye to **pehle rotate karo**, phir history se hatao.""",
mnemonics=[
("Git areas", "W-S-L-R: Working dir, Staging, Local repo, Remote"),
("Undo", "Local mistake: restore/reset; shared mistake: revert"),
("Daily flow", "switch -c > add > commit > push > PR > merge > pull"),
("Conflict fix", "Edit, add, continue (or commit)")],
client=dict(
s30="""Git is our version control system: it records every change to code and infrastructure files, lets many people work in parallel, and makes review and rollback easy. It is also what triggers our automated builds and deployments.""",
m2="""Every change to the application and to our infrastructure is stored in Git with who changed what and why. Developers work on separate branches and submit pull requests. Before anything is merged, automated tests and security scans run and a colleague reviews it. If a release has a problem we can identify the exact change and revert it. Because deployments are triggered from Git, the repository becomes the audit trail for compliance and the single source of truth for what is running.""",
m5="""Three ideas. **History and collaboration:** Git stores snapshots called commits, so we can compare versions, find who changed what and restore anything; branches let people work independently and pull requests provide review. **Governance:** we protect the main branch with required reviews and checks, use signed commits and tags for releases, and scan for secrets before code is accepted. **Automation:** merges trigger CI pipelines, and with GitOps the repository defines the desired state of the environments, so a rollback is a Git revert. We choose a branching model that fits the release cadence, typically trunk-based development with short-lived branches for continuous delivery. The result is a traceable, secure and repeatable delivery process."""),
roadmap=[
("Beginner", ["init, clone, add, commit, status, log", "Remotes: push, pull, fetch", "Branches: switch, merge", ".gitignore"]),
("Intermediate", ["Pull requests and code review", "Conflict resolution", "rebase, cherry-pick, stash, tags", "Undo: restore, reset, revert, reflog"]),
("Advanced", ["Interactive rebase, bisect", "Hooks, pre-commit", "Submodules/monorepo strategies", "Signed commits, history rewriting"]),
("Production", ["Branch protection, CODEOWNERS", "Release/tagging strategy", "Secret scanning", "GitOps"]),
("Interview", ["merge vs rebase", "Undo strategies", "Branching models", "Recover deleted commits"])],
miniproject=dict(title="Team workflow with PR, protection and secret scanning",
arch="""feature branch --> push --> Pull Request
   CI: tests + gitleaks + lint  --> review (CODEOWNERS)
   --> squash merge to main --> tag v1.0.0 --> pipeline deploys""",
steps=[
("Step 1: Create repo and first commit", """git init demo && cd demo
git config user.name "Your Name" && git config user.email "you@example.com"
printf 'node_modules\\n.env\\n' > .gitignore
echo '# demo' > README.md
git add . && git commit -m "chore: initial commit"
git branch -M main""", "`.gitignore` prevents committing dependencies and secrets. The first commit forms the root of the history."),
("Step 2: Work on a feature branch", """git switch -c feature/login
echo 'login page' > login.txt
git add login.txt && git commit -m "feat: add login page"
git push -u origin feature/login""", "Branch per feature keeps `main` stable. `-u` links the local branch to the remote for future pushes."),
("Step 3: Pre-commit secret scan", """cat > .pre-commit-config.yaml <<'EOF'
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks: [{ id: gitleaks }]
EOF
pip install pre-commit && pre-commit install""", "Blocks commits containing secrets. Pin the `rev` to a current release: check the project's tags."),
("Step 4: Merge, tag and recover", """git switch main && git pull
git merge --no-ff feature/login
git tag -a v1.0.0 -m "first release" && git push origin main --tags
git reflog | head   # recover anything lost""", "Merge with a merge commit, tag the release for the pipeline, and know that `reflog` can restore lost commits.")]),
interview=[
("Beginner", "What is Git?", "A distributed version control system that tracks changes and supports collaboration.", "Foundation.", "Track code and Terraform files."),
("Beginner", "Git vs GitHub?", "Git is the tool; GitHub is a hosting service for Git repositories.", "Common confusion.", "GitLab and Bitbucket are alternatives."),
("Beginner", "What is a commit?", "A snapshot of tracked files with author, message and parent pointer(s), identified by a SHA.", "Core concept.", "`git commit -m 'msg'`."),
("Beginner", "What is the staging area?", "A place where you assemble the next commit.", "Understand `add`.", "`git add -p` to stage parts."),
("Beginner", "What is a branch?", "A movable pointer to a commit for parallel work.", "Workflow.", "`git switch -c feature/x`."),
("Beginner", "What is `.gitignore`?", "File listing paths Git should not track.", "Avoid junk/secrets.", "node_modules, .env."),
("Beginner", "clone vs fork?", "Clone copies a repo locally; fork copies a repo to your account on the host for contributing.", "Open source workflow.", "Fork then PR."),
("Beginner", "What is `git pull`?", "Fetch remote changes and integrate them (merge or rebase).", "Sync.", "`git pull --rebase`."),
("Beginner", "How do you see history?", "`git log --oneline --graph --decorate`.", "Basics.", "Find who changed a line: `git blame`."),
("Beginner", "What is a tag?", "A named pointer to a commit, used for releases.", "Versioning.", "`v1.2.0`."),
("Intermediate", "merge vs rebase?", "Merge joins histories with a merge commit; rebase replays commits on a new base for linear history; do not rebase published commits.", "Very common.", "Rebase local feature branch on main."),
("Intermediate", "How to resolve a merge conflict?", "Open conflicted files, choose the correct content, remove markers, `git add`, then commit/continue.", "Practical skill.", "Use a merge tool."),
("Intermediate", "reset vs revert vs restore?", "`restore` discards working changes; `reset` moves the branch pointer (soft/mixed/hard); `revert` creates an inverse commit.", "Undo strategies.", "Revert on main."),
("Intermediate", "What is `git stash`?", "Temporarily saves uncommitted changes.", "Context switching.", "`git stash pop`."),
("Intermediate", "cherry-pick?", "Applies a specific commit onto the current branch.", "Hotfix backport.", "Copy a fix to release branch."),
("Intermediate", "What is a pull request?", "A request to merge a branch with discussion, review and CI checks.", "Team process.", "Two approvals required."),
("Intermediate", "Explain fast-forward vs no-ff merge.", "Fast-forward moves the pointer without a merge commit; `--no-ff` always creates one to preserve branch context.", "History design.", "Squash for clean history."),
("Intermediate", "Squash merge?", "Combines all PR commits into one on main.", "Clean history.", "One commit per feature."),
("Intermediate", "What is HEAD?", "Pointer to the current commit/branch checked out; detached HEAD means it points to a commit, not a branch.", "Internals.", "`git checkout <sha>`."),
("Intermediate", "How to undo the last commit but keep changes?", "`git reset --soft HEAD~1`.", "Common task.", "Fix commit message."),
("Intermediate", "What are Git hooks?", "Scripts triggered by Git events (pre-commit, commit-msg, pre-push).", "Quality gates.", "Lint before commit."),
("Intermediate", "Branching strategies?", "Trunk-based, GitHub Flow, GitFlow.", "Process.", "Trunk-based for CI/CD."),
("Intermediate", "What is CODEOWNERS?", "File mapping paths to required reviewers.", "Governance.", "`/infra/ @platform-team`."),
("Intermediate", "How to sync a fork?", "Add `upstream`, fetch, merge/rebase, push.", "OSS.", "`git remote add upstream`."),
("Advanced", "How does Git store data?", "Content-addressed objects (blob, tree, commit, tag) in `.git/objects`, referenced by SHA; branches are refs.", "Internals.", "`git cat-file -p HEAD`."),
("Advanced", "What is `git reflog`?", "Local log of where HEAD/branches pointed; lets you recover commits after resets.", "Recovery.", "Undo a bad rebase."),
("Advanced", "Interactive rebase use cases?", "Squash, reorder, edit, drop commits before sharing.", "History hygiene.", "`git rebase -i HEAD~5`."),
("Advanced", "How do you remove a secret from history?", "Rotate secret, rewrite history with git filter-repo/BFG, force-push, ask collaborators to re-clone, add scanning.", "Security response.", "AWS key leaked."),
("Advanced", "`git bisect`?", "Binary search through commits to find the one that introduced a bug.", "Debugging.", "`git bisect start; good; bad`."),
("Advanced", "Submodules vs subtrees vs monorepo?", "Submodule pins another repo at a commit; subtree merges another repo's history; monorepo keeps everything in one repo with tooling.", "Repo strategy.", "Shared library across services."),
("Advanced", "How to enforce quality on a team?", "Branch protection, required CI/reviews, CODEOWNERS, signed commits, commit lint, pre-commit and server-side hooks.", "Governance.", "GitHub rulesets."),
("Advanced", "Explain shallow clone and its uses.", "`--depth N` fetches limited history for speed; used in CI but some tools need full history (versioning, blame).", "CI optimisation.", "GitHub Actions `fetch-depth`."),
("Advanced", "What is Git LFS?", "Stores large binaries outside the repo, keeping pointers in Git.", "Large files.", "Design assets, datasets."),
("Advanced", "Signed commits and tags?", "GPG/SSH signatures verify authorship.", "Supply chain.", "Required on protected branches."),
("Advanced", "GitOps and Git?", "Git as source of truth for desired state; controllers reconcile clusters to it.", "Modern delivery.", "ArgoCD watching a repo."),
("Advanced", "Trunk-based development needs what?", "Small changes, strong automated tests, feature flags, fast reviews.", "Prerequisites.", "Deploy daily."),
("Advanced", "Explain three-way merge.", "Git uses common ancestor and both tips to combine changes; conflicts appear when both changed same region.", "Merge internals.", "Merge base via `git merge-base`."),
("Advanced", "How do you handle a monorepo CI?", "Path filters/affected detection, caching, sparse checkout, CODEOWNERS per path.", "Scale.", "Nx/Bazel."),
("Scenario-Based", "You accidentally pushed a password.", "Revoke/rotate immediately, remove from history, force-push per policy, scan repo, add pre-commit hook.", "Incident response.", "See troubleshooting."),
("Scenario-Based", "Production is broken after a merge.", "Revert the merge/PR commit (`git revert -m 1 <merge>`), redeploy, then fix forward via new PR.", "Rollback.", "Revert instead of reset."),
("Scenario-Based", "Two developers changed the same file.", "Rebase/merge, resolve conflicts communicating with the author, run tests, push.", "Collaboration.", "Ask the author intent."),
("Scenario-Based", "Need a hotfix on an old release.", "Branch from release tag, fix, cherry-pick to main, tag patch version.", "Release management.", "v1.2.1 from v1.2.0."),
("Scenario-Based", "Repo is huge and slow.", "Find large objects, move to LFS, shallow/partial clone, gc, split repo.", "Performance.", "Removed 2GB of binaries."),
("Scenario-Based", "Enforce that only tested code reaches main.", "Protected branch with required status checks and reviews, no direct pushes.", "Governance.", "Required CI job."),
("Scenario-Based", "Choose branching strategy for weekly releases and hotfixes.", "GitHub Flow or trunk-based with release branches/tags; GitFlow only if multiple supported versions.", "Design judgement.", "Mobile app with staged releases."),
("Scenario-Based", "Someone force-pushed and lost commits.", "Recover from other clones, reflog on server, CI caches; then disable force-push via branch protection.", "Recovery and prevention.", "`git reflog` from a teammate."),
("Scenario-Based", "Team unsure which commit is deployed.", "Tag releases, embed git SHA in the image/build metadata, expose /version endpoint.", "Traceability.", "Image tag equals SHA."),
("Scenario-Based", "Manage environment configs in Git.", "Separate config repo or folders per env, no secrets, use overlays and GitOps.", "IaC hygiene.", "values-prod.yaml."),
("Scenario-Based", "Contractors need limited repo access.", "Team-based least privilege, forks or scoped roles, time-boxed access, audit.", "Access control.", "Read-only role."),
("Scenario-Based", "Code review is a bottleneck.", "Smaller PRs, CODEOWNERS, automation for style, review SLAs, pairing.", "Process.", "Limit PR size to 400 lines."),
("Scenario-Based", "Need to find who introduced a bug in a line.", "`git blame`, `git log -L`, `git bisect`.", "Investigation.", "Blame plus PR link."),
("Scenario-Based", "Migrate from SVN/another VCS.", "Use git-svn or import tooling, keep history, train team, freeze old repo.", "Migration.", "Move with authors mapping."),
("Troubleshooting-Based", "`fatal: not a git repository`.", "Not inside a repo or .git missing; `git init` or cd to the right dir.", "Basics.", "Wrong directory."),
("Troubleshooting-Based", "`Permission denied (publickey)` on push.", "SSH key not added to the account/agent; check `ssh -T git@github.com`, `ssh-add -l`.", "Auth.", "Wrong key loaded."),
("Troubleshooting-Based", "`detached HEAD` state.", "You checked out a commit; create a branch to keep work: `git switch -c new`.", "State confusion.", "After checking out a tag."),
("Troubleshooting-Based", "`refusing to merge unrelated histories`.", "Repos have no common ancestor; use `--allow-unrelated-histories` deliberately.", "Repo joins.", "Merging a new repo into an existing one."),
("Troubleshooting-Based", "Pre-commit hook blocks commit.", "Read the message, fix the issue; skip only with justification (`--no-verify`) and never for secret scans.", "Hooks.", "Lint error."),
("Troubleshooting-Based", "File tracked despite .gitignore.", "Already tracked: `git rm --cached file`, commit.", "Ignore rules.", ".env accidentally committed."),
("Troubleshooting-Based", "Line ending changes everywhere.", "Set `.gitattributes`/`core.autocrlf`; normalise once.", "Cross-platform teams.", "Windows vs Linux."),
("Troubleshooting-Based", "Cannot delete a branch.", "You are on it or it is unmerged: switch away; `-D` to force after checking.", "Branch cleanup.", "`git branch -d feature`."),
("Troubleshooting-Based", "Push rejected due to file size.", "Remove large file from history/use LFS.", "Size limits.", "100MB GitHub limit."),
("Troubleshooting-Based", "CI cannot clone private repo.", "Missing deploy key/token, expired PAT, org SSO not authorised.", "CI access.", "Use GitHub App/OIDC.")],
cheatsheet={
"Definitions": ["Commit=snapshot; branch=movable pointer; HEAD=current; tag=fixed pointer; remote=hosted copy; PR=review + merge request."],
"Commands": ["`git init|clone` `git status` `git add -p` `git commit -m` `git log --oneline --graph`", "`git switch -c b` `git merge b` `git rebase main` `git cherry-pick sha`", "`git fetch` `git pull --rebase` `git push -u origin b`", "`git restore f` `git reset --soft HEAD~1` `git revert sha` `git reflog`", "`git stash` `git stash pop` `git tag -a v1 -m ''` `git bisect`"],
"Files": [".gitignore .gitattributes CODEOWNERS .pre-commit-config.yaml .git/config .github/workflows"],
"Architecture": ["Working dir > staging > local repo > remote > PR > main > CI/CD."],
"Ports": ["SSH 22 (git@), HTTPS 443, git protocol 9418 (rare)"],
"Differences": ["merge vs rebase; reset vs revert; fetch vs pull; tag vs branch; Git vs GitHub."],
"Troubleshooting commands": ["`git status` > `git diff` > `git log` > `git reflog` > `ssh -T git@github.com` > `git remote -v`"],
"Best practices": ["Small commits, PRs, protected main, no secrets, tags for releases, rebase only local branches."]}
),
subs={
"git-basics": dict(
define=dict(simple="Git saves versions of your files so you can go back and collaborate.",
technical="Git is a distributed VCS storing snapshots as content-addressed objects; each clone has full history; commits form a DAG.",
why="Track and share changes safely.", without="Overwritten work, no history.", use="All code and config.", avoid="Storing large binaries/secrets.", analogy="Save points in a video game."),
internals="""`git add` writes file content as blob objects into `.git/objects` and updates the index; `git commit` writes a tree (directory snapshot) and a commit object pointing to it and to its parent, then moves the current branch ref. `git push` sends missing objects to the remote and updates its ref.""",
lab=dict(goal="Make your first repository and history.", prereq=["Git installed"],
steps=[("git init lab && cd lab && echo hi > a.txt && git add a.txt && git commit -m 'first'", "Creates repo and first commit."),
("echo more >> a.txt && git diff && git add -A && git commit -m 'update'", "See the diff, then commit."),
("git log --oneline && git show HEAD", "Inspect history."),
("git restore --source=HEAD~1 a.txt && git status", "Restore an older version of a file.")]),
commands=[("git status -sb", "Shows changed, staged and untracked files with branch info.", "`-s` short, `-b` branch.", "## main...origin/main", "Ignoring the message about being behind.", "Unexpected files: check .gitignore.")],
mnemonics=[("Areas", "W-S-L-R")], hinglish="**add** se staging, **commit** se snapshot, **push** se remote. Har commit ka message clear likho.",
practices={"Development": ["Conventional Commit messages; small commits."]}, mistakes={"Beginner mistakes": ["`git add .` without reviewing `git status`."]},
qa_extra=[("Intermediate", "What is in the .git folder?", "Objects, refs, HEAD, config, hooks, index: the entire repository database.", "Internals.", "Copying .git copies history.")]),

"branching-merging": dict(
define=dict(simple="Branches let you work separately, merging combines the work.",
technical="A branch is a ref to a commit; merge creates a commit with two parents (or fast-forwards); rebase replays commits onto a new base.",
why="Parallel work without breaking main.", without="Everyone editing one line of history.", use="Every feature/fix.", avoid="Rebase on shared branches.", analogy="Parallel roads that later merge."),
internals="""Merge finds the common ancestor of both tips and performs a three-way merge; conflicts occur where both sides changed the same lines. Rebase temporarily removes your commits, moves the base to the target tip and re-applies each, which can conflict per commit.""",
lab=dict(goal="Create and resolve a conflict.", prereq=["Git"],
steps=[("git init c && cd c && echo one > f && git add f && git commit -m base && git switch -c a && echo A > f && git commit -am a && git switch main && echo B > f && git commit -am b", "Two branches change the same line."),
("git merge a", "CONFLICT reported."),
("Edit f to the desired text, then: git add f && git commit", "Conflict resolved and merged.")]),
compare=[("Ways to integrate", ["Method", "History", "Use"], [["merge", "Keeps branches", "Default, shared branches"], ["squash merge", "One commit", "Clean main"], ["rebase", "Linear", "Local branches"]])],
mnemonics=[("Golden rule", "Do not rebase what you have pushed and others use")], hinglish="Conflict ka matlab **dono ne same line badli**. File edit karo, `git add`, phir commit. **Shared branch par rebase nahi.**",
practices={"Development": ["Rebase your feature branch on main before PR; merge into main via PR."]}, mistakes={"Developer mistakes": ["Rebasing shared branches.", "Resolving conflicts without running tests."]},
qa_extra=[("Scenario-Based", "You rebased and now the push is rejected.", "History was rewritten; on your own feature branch use `git push --force-with-lease` (never on shared branches).", "Safe force push.", "`--force-with-lease` protects against overwriting others' work.")]),

"branching-strategies": dict(
define=dict(simple="A team agreement on how branches are named, used and merged.",
technical="Strategies such as trunk-based, GitHub Flow and GitFlow define long-lived vs short-lived branches, release/hotfix paths and PR rules.",
why="Predictable releases and fewer conflicts.", without="Chaos and long-lived diverging branches.", use="Every team.", avoid="GitFlow for continuous deployment.", analogy="Traffic rules for a busy road."),
internals="""In trunk-based development branches live hours/days, are merged via PR after CI passes, and unfinished work is hidden behind feature flags. In GitFlow, `develop` integrates features, `release/*` stabilises, `hotfix/*` patches production and both merge back to main.""",
lab=dict(goal="Set up branch protection and PR flow on GitHub.", prereq=["GitHub repo"],
steps=[("Settings > Branches > Add rule for main", "Require pull request reviews, require status checks, block force pushes."),
("git switch -c feature/x && git commit --allow-empty -m 'test' && git push -u origin feature/x", "Open a PR."),
("Merge after checks pass", "Direct push to main is now blocked.")]),
mnemonics=[("Trunk-based", "Short branches, small PRs, feature flags")], hinglish="**CI/CD ke liye trunk-based best hai:** chhoti branches, jaldi merge, feature flags.",
practices={"Production": ["Protected main; required checks; CODEOWNERS."]}, mistakes={"DevOps mistakes": ["Long-lived feature branches."]},
qa_extra=[("Scenario-Based", "Choose a strategy for a SaaS with daily deployments.", "Trunk-based with feature flags, short-lived branches, automated tests and continuous deployment.", "Fit-for-purpose.", "Daily deploys.")]),

"git-hooks-security": dict(
define=dict(simple="Hooks run scripts automatically at Git events; security tools stop secrets from being committed.",
technical="Client hooks (`pre-commit`, `commit-msg`, `pre-push`) run locally; server-side hooks/branch rules run on the remote; scanners like gitleaks analyse commits and history.",
why="Catch problems before they enter history.", without="Leaked secrets, broken commits.", use="All repos.", avoid="Relying only on local hooks (they can be bypassed); enforce in CI too.", analogy="Airport security before boarding."),
internals="""On `git commit`, Git executes `.git/hooks/pre-commit`; a non-zero exit aborts the commit. Frameworks like `pre-commit` manage hooks from a versioned config file. CI re-runs the same checks so bypassing locally does not help.""",
lab=dict(goal="Block secrets before commit.", prereq=["Python pip", "Git repo"],
steps=[("pip install pre-commit && printf 'repos:\\n  - repo: https://github.com/gitleaks/gitleaks\\n    rev: v8.18.4\\n    hooks: [{ id: gitleaks }]\\n' > .pre-commit-config.yaml && pre-commit install", "Installs the hook (pin `rev` to a current release)."),
("echo 'AWS_SECRET_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE1234567890abcdefgh12' > t.txt && git add t.txt && git commit -m t", "The commit should be blocked by the scanner (pattern-dependent)."),
("git rm --cached t.txt && rm t.txt", "Clean up.")]),
mnemonics=[("Secrets", "Rotate first, clean later")], hinglish="Secret leak ho jaye to **pehle rotate karo**, phir history clean karo. Sirf file delete karna kaafi nahi, history mein rehta hai.",
practices={"Security": ["Pre-commit + CI scan + GitHub push protection; use secret managers; scoped short-lived tokens."]}, mistakes={"Security mistakes": ["`--no-verify` habitually.", "Only deleting the file."]},
qa_extra=[("Advanced", "Why isn't a local pre-commit hook enough?", "Hooks are client-side and optional; enforce the same checks in CI and with server-side push protection.", "Defence in depth.", "Developer skipped hook.")])
})
