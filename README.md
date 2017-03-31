# meetup_api_snippets

Getting list of my Meetups and filtering out relevant ones (to broadcast a new event in):

If you don't have Python installed: https://wiki.python.org/moin/BeginnersGuide/Download

usage:

1. Go to https://secure.meetup.com/meetup_api/key/ and get you API key.
2. run `python src/find_potential_meetup_groups.py --api_key <API KEY> --contributor_name <YOUR USER ID ETC> --dont_list_member_ids`
3. It will create a new file called "meetups_<contributor_name>.txt".
