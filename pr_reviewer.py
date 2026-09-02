name: PR Doorbell Review

# Concept 7: event-driven. No cron, no manual trigger — this job only
# runs because GitHub fired a pull_request event. "synchronize" means
# every new push to the PR re-fires this workflow automatically.
on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  pull-requests: write
  contents: read

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - name: Check out the PR branch
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Run the automated review
        id: review
        run: |
          git fetch origin ${{ github.event.pull_request.base.ref }} --depth=50
          python pr_reviewer.py origin/${{ github.event.pull_request.base.ref }} HEAD > review_output.txt
          cat review_output.txt

      - name: Post review as a PR comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const body = fs.readFileSync('review_output.txt', 'utf8');
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: body
            });
