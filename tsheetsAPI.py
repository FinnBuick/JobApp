import requests, json

access_token = 'S.4__9bcc94de60021a9ea6595480dfda2deae73c2027'

## Returns a dict mapping ClientNames in tsheets to respective tsheets jobcode ids
def get_jobcode_ids():
    parentId = {}
    morePages = True
    pageNo = 0
    while morePages:

        r = requests.get('https://rest.tsheets.com/api/v1/jobcodes?parent_ids=0&page=' + str(pageNo),
                         headers={'Authorization': 'Bearer ' + access_token})

        data = json.loads(r.text)['results']
        morePages = json.loads(r.text)['more']

        for id in data['jobcodes']:
            parentId[data['jobcodes'][id]['name']] = data['jobcodes'][id]['id'] ## Populating dict with {ClientName, jobcode_ids}

        pageNo += 1

    return parentId

## Post a new job to tsheets
def post_new_job(jobid, jobname, clientname):
    parentIds = get_jobcode_ids()

    parent = parentIds[clientname]

    data = {
        "data":
            [
                {
                    "parent_id": parent,
                    "name": jobid + " " + jobname,
                }
            ]
    }

    r = requests.post('https://rest.tsheets.com/api/v1/jobcodes',
                      headers={'Authorization': 'Bearer ' + access_token}, data=json.dumps(data))
    return r.status_code