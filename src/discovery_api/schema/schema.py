import sgqlc.types
import sgqlc.types.datetime
import sgqlc.types.relay


schema = sgqlc.types.Schema()


# Unexport Node/PageInfo, let schema re-declare them
schema -= sgqlc.types.relay.Node
schema -= sgqlc.types.relay.PageInfo



########################################################################
# Scalars and Enumerations
########################################################################
class AccessLevel(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('private', 'protected', 'public')


class AncestorNodeType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('Exposure', 'Macro', 'Model', 'Seed', 'Snapshot', 'Source')


class AnyScalar(sgqlc.types.Scalar):
    __schema__ = schema


class AppliedModelSortField(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('executeCompletedAt', 'queryUsageCount', 'rowCount', 'uniqueId')


class AutoExposureBIProvider(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('powerbi', 'tableau')


class BigInt(sgqlc.types.Scalar):
    __schema__ = schema


Boolean = sgqlc.types.Boolean

DateTime = sgqlc.types.datetime.DateTime

class ExposureHealthIssueType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('CautionUpstreamSources', 'DegradedUpstreamSources', 'FailedTestUpstreamModels', 'LastRunFailedUpstreamModels', 'Unknown', 'WarnedTestUpstreamModels')


Float = sgqlc.types.Float

class FreshnessStatus(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('Error', 'Pass', 'Skipped', 'Unknown', 'Warn')


Int = sgqlc.types.Int

class JSONObject(sgqlc.types.Scalar):
    __schema__ = schema


class OwnerResourceType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('exposure', 'group')


class PackageResourceType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('macro', 'model')


class Quality(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('Error', 'Pass', 'Unknown', 'Warn')


class ReleaseVersion(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('latest', 'none', 'old', 'prerelease')


class ResourceNodeType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('Exposure', 'Macro', 'Metric', 'Model', 'SavedQuery', 'Seed', 'SemanticModel', 'Snapshot', 'Source', 'Test')


class RunStatus(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('error', 'skipped', 'success')


class SortDirection(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('asc', 'desc')


String = sgqlc.types.String

class TestType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('GENERIC_DATA_TEST', 'SINGULAR_DATA_TEST', 'UNIT_TEST')


class TimePeriod(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('day', 'hour', 'minute')



########################################################################
# Input Objects
########################################################################
class AppliedModelSort(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('direction', 'field')
    direction = sgqlc.types.Field(sgqlc.types.non_null(SortDirection), graphql_name='direction')
    field = sgqlc.types.Field(sgqlc.types.non_null(AppliedModelSortField), graphql_name='field')


class AppliedResourcesFilter(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('tags', 'types', 'unique_ids')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    types = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ResourceNodeType))), graphql_name='types')
    unique_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='uniqueIds')


class DefinitionResourcesFilter(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('tags', 'types', 'unique_ids')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    types = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ResourceNodeType))), graphql_name='types')
    unique_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='uniqueIds')


class ExposureFilter(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('exposure_type', 'tags', 'unique_ids')
    exposure_type = sgqlc.types.Field(String, graphql_name='exposureType')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    unique_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='uniqueIds')


class ExposureTileFilter(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('auto_bi_provider', 'bi_resource_id', 'unique_id')
    auto_bi_provider = sgqlc.types.Field(AutoExposureBIProvider, graphql_name='autoBiProvider')
    bi_resource_id = sgqlc.types.Field(String, graphql_name='biResourceId')
    unique_id = sgqlc.types.Field(String, graphql_name='uniqueId')


class GenericMaterializedFilter(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('database', 'identifier', 'schema', 'tags', 'unique_ids')
    database = sgqlc.types.Field(String, graphql_name='database')
    identifier = sgqlc.types.Field(String, graphql_name='identifier')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    unique_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='uniqueIds')


class GroupFilter(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('unique_ids',)
    unique_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='uniqueIds')


class LineageFilter(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('column_names', 'exclude', 'select', 'tags', 'types', 'unique_ids')
    column_names = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='columnNames')
    exclude = sgqlc.types.Field(String, graphql_name='exclude')
    select = sgqlc.types.Field(String, graphql_name='select')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    types = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ResourceNodeType)), graphql_name='types')
    unique_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='uniqueIds')


class MacroDefinitionFilter(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('package_name', 'unique_ids')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    unique_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='uniqueIds')


class ModelAppliedFilter(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('access', 'database', 'group', 'identifier', 'last_run_status', 'modeling_layer', 'package_name', 'schema', 'tags', 'unique_ids')
    access = sgqlc.types.Field(AccessLevel, graphql_name='access')
    database = sgqlc.types.Field(String, graphql_name='database')
    group = sgqlc.types.Field(String, graphql_name='group')
    identifier = sgqlc.types.Field(String, graphql_name='identifier')
    last_run_status = sgqlc.types.Field(RunStatus, graphql_name='lastRunStatus')
    modeling_layer = sgqlc.types.Field(String, graphql_name='modelingLayer')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    unique_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='uniqueIds')


class ModelDefinitionFilter(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('access', 'database', 'group', 'identifier', 'modeling_layer', 'schema', 'tags', 'unique_ids')
    access = sgqlc.types.Field(AccessLevel, graphql_name='access')
    database = sgqlc.types.Field(String, graphql_name='database')
    group = sgqlc.types.Field(String, graphql_name='group')
    identifier = sgqlc.types.Field(String, graphql_name='identifier')
    modeling_layer = sgqlc.types.Field(String, graphql_name='modelingLayer')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    unique_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='uniqueIds')


class SourceAppliedFilter(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('database', 'freshness_checked', 'freshness_status', 'identifier', 'schema', 'source_names', 'tags', 'unique_ids')
    database = sgqlc.types.Field(String, graphql_name='database')
    freshness_checked = sgqlc.types.Field(Boolean, graphql_name='freshnessChecked')
    freshness_status = sgqlc.types.Field(FreshnessStatus, graphql_name='freshnessStatus')
    identifier = sgqlc.types.Field(String, graphql_name='identifier')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    source_names = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='sourceNames')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    unique_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='uniqueIds')


class SourceDefinitionFilter(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('database', 'identifier', 'schema', 'source_names', 'tags', 'unique_ids')
    database = sgqlc.types.Field(String, graphql_name='database')
    identifier = sgqlc.types.Field(String, graphql_name='identifier')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    source_names = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='sourceNames')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    unique_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='uniqueIds')


class TestAppliedFilter(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('status', 'tags', 'test_types', 'unique_ids')
    status = sgqlc.types.Field(String, graphql_name='status')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    test_types = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(TestType)), graphql_name='testTypes')
    unique_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='uniqueIds')


class TestDefinitionFilter(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('tags', 'unique_ids')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    unique_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='uniqueIds')



########################################################################
# Output Objects and Interfaces
########################################################################
class CloudArtifactInterface(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('account_id', 'environment_id', 'job_id', 'project_id', 'run_id')
    account_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='accountId')
    environment_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='environmentId')
    job_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='jobId')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='projectId')
    run_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='runId')


class EnvironmentAppliedNestedNode(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('description', 'file_path', 'fqn', 'name', 'resource_type', 'unique_id')
    description = sgqlc.types.Field(String, graphql_name='description')
    file_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='filePath')
    fqn = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='fqn')
    name = sgqlc.types.Field(String, graphql_name='name')
    resource_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='resourceType')
    unique_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='uniqueId')


class EnvironmentAppliedNode(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('account_id', 'description', 'environment_id', 'file_path', 'meta', 'name', 'project_id', 'resource_type', 'tags', 'unique_id')
    account_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='accountId')
    description = sgqlc.types.Field(String, graphql_name='description')
    environment_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='environmentId')
    file_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='filePath')
    meta = sgqlc.types.Field(JSONObject, graphql_name='meta')
    name = sgqlc.types.Field(String, graphql_name='name')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='projectId')
    resource_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='resourceType')
    tags = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='tags')
    unique_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='uniqueId')


class EnvironmentDefinitionNestedNode(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('description', 'file_path', 'name', 'resource_type', 'run_generated_at', 'unique_id')
    description = sgqlc.types.Field(String, graphql_name='description')
    file_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='filePath')
    name = sgqlc.types.Field(String, graphql_name='name')
    resource_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='resourceType')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')
    unique_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='uniqueId')


class EnvironmentDefinitionNode(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('account_id', 'description', 'environment_id', 'file_path', 'meta', 'name', 'project_id', 'resource_type', 'run_generated_at', 'tags', 'unique_id')
    account_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='accountId')
    description = sgqlc.types.Field(String, graphql_name='description')
    environment_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='environmentId')
    file_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='filePath')
    meta = sgqlc.types.Field(JSONObject, graphql_name='meta')
    name = sgqlc.types.Field(String, graphql_name='name')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='projectId')
    resource_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='resourceType')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')
    tags = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='tags')
    unique_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='uniqueId')


class LineageNode(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('access', 'alias', 'database', 'file_path', 'group', 'matches_method', 'materialization_type', 'name', 'parent_ids', 'project_id', 'public_parent_ids', 'resource_type', 'schema', 'tags', 'unique_id', 'version')
    access = sgqlc.types.Field(String, graphql_name='access')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    database = sgqlc.types.Field(String, graphql_name='database')
    file_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='filePath')
    group = sgqlc.types.Field(String, graphql_name='group')
    matches_method = sgqlc.types.Field(Boolean, graphql_name='matchesMethod')
    materialization_type = sgqlc.types.Field(String, graphql_name='materializationType')
    name = sgqlc.types.Field(String, graphql_name='name')
    parent_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='parentIds')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='projectId')
    public_parent_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='publicParentIds')
    resource_type = sgqlc.types.Field(sgqlc.types.non_null(ResourceNodeType), graphql_name='resourceType')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    tags = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='tags')
    unique_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='uniqueId')
    version = sgqlc.types.Field(String, graphql_name='version')


class NodeInterface(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('dbt_version', 'description', 'meta', 'name', 'resource_type', 'tags', 'unique_id')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    description = sgqlc.types.Field(String, graphql_name='description')
    meta = sgqlc.types.Field(JSONObject, graphql_name='meta')
    name = sgqlc.types.Field(String, graphql_name='name')
    resource_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='resourceType')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    unique_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='uniqueId')


class LineageGraphNode(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('access', 'alias', 'database', 'file_path', 'fqn', 'group', 'matches_method', 'materialization_type', 'name', 'parent_ids', 'project_id', 'public_parent_ids', 'resource_type', 'schema', 'tags', 'unique_id', 'version')
    access = sgqlc.types.Field(String, graphql_name='access')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    database = sgqlc.types.Field(String, graphql_name='database')
    file_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='filePath')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    group = sgqlc.types.Field(String, graphql_name='group')
    matches_method = sgqlc.types.Field(Boolean, graphql_name='matchesMethod')
    materialization_type = sgqlc.types.Field(String, graphql_name='materializationType')
    name = sgqlc.types.Field(String, graphql_name='name')
    parent_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='parentIds')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='projectId')
    public_parent_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='publicParentIds')
    resource_type = sgqlc.types.Field(sgqlc.types.non_null(ResourceNodeType), graphql_name='resourceType')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    tags = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='tags')
    unique_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='uniqueId')
    version = sgqlc.types.Field(String, graphql_name='version')


class LineageNodeExecutable(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('access', 'alias', 'database', 'file_path', 'group', 'last_run_status', 'matches_method', 'materialization_type', 'name', 'parent_ids', 'project_id', 'public_parent_ids', 'resource_type', 'schema', 'tags', 'unique_id', 'version')
    access = sgqlc.types.Field(String, graphql_name='access')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    database = sgqlc.types.Field(String, graphql_name='database')
    file_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='filePath')
    group = sgqlc.types.Field(String, graphql_name='group')
    last_run_status = sgqlc.types.Field(String, graphql_name='lastRunStatus')
    matches_method = sgqlc.types.Field(Boolean, graphql_name='matchesMethod')
    materialization_type = sgqlc.types.Field(String, graphql_name='materializationType')
    name = sgqlc.types.Field(String, graphql_name='name')
    parent_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='parentIds')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='projectId')
    public_parent_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='publicParentIds')
    resource_type = sgqlc.types.Field(sgqlc.types.non_null(ResourceNodeType), graphql_name='resourceType')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    tags = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='tags')
    unique_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='uniqueId')
    version = sgqlc.types.Field(String, graphql_name='version')


class LineageNodeTestable(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('access', 'alias', 'database', 'file_path', 'group', 'matches_method', 'materialization_type', 'name', 'parent_ids', 'project_id', 'public_parent_ids', 'resource_type', 'schema', 'tags', 'unique_id', 'version', 'worst_test_status')
    access = sgqlc.types.Field(String, graphql_name='access')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    database = sgqlc.types.Field(String, graphql_name='database')
    file_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='filePath')
    group = sgqlc.types.Field(String, graphql_name='group')
    matches_method = sgqlc.types.Field(Boolean, graphql_name='matchesMethod')
    materialization_type = sgqlc.types.Field(String, graphql_name='materializationType')
    name = sgqlc.types.Field(String, graphql_name='name')
    parent_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='parentIds')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='projectId')
    public_parent_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='publicParentIds')
    resource_type = sgqlc.types.Field(sgqlc.types.non_null(ResourceNodeType), graphql_name='resourceType')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    tags = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='tags')
    unique_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='uniqueId')
    version = sgqlc.types.Field(String, graphql_name='version')
    worst_test_status = sgqlc.types.Field(String, graphql_name='worstTestStatus')


class LineageNodeWithParents(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('access', 'alias', 'database', 'file_path', 'group', 'matches_method', 'materialization_type', 'name', 'parent_ids', 'project_id', 'public_parent_ids', 'resource_type', 'schema', 'tags', 'unique_id', 'version')
    access = sgqlc.types.Field(String, graphql_name='access')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    database = sgqlc.types.Field(String, graphql_name='database')
    file_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='filePath')
    group = sgqlc.types.Field(String, graphql_name='group')
    matches_method = sgqlc.types.Field(Boolean, graphql_name='matchesMethod')
    materialization_type = sgqlc.types.Field(String, graphql_name='materializationType')
    name = sgqlc.types.Field(String, graphql_name='name')
    parent_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='parentIds')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='projectId')
    public_parent_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='publicParentIds')
    resource_type = sgqlc.types.Field(sgqlc.types.non_null(ResourceNodeType), graphql_name='resourceType')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    tags = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='tags')
    unique_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='uniqueId')
    version = sgqlc.types.Field(String, graphql_name='version')


class AppliedState(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('exposure_tile', 'exposures', 'last_updated_at', 'latest_git_sha', 'lineage', 'model_historical_runs', 'models', 'owners', 'packages', 'resource_counts', 'resources', 'seeds', 'snapshots', 'sources', 'tags', 'tests')
    exposure_tile = sgqlc.types.Field('ExposureTileNode', graphql_name='exposureTile', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(sgqlc.types.non_null(ExposureTileFilter), graphql_name='filter', default=None)),
))
    )
    exposures = sgqlc.types.Field(sgqlc.types.non_null('ExposureAppliedStateNodeConnection'), graphql_name='exposures', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(ExposureFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    last_updated_at = sgqlc.types.Field(DateTime, graphql_name='lastUpdatedAt')
    latest_git_sha = sgqlc.types.Field(String, graphql_name='latestGitSha')
    lineage = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(LineageNode))), graphql_name='lineage', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(sgqlc.types.non_null(LineageFilter), graphql_name='filter', default=None)),
))
    )
    model_historical_runs = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelNode'))), graphql_name='modelHistoricalRuns', args=sgqlc.types.ArgDict((
        ('identifier', sgqlc.types.Arg(String, graphql_name='identifier', default=None)),
        ('last_run_count', sgqlc.types.Arg(Int, graphql_name='lastRunCount', default=1)),
        ('unique_id', sgqlc.types.Arg(String, graphql_name='uniqueId', default=None)),
        ('with_catalog', sgqlc.types.Arg(Boolean, graphql_name='withCatalog', default=False)),
))
    )
    models = sgqlc.types.Field(sgqlc.types.non_null('ModelAppliedStateNodeConnection'), graphql_name='models', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(ModelAppliedFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('sort', sgqlc.types.Arg(AppliedModelSort, graphql_name='sort', default=None)),
))
    )
    owners = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ExposureOwner'))), graphql_name='owners', args=sgqlc.types.ArgDict((
        ('resource', sgqlc.types.Arg(sgqlc.types.non_null(OwnerResourceType), graphql_name='resource', default=None)),
))
    )
    packages = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='packages', args=sgqlc.types.ArgDict((
        ('resource', sgqlc.types.Arg(sgqlc.types.non_null(PackageResourceType), graphql_name='resource', default=None)),
))
    )
    resource_counts = sgqlc.types.Field(JSONObject, graphql_name='resourceCounts')
    resources = sgqlc.types.Field(sgqlc.types.non_null('EnvironmentAppliedNodeConnection'), graphql_name='resources', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(sgqlc.types.non_null(AppliedResourcesFilter), graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    seeds = sgqlc.types.Field(sgqlc.types.non_null('SeedAppliedStateNodeConnection'), graphql_name='seeds', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(GenericMaterializedFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    snapshots = sgqlc.types.Field(sgqlc.types.non_null('SnapshotAppliedStateNodeConnection'), graphql_name='snapshots', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(GenericMaterializedFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    sources = sgqlc.types.Field(sgqlc.types.non_null('SourceAppliedStateNodeConnection'), graphql_name='sources', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(SourceAppliedFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Tag'))), graphql_name='tags')
    tests = sgqlc.types.Field(sgqlc.types.non_null('TestAppliedStateNodeConnection'), graphql_name='tests', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(TestAppliedFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )


class CatalogColumn(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('comment', 'description', 'index', 'meta', 'name', 'tags', 'type')
    comment = sgqlc.types.Field(String, graphql_name='comment')
    description = sgqlc.types.Field(String, graphql_name='description')
    index = sgqlc.types.Field(Int, graphql_name='index')
    meta = sgqlc.types.Field(JSONObject, graphql_name='meta')
    name = sgqlc.types.Field(String, graphql_name='name')
    tags = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='tags')
    type = sgqlc.types.Field(String, graphql_name='type')


class CatalogNode(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('bytes_stat', 'columns', 'comment', 'environment_id', 'job_definition_id', 'owner', 'row_count_stat', 'run_generated_at', 'run_id', 'stats', 'type', 'unique_id')
    bytes_stat = sgqlc.types.Field(BigInt, graphql_name='bytesStat')
    columns = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CatalogColumn)), graphql_name='columns')
    comment = sgqlc.types.Field(String, graphql_name='comment')
    environment_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='environmentId')
    job_definition_id = sgqlc.types.Field(BigInt, graphql_name='jobDefinitionId')
    owner = sgqlc.types.Field(String, graphql_name='owner')
    row_count_stat = sgqlc.types.Field(BigInt, graphql_name='rowCountStat')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')
    stats = sgqlc.types.Field(sgqlc.types.list_of('CatalogStat'), graphql_name='stats')
    type = sgqlc.types.Field(String, graphql_name='type')
    unique_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='uniqueId')


class CatalogStat(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('description', 'id', 'include', 'label', 'value')
    description = sgqlc.types.Field(String, graphql_name='description')
    id = sgqlc.types.Field(String, graphql_name='id')
    include = sgqlc.types.Field(Boolean, graphql_name='include')
    label = sgqlc.types.Field(String, graphql_name='label')
    value = sgqlc.types.Field(AnyScalar, graphql_name='value')


class Criteria(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('error_after', 'warn_after')
    error_after = sgqlc.types.Field('CriteriaInfo', graphql_name='errorAfter')
    warn_after = sgqlc.types.Field('CriteriaInfo', graphql_name='warnAfter')


class CriteriaInfo(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('count', 'period')
    count = sgqlc.types.Field(Int, graphql_name='count')
    period = sgqlc.types.Field(TimePeriod, graphql_name='period')


class DefinitionState(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('exposures', 'groups', 'last_updated_at', 'lineage', 'macros', 'metrics', 'models', 'packages', 'resource_counts', 'resources', 'saved_queries', 'seeds', 'semantic_models', 'snapshots', 'sources', 'tags', 'tests')
    exposures = sgqlc.types.Field(sgqlc.types.non_null('ExposureDefinitionNodeConnection'), graphql_name='exposures', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(ExposureFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    groups = sgqlc.types.Field(sgqlc.types.non_null('GroupNodeConnection'), graphql_name='groups', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(GroupFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    last_updated_at = sgqlc.types.Field(DateTime, graphql_name='lastUpdatedAt')
    lineage = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(LineageNode))), graphql_name='lineage', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(sgqlc.types.non_null(LineageFilter), graphql_name='filter', default=None)),
))
    )
    macros = sgqlc.types.Field(sgqlc.types.non_null('MacroDefinitionNodeConnection'), graphql_name='macros', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(MacroDefinitionFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    metrics = sgqlc.types.Field(sgqlc.types.non_null('MetricDefinitionNodeConnection'), graphql_name='metrics', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(GenericMaterializedFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    models = sgqlc.types.Field(sgqlc.types.non_null('ModelDefinitionNodeConnection'), graphql_name='models', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(ModelDefinitionFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    packages = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='packages', args=sgqlc.types.ArgDict((
        ('resource', sgqlc.types.Arg(sgqlc.types.non_null(PackageResourceType), graphql_name='resource', default=None)),
))
    )
    resource_counts = sgqlc.types.Field(JSONObject, graphql_name='resourceCounts')
    resources = sgqlc.types.Field(sgqlc.types.non_null('EnvironmentDefinitionNodeConnection'), graphql_name='resources', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(sgqlc.types.non_null(DefinitionResourcesFilter), graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    saved_queries = sgqlc.types.Field(sgqlc.types.non_null('SavedQueryDefinitionNodeConnection'), graphql_name='savedQueries', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(GenericMaterializedFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    seeds = sgqlc.types.Field(sgqlc.types.non_null('SeedDefinitionNodeConnection'), graphql_name='seeds', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(GenericMaterializedFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    semantic_models = sgqlc.types.Field(sgqlc.types.non_null('SemanticModelDefinitionNodeConnection'), graphql_name='semanticModels', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(GenericMaterializedFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    snapshots = sgqlc.types.Field(sgqlc.types.non_null('SnapshotDefinitionNodeConnection'), graphql_name='snapshots', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(GenericMaterializedFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    sources = sgqlc.types.Field(sgqlc.types.non_null('SourceDefinitionNodeConnection'), graphql_name='sources', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(SourceDefinitionFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Tag'))), graphql_name='tags')
    tests = sgqlc.types.Field(sgqlc.types.non_null('TestDefinitionNodeConnection'), graphql_name='tests', args=sgqlc.types.ArgDict((
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('filter', sgqlc.types.Arg(TestDefinitionFilter, graphql_name='filter', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
))
    )


class Environment(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('adapter_type', 'applied', 'dbt_project_name', 'definition')
    adapter_type = sgqlc.types.Field(String, graphql_name='adapterType')
    applied = sgqlc.types.Field(AppliedState, graphql_name='applied')
    dbt_project_name = sgqlc.types.Field(String, graphql_name='dbtProjectName')
    definition = sgqlc.types.Field(DefinitionState, graphql_name='definition')


class EnvironmentAppliedNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('EnvironmentAppliedNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class EnvironmentAppliedNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null(EnvironmentAppliedNode), graphql_name='node')


class EnvironmentDefinitionNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('EnvironmentDefinitionNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class EnvironmentDefinitionNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null(EnvironmentDefinitionNode), graphql_name='node')


class ExposureAppliedStateNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ExposureAppliedStateNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class ExposureAppliedStateNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('ExposureAppliedStateNode'), graphql_name='node')


class ExposureDefinitionNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ExposureDefinitionNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class ExposureDefinitionNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('ExposureDefinitionNode'), graphql_name='node')


class ExposureOwner(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('email', 'name')
    email = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='email')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class GroupNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('GroupNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class GroupNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('GroupNode'), graphql_name='node')


class JobNode(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('exposure', 'exposures', 'id', 'macro', 'macros', 'metric', 'metrics', 'model', 'models', 'run_id', 'seed', 'seeds', 'snapshot', 'snapshots', 'source', 'sources', 'test', 'tests')
    exposure = sgqlc.types.Field('ExposureNode', graphql_name='exposure', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    exposures = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ExposureNode'))), graphql_name='exposures')
    id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='id')
    macro = sgqlc.types.Field('MacroNode', graphql_name='macro', args=sgqlc.types.ArgDict((
        ('unique_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='uniqueId', default=None)),
))
    )
    macros = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MacroNode'))), graphql_name='macros')
    metric = sgqlc.types.Field('MetricNode', graphql_name='metric', args=sgqlc.types.ArgDict((
        ('unique_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='uniqueId', default=None)),
))
    )
    metrics = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MetricNode'))), graphql_name='metrics')
    model = sgqlc.types.Field('ModelNode', graphql_name='model', args=sgqlc.types.ArgDict((
        ('unique_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='uniqueId', default=None)),
))
    )
    models = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelNode'))), graphql_name='models', args=sgqlc.types.ArgDict((
        ('database', sgqlc.types.Arg(String, graphql_name='database', default=None)),
        ('identifier', sgqlc.types.Arg(String, graphql_name='identifier', default=None)),
        ('schema', sgqlc.types.Arg(String, graphql_name='schema', default=None)),
))
    )
    run_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='runId')
    seed = sgqlc.types.Field('SeedNode', graphql_name='seed', args=sgqlc.types.ArgDict((
        ('unique_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='uniqueId', default=None)),
))
    )
    seeds = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SeedNode'))), graphql_name='seeds')
    snapshot = sgqlc.types.Field('SnapshotNode', graphql_name='snapshot', args=sgqlc.types.ArgDict((
        ('unique_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='uniqueId', default=None)),
))
    )
    snapshots = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SnapshotNode'))), graphql_name='snapshots')
    source = sgqlc.types.Field('SourceNode', graphql_name='source', args=sgqlc.types.ArgDict((
        ('unique_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='uniqueId', default=None)),
))
    )
    sources = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SourceNode'))), graphql_name='sources', args=sgqlc.types.ArgDict((
        ('database', sgqlc.types.Arg(String, graphql_name='database', default=None)),
        ('identifier', sgqlc.types.Arg(String, graphql_name='identifier', default=None)),
        ('schema', sgqlc.types.Arg(String, graphql_name='schema', default=None)),
))
    )
    test = sgqlc.types.Field('TestNode', graphql_name='test', args=sgqlc.types.ArgDict((
        ('unique_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='uniqueId', default=None)),
))
    )
    tests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TestNode'))), graphql_name='tests')


class MacroArguments(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('description', 'name', 'type')
    description = sgqlc.types.Field(String, graphql_name='description')
    name = sgqlc.types.Field(String, graphql_name='name')
    type = sgqlc.types.Field(String, graphql_name='type')


class MacroDefinitionNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MacroDefinitionNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class MacroDefinitionNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('MacroDefinitionNode'), graphql_name='node')


class MetricDefinitionNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MetricDefinitionNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class MetricDefinitionNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('MetricDefinitionNode'), graphql_name='node')


class MetricFilter(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('field', 'operator', 'value')
    field = sgqlc.types.Field(String, graphql_name='field')
    operator = sgqlc.types.Field(String, graphql_name='operator')
    value = sgqlc.types.Field(String, graphql_name='value')


class ModelAppliedStateNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelAppliedStateNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class ModelAppliedStateNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('ModelAppliedStateNode'), graphql_name='node')


class ModelDefinitionNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelDefinitionNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class ModelDefinitionNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('ModelDefinitionNode'), graphql_name='node')


class ModelExecutionInfoNode(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('compile_completed_at', 'compile_started_at', 'execute_completed_at', 'execute_started_at', 'execution_time', 'last_job_definition_id', 'last_run_error', 'last_run_generated_at', 'last_run_id', 'last_run_status', 'last_success_job_definition_id', 'last_success_run_id', 'run_elapsed_time', 'run_generated_at')
    compile_completed_at = sgqlc.types.Field(DateTime, graphql_name='compileCompletedAt')
    compile_started_at = sgqlc.types.Field(DateTime, graphql_name='compileStartedAt')
    execute_completed_at = sgqlc.types.Field(DateTime, graphql_name='executeCompletedAt')
    execute_started_at = sgqlc.types.Field(DateTime, graphql_name='executeStartedAt')
    execution_time = sgqlc.types.Field(Float, graphql_name='executionTime')
    last_job_definition_id = sgqlc.types.Field(BigInt, graphql_name='lastJobDefinitionId')
    last_run_error = sgqlc.types.Field(String, graphql_name='lastRunError')
    last_run_generated_at = sgqlc.types.Field(DateTime, graphql_name='lastRunGeneratedAt')
    last_run_id = sgqlc.types.Field(BigInt, graphql_name='lastRunId')
    last_run_status = sgqlc.types.Field(RunStatus, graphql_name='lastRunStatus')
    last_success_job_definition_id = sgqlc.types.Field(BigInt, graphql_name='lastSuccessJobDefinitionId')
    last_success_run_id = sgqlc.types.Field(BigInt, graphql_name='lastSuccessRunId')
    run_elapsed_time = sgqlc.types.Field(Float, graphql_name='runElapsedTime')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')


class ModelLevelConstraint(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('columns', 'expression', 'name', 'type', 'warn_unenforced', 'warn_unsupported')
    columns = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='columns')
    expression = sgqlc.types.Field(String, graphql_name='expression')
    name = sgqlc.types.Field(String, graphql_name='name')
    type = sgqlc.types.Field(String, graphql_name='type')
    warn_unenforced = sgqlc.types.Field(Boolean, graphql_name='warnUnenforced')
    warn_unsupported = sgqlc.types.Field(Boolean, graphql_name='warnUnsupported')


class ModelVersion(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name', 'release_version', 'unique_id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    release_version = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='releaseVersion')
    unique_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='uniqueId')


class PageInfo(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('end_cursor', 'has_next_page', 'has_previous_page', 'start_cursor')
    end_cursor = sgqlc.types.Field(String, graphql_name='endCursor')
    has_next_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hasNextPage')
    has_previous_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hasPreviousPage')
    start_cursor = sgqlc.types.Field(String, graphql_name='startCursor')


class Query(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('environment', 'exposure', 'exposures', 'job', 'macro', 'macros', 'metric', 'metrics', 'model', 'model_by_environment', 'models', 'seed', 'seeds', 'snapshot', 'snapshots', 'source', 'sources', 'test', 'tests')
    environment = sgqlc.types.Field(sgqlc.types.non_null(Environment), graphql_name='environment', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(BigInt), graphql_name='id', default=None)),
))
    )
    exposure = sgqlc.types.Field('ExposureNode', graphql_name='exposure', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
))
    )
    exposures = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ExposureNode'))), graphql_name='exposures', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
))
    )
    job = sgqlc.types.Field(JobNode, graphql_name='job', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(BigInt), graphql_name='id', default=None)),
        ('run_id', sgqlc.types.Arg(BigInt, graphql_name='runId', default=None)),
))
    )
    macro = sgqlc.types.Field('MacroNode', graphql_name='macro', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
        ('unique_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='uniqueId', default=None)),
))
    )
    macros = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MacroNode'))), graphql_name='macros', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
))
    )
    metric = sgqlc.types.Field('MetricNode', graphql_name='metric', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
        ('unique_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='uniqueId', default=None)),
))
    )
    metrics = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MetricNode'))), graphql_name='metrics', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
))
    )
    model = sgqlc.types.Field('ModelNode', graphql_name='model', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
        ('unique_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='uniqueId', default=None)),
))
    )
    model_by_environment = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelNode'))), graphql_name='modelByEnvironment', args=sgqlc.types.ArgDict((
        ('environment_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='environmentId', default=None)),
        ('identifier', sgqlc.types.Arg(String, graphql_name='identifier', default=None)),
        ('last_run_count', sgqlc.types.Arg(Int, graphql_name='lastRunCount', default=1)),
        ('unique_id', sgqlc.types.Arg(String, graphql_name='uniqueId', default=None)),
        ('with_catalog', sgqlc.types.Arg(Boolean, graphql_name='withCatalog', default=False)),
))
    )
    models = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelNode'))), graphql_name='models', args=sgqlc.types.ArgDict((
        ('database', sgqlc.types.Arg(String, graphql_name='database', default=None)),
        ('identifier', sgqlc.types.Arg(String, graphql_name='identifier', default=None)),
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
        ('schema', sgqlc.types.Arg(String, graphql_name='schema', default=None)),
))
    )
    seed = sgqlc.types.Field('SeedNode', graphql_name='seed', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
        ('unique_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='uniqueId', default=None)),
))
    )
    seeds = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SeedNode'))), graphql_name='seeds', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
))
    )
    snapshot = sgqlc.types.Field('SnapshotNode', graphql_name='snapshot', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
        ('unique_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='uniqueId', default=None)),
))
    )
    snapshots = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SnapshotNode'))), graphql_name='snapshots', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
))
    )
    source = sgqlc.types.Field('SourceNode', graphql_name='source', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
        ('unique_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='uniqueId', default=None)),
))
    )
    sources = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SourceNode'))), graphql_name='sources', args=sgqlc.types.ArgDict((
        ('database', sgqlc.types.Arg(String, graphql_name='database', default=None)),
        ('identifier', sgqlc.types.Arg(String, graphql_name='identifier', default=None)),
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
        ('schema', sgqlc.types.Arg(String, graphql_name='schema', default=None)),
))
    )
    test = sgqlc.types.Field('TestNode', graphql_name='test', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
        ('unique_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='uniqueId', default=None)),
))
    )
    tests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TestNode'))), graphql_name='tests', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='jobId', default=None)),
        ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
))
    )


class QueryExportConfig(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('alias', 'database', 'export_as', 'schema')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    database = sgqlc.types.Field(String, graphql_name='database')
    export_as = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='exportAs')
    schema = sgqlc.types.Field(String, graphql_name='schema')


class QueryExports(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('config', 'name')
    config = sgqlc.types.Field(QueryExportConfig, graphql_name='config')
    name = sgqlc.types.Field(String, graphql_name='name')


class QueryParams(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('group_by', 'limit', 'metrics', 'order_by', 'where')
    group_by = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='groupBy')
    limit = sgqlc.types.Field(BigInt, graphql_name='limit')
    metrics = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='metrics')
    order_by = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='orderBy')
    where = sgqlc.types.Field('QueryWhere', graphql_name='where')


class QueryWhere(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('where_filters',)
    where_filters = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('QueryWhereFilter'))), graphql_name='whereFilters')


class QueryWhereFilter(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('where_sql_template',)
    where_sql_template = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='whereSqlTemplate')


class RunInfoNode(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('args', 'compile_completed_at', 'compile_started_at', 'error', 'execute_completed_at', 'execute_started_at', 'execution_time', 'invocation_id', 'run_elapsed_time', 'run_generated_at', 'skip', 'status', 'thread_id')
    args = sgqlc.types.Field(String, graphql_name='args')
    compile_completed_at = sgqlc.types.Field(DateTime, graphql_name='compileCompletedAt')
    compile_started_at = sgqlc.types.Field(DateTime, graphql_name='compileStartedAt')
    error = sgqlc.types.Field(String, graphql_name='error')
    execute_completed_at = sgqlc.types.Field(DateTime, graphql_name='executeCompletedAt')
    execute_started_at = sgqlc.types.Field(DateTime, graphql_name='executeStartedAt')
    execution_time = sgqlc.types.Field(Float, graphql_name='executionTime')
    invocation_id = sgqlc.types.Field(String, graphql_name='invocationId')
    run_elapsed_time = sgqlc.types.Field(Float, graphql_name='runElapsedTime')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')
    skip = sgqlc.types.Field(Boolean, graphql_name='skip')
    status = sgqlc.types.Field(String, graphql_name='status')
    thread_id = sgqlc.types.Field(String, graphql_name='threadId')


class SavedQueryDefinitionNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SavedQueryDefinitionNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class SavedQueryDefinitionNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('SavedQueryDefinitionNode'), graphql_name='node')


class SeedAppliedStateNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SeedAppliedStateNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class SeedAppliedStateNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('SeedAppliedStateNode'), graphql_name='node')


class SeedDefinitionNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SeedDefinitionNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class SeedDefinitionNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('SeedDefinitionNode'), graphql_name='node')


class SeedExecutionInfoNode(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('compile_completed_at', 'compile_started_at', 'execute_completed_at', 'execute_started_at', 'execution_time', 'last_job_definition_id', 'last_run_error', 'last_run_generated_at', 'last_run_id', 'last_run_skip', 'last_run_status', 'last_success_job_definition_id', 'last_success_run_id', 'run_elapsed_time', 'run_generated_at')
    compile_completed_at = sgqlc.types.Field(DateTime, graphql_name='compileCompletedAt')
    compile_started_at = sgqlc.types.Field(DateTime, graphql_name='compileStartedAt')
    execute_completed_at = sgqlc.types.Field(DateTime, graphql_name='executeCompletedAt')
    execute_started_at = sgqlc.types.Field(DateTime, graphql_name='executeStartedAt')
    execution_time = sgqlc.types.Field(Float, graphql_name='executionTime')
    last_job_definition_id = sgqlc.types.Field(BigInt, graphql_name='lastJobDefinitionId')
    last_run_error = sgqlc.types.Field(String, graphql_name='lastRunError')
    last_run_generated_at = sgqlc.types.Field(DateTime, graphql_name='lastRunGeneratedAt')
    last_run_id = sgqlc.types.Field(BigInt, graphql_name='lastRunId')
    last_run_skip = sgqlc.types.Field(Boolean, graphql_name='lastRunSkip')
    last_run_status = sgqlc.types.Field(String, graphql_name='lastRunStatus')
    last_success_job_definition_id = sgqlc.types.Field(BigInt, graphql_name='lastSuccessJobDefinitionId')
    last_success_run_id = sgqlc.types.Field(BigInt, graphql_name='lastSuccessRunId')
    run_elapsed_time = sgqlc.types.Field(Float, graphql_name='runElapsedTime')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')


class SemanticModelDefinitionNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SemanticModelDefinitionNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class SemanticModelDefinitionNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('SemanticModelDefinitionNode'), graphql_name='node')


class SemanticModelDimension(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('description', 'name', 'type', 'type_params')
    description = sgqlc.types.Field(String, graphql_name='description')
    name = sgqlc.types.Field(String, graphql_name='name')
    type = sgqlc.types.Field(String, graphql_name='type')
    type_params = sgqlc.types.Field(JSONObject, graphql_name='typeParams')


class SemanticModelEntity(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('description', 'name', 'type')
    description = sgqlc.types.Field(String, graphql_name='description')
    name = sgqlc.types.Field(String, graphql_name='name')
    type = sgqlc.types.Field(String, graphql_name='type')


class SemanticModelMeasure(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('agg', 'create_metric', 'description', 'expr', 'name')
    agg = sgqlc.types.Field(String, graphql_name='agg')
    create_metric = sgqlc.types.Field(Boolean, graphql_name='createMetric')
    description = sgqlc.types.Field(String, graphql_name='description')
    expr = sgqlc.types.Field(String, graphql_name='expr')
    name = sgqlc.types.Field(String, graphql_name='name')


class SnapshotAppliedStateNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SnapshotAppliedStateNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class SnapshotAppliedStateNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('SnapshotAppliedStateNode'), graphql_name='node')


class SnapshotDefinitionNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SnapshotDefinitionNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class SnapshotDefinitionNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('SnapshotDefinitionNode'), graphql_name='node')


class SnapshotExecutionInfoNode(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('compile_completed_at', 'compile_started_at', 'execute_completed_at', 'execute_started_at', 'execution_time', 'last_job_definition_id', 'last_run_error', 'last_run_generated_at', 'last_run_id', 'last_run_status', 'last_success_job_definition_id', 'last_success_run_id', 'run_elapsed_time', 'run_generated_at')
    compile_completed_at = sgqlc.types.Field(DateTime, graphql_name='compileCompletedAt')
    compile_started_at = sgqlc.types.Field(DateTime, graphql_name='compileStartedAt')
    execute_completed_at = sgqlc.types.Field(DateTime, graphql_name='executeCompletedAt')
    execute_started_at = sgqlc.types.Field(DateTime, graphql_name='executeStartedAt')
    execution_time = sgqlc.types.Field(Float, graphql_name='executionTime')
    last_job_definition_id = sgqlc.types.Field(BigInt, graphql_name='lastJobDefinitionId')
    last_run_error = sgqlc.types.Field(String, graphql_name='lastRunError')
    last_run_generated_at = sgqlc.types.Field(DateTime, graphql_name='lastRunGeneratedAt')
    last_run_id = sgqlc.types.Field(BigInt, graphql_name='lastRunId')
    last_run_status = sgqlc.types.Field(String, graphql_name='lastRunStatus')
    last_success_job_definition_id = sgqlc.types.Field(BigInt, graphql_name='lastSuccessJobDefinitionId')
    last_success_run_id = sgqlc.types.Field(BigInt, graphql_name='lastSuccessRunId')
    run_elapsed_time = sgqlc.types.Field(Float, graphql_name='runElapsedTime')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')


class SourceAppliedStateNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SourceAppliedStateNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class SourceAppliedStateNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('SourceAppliedStateNode'), graphql_name='node')


class SourceDefinitionNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SourceDefinitionNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class SourceDefinitionNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('SourceDefinitionNode'), graphql_name='node')


class SourceFreshnessNode(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('criteria', 'freshness_checked', 'freshness_job_definition_id', 'freshness_run_generated_at', 'freshness_run_id', 'freshness_status', 'max_loaded_at', 'max_loaded_at_time_ago_in_s', 'snapshotted_at')
    criteria = sgqlc.types.Field(sgqlc.types.non_null(Criteria), graphql_name='criteria')
    freshness_checked = sgqlc.types.Field(Boolean, graphql_name='freshnessChecked')
    freshness_job_definition_id = sgqlc.types.Field(BigInt, graphql_name='freshnessJobDefinitionId')
    freshness_run_generated_at = sgqlc.types.Field(DateTime, graphql_name='freshnessRunGeneratedAt')
    freshness_run_id = sgqlc.types.Field(BigInt, graphql_name='freshnessRunId')
    freshness_status = sgqlc.types.Field(FreshnessStatus, graphql_name='freshnessStatus')
    max_loaded_at = sgqlc.types.Field(DateTime, graphql_name='maxLoadedAt')
    max_loaded_at_time_ago_in_s = sgqlc.types.Field(Float, graphql_name='maxLoadedAtTimeAgoInS')
    snapshotted_at = sgqlc.types.Field(DateTime, graphql_name='snapshottedAt')


class Tag(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class TestAppliedStateNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TestAppliedStateNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class TestAppliedStateNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('TestAppliedStateNode'), graphql_name='node')


class TestDefinitionNodeConnection(sgqlc.types.relay.Connection):
    __schema__ = schema
    __field_names__ = ('edges', 'page_info', 'total_count')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TestDefinitionNodeEdge'))), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class TestDefinitionNodeEdge(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('TestDefinitionNode'), graphql_name='node')


class TestExecutionInfoNode(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('compile_completed_at', 'compile_started_at', 'execute_completed_at', 'execute_started_at', 'execution_time', 'last_job_definition_id', 'last_run_error', 'last_run_failures', 'last_run_generated_at', 'last_run_id', 'last_run_status', 'last_success_job_definition_id', 'last_success_run_id', 'run_elapsed_time', 'run_generated_at')
    compile_completed_at = sgqlc.types.Field(DateTime, graphql_name='compileCompletedAt')
    compile_started_at = sgqlc.types.Field(DateTime, graphql_name='compileStartedAt')
    execute_completed_at = sgqlc.types.Field(DateTime, graphql_name='executeCompletedAt')
    execute_started_at = sgqlc.types.Field(DateTime, graphql_name='executeStartedAt')
    execution_time = sgqlc.types.Field(Float, graphql_name='executionTime')
    last_job_definition_id = sgqlc.types.Field(BigInt, graphql_name='lastJobDefinitionId')
    last_run_error = sgqlc.types.Field(String, graphql_name='lastRunError')
    last_run_failures = sgqlc.types.Field(BigInt, graphql_name='lastRunFailures')
    last_run_generated_at = sgqlc.types.Field(DateTime, graphql_name='lastRunGeneratedAt')
    last_run_id = sgqlc.types.Field(BigInt, graphql_name='lastRunId')
    last_run_status = sgqlc.types.Field(String, graphql_name='lastRunStatus')
    last_success_job_definition_id = sgqlc.types.Field(BigInt, graphql_name='lastSuccessJobDefinitionId')
    last_success_run_id = sgqlc.types.Field(BigInt, graphql_name='lastSuccessRunId')
    run_elapsed_time = sgqlc.types.Field(Float, graphql_name='runElapsedTime')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')


class TestMetadata(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('column_name', 'kwargs', 'name', 'namespace')
    column_name = sgqlc.types.Field(String, graphql_name='columnName')
    kwargs = sgqlc.types.Field(JSONObject, graphql_name='kwargs')
    name = sgqlc.types.Field(String, graphql_name='name')
    namespace = sgqlc.types.Field(String, graphql_name='namespace')


class ExposureAppliedStateNestedNode(sgqlc.types.Type, EnvironmentAppliedNestedNode):
    __schema__ = schema
    __field_names__ = ('dbt_version', 'exposure_type', 'label', 'manifest_generated_at', 'maturity', 'owner_email', 'owner_name', 'package_name', 'patch_path', 'url')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    exposure_type = sgqlc.types.Field(String, graphql_name='exposureType')
    label = sgqlc.types.Field(String, graphql_name='label')
    manifest_generated_at = sgqlc.types.Field(DateTime, graphql_name='manifestGeneratedAt')
    maturity = sgqlc.types.Field(String, graphql_name='maturity')
    owner_email = sgqlc.types.Field(String, graphql_name='ownerEmail')
    owner_name = sgqlc.types.Field(String, graphql_name='ownerName')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    url = sgqlc.types.Field(String, graphql_name='url')


class ExposureAppliedStateNode(sgqlc.types.Type, EnvironmentAppliedNode):
    __schema__ = schema
    __field_names__ = ('ancestors', 'dbt_version', 'exposure_type', 'fqn', 'label', 'manifest_generated_at', 'maturity', 'owner_email', 'owner_name', 'package_name', 'parents', 'patch_path', 'url')
    ancestors = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentAppliedNestedNode))), graphql_name='ancestors', args=sgqlc.types.ArgDict((
        ('types', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(AncestorNodeType))), graphql_name='types', default=None)),
))
    )
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    exposure_type = sgqlc.types.Field(String, graphql_name='exposureType')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    label = sgqlc.types.Field(String, graphql_name='label')
    manifest_generated_at = sgqlc.types.Field(DateTime, graphql_name='manifestGeneratedAt')
    maturity = sgqlc.types.Field(String, graphql_name='maturity')
    owner_email = sgqlc.types.Field(String, graphql_name='ownerEmail')
    owner_name = sgqlc.types.Field(String, graphql_name='ownerName')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    parents = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentAppliedNestedNode))), graphql_name='parents')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    url = sgqlc.types.Field(String, graphql_name='url')


class ExposureDefinitionNestedNode(sgqlc.types.Type, EnvironmentDefinitionNestedNode):
    __schema__ = schema
    __field_names__ = ('dbt_version', 'exposure_type', 'label', 'manifest_generated_at', 'maturity', 'owner_email', 'owner_name', 'package_name', 'patch_path', 'url')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    exposure_type = sgqlc.types.Field(String, graphql_name='exposureType')
    label = sgqlc.types.Field(String, graphql_name='label')
    manifest_generated_at = sgqlc.types.Field(DateTime, graphql_name='manifestGeneratedAt')
    maturity = sgqlc.types.Field(String, graphql_name='maturity')
    owner_email = sgqlc.types.Field(String, graphql_name='ownerEmail')
    owner_name = sgqlc.types.Field(String, graphql_name='ownerName')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    url = sgqlc.types.Field(String, graphql_name='url')


class ExposureDefinitionNode(sgqlc.types.Type, EnvironmentDefinitionNode):
    __schema__ = schema
    __field_names__ = ('ancestors', 'dbt_version', 'exposure_type', 'fqn', 'freshness_status', 'label', 'manifest_generated_at', 'maturity', 'owner_email', 'owner_name', 'package_name', 'parents', 'patch_path', 'url')
    ancestors = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='ancestors')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    exposure_type = sgqlc.types.Field(String, graphql_name='exposureType')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    freshness_status = sgqlc.types.Field(FreshnessStatus, graphql_name='freshnessStatus')
    label = sgqlc.types.Field(String, graphql_name='label')
    manifest_generated_at = sgqlc.types.Field(DateTime, graphql_name='manifestGeneratedAt')
    maturity = sgqlc.types.Field(String, graphql_name='maturity')
    owner_email = sgqlc.types.Field(String, graphql_name='ownerEmail')
    owner_name = sgqlc.types.Field(String, graphql_name='ownerName')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    parents = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='parents')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    url = sgqlc.types.Field(String, graphql_name='url')


class ExposureLineageNode(sgqlc.types.Type, LineageGraphNode, LineageNode, LineageNodeWithParents):
    __schema__ = schema
    __field_names__ = ()


class ExposureNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = ('compile_completed_at', 'compile_started_at', 'depends_on', 'execute_completed_at', 'execute_started_at', 'execution_time', 'exposure_type', 'manifest_generated_at', 'maturity', 'owner_email', 'owner_name', 'package_name', 'parents', 'parents_models', 'parents_sources', 'status', 'thread_id', 'url')
    compile_completed_at = sgqlc.types.Field(DateTime, graphql_name='compileCompletedAt')
    compile_started_at = sgqlc.types.Field(DateTime, graphql_name='compileStartedAt')
    depends_on = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='dependsOn')
    execute_completed_at = sgqlc.types.Field(DateTime, graphql_name='executeCompletedAt')
    execute_started_at = sgqlc.types.Field(DateTime, graphql_name='executeStartedAt')
    execution_time = sgqlc.types.Field(Float, graphql_name='executionTime')
    exposure_type = sgqlc.types.Field(String, graphql_name='exposureType')
    manifest_generated_at = sgqlc.types.Field(DateTime, graphql_name='manifestGeneratedAt')
    maturity = sgqlc.types.Field(String, graphql_name='maturity')
    owner_email = sgqlc.types.Field(String, graphql_name='ownerEmail')
    owner_name = sgqlc.types.Field(String, graphql_name='ownerName')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    parents = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(NodeInterface))), graphql_name='parents')
    parents_models = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelNode'))), graphql_name='parentsModels')
    parents_sources = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SourceNode'))), graphql_name='parentsSources')
    status = sgqlc.types.Field(String, graphql_name='status')
    thread_id = sgqlc.types.Field(String, graphql_name='threadId')
    url = sgqlc.types.Field(String, graphql_name='url')


class ExposureTileNode(sgqlc.types.Type, EnvironmentAppliedNode):
    __schema__ = schema
    __field_names__ = ('auto_bi_provider', 'exposure_type', 'freshness_status', 'health_issues', 'max_snapshotted_at', 'package_name', 'quality', 'upstream_stats')
    auto_bi_provider = sgqlc.types.Field(AutoExposureBIProvider, graphql_name='autoBiProvider')
    exposure_type = sgqlc.types.Field(String, graphql_name='exposureType')
    freshness_status = sgqlc.types.Field(FreshnessStatus, graphql_name='freshnessStatus')
    health_issues = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExposureHealthIssueType))), graphql_name='healthIssues')
    max_snapshotted_at = sgqlc.types.Field(DateTime, graphql_name='maxSnapshottedAt')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    quality = sgqlc.types.Field(Quality, graphql_name='quality')
    upstream_stats = sgqlc.types.Field(JSONObject, graphql_name='upstreamStats')


class ExternalModelNode(sgqlc.types.Type, EnvironmentAppliedNestedNode, EnvironmentDefinitionNestedNode):
    __schema__ = schema
    __field_names__ = ('account_id', 'database', 'dbt_project_name', 'environment_id', 'identifier', 'latest_version', 'meta', 'package_name', 'patch_path', 'project_id', 'relation_name', 'release_version', 'schema', 'tags', 'version')
    account_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='accountId')
    database = sgqlc.types.Field(String, graphql_name='database')
    dbt_project_name = sgqlc.types.Field(String, graphql_name='dbtProjectName')
    environment_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='environmentId')
    identifier = sgqlc.types.Field(String, graphql_name='identifier')
    latest_version = sgqlc.types.Field(String, graphql_name='latestVersion')
    meta = sgqlc.types.Field(JSONObject, graphql_name='meta')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='projectId')
    relation_name = sgqlc.types.Field(String, graphql_name='relationName')
    release_version = sgqlc.types.Field(ReleaseVersion, graphql_name='releaseVersion')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    tags = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='tags')
    version = sgqlc.types.Field(String, graphql_name='version')


class GroupNode(sgqlc.types.Type, EnvironmentDefinitionNode):
    __schema__ = schema
    __field_names__ = ('job_id', 'model_count', 'models', 'owner_email', 'owner_name', 'package_name', 'run_id')
    job_id = sgqlc.types.Field(BigInt, graphql_name='jobId')
    model_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='modelCount')
    models = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelDefinitionNestedNode'))), graphql_name='models')
    owner_email = sgqlc.types.Field(String, graphql_name='ownerEmail')
    owner_name = sgqlc.types.Field(String, graphql_name='ownerName')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')


class MacroDefinitionNestedNode(sgqlc.types.Type, EnvironmentAppliedNestedNode, EnvironmentDefinitionNestedNode):
    __schema__ = schema
    __field_names__ = ('dbt_version', 'job_id', 'package_name', 'patch_path', 'run_id')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    job_id = sgqlc.types.Field(BigInt, graphql_name='jobId')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')


class MacroDefinitionNode(sgqlc.types.Type, EnvironmentAppliedNode, EnvironmentDefinitionNode):
    __schema__ = schema
    __field_names__ = ('arguments', 'dbt_version', 'job_id', 'macro_sql', 'package_name', 'parents', 'patch_path', 'run_id')
    arguments = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MacroArguments))), graphql_name='arguments')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    job_id = sgqlc.types.Field(BigInt, graphql_name='jobId')
    macro_sql = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='macroSql')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    parents = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='parents')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')


class MacroLineageNode(sgqlc.types.Type, LineageNode, LineageNodeWithParents):
    __schema__ = schema
    __field_names__ = ()


class MacroNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = ('depends_on', 'macro_sql', 'original_file_path', 'package_name', 'path', 'root_path')
    depends_on = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='dependsOn')
    macro_sql = sgqlc.types.Field(String, graphql_name='macroSql')
    original_file_path = sgqlc.types.Field(String, graphql_name='originalFilePath')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    path = sgqlc.types.Field(String, graphql_name='path')
    root_path = sgqlc.types.Field(String, graphql_name='rootPath')


class MetricDefinitionNestedNode(sgqlc.types.Type, EnvironmentAppliedNestedNode, EnvironmentDefinitionNestedNode):
    __schema__ = schema
    __field_names__ = ('dbt_version', 'filter', 'formula', 'group', 'job_definition_id', 'package_name', 'patch_path', 'run_id', 'type', 'type_params')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    filter = sgqlc.types.Field(JSONObject, graphql_name='filter')
    formula = sgqlc.types.Field(String, graphql_name='formula')
    group = sgqlc.types.Field(String, graphql_name='group')
    job_definition_id = sgqlc.types.Field(BigInt, graphql_name='jobDefinitionId')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')
    type = sgqlc.types.Field(String, graphql_name='type')
    type_params = sgqlc.types.Field(JSONObject, graphql_name='typeParams')


class MetricDefinitionNode(sgqlc.types.Type, EnvironmentAppliedNode, EnvironmentDefinitionNode):
    __schema__ = schema
    __field_names__ = ('ancestors', 'children', 'dbt_version', 'filter', 'formula', 'fqn', 'group', 'job_definition_id', 'package_name', 'parents', 'patch_path', 'run_id', 'type', 'type_params')
    ancestors = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='ancestors')
    children = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='children')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    filter = sgqlc.types.Field(JSONObject, graphql_name='filter')
    formula = sgqlc.types.Field(String, graphql_name='formula')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    group = sgqlc.types.Field(String, graphql_name='group')
    job_definition_id = sgqlc.types.Field(BigInt, graphql_name='jobDefinitionId')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    parents = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='parents')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')
    type = sgqlc.types.Field(String, graphql_name='type')
    type_params = sgqlc.types.Field(JSONObject, graphql_name='typeParams')


class MetricLineageNode(sgqlc.types.Type, LineageGraphNode, LineageNode, LineageNodeWithParents):
    __schema__ = schema
    __field_names__ = ()


class MetricNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = ('calculation_method', 'depends_on', 'dimensions', 'environment_name', 'expression', 'filters', 'label', 'model', 'package_name', 'sql', 'time_grains', 'timestamp', 'type')
    calculation_method = sgqlc.types.Field(String, graphql_name='calculation_method')
    depends_on = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='dependsOn')
    dimensions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='dimensions')
    environment_name = sgqlc.types.Field(String, graphql_name='environmentName')
    expression = sgqlc.types.Field(String, graphql_name='expression')
    filters = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MetricFilter))), graphql_name='filters')
    label = sgqlc.types.Field(String, graphql_name='label')
    model = sgqlc.types.Field('ModelNode', graphql_name='model')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    sql = sgqlc.types.Field(String, graphql_name='sql')
    time_grains = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='timeGrains')
    timestamp = sgqlc.types.Field(String, graphql_name='timestamp')
    type = sgqlc.types.Field(String, graphql_name='type')


class ModelAppliedStateNestedNode(sgqlc.types.Type, EnvironmentAppliedNestedNode):
    __schema__ = schema
    __field_names__ = ('access', 'alias', 'contract_enforced', 'database', 'dbt_version', 'execution_info', 'group', 'latest_version', 'materialized_type', 'modeling_layer', 'package_name', 'patch_path', 'release_version', 'schema', 'test_statuses', 'version')
    access = sgqlc.types.Field(String, graphql_name='access')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    contract_enforced = sgqlc.types.Field(Boolean, graphql_name='contractEnforced')
    database = sgqlc.types.Field(String, graphql_name='database')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    execution_info = sgqlc.types.Field(ModelExecutionInfoNode, graphql_name='executionInfo')
    group = sgqlc.types.Field(String, graphql_name='group')
    latest_version = sgqlc.types.Field(String, graphql_name='latestVersion')
    materialized_type = sgqlc.types.Field(String, graphql_name='materializedType')
    modeling_layer = sgqlc.types.Field(String, graphql_name='modelingLayer')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    release_version = sgqlc.types.Field(ReleaseVersion, graphql_name='releaseVersion')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    test_statuses = sgqlc.types.Field(sgqlc.types.non_null(JSONObject), graphql_name='testStatuses')
    version = sgqlc.types.Field(String, graphql_name='version')


class ModelAppliedStateNode(sgqlc.types.Type, EnvironmentAppliedNode):
    __schema__ = schema
    __field_names__ = ('access', 'alias', 'ancestors', 'catalog', 'children', 'compiled_code', 'config', 'constraints', 'contract_enforced', 'database', 'dbt_version', 'deprecation_date', 'execution_info', 'fqn', 'group', 'is_description_inherited', 'language', 'latest_version', 'materialized_type', 'modeling_layer', 'package_name', 'packages', 'parents', 'patch_path', 'raw_code', 'release_version', 'schema', 'tests', 'version', 'versions')
    access = sgqlc.types.Field(String, graphql_name='access')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    ancestors = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentAppliedNestedNode))), graphql_name='ancestors', args=sgqlc.types.ArgDict((
        ('types', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(AncestorNodeType))), graphql_name='types', default=None)),
))
    )
    catalog = sgqlc.types.Field(CatalogNode, graphql_name='catalog')
    children = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentAppliedNestedNode))), graphql_name='children')
    compiled_code = sgqlc.types.Field(String, graphql_name='compiledCode')
    config = sgqlc.types.Field(JSONObject, graphql_name='config')
    constraints = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelLevelConstraint))), graphql_name='constraints')
    contract_enforced = sgqlc.types.Field(Boolean, graphql_name='contractEnforced')
    database = sgqlc.types.Field(String, graphql_name='database')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    deprecation_date = sgqlc.types.Field(DateTime, graphql_name='deprecationDate')
    execution_info = sgqlc.types.Field(ModelExecutionInfoNode, graphql_name='executionInfo')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    group = sgqlc.types.Field(String, graphql_name='group')
    is_description_inherited = sgqlc.types.Field(Boolean, graphql_name='isDescriptionInherited')
    language = sgqlc.types.Field(String, graphql_name='language')
    latest_version = sgqlc.types.Field(String, graphql_name='latestVersion')
    materialized_type = sgqlc.types.Field(String, graphql_name='materializedType')
    modeling_layer = sgqlc.types.Field(String, graphql_name='modelingLayer')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    packages = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='packages')
    parents = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentAppliedNestedNode))), graphql_name='parents')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    raw_code = sgqlc.types.Field(String, graphql_name='rawCode')
    release_version = sgqlc.types.Field(ReleaseVersion, graphql_name='releaseVersion')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    tests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TestAppliedStateNestedNode'))), graphql_name='tests')
    version = sgqlc.types.Field(String, graphql_name='version')
    versions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelVersion))), graphql_name='versions')


class ModelDefinitionNestedNode(sgqlc.types.Type, EnvironmentDefinitionNestedNode):
    __schema__ = schema
    __field_names__ = ('access', 'alias', 'contract_enforced', 'database', 'group', 'job_definition_id', 'latest_version', 'materialized_type', 'package_name', 'patch_path', 'release_version', 'run_id', 'schema', 'version')
    access = sgqlc.types.Field(String, graphql_name='access')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    contract_enforced = sgqlc.types.Field(Boolean, graphql_name='contractEnforced')
    database = sgqlc.types.Field(String, graphql_name='database')
    group = sgqlc.types.Field(String, graphql_name='group')
    job_definition_id = sgqlc.types.Field(BigInt, graphql_name='jobDefinitionId')
    latest_version = sgqlc.types.Field(String, graphql_name='latestVersion')
    materialized_type = sgqlc.types.Field(String, graphql_name='materializedType')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    release_version = sgqlc.types.Field(ReleaseVersion, graphql_name='releaseVersion')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    version = sgqlc.types.Field(String, graphql_name='version')


class ModelDefinitionNode(sgqlc.types.Type, EnvironmentDefinitionNode):
    __schema__ = schema
    __field_names__ = ('access', 'alias', 'ancestors', 'children', 'constraints', 'contract_enforced', 'database', 'deprecation_date', 'fqn', 'group', 'job_definition_id', 'language', 'latest_version', 'materialized_type', 'modeling_layer', 'package_name', 'packages', 'parents', 'patch_path', 'raw_code', 'release_version', 'run_id', 'schema', 'tests', 'version')
    access = sgqlc.types.Field(String, graphql_name='access')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    ancestors = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='ancestors', args=sgqlc.types.ArgDict((
        ('types', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(AncestorNodeType))), graphql_name='types', default=None)),
))
    )
    children = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='children')
    constraints = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelLevelConstraint))), graphql_name='constraints')
    contract_enforced = sgqlc.types.Field(Boolean, graphql_name='contractEnforced')
    database = sgqlc.types.Field(String, graphql_name='database')
    deprecation_date = sgqlc.types.Field(DateTime, graphql_name='deprecationDate')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    group = sgqlc.types.Field(String, graphql_name='group')
    job_definition_id = sgqlc.types.Field(BigInt, graphql_name='jobDefinitionId')
    language = sgqlc.types.Field(String, graphql_name='language')
    latest_version = sgqlc.types.Field(String, graphql_name='latestVersion')
    materialized_type = sgqlc.types.Field(String, graphql_name='materializedType')
    modeling_layer = sgqlc.types.Field(String, graphql_name='modelingLayer')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    packages = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='packages')
    parents = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='parents')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    raw_code = sgqlc.types.Field(String, graphql_name='rawCode')
    release_version = sgqlc.types.Field(ReleaseVersion, graphql_name='releaseVersion')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    tests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TestDefinitionNestedNode'))), graphql_name='tests')
    version = sgqlc.types.Field(String, graphql_name='version')


class ModelLineageNode(sgqlc.types.Type, LineageGraphNode, LineageNode, LineageNodeExecutable, LineageNodeTestable, LineageNodeWithParents):
    __schema__ = schema
    __field_names__ = ('modeling_layer',)
    modeling_layer = sgqlc.types.Field(String, graphql_name='modelingLayer')


class ModelNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = ('access', 'alias', 'args', 'children_l1', 'columns', 'comment', 'compile_completed_at', 'compile_started_at', 'compiled_code', 'compiled_sql', 'database', 'dbt_group', 'depends_on', 'error', 'execute_completed_at', 'execute_started_at', 'execution_time', 'invocation_id', 'language', 'materialized_type', 'owner', 'package_name', 'packages', 'parents_models', 'parents_sources', 'raw_code', 'raw_sql', 'run_elapsed_time', 'run_generated_at', 'run_results', 'schema', 'skip', 'stats', 'status', 'tests', 'thread_id', 'type')
    access = sgqlc.types.Field(String, graphql_name='access')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    args = sgqlc.types.Field(String, graphql_name='args')
    children_l1 = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='childrenL1')
    columns = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CatalogColumn)), graphql_name='columns')
    comment = sgqlc.types.Field(String, graphql_name='comment')
    compile_completed_at = sgqlc.types.Field(DateTime, graphql_name='compileCompletedAt')
    compile_started_at = sgqlc.types.Field(DateTime, graphql_name='compileStartedAt')
    compiled_code = sgqlc.types.Field(String, graphql_name='compiledCode')
    compiled_sql = sgqlc.types.Field(String, graphql_name='compiledSql')
    database = sgqlc.types.Field(String, graphql_name='database')
    dbt_group = sgqlc.types.Field(String, graphql_name='dbtGroup')
    depends_on = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='dependsOn')
    error = sgqlc.types.Field(String, graphql_name='error')
    execute_completed_at = sgqlc.types.Field(DateTime, graphql_name='executeCompletedAt')
    execute_started_at = sgqlc.types.Field(DateTime, graphql_name='executeStartedAt')
    execution_time = sgqlc.types.Field(Float, graphql_name='executionTime')
    invocation_id = sgqlc.types.Field(String, graphql_name='invocationId')
    language = sgqlc.types.Field(String, graphql_name='language')
    materialized_type = sgqlc.types.Field(String, graphql_name='materializedType')
    owner = sgqlc.types.Field(String, graphql_name='owner')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    packages = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='packages')
    parents_models = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelNode'))), graphql_name='parentsModels')
    parents_sources = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SourceNode'))), graphql_name='parentsSources')
    raw_code = sgqlc.types.Field(String, graphql_name='rawCode')
    raw_sql = sgqlc.types.Field(String, graphql_name='rawSql')
    run_elapsed_time = sgqlc.types.Field(Float, graphql_name='runElapsedTime')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')
    run_results = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(RunInfoNode))), graphql_name='runResults')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    skip = sgqlc.types.Field(Boolean, graphql_name='skip')
    stats = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CatalogStat))), graphql_name='stats')
    status = sgqlc.types.Field(String, graphql_name='status')
    tests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TestNode'))), graphql_name='tests')
    thread_id = sgqlc.types.Field(String, graphql_name='threadId')
    type = sgqlc.types.Field(String, graphql_name='type')


class SavedQueryDefinitionNestedNode(sgqlc.types.Type, EnvironmentAppliedNestedNode, EnvironmentDefinitionNestedNode):
    __schema__ = schema
    __field_names__ = ('dbt_version', 'exports', 'group', 'job_definition_id', 'package_name', 'query_params', 'run_id')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    exports = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(QueryExports))), graphql_name='exports')
    group = sgqlc.types.Field(String, graphql_name='group')
    job_definition_id = sgqlc.types.Field(BigInt, graphql_name='jobDefinitionId')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    query_params = sgqlc.types.Field(sgqlc.types.non_null(QueryParams), graphql_name='queryParams')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')


class SavedQueryDefinitionNode(sgqlc.types.Type, EnvironmentAppliedNode, EnvironmentDefinitionNode):
    __schema__ = schema
    __field_names__ = ('ancestors', 'children', 'dbt_version', 'exports', 'fqn', 'group', 'job_definition_id', 'package_name', 'parents', 'query_params', 'run_id')
    ancestors = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='ancestors')
    children = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='children')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    exports = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(QueryExports))), graphql_name='exports')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    group = sgqlc.types.Field(String, graphql_name='group')
    job_definition_id = sgqlc.types.Field(BigInt, graphql_name='jobDefinitionId')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    parents = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='parents')
    query_params = sgqlc.types.Field(sgqlc.types.non_null(QueryParams), graphql_name='queryParams')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')


class SavedQueryLineageNode(sgqlc.types.Type, LineageGraphNode, LineageNode, LineageNodeWithParents):
    __schema__ = schema
    __field_names__ = ()


class SeedAppliedStateNestedNode(sgqlc.types.Type, EnvironmentAppliedNestedNode):
    __schema__ = schema
    __field_names__ = ('alias', 'database', 'dbt_version', 'execution_info', 'package_name', 'patch_path', 'schema')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    database = sgqlc.types.Field(String, graphql_name='database')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    execution_info = sgqlc.types.Field(sgqlc.types.non_null(SeedExecutionInfoNode), graphql_name='executionInfo')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    schema = sgqlc.types.Field(String, graphql_name='schema')


class SeedAppliedStateNode(sgqlc.types.Type, EnvironmentAppliedNode):
    __schema__ = schema
    __field_names__ = ('alias', 'catalog', 'children', 'database', 'dbt_version', 'execution_info', 'fqn', 'package_name', 'patch_path', 'schema', 'tests')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    catalog = sgqlc.types.Field(CatalogNode, graphql_name='catalog')
    children = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentAppliedNestedNode))), graphql_name='children')
    database = sgqlc.types.Field(String, graphql_name='database')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    execution_info = sgqlc.types.Field(sgqlc.types.non_null(SeedExecutionInfoNode), graphql_name='executionInfo')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    tests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TestAppliedStateNestedNode'))), graphql_name='tests')


class SeedDefinitionNestedNode(sgqlc.types.Type, EnvironmentDefinitionNestedNode):
    __schema__ = schema
    __field_names__ = ('alias', 'database', 'dbt_version', 'job_definition_id', 'package_name', 'patch_path', 'run_id', 'schema')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    database = sgqlc.types.Field(String, graphql_name='database')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    job_definition_id = sgqlc.types.Field(BigInt, graphql_name='jobDefinitionId')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')
    schema = sgqlc.types.Field(String, graphql_name='schema')


class SeedDefinitionNode(sgqlc.types.Type, EnvironmentDefinitionNode):
    __schema__ = schema
    __field_names__ = ('alias', 'children', 'database', 'dbt_version', 'fqn', 'job_definition_id', 'package_name', 'patch_path', 'run_id', 'schema')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    children = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='children')
    database = sgqlc.types.Field(String, graphql_name='database')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    job_definition_id = sgqlc.types.Field(BigInt, graphql_name='jobDefinitionId')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')
    schema = sgqlc.types.Field(String, graphql_name='schema')


class SeedLineageNode(sgqlc.types.Type, LineageGraphNode, LineageNode, LineageNodeExecutable, LineageNodeTestable):
    __schema__ = schema
    __field_names__ = ()


class SeedNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = ('alias', 'children_l1', 'columns', 'comment', 'compile_completed_at', 'compile_started_at', 'compiled_code', 'compiled_sql', 'database', 'error', 'execute_completed_at', 'execute_started_at', 'execution_time', 'owner', 'package_name', 'raw_code', 'raw_sql', 'run_elapsed_time', 'run_generated_at', 'schema', 'skip', 'stats', 'status', 'thread_id', 'type')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    children_l1 = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='childrenL1')
    columns = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CatalogColumn)), graphql_name='columns')
    comment = sgqlc.types.Field(String, graphql_name='comment')
    compile_completed_at = sgqlc.types.Field(DateTime, graphql_name='compileCompletedAt')
    compile_started_at = sgqlc.types.Field(DateTime, graphql_name='compileStartedAt')
    compiled_code = sgqlc.types.Field(String, graphql_name='compiledCode')
    compiled_sql = sgqlc.types.Field(String, graphql_name='compiledSql')
    database = sgqlc.types.Field(String, graphql_name='database')
    error = sgqlc.types.Field(String, graphql_name='error')
    execute_completed_at = sgqlc.types.Field(DateTime, graphql_name='executeCompletedAt')
    execute_started_at = sgqlc.types.Field(DateTime, graphql_name='executeStartedAt')
    execution_time = sgqlc.types.Field(Float, graphql_name='executionTime')
    owner = sgqlc.types.Field(String, graphql_name='owner')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    raw_code = sgqlc.types.Field(String, graphql_name='rawCode')
    raw_sql = sgqlc.types.Field(String, graphql_name='rawSql')
    run_elapsed_time = sgqlc.types.Field(Float, graphql_name='runElapsedTime')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    skip = sgqlc.types.Field(Boolean, graphql_name='skip')
    stats = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CatalogStat))), graphql_name='stats')
    status = sgqlc.types.Field(String, graphql_name='status')
    thread_id = sgqlc.types.Field(String, graphql_name='thread_id')
    type = sgqlc.types.Field(String, graphql_name='type')


class SemanticModelDefinitionNestedNode(sgqlc.types.Type, EnvironmentAppliedNestedNode, EnvironmentDefinitionNestedNode):
    __schema__ = schema
    __field_names__ = ('dbt_version', 'dimensions', 'entities', 'job_definition_id', 'measures', 'package_name', 'patch_path', 'run_id')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    dimensions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(SemanticModelDimension))), graphql_name='dimensions')
    entities = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(SemanticModelEntity))), graphql_name='entities')
    job_definition_id = sgqlc.types.Field(BigInt, graphql_name='jobDefinitionId')
    measures = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(SemanticModelMeasure))), graphql_name='measures')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')


class SemanticModelDefinitionNode(sgqlc.types.Type, EnvironmentAppliedNode, EnvironmentDefinitionNode):
    __schema__ = schema
    __field_names__ = ('ancestors', 'children', 'dbt_version', 'dimensions', 'entities', 'fqn', 'job_definition_id', 'measures', 'package_name', 'parents', 'patch_path', 'run_id')
    ancestors = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='ancestors')
    children = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='children')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    dimensions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(SemanticModelDimension))), graphql_name='dimensions')
    entities = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(SemanticModelEntity))), graphql_name='entities')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    job_definition_id = sgqlc.types.Field(BigInt, graphql_name='jobDefinitionId')
    measures = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(SemanticModelMeasure))), graphql_name='measures')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    parents = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='parents')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')


class SemanticModelLineageNode(sgqlc.types.Type, LineageGraphNode, LineageNode, LineageNodeWithParents):
    __schema__ = schema
    __field_names__ = ()


class SnapshotAppliedStateNestedNode(sgqlc.types.Type, EnvironmentAppliedNestedNode):
    __schema__ = schema
    __field_names__ = ('alias', 'database', 'dbt_version', 'execution_info', 'package_name', 'patch_path', 'schema')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    database = sgqlc.types.Field(String, graphql_name='database')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    execution_info = sgqlc.types.Field(SnapshotExecutionInfoNode, graphql_name='executionInfo')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    schema = sgqlc.types.Field(String, graphql_name='schema')


class SnapshotAppliedStateNode(sgqlc.types.Type, EnvironmentAppliedNode):
    __schema__ = schema
    __field_names__ = ('alias', 'catalog', 'children', 'compiled_code', 'config', 'database', 'dbt_version', 'execution_info', 'fqn', 'package_name', 'parents', 'patch_path', 'raw_code', 'schema', 'tests')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    catalog = sgqlc.types.Field(CatalogNode, graphql_name='catalog')
    children = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentAppliedNestedNode))), graphql_name='children')
    compiled_code = sgqlc.types.Field(String, graphql_name='compiledCode')
    config = sgqlc.types.Field(JSONObject, graphql_name='config')
    database = sgqlc.types.Field(String, graphql_name='database')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    execution_info = sgqlc.types.Field(SnapshotExecutionInfoNode, graphql_name='executionInfo')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    parents = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentAppliedNestedNode))), graphql_name='parents')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    raw_code = sgqlc.types.Field(String, graphql_name='rawCode')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    tests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TestAppliedStateNestedNode'))), graphql_name='tests')


class SnapshotDefinitionNestedNode(sgqlc.types.Type, EnvironmentDefinitionNestedNode):
    __schema__ = schema
    __field_names__ = ('alias', 'database', 'job_definition_id', 'package_name', 'patch_path', 'run_id', 'schema')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    database = sgqlc.types.Field(String, graphql_name='database')
    job_definition_id = sgqlc.types.Field(BigInt, graphql_name='jobDefinitionId')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')
    schema = sgqlc.types.Field(String, graphql_name='schema')


class SnapshotDefinitionNode(sgqlc.types.Type, EnvironmentDefinitionNode):
    __schema__ = schema
    __field_names__ = ('alias', 'children', 'database', 'fqn', 'job_definition_id', 'package_name', 'parents', 'patch_path', 'raw_code', 'run_id', 'schema')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    children = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='children')
    database = sgqlc.types.Field(String, graphql_name='database')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    job_definition_id = sgqlc.types.Field(BigInt, graphql_name='jobDefinitionId')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    parents = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='parents')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    raw_code = sgqlc.types.Field(String, graphql_name='rawCode')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')
    schema = sgqlc.types.Field(String, graphql_name='schema')


class SnapshotLineageNode(sgqlc.types.Type, LineageGraphNode, LineageNode, LineageNodeExecutable, LineageNodeTestable, LineageNodeWithParents):
    __schema__ = schema
    __field_names__ = ()


class SnapshotNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = ('alias', 'children_l1', 'columns', 'comment', 'compile_completed_at', 'compile_started_at', 'compiled_code', 'compiled_sql', 'database', 'error', 'execute_completed_at', 'execute_started_at', 'execution_time', 'owner', 'package_name', 'parents_models', 'parents_sources', 'raw_code', 'raw_sql', 'run_elapsed_time', 'run_generated_at', 'schema', 'skip', 'stats', 'status', 'thread_id', 'type')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    children_l1 = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='childrenL1')
    columns = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CatalogColumn)), graphql_name='columns')
    comment = sgqlc.types.Field(String, graphql_name='comment')
    compile_completed_at = sgqlc.types.Field(DateTime, graphql_name='compileCompletedAt')
    compile_started_at = sgqlc.types.Field(DateTime, graphql_name='compileStartedAt')
    compiled_code = sgqlc.types.Field(String, graphql_name='compiledCode')
    compiled_sql = sgqlc.types.Field(String, graphql_name='compiledSql')
    database = sgqlc.types.Field(String, graphql_name='database')
    error = sgqlc.types.Field(String, graphql_name='error')
    execute_completed_at = sgqlc.types.Field(DateTime, graphql_name='executeCompletedAt')
    execute_started_at = sgqlc.types.Field(DateTime, graphql_name='executeStartedAt')
    execution_time = sgqlc.types.Field(Float, graphql_name='executionTime')
    owner = sgqlc.types.Field(String, graphql_name='owner')
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    parents_models = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelNode))), graphql_name='parentsModels')
    parents_sources = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SourceNode'))), graphql_name='parentsSources')
    raw_code = sgqlc.types.Field(String, graphql_name='rawCode')
    raw_sql = sgqlc.types.Field(String, graphql_name='rawSql')
    run_elapsed_time = sgqlc.types.Field(Float, graphql_name='runElapsedTime')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    skip = sgqlc.types.Field(Boolean, graphql_name='skip')
    stats = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CatalogStat))), graphql_name='stats')
    status = sgqlc.types.Field(String, graphql_name='status')
    thread_id = sgqlc.types.Field(String, graphql_name='threadId')
    type = sgqlc.types.Field(String, graphql_name='type')


class SourceAppliedStateNestedNode(sgqlc.types.Type, EnvironmentAppliedNestedNode):
    __schema__ = schema
    __field_names__ = ('database', 'dbt_version', 'freshness', 'identifier', 'loader', 'patch_path', 'schema', 'source_description', 'source_name', 'test_statuses')
    database = sgqlc.types.Field(String, graphql_name='database')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    freshness = sgqlc.types.Field(sgqlc.types.non_null(SourceFreshnessNode), graphql_name='freshness')
    identifier = sgqlc.types.Field(String, graphql_name='identifier')
    loader = sgqlc.types.Field(String, graphql_name='loader')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    source_description = sgqlc.types.Field(String, graphql_name='sourceDescription')
    source_name = sgqlc.types.Field(String, graphql_name='sourceName')
    test_statuses = sgqlc.types.Field(sgqlc.types.non_null(JSONObject), graphql_name='testStatuses')


class SourceAppliedStateNode(sgqlc.types.Type, EnvironmentAppliedNode):
    __schema__ = schema
    __field_names__ = ('catalog', 'children', 'database', 'dbt_version', 'fqn', 'freshness', 'identifier', 'loader', 'patch_path', 'schema', 'source_description', 'source_name', 'tests')
    catalog = sgqlc.types.Field(CatalogNode, graphql_name='catalog')
    children = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentAppliedNestedNode))), graphql_name='children')
    database = sgqlc.types.Field(String, graphql_name='database')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    freshness = sgqlc.types.Field(sgqlc.types.non_null(SourceFreshnessNode), graphql_name='freshness')
    identifier = sgqlc.types.Field(String, graphql_name='identifier')
    loader = sgqlc.types.Field(String, graphql_name='loader')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    source_description = sgqlc.types.Field(String, graphql_name='sourceDescription')
    source_name = sgqlc.types.Field(String, graphql_name='sourceName')
    tests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TestAppliedStateNestedNode'))), graphql_name='tests')


class SourceDefinitionNestedNode(sgqlc.types.Type, EnvironmentDefinitionNestedNode):
    __schema__ = schema
    __field_names__ = ('database', 'dbt_version', 'identifier', 'loader', 'patch_path', 'schema', 'source_description', 'source_name')
    database = sgqlc.types.Field(String, graphql_name='database')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    identifier = sgqlc.types.Field(String, graphql_name='identifier')
    loader = sgqlc.types.Field(String, graphql_name='loader')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    source_description = sgqlc.types.Field(String, graphql_name='sourceDescription')
    source_name = sgqlc.types.Field(String, graphql_name='sourceName')


class SourceDefinitionNode(sgqlc.types.Type, EnvironmentDefinitionNode):
    __schema__ = schema
    __field_names__ = ('children', 'database', 'dbt_version', 'fqn', 'identifier', 'loader', 'patch_path', 'schema', 'source_description', 'source_name', 'tests')
    children = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='children')
    database = sgqlc.types.Field(String, graphql_name='database')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    identifier = sgqlc.types.Field(String, graphql_name='identifier')
    loader = sgqlc.types.Field(String, graphql_name='loader')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    source_description = sgqlc.types.Field(String, graphql_name='sourceDescription')
    source_name = sgqlc.types.Field(String, graphql_name='sourceName')
    tests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TestDefinitionNestedNode'))), graphql_name='tests')


class SourceLineageNode(sgqlc.types.Type, LineageGraphNode, LineageNode, LineageNodeTestable):
    __schema__ = schema
    __field_names__ = ('source_name',)
    source_name = sgqlc.types.Field(String, graphql_name='sourceName')


class SourceNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = ('children_l1', 'columns', 'comment', 'criteria', 'database', 'freshness_checked', 'identifier', 'loader', 'max_loaded_at', 'max_loaded_at_time_ago_in_s', 'owner', 'run_elapsed_time', 'run_generated_at', 'schema', 'snapshotted_at', 'source_description', 'source_name', 'state', 'stats', 'tests', 'type')
    children_l1 = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='childrenL1')
    columns = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CatalogColumn)), graphql_name='columns')
    comment = sgqlc.types.Field(String, graphql_name='comment')
    criteria = sgqlc.types.Field(sgqlc.types.non_null(Criteria), graphql_name='criteria')
    database = sgqlc.types.Field(String, graphql_name='database')
    freshness_checked = sgqlc.types.Field(Boolean, graphql_name='freshnessChecked')
    identifier = sgqlc.types.Field(String, graphql_name='identifier')
    loader = sgqlc.types.Field(String, graphql_name='loader')
    max_loaded_at = sgqlc.types.Field(DateTime, graphql_name='maxLoadedAt')
    max_loaded_at_time_ago_in_s = sgqlc.types.Field(Float, graphql_name='maxLoadedAtTimeAgoInS')
    owner = sgqlc.types.Field(String, graphql_name='owner')
    run_elapsed_time = sgqlc.types.Field(Float, graphql_name='runElapsedTime')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    snapshotted_at = sgqlc.types.Field(DateTime, graphql_name='snapshottedAt')
    source_description = sgqlc.types.Field(String, graphql_name='sourceDescription')
    source_name = sgqlc.types.Field(String, graphql_name='sourceName')
    state = sgqlc.types.Field(FreshnessStatus, graphql_name='state')
    stats = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CatalogStat))), graphql_name='stats')
    tests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TestNode'))), graphql_name='tests')
    type = sgqlc.types.Field(String, graphql_name='type')


class TestAppliedStateNestedNode(sgqlc.types.Type, EnvironmentAppliedNestedNode):
    __schema__ = schema
    __field_names__ = ('column_name', 'dbt_version', 'execution_info', 'patch_path', 'test_metadata', 'test_type')
    column_name = sgqlc.types.Field(String, graphql_name='columnName')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    execution_info = sgqlc.types.Field(sgqlc.types.non_null(TestExecutionInfoNode), graphql_name='executionInfo')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    test_metadata = sgqlc.types.Field(sgqlc.types.non_null(TestMetadata), graphql_name='testMetadata')
    test_type = sgqlc.types.Field(sgqlc.types.non_null(TestType), graphql_name='testType')


class TestAppliedStateNode(sgqlc.types.Type, EnvironmentAppliedNode):
    __schema__ = schema
    __field_names__ = ('column_name', 'compiled_code', 'config', 'dbt_version', 'event_status', 'execution_info', 'expect', 'fqn', 'given', 'model', 'num_expect_rows', 'num_given', 'num_given_rows', 'overrides', 'parents', 'patch_path', 'raw_code', 'test_metadata', 'test_type', 'tested_node_unique_id', 'this_input_node_unique_id')
    column_name = sgqlc.types.Field(String, graphql_name='columnName')
    compiled_code = sgqlc.types.Field(String, graphql_name='compiledCode')
    config = sgqlc.types.Field(JSONObject, graphql_name='config')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    event_status = sgqlc.types.Field(JSONObject, graphql_name='eventStatus')
    execution_info = sgqlc.types.Field(sgqlc.types.non_null(TestExecutionInfoNode), graphql_name='executionInfo')
    expect = sgqlc.types.Field(JSONObject, graphql_name='expect')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    given = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(JSONObject)), graphql_name='given')
    model = sgqlc.types.Field(String, graphql_name='model')
    num_expect_rows = sgqlc.types.Field(Int, graphql_name='numExpectRows')
    num_given = sgqlc.types.Field(Int, graphql_name='numGiven')
    num_given_rows = sgqlc.types.Field(Int, graphql_name='numGivenRows')
    overrides = sgqlc.types.Field(JSONObject, graphql_name='overrides')
    parents = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentAppliedNestedNode))), graphql_name='parents')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    raw_code = sgqlc.types.Field(String, graphql_name='rawCode')
    test_metadata = sgqlc.types.Field(sgqlc.types.non_null(TestMetadata), graphql_name='testMetadata')
    test_type = sgqlc.types.Field(sgqlc.types.non_null(TestType), graphql_name='testType')
    tested_node_unique_id = sgqlc.types.Field(String, graphql_name='testedNodeUniqueId')
    this_input_node_unique_id = sgqlc.types.Field(String, graphql_name='thisInputNodeUniqueId')


class TestDefinitionNestedNode(sgqlc.types.Type, EnvironmentDefinitionNestedNode):
    __schema__ = schema
    __field_names__ = ('column_name', 'dbt_version', 'job_definition_id', 'patch_path', 'run_id', 'test_type')
    column_name = sgqlc.types.Field(String, graphql_name='columnName')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    job_definition_id = sgqlc.types.Field(BigInt, graphql_name='jobDefinitionId')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')
    test_type = sgqlc.types.Field(TestType, graphql_name='testType')


class TestDefinitionNode(sgqlc.types.Type, EnvironmentDefinitionNode):
    __schema__ = schema
    __field_names__ = ('column_name', 'dbt_version', 'event_status', 'expect', 'fqn', 'given', 'job_definition_id', 'model', 'num_expect_rows', 'num_given', 'num_given_rows', 'overrides', 'parents', 'patch_path', 'raw_code', 'resource', 'run_id', 'test_type', 'tested_node_unique_id', 'this_input_node_unique_id')
    column_name = sgqlc.types.Field(String, graphql_name='columnName')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    event_status = sgqlc.types.Field(sgqlc.types.non_null(JSONObject), graphql_name='eventStatus')
    expect = sgqlc.types.Field(sgqlc.types.non_null(JSONObject), graphql_name='expect')
    fqn = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fqn')
    given = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(JSONObject))), graphql_name='given')
    job_definition_id = sgqlc.types.Field(BigInt, graphql_name='jobDefinitionId')
    model = sgqlc.types.Field(String, graphql_name='model')
    num_expect_rows = sgqlc.types.Field(Int, graphql_name='numExpectRows')
    num_given = sgqlc.types.Field(Int, graphql_name='numGiven')
    num_given_rows = sgqlc.types.Field(Int, graphql_name='numGivenRows')
    overrides = sgqlc.types.Field(sgqlc.types.non_null(JSONObject), graphql_name='overrides')
    parents = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EnvironmentDefinitionNestedNode))), graphql_name='parents')
    patch_path = sgqlc.types.Field(String, graphql_name='patchPath')
    raw_code = sgqlc.types.Field(String, graphql_name='rawCode')
    resource = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='resource')
    run_id = sgqlc.types.Field(BigInt, graphql_name='runId')
    test_type = sgqlc.types.Field(TestType, graphql_name='testType')
    tested_node_unique_id = sgqlc.types.Field(String, graphql_name='testedNodeUniqueId')
    this_input_node_unique_id = sgqlc.types.Field(String, graphql_name='thisInputNodeUniqueId')


class TestLineageNode(sgqlc.types.Type, LineageGraphNode, LineageNode, LineageNodeExecutable, LineageNodeWithParents):
    __schema__ = schema
    __field_names__ = ()


class TestNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = ('column_name', 'compile_completed_at', 'compile_started_at', 'compiled_code', 'compiled_sql', 'depends_on', 'error', 'execute_completed_at', 'execute_started_at', 'execution_time', 'fail', 'invocation_id', 'language', 'raw_code', 'raw_sql', 'run_elapsed_time', 'run_generated_at', 'skip', 'state', 'status', 'thread_id', 'warn')
    column_name = sgqlc.types.Field(String, graphql_name='columnName')
    compile_completed_at = sgqlc.types.Field(DateTime, graphql_name='compileCompletedAt')
    compile_started_at = sgqlc.types.Field(DateTime, graphql_name='compileStartedAt')
    compiled_code = sgqlc.types.Field(String, graphql_name='compiledCode')
    compiled_sql = sgqlc.types.Field(String, graphql_name='compiledSql')
    depends_on = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='dependsOn')
    error = sgqlc.types.Field(String, graphql_name='error')
    execute_completed_at = sgqlc.types.Field(DateTime, graphql_name='executeCompletedAt')
    execute_started_at = sgqlc.types.Field(DateTime, graphql_name='executeStartedAt')
    execution_time = sgqlc.types.Field(Float, graphql_name='executionTime')
    fail = sgqlc.types.Field(Boolean, graphql_name='fail')
    invocation_id = sgqlc.types.Field(String, graphql_name='invocationId')
    language = sgqlc.types.Field(String, graphql_name='language')
    raw_code = sgqlc.types.Field(String, graphql_name='rawCode')
    raw_sql = sgqlc.types.Field(String, graphql_name='rawSql')
    run_elapsed_time = sgqlc.types.Field(Float, graphql_name='runElapsedTime')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')
    skip = sgqlc.types.Field(Boolean, graphql_name='skip')
    state = sgqlc.types.Field(String, graphql_name='state')
    status = sgqlc.types.Field(String, graphql_name='status')
    thread_id = sgqlc.types.Field(String, graphql_name='threadId')
    warn = sgqlc.types.Field(Boolean, graphql_name='warn')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
schema.query_type = Query
schema.mutation_type = None
schema.subscription_type = None

