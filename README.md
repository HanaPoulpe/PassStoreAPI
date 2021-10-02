# PassStore - AWS API

PassStore AWS API, is the AWS APIGateway implementation for PassStore. It aims to allow authenticated users to Store and Retrieve KeePass files and secrets.

It's a small project mostly implemented while [streaming](https://twitch.tv/hanapoulpe). More details on my [website](https://www.hanaburtin.net).

## Learn by doing:

I'm using this project to both learn and improve my skills, and share it what I learn to others.

This project is developed implemented using red/green process.

# PasswordFile API:

Password files are stored in S3, and can be retrieved by identified users on a group model. File are owned by a group, and users are part of the groups with 2 access level (read only, read/write).
This is aiming to allow team sharing of secrets with access granularity.

API Calls are:
* PUT api/file: Store/Create/Update a file
* GET api/file: Read a file
* DELETE api/file: Delete a file
* GET api/file_list: List user authorized files

# Secrets API:

Secrets are stored using S3, and can be retrieved by identified users on a group model. Basically almost identical to the PasswordFile API.
I might want to move to secrets manager at some point, still need to do some research on this topic

API Calls are:
* PUT api/secret: Store/Create/Update a secret
* GET api/secret: Read a secret
* DELETE api/secret: Delete a secret
* GET api/secret_list: List user authorized secrets
