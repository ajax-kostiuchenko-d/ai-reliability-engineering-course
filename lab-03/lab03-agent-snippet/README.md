# lab03-agent-snippet

Reference `app/agent.py` only — **not** a full agents-cli project.

Create the real project:

```bash
cd lab-03
agents-cli create lab03-agent --prototype --yes
cp lab03-agent-snippet/app/agent.py lab03-agent/app/agent.py
cd lab03-agent && agents-cli install
```

Add `lab03-agent/` to gitignore locally if you generate it inside the course repo.
