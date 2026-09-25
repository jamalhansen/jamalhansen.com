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

Posts are written in the BrainSync vault (`blog/series/<series>/posts/...`) and published with
[obsidian-hugo-bridge](https://github.com/jamalhansen/obsidian-hugo-bridge):

```bash
make preview POST=blog/series/<series>/posts/<post>/<note>.md   # draft render in the real theme
make publish POST=blog/series/<series>/posts/<post>/<note>.md   # write the page bundle
make find FIND=_finds/<find>.md
make drift                                                      # posts whose vault note and live copy disagree
```

The note's `status` decides visibility: `published` goes live, anything else is a draft. A post
already on the site is updated in place; if the live copy was edited after publishing, `make publish`
stops and shows the diff (backport the edit to the note, or `ARGS=--overwrite`). After a live
publish the note gets `published_date` and `canonical_url` filled in. Then commit and push to deploy.

## Deployment

Pushes to `main` trigger an automatic build on AWS Amplify. A weekly scheduled rebuild also runs every Monday via GitHub Actions.
