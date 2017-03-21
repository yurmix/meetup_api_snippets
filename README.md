# meetup_api_snippets

Getting list of my Meetups and filtering out relevant ones (to broadcast a new event in):

If you don't have Python installed: https://wiki.python.org/moin/BeginnersGuide/Download

usage:

1. Go to https://secure.meetup.com/meetup_api/key/ and get you API key.
2. run `python src/find_potential_meetup_groups.py --api_key <API KEY> --contributor_name <YOUR USER ID ETC>`
3. It will create a new file called "meetups_<contributor_name>.txt".
4. If you prefer to opt-out on members list, add `--dont_list_member_ids`.

issues:

1. If API gets throttled, we will do retries. i.e.:
```reading...
so far 1800 records.
reading...
Error: No JSON object could be decoded. Retrying in 1 seconds...
Error: No JSON object could be decoded. Retrying in 2 seconds...
Error: No JSON object could be decoded. Retrying in 4 seconds...
Error: No JSON object could be decoded. Retrying in 8 seconds...
so far 2000 records.```

