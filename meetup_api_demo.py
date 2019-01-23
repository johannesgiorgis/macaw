import meetup.api
import os
import logging
import math

PAGE_SIZE = 200
logging.getLogger("meetup.api").setLevel(logging.WARNING)

if 'MEETUP_API_KEY' not in os.environ:
    raise AssertionError('MEETUP_API_KEY not found in environment, aborting execution.')

API_KEY = os.environ['MEETUP_API_KEY']
print(f"The API_KEY in the environment is {API_KEY}")

client = meetup.api.Client(API_KEY)


def print_members_starting_with_page(page_number, step=1):
    print(f"Offset: {page_number}, Step: {step}")
    page_number = page_number
    keep_going = True
    retry_count, retry_max = 0, 3
    while keep_going and retry_count <= retry_max:
        try:
            members = client.GetMembers(
                group_id=group_info.id, order="joined", page=PAGE_SIZE, offset=page_number)
            if members.__dict__["meta"]["next"] == '':
                keep_going = False
            member_list = members.results
            for i, member in enumerate(member_list):
                print(
                    f"Member {PAGE_SIZE * page_number + i}: Name: {member.get('name',''):40}, "
                    f"Joined: {member.get('joined','')}")
            retry_count = 0
            page_number += step
        except Exception as e:
            retry_count += 1
            if retry_count == retry_max:
                print(f"Failure: {e}")


if __name__ == "__main__":
    # This is the Sunnyvale AI Frontiers forum at https://www.meetup.com/svaibd/
    url = 'svaibd'
    group_info = client.GetGroup({'urlname': 'svaibd'})
    keys = list(group_info.__dict__.keys())

    # Display group information
    #for key in keys:
    #    print(f"Key: {key}, Value: {group_info.__dict__[key]}")

    total_pages = math.ceil(group_info.members / float(PAGE_SIZE))
    print(f"There are {group_info.members} members in this group and {total_pages} total pages.")
    print(total_pages)

    #NOTE: This is a candidate for asynchronous i/o instead of a single synchronous loop

    # print the last page
    print_members_starting_with_page(total_pages - 1)


