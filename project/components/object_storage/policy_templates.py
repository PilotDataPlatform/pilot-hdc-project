# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

def get_admin_policy(project_code: str) -> str:
    """Create policy template for admin user."""
    template = f'''
    {{
        "Version": "2012-10-17",
        "Statement": [
            {{
            "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
            "Effect": "Allow",
            "Resource": ["arn:aws:s3:::gr-{project_code}", "arn:aws:s3:::core-{project_code}"]
            }},
            {{
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Effect": "Allow",
            "Resource": ["arn:aws:s3:::gr-{project_code}/*", "arn:aws:s3:::core-{project_code}/*"]
            }}
        ]
    }}
    '''
    return template


def get_collaborator_policy(project_code: str) -> str:
    """Create policy template for collaborator user."""
    template = f'''
    {{
        "Version": "2012-10-17",
        "Statement": [
            {{
            "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
            "Effect": "Allow",
            "Resource": ["arn:aws:s3:::gr-{project_code}", "arn:aws:s3:::core-{project_code}"]
            }},
            {{
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Effect": "Allow",
            "Resource": ["arn:aws:s3:::gr-{project_code}/${{jwt:preferred_username}}/*",
             "arn:aws:s3:::core-{project_code}/*"]
            }}
        ]
    }}
    '''
    return template


def get_contributor_policy(project_code: str) -> str:
    """Create policy template for contributor user."""
    template = f'''
    {{
        "Version": "2012-10-17",
        "Statement": [
            {{
            "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
            "Effect": "Allow",
            "Resource": ["arn:aws:s3:::gr-{project_code}", "arn:aws:s3:::core-{project_code}"]
            }},
            {{
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Effect": "Allow",
            "Resource": ["arn:aws:s3:::gr-{project_code}/${{jwt:preferred_username}}/*",
             "arn:aws:s3:::core-{project_code}/${{jwt:preferred_username}}/*"]
            }}
        ]
    }}
    '''
    return template


TEMPLATES_LIBRARY = {
    'admin': get_admin_policy,
    'contributor': get_contributor_policy,
    'collaborator': get_collaborator_policy,
}
