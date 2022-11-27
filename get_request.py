#!/usr/bin/python

import urllib3
import json
import os


def get_repo_list(auth, org):

    http = urllib3.PoolManager()
    # set args for http request
    all_repo_list = []
    page = 1
    url = f"https://api.github.com/orgs/{org}/repos"
    req_fields = {"per_page": 100, "page": page}
    req_headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": auth,
    }
    resp = http.request("GET", url, fields=req_fields, headers=req_headers)
    json_resp = json.loads(resp.data.decode("utf-8"))
    all_repo_list.append(json_resp)

    if len(json_resp) == 100:
        while len(json_resp) == 100:
            page += 1
            req_fields = {"per_page": 100, "page": page}
            resp = http.request(
                "GET", url, fields=req_fields, headers=req_headers
            )
            json_resp = json.loads(resp.data.decode("utf-8"))
            all_repo_list.append(json_resp)

    # flatten the list of json lists to a single list
    final_list = sum(all_repo_list, [])

    # create separte lists for archived and non-archived repos
    archived = []
    non_archived = []
    for item in final_list:
        if item["archived"] is False:
            non_archived.append(item["name"])
        if item["archived"] is True:
            archived.append(item["name"])

    return non_archived, archived


def get_dependabot_alerts(auth, org):

    http = urllib3.PoolManager()
    # set args for http request
    page = 1
    url = f"https://api.github.com/repos/{org}/optimus/dependabot/alerts"
    req_fields = {"first": 100}
    req_headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": auth,
    }
    resp = http.request("GET", url, fields=req_fields, headers=req_headers)
    json_resp = json.loads(resp.data.decode("utf-8"))

    print(json_resp[0])

    print()
    print(len(json_resp))


def main():

    try:
        apikey = os.environ["GH_API_KEY"]
        auth = "Bearer " + apikey
    except KeyError:
        print("GH_API_KEY environment variable not set")
        print("Please set the Github API via environment variable.")
        print("Eg. export GH_API_KEY=ghp_XXXXXXXXXXXXXXXXXXXXX")
        quit()

    # non_archived, archived = get_repo_list(auth, "procurify")

    # print(non_archived)
    # print()
    # print(archived)

    get_dependabot_alerts(auth, "procurify")


if __name__ == "__main__":
    main()
