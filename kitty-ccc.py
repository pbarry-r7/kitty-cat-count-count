#!/usr/bin/env python

# Module depdencies should be listed here...
import json
import urllib2
from sys import stdout,exit

# Consts...
OAUTH_TOKEN = "<put token here, see https://github.com/blog/1509-personal-api-tokens on how to create a personal token>"
REQUEST_HEADERS = {
	"Authorization": "token " + OAUTH_TOKEN,
	"Accept": "application/vnd.github.squirrel-girl-preview" # see https://developer.github.com/changes/2016-05-12-reactions-api-preview/
}
CONFIG_FILENAME = "config.json"

# Functions...
def api_repo_endpoint(owner, repo):
	return "https://api.github.com/repos/" + owner + "/" + repo

def api_repo_prs_endpoint(owner, repo):
	return api_repo_endpoint(owner, repo) + "/pulls"

def api_repo_issues_endpoint(owner, repo):
	return api_repo_endpoint(owner, repo) + "/issues"

def api_repo_reactions_endpoint(owner, repo, issue_num):
	return api_repo_endpoint(owner, repo) + "/issues/" + str(issue_num) + "/reactions"

def gh_request(url, headers):
	if headers is not None:
		return urllib2.Request(url, headers = headers)
	else:
		return urllib2.Request(url)

def verify_repo(owner, repo):
	try:
		repo = urllib2.urlopen(gh_request(api_repo_endpoint(owner, repo), REQUEST_HEADERS))
		if repo.getcode() != 200:
			return None
		return repo.read()	
	except:
		return None

def tally_repo_pr_reactions(owner, repo):
	try:
		prs = urllib2.urlopen(gh_request(api_repo_prs_endpoint(owner, repo), REQUEST_HEADERS))
		if prs.getcode() != 200:
			return {}
		full_tally = {}
		prs_json = json.loads(prs.read())
		for pr in prs_json:
			pr_tally = {}
			stdout.write(".")
			stdout.flush()
			reactions = urllib2.urlopen(gh_request(api_repo_reactions_endpoint(owner, repo, pr["number"]), REQUEST_HEADERS))
			if reactions.getcode() != 200:
                        	return {}
			reactions_json = json.loads(reactions.read())
			for reaction in reactions_json:
				if reaction["content"] in pr_tally:
					pr_tally[reaction["content"]] += 1
				else:
					pr_tally[reaction["content"]] = 1
			full_tally[str(pr["number"])] = pr_tally
		print " Done."
		return full_tally
	except:
		return {}

def tally_repo_issue_reactions(owner, repo):
	# Same mechanism as used for tallying PR reactions...
	return tally_repo_pr_reactions(owner, repo)

def save_results(owner, repo, item_type, data):
	filename = owner + "_" + repo + "_" + item_type + ".out"
	try:
		fd = open(filename, "w")
		stdout.write(" - Saving as '" + filename + "'...")
		json.dump(data, fd)
		print " Done."
	except:
		print "Couldn't open/write output file '" + filename + "'"
		raise
	
#
# MAIN
#

# Open the config...
try:
	fd = open(CONFIG_FILENAME, "r")
except:
	print "Couldn't open config file '" + CONFIG_FILENAME + "'"
	raise

# Now load+parse the config!
try:
	config_contents = json.load(fd)
except:
	print "Error parsing the JSON in the config file '" + CONFIG_FILENAME + "'"
	raise

# Iterate all the repos in the config, counting the PRs and/or issues...
try:
	for owner, owner_value in list(config_contents.items()):
		for repo, config in list(owner_value.items()):
			prs = config["PRs"]
			issues = config['Issues']
			repo_contents = verify_repo(owner, repo)
			if repo_contents is None:
				print "Repo '" + repo + "' failed to verify as a valid, accessible repo.  Skipping..."
			print "Located GitHub repo '" + repo + "':"
			if prs:
				stdout.write(" - Counting PR reactions...")
				repo_pr_reaction_counts = tally_repo_pr_reactions(owner, repo)
				save_results(owner, repo, "prs", repo_pr_reaction_counts)
			if issues:
				stdout.write(" - Counting Issue reactions...")
				repo_issue_reaction_counts = tally_repo_issue_reactions(owner, repo)
				save_results(owner, repo, "issues", repo_issue_reaction_counts)
except:
	exit(1)

exit(0)
