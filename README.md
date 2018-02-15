# kitty-cat-count-count

This program will scan a given public GitHib repo (or repos), looking at open PRs and/or issues
and counting any [reactions](https://developer.github.com/v3/reactions/) that GitHub users have
left on the PR/issue "description" itself.  It uses a simple, JSON-based config file, of the following
format:

```
{
	"<GH owner/org>": {
		"<GH repo name>" :{
			"PRs": <true|false>,
			"Issues": <true|false>
		}
	}
}
```

And you can have multiple repos in the above `<GH owner/org>` object, or multple `<GH owner/org>`
objects in the overall object.  The `true` and `false` denote if the particular item (e.g. "PRs" or "Issues")
should be scanned for reaction counts.

Once a scan has completed, the result will be saved in a `.out` file whose filename will be displayed
to the user.
