import argparse
import sys

import dfareporting_utils
from oauth2client import client

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument(
    'profile_id', type=int,
    help='The ID of the profile to look up sites for')


def main(argv):
  # Retrieve command line arguments.
  flags = dfareporting_utils.get_arguments(argv, __doc__, parents=[argparser])

  # Authenticate and construct service.
  service = dfareporting_utils.setup(flags)

  profile_id = flags.profile_id

  try:
    # Construct the request.
    request = service.sites().list(profileId=profile_id)

    while True:
      # Execute request and print response.
      response = request.execute()

      for site in response['sites']:
        print ('Found site with ID %s and key name "%s".'
               % (site['id'], site['keyName']))

      if response['sites'] and response['nextPageToken']:
        request = service.sites().list_next(request, response)
      else:
        break

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')


if __name__ == '__main__':
  main(sys.argv)