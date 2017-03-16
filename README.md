# meetup_api_snippetsdd

Getting list of my Meetups and filtering out relevant ones (to broadcast a new event in):

usage:

1. Go to https://secure.meetup.com/meetup_api/key/ and get you API key.
2. run `python src/find_potential_meetup_groups.py --api_key <API KEY> --contributor_name <YOUR USER ID ETC>`
3. It will create a new file called "meetups_<contributor_name>.txt".
4. If you prefer to opt-out on members list, add --dont_list_member_ids.`
