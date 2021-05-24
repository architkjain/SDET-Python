from jira import JIRA
from jira import JIRAError
from base64 import b64encode

''' 
    Prerequisite: Install Python Jira Library (Requires Python Version : Python 3.5+)
                  Install Command : pip install jira
                  
    :param
    username    : UserName Of The Jira User
    password    : Password Of Jira User
    jira_URL    : Jira URL Of Your Organization 
    
'''

class Jira_Integration:

    # For Demo Purpose Use Your Xoriant AD credentials.

    username = ''
    password = ''
    jira_URL = 'https://jira.xoriant.com/'

    '''
    This Method Update Task Status From Open To Start Progress
   
    :param
    task_id      : ID of task which Is Suppose To Be Updated 
    project_name : NAME of the Jira Project  
    
    :return
    True         : If Task Is Updated 
    False        : If Any Failure 
    '''

    def Update_Task_Status(self, task_id, project_name):
        try:
            to_encode = '{}:{}'.format(self.username, self.password)
            encoded_auth = b64encode(bytes(to_encode, 'utf-8')).decode('utf-8')

            options = {'server': self.jira_URL,
                       'headers': {
                           'Authorization': 'Basic {}'.format(encoded_auth),
                           'Content-Type': 'application/json',
                       },
                       }
            auth_jira = JIRA(options=options)

            projects = auth_jira.projects()

            project_id = ''
            for project in projects:
                if str(project.name) == project_name:
                    project_id = project.id

            search_issue_parameter = 'project=' + project_id
            search_issues_in_project = auth_jira.search_issues(search_issue_parameter)

            for issue in search_issues_in_project:
                if str(issue.fields.issuetype) == 'Task' and issue.key == task_id:
                    auth_jira.transition_issue(issue, '11')

        except JIRAError as e:
            print("Status Code : " + str(e.status_code))
            print("Error Message : " + e.text)
            return False
        return True


'''
object_Update_Task_Status = Jira_Integration()
if object_Update_Task_Status.Update_Task_Status('AD-1', 'AX360 Demo'):
    print("Task Update Successfully")
else:
    print("Error : There Was A Failure")
'''
