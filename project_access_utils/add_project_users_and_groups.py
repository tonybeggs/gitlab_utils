#!/usr/bin/env python
"""
Give groups access to a given set of Gitlab projects using Gitlab Python API.
"""

import gitlab

# Private token authentication. Ensure your token file is ignored by git.
with open('token.txt') as token_file:
    PRIVATE_TOKEN = token_file.read()


GITLAB_ORG = 'https://somecompany.gitlab.com'

gl = gitlab.Gitlab(GITLAB_ORG, private_token=PRIVATE_TOKEN)
gl.auth()

# Set Gitlab group IDs to give access to and projects to which access should be given.
GROUP_IDS = [1234]
PROJECT_IDS = [
    56789,
    12345,
]

# Set access level to assign to selected groups over selected projects. One of:
# - gitlab.GUEST_ACCESS
# - gitlab.REPORTER_ACCESS
# - gitlab.DEVELOPER_ACCESS
# - gitlab.MAINTAINER_ACCESS
# - gitlab.OWNER_ACCESS

GITLAB_ACCESS_LEVEL = gitlab.GUEST_ACCESS


def add_groups_to_project(
    group_ids,
    project_id,
    gitlab_access_level
):
    '''Add a GitLab group to a project at a specified access level. This can be used in place of manually giving project
    access to a group/groups over multiple projects.

    Args:
        group_ids (list): GitLab group IDs for group or groups to give access to.
        project_id (int): GitLab project ID to give access to.
        gitlab_access_level (gitlab.const): Level of project access to give to group (Developer, Maintainer etc).

    '''

    # Get specific project from global GitLab object.
    project = gl.projects.get(project_id)

    # Add all required GitLab groups to specified project.
    for group_id in group_ids:
        try:
            project.share(group_id, gitlab_access_level)
            print(f'Successfully shared project ID {project_id} with group ID {group_id}.')
        except:
            print(f'Failed to share project ID {project_id} with group ID {group_id}.')

    pass

def main():
    # Loop over project IDs and group IDs and share each project as required.
    for project_id in PROJECT_IDS:
        add_groups_to_project(
            group_ids=GROUP_IDS,
            project_id=project_id,
            gitlab_access_level=GITLAB_ACCESS_LEVEL
        )


if __name__ == "__main__":
    main()
