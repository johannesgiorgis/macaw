import asyncio
import concurrent.futures
import logging
import math
import meetup.api
import os
import requests
import time

from queue import Queue

API_KEY = None
PAGE_SIZE = 200
GROUP_ID = None
MAX_WORKERS = 10
q = Queue()


async def main():
    """Does the work of making parallel requests from meetup"""
    def make_request(uri, payload):
        """Attaches a payload to a request"""
        logger.debug("Requesting")
        start = time.time()
        response = requests.get(uri, params=payload)
        end = time.time()
        logger.info(f"Elapsed time: {end - start} seconds.")
        return response

    def get_page_total(url):
        """get total number of pages"""
        group_info = client.GetGroup({'urlname': url})
        keys = list(group_info.__dict__.keys())

        # Display group information
        # for key in keys:
        #    print(f"Key: {key}, Value: {group_info.__dict__[key]}")

        total_pages = math.ceil(group_info.members / float(PAGE_SIZE))
        logger.info(f"There are {group_info.members} members in this group and {total_pages} total pages.")
        return total_pages

    page_total = get_page_total('svaibd')  # This is the Sunnyvale AI Frontiers forum at https://www.meetup.com/svaibd/
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        my_loop = asyncio.get_event_loop()
        payloads = [
            {
                    "offset": page_number,
                    "format": 'json',
                    "group_id": '15746682',
                    "page": PAGE_SIZE,
                    "key": API_KEY,
                    "order": 'joined'
            } for page_number in range(page_total)]
        futures = [
            my_loop.run_in_executor(
                executor,
                make_request,
                'https://api.meetup.com/2/members',
                payload
            )
            for payload in payloads
        ]
        for response in await asyncio.gather(*futures):
            logger.info("Processing response")
            results = response.json().get("results", {})
            for r in results:
                q.put(r)


if __name__ == "__main__":
    """Main program"""
    logging.basicConfig(format='%(levelname)s %(threadName)10s %(asctime)s %(message)s')
    logger = logging.getLogger('meetup_api_demo')
    logger.setLevel(logging.DEBUG)

    # Get the API key from the operating system's environment
    if 'MEETUP_API_KEY' not in os.environ:
        raise AssertionError('MEETUP_API_KEY not found in environment, aborting execution.')

    API_KEY = os.environ['MEETUP_API_KEY']
    logger.warning(f"API_KEY loaded from environment")

    client = meetup.api.Client(API_KEY)

    # Get all of the results asynchronously
    loop = asyncio.get_event_loop()
    start = time.time()
    loop.run_until_complete(main())
    end = time.time()

    c = 0
    while not q.empty():
        logger.info(f"c: {c}, {q.get()}")
        c += 1
    logger.warning(f"Total Time taken: {end - start:3.2f} seconds")

