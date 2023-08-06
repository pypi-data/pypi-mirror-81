# B.JiraFilter

A CLI based scripts library to interact with JIRA API. Not all actions are 
implemented in JIRA UI, therefore, we have created this library with custom
logic and custom functionality that can be used by anyone.

### Description

Sometimes it is more convenient and straight-forward to do stuff via CLI
rather than via UI. Also, the JIRA UI can not support every single functionality
possible, therefore, for custom logic and custom commands we have developed
this CLI based library. Scroll down to see what are the available custom
logic commands.

### Remarks

[Biomapas](https://biomapas.com) aims to modernise life-science 
industry by sharing its IT knowledge with other companies and 
the community. This is an open source library intended to be used 
by anyone. Improvements and pull requests are welcome.

### Related technology

- Python 3
- JIRA
- JIRA Python SDK

### Assumptions

The project assumes the following:

- You have basic knowledge in JIRA software.

### Useful sources

- Since this library uses JIRA SDK, it is a good idea to familiarize
yourself with it:<br>
https://github.com/pycontribs/jira.

### Install

The project is built and uploaded to PyPi. Install it by using pip.

```bash
pip install b-jira-filter
```

Or directly install it through source.

```bash
pip install .
```

### Usage & Examples

This section shows what are the available commands and how to use them.

#### Credentials management

The library has a flexible credentials management.

You can pass credentials to the constructor:
```python
from b_jira_filter.objects.credentials import Credentials

Credentials(
    username='Username',
    password='Password',
    server='Server'
)
```

Or you can set the OS environment:
```python
from b_jira_filter.objects.credentials import Credentials

Credentials()
```
```
export/set JIRA_USERNAME=Username
export/set JIRA_PASSWORD=Password
export/set JIRA_SERVER=Server
```

Or you can enter these value manually in a prompt:
```python
from b_jira_filter.objects.credentials import Credentials

Credentials()
```
```
(venv) > jira.sprints.storypoints
Username: ...
Password: ...
Server: ...
```

#### Commands

The library exposes CLI commands:

---

##### jira

Use this command to see what are available different commands and sections.
```
(venv) > jira

Available sections:
- sprints
```

---

##### jira.sprints

Use this command to see what are available different commands and sections in sprints section.
```
(venv) > jira

Available commands:
- storypoints
```

---

##### jira.sprints.storypoints

Use this command to calculate story points for each assignee in any sprint. For example:
```
(venv) > jira.sprints.storypoints

Select a board (1-2):

1. TEST1 board
2. TEST2 board

Board number[Default 1]:

> ENTER

Select a sprint (1-2):

1. TEST Sprint 1
2. TEST Sprint 2

Sprint number[Default 2]:

> ENTER

----------------------------------------------------------------

Dev 1   : Total:  68 | Completed:  21( 30.9%) | Not completed:  47( 69.1%).
Dev 2   : Total:  61 | Completed:  21( 34.4%) | Not completed:  40( 65.6%).

----------------------------------------------------------------
```

---

#### Testing

Currently this package has no tests.

#### Contribution

Found a bug? Want to add or suggest a new feature?<br>
Contributions of any kind are gladly welcome. You may contact us 
directly, create a pull-request or an issue in github platform.
Lets modernize the world together.
