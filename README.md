# kitty-cat-count-count

This script will scan a given public GitHib repo (or repos), looking at open PRs and/or issues
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

And you can have multiple repos in the `<GH owner/org>` object, or multple `<GH owner/org>`
objects in the overall object.  The `true` and `false` denote if the particular item (e.g. "PRs" or "Issues")
should be scanned for reaction counts (true) or not scanned (false).

Once a scan has completed, the result will be saved in a `.out` file whose filename will be displayed
to the user.

NOTE: this script uses a [GitHub OAuth token](https://github.com/blog/1509-personal-api-tokens) in order to get 
around the [60-API-queries-per-hour limit](https://developer.github.com/v3/#rate-limiting) that unauthenticated API queries are held to by GitHub
(queries using an OAuth token are allowed up to 5000 API queries per hour!).
