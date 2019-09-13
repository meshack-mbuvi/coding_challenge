import requests
import json
from flask_restplus import Resource, Namespace
from flask import request, jsonify
from requests.exceptions import ConnectionError

GITHUB_URL = "https://api.github.com/users"
BIT_BUCKET_URL = "https://api.bitbucket.org/2.0/users"

api = Namespace('Ride offers', Description='Operations on Rides')


class Profile(Resource):

    def get_repo_languages(self, repositories):
        """
        Aggregates programing languages used in various repositories

        Parameters:
          repositories(list): A list of dict object containing repositories for
            a given user.
        """

        repo_languages = set()
        for index in range(len(repositories)):
            language = repositories[index]["language"]
            if(language):
                repo_languages.add(language)

        return list(repo_languages)

    def aggregate_data(self, repositories):
        """
        Format profile data for a given user

        Parameters:
          repositories(list): A list containing a repository object.

        Returns:
          profile(dict): An object containing user information.

        """

        forked_repositories = [
            repo for repo in repositories if ("fork"in repo and repo['fork']) or "parent" in repo]

        original_repositories = [
            repo for repo in repositories if not ("fork"in repo and repo['fork']) or "parent" not in repo]

        languages = self.get_repo_languages(repositories)

        profile = {
            "total": len(repositories),
            "forked repositories": len(forked_repositories),
            "original repositories": len(original_repositories),
            "languages used": languages,
        }

        return profile

    def get(self):
        """
        Get profile for a given user, organization or team

        parameters:
          username (str): A name of a given user, organization or team.

        returns:
          A dictionary with the data for a given username.

        """
        args = request.args
        if "username" not in args or not args['username'].strip():
            return {
                "message": "Username is required and must not be empty"
            }, 400

        username = request.args['username']

        try:
            github_response = requests.get(
                '{}/{}/repos' .format(GITHUB_URL, username))

            bit_bucket_response = requests.get(
                '{}/{}/repositories' .format(BIT_BUCKET_URL, username))

            if(github_response
                .status_code == 404 and bit_bucket_response
                    .status_code == 404):
                return {"message": "No user found with given username"}, 404

            bit_bucket_repositories = bit_bucket_response.json()["values"]
            github_repositories = github_response.json()

            all_repositories = github_repositories + bit_bucket_repositories

            profile = self.aggregate_data(all_repositories)

            # Retrieve user followers
            followers = self.get_followers_count(username)
            profile["followers"] = len(followers)

            return jsonify(profile)
        except Exception as e:
            return jsonify({"message": "There is not network connetion"})

    def get_followers_count(self, username=''):
        """
        Retrieves user github followers

        Parameters:
          username (str): name of the user, organization or team

        Returns:
          followers(list): A list dict objects containing details of each
              follower
        """
        followers = requests.get(
            '{}/{}/followers'.format(GITHUB_URL, username)).json()

        return followers


api.add_resource(Profile, '/profile')
