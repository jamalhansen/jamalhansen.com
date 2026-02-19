# jamalhansen.com

Personal technical blog built with [Hugo](https://gohugo.io/) and the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme, deployed on AWS Amplify.

## Prerequisites

- [Hugo Extended](https://gohugo.io/installation/) v0.146.7+
- [Go](https://go.dev/dl/) 1.23+

## Running locally

```bash
hugo server
```

The site will be available at `http://localhost:1313`.

## Writing posts

Posts are written in Obsidian and converted to Hugo page bundles using the conversion script. See [scripts/README.md](scripts/README.md) for the full workflow.

```bash
./scripts/new-post jamalhansen.com/_drafts/my-post.md my-post-slug
```

Set `draft: false` in the frontmatter when ready to publish, then commit and push to trigger a deploy.

## Deployment

Pushes to `main` trigger an automatic build on AWS Amplify. A weekly scheduled rebuild also runs every Monday via GitHub Actions.
