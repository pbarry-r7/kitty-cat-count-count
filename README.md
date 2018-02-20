# kitty-cat-count-count

This script will scan a given GitHub repo (or repos), looking at open PRs and/or issues
and counting any [reactions](https://developer.github.com/v3/reactions/) that GitHub users have
left on each PR/issue "description".  Public and private GitHub repos are supported.

## Config

This script uses a simple, JSON-based config file of the following format:

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

You can have multiple repos in the `<GH owner/org>` object and/or multple `<GH owner/org>`
objects in the overall object.  The `true` and `false` denote if the particular item (e.g. "PRs" or "Issues")
should be scanned for reaction counts (true) or not scanned (false).

Once a scan has completed, the result will be saved in a `.out` file whose filename will be displayed
to the user.

## OAuth Token

This script uses a [GitHub OAuth token](https://github.com/blog/1509-personal-api-tokens) in order to get 
around the [60-API-queries-per-hour limit](https://developer.github.com/v3/#rate-limiting) that unauthenticated
API queries are held to by GitHub (queries using an OAuth token are allowed up to 5000 API queries per hour!).

Once you have an OAuth token, create a new environment variable named KCCC_OAUTH_TOKEN and set its value to the
token.  The kitty-ccc.py script will look for the OAuth token to be used in this env var.

Using an OAuth Token also allows this script to work with private GitHub repos.

## Example Run

```
$ export KCCC_OAUTH_TOKEN=<my OAuth token value>
$ ./kitty-ccc.py
Located GitHub repo 'rapid7/metasploit-framework':
 - Counting PR reactions................................. Done.
 - Saving as 'rapid7_metasploit-framework_prs.out'... Done.
 - Counting Issue reactions................................. Done.
 - Saving as 'rapid7_metasploit-framework_issues.out'... Done.
```
