# Create a `RunCheck` type for the ReverseETL orchestration flow.

> This type is used to represent a check that must pass for a run to be executed.

It can be further broken into two variants:
- `PreRunCheck`: A check that must pass before the run can begin
- `PostRunCheck`: A check that must pass after the run has completed to move the run to the `success` state

## dbt discovery API integration

Extend the `RunCheck` type to include additional properties specific to the dbt discovery API, such as the model name and environment ID.

Expose `dbtModelRunCheck` type to ReverseETL orchestration flow as a selectable check type.

ReverseETL orchestration flow then uses `dbtModelRunCheck` as the check-type for any orchestration job that depends upon the status of a dbt model.
 - successCriteria: a set of different criterion that can be used to modify what constitutes a successful run from a dbt model perspective
    - freshness check variability length
    - max history length
    - last run status
    - last run execution time 
    - etc

ReverseETL orchestration doesn't need to know or care about how or why the check passes or fails - it only needs to know that it passes or fails based upon the criteria defined in the `successCriteria` property, completely abstrtacting the details of how the check passes or fails from the ReverseETL orchestration flow perspective