const core = require("@actions/core");
const github = require("@actions/github");

async function run() {
  try {
    const token = process.env.INPUT_TOKEN;
    const section = process.env.INPUT_SECTION;
    const results = process.env.INPUT_RESULTS;
    const prNumber = parseInt(process.env.INPUT_PR_NUMBER, 10);

    if (!token || !section || !results || !prNumber) {
      core.setFailed("Missing required inputs (token, section, results, prNumber)");
      return;
    }

    const octokit = github.getOctokit(token);

    const marker = "<!-- unified-pr-comment -->";

    const newSection = `
### ${section}
${results}
`;

    // Get existing comments
    const { data: comments } = await octokit.rest.issues.listComments({
      issue_number: prNumber,
      owner: github.context.repo.owner,
      repo: github.context.repo.repo,
    });

    // Find existing unified comment
    const existing = comments.find((c) => c.body && c.body.includes(marker));

    if (existing) {
      const updatedBody = existing.body.replace(
        marker,
        `${marker}\n${newSection}`
      );
      await octokit.rest.issues.updateComment({
        comment_id: existing.id,
        owner: github.context.repo.owner,
        repo: github.context.repo.repo,
        body: updatedBody,
      });
    } else {
      const body = `${marker}\n${newSection}`;
      await octokit.rest.issues.createComment({
        issue_number: prNumber,
        owner: github.context.repo.owner,
        repo: github.context.repo.repo,
        body,
      });
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
