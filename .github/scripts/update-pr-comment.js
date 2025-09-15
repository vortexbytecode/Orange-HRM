const core = require("@actions/core");
const github = require("@actions/github");

async function run() {
  try {
    const token = process.env.INPUT_TOKEN;
    const section = process.env.INPUT_SECTION;
    const results = process.env.INPUT_RESULTS;
    const prNumber = process.env.INPUT_PR_NUMBER;

    if (!token || !section || !results || !prNumber) {
      throw new Error("Missing required inputs (token, section, results, prNumber)");
    }

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;

    // Fetch existing comments
    const { data: comments } = await octokit.rest.issues.listComments({
      owner,
      repo,
      issue_number: prNumber,
    });

    const marker = `<!-- ci-comment-${section} -->`;
    const newBody = `${marker}\n### ${section}\n${results}`;

    const existing = comments.find(c => c.body && c.body.includes(marker));

    if (existing) {
      // Update
      await octokit.rest.issues.updateComment({
        owner,
        repo,
        comment_id: existing.id,
        body: newBody,
      });
    } else {
      // Create
      await octokit.rest.issues.createComment({
        owner,
        repo,
        issue_number: prNumber,
        body: newBody,
      });
    }

    console.log(`✅ Updated PR comment for section: ${section}`);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
