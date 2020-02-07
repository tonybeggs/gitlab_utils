#!/usr/bin/env python
"""
Give groups access to a given set of Gitlab projects using Gitlab Python API.
###### WARNING - THIS IS A VERY POWERFUL BIT OF SCRIPT. DO NOT LIGHTLY TRANSFER
###### GITLAB PROJECTS AROUND AS YOU MAY BREAK THINGS IN VARIOUS TERRIBLE WAYS.
"""

import gitlab

# Private token authentication. Ensure your token file is ignored by git at all times.
with open('token.txt') as token_file:
    PRIVATE_TOKEN = token_file.read()

GITLAB_ORG = 'https://somecompany.gitlab.com'

gl = gitlab.Gitlab(GITLAB_ORG, private_token=PRIVATE_TOKEN)
gl.auth()

PROJECT_IDS = [
    54321,
]

GROUP_ID = 5229


def get_project_names_and_ids(project_ids):
    '''Helper function to identify project names in a Gitlab organisation using project IDs.

    Args:
        project_ids (list): List of integer project IDs to find project names for.

    Returns:
        project_names (list): List of found project names for input project IDs.
    '''

    projects = [gl.projects.get(p_id) for p_id in project_ids]
    project_names = [[p.id, p.name] for p in projects]
    project_names.sort(key=lambda x: x[1])

    return project_names


def transfer_project_to_group_namespace(group_id, project_id):
    '''Transfer a GitLab project to a group. This can be used in place of manually transferring projects to a group
    for multiple project transfers.

    Args:
        group_id (int): GitLab group ID to transfer project ownership to.
        project_id (int): GitLab project ID transfer ownership of.
    '''

    # Get specific project object from global GitLab object.
    project = gl.projects.get(project_id)

    # Transfer project to specified group.
    project.transfer_project(to_namespace=group_id)


def main():
    # Loop over project IDs and transfer each project to specified group.
    for project_id in PROJECT_IDS:
        transfer_project_to_group_namespace(
            group_id=GROUP_ID,
            project_id=project_id
        )


if __name__ == "__main__":
    main()

