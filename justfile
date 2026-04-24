# Add a repo to the contributed-project candidate list and refresh README.md.
add-contributed-repo repo:
    @python scripts/add_contributed_repo.py "{{repo}}"
    @python scripts/update_contributed_projects.py
