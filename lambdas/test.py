response = {'took': 3, 'timed_out': False, '_shards': {'total': 5, 'successful': 5, 'skipped': 0, 'failed': 0}, 'hits': {'total': {'value': 3, 'relation': 'eq'}, 'max_score': 1.0, 'hits': [{'_index': 'test', '_type': 'lambda-type', '_id': '2022-05-12 06:33:55.350112', '_score': 1.0, '_source': {'UserIdOfComment': '', 'UserNameOfComment': '', 'commentTimestamp': '2022-05-12 17:01:03.835328', 'comment': {'UserIdOfComment': '', 'UserNameOfComment': '', 'commentTimestamp': '2022-05-12 17:01:03.835328', 'comment': 'asd'}}}, {'_index': 'test', '_type': 'lambda-type', '_id': '2022-05-12 19:02:40.837034', '_score': 1.0, '_source': {'userid': '', 'userName': '', 'loggedInEmail': '', 'Thread_Title': 'asd', 'Thread_content': 'cxvc', 'timestamp': '2022-05-12 19:02:40.837034', 'comments': [], 'likes': ''}}, {'_index': 'test', '_type': 'lambda-type', '_id': '2022-05-12 06:36:14.004119', '_score': 1.0, '_source': {'userid': '', 'userName': '', 'loggedInEmail': '', 'Thread_Title': 's', 'Thread_content': 'fas', 'timestamp': '2022-05-12 06:36:14.004119', 'comments': [], 'likes': ''}}]}}

thread_list = []
for item in response['hits']['hits']:
    if item['_source'].get('userid') is None:
        continue
    
    document={
        "userid": item['_source']['userid'],
        "userName" :item['_source']['userName'],
        "loggedInEmail": item['_source']['loggedInEmail'],
        "Thread_Title": item['_source']['Thread_Title'],
        "Thread_content": item['_source']['Thread_content'],
        "timestamp": item['_source']['timestamp'],
        "comments":item['_source']['comments'],
        "likes": item['_source']['likes']
    }
    print("x=", document)
    thread_list.append(document)