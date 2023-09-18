# mkdocs-action-yml
A markdown extension for mkdocs to document action.yml files


## Reference

### Block syntax

The syntax for a `mkdocs-action-yml` block is the following:

```md
::: mkdocs-action-yml
    :path: action.yml
    :owner: organization or user
    :version: v0.0.1
```

Options:

    - `path`: [required] Path to the action.yml file
    - `owner`: [required] Owner of the action file (to locate the action)
    - `version`: [optional] The latest version of the action
