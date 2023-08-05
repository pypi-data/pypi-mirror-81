import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_7760e8e4,
    CfnTag as _CfnTag_b4661f1a,
    Construct as _Construct_f50a3f53,
    Duration as _Duration_5170c158,
    IInspectable as _IInspectable_051e6ed8,
    IResolvable as _IResolvable_9ceae33e,
    IResource as _IResource_72f7ee7e,
    RemovalPolicy as _RemovalPolicy_5986e9f3,
    Resource as _Resource_884d0774,
    SecretValue as _SecretValue_99478b8b,
    TagManager as _TagManager_2508893f,
    TreeInspector as _TreeInspector_154f5999,
)
from ..assets import FollowMode as _FollowMode_f74e7125
from ..aws_cloudwatch import (
    Metric as _Metric_53e89548,
    MetricOptions as _MetricOptions_ad2c4d5d,
    Unit as _Unit_e1b74f3c,
)
from ..aws_codecommit import IRepository as _IRepository_91f381de
from ..aws_ec2 import (
    Connections as _Connections_231f38b5,
    IConnectable as _IConnectable_a587039f,
    ISecurityGroup as _ISecurityGroup_d72ab8e8,
    IVpc as _IVpc_3795853f,
    SubnetSelection as _SubnetSelection_36a13cd6,
)
from ..aws_ecr import IRepository as _IRepository_aa6e452c
from ..aws_ecr_assets import DockerImageAssetProps as _DockerImageAssetProps_74635209
from ..aws_events import (
    EventPattern as _EventPattern_8aa7b781,
    IRuleTarget as _IRuleTarget_41800a77,
    OnEventOptions as _OnEventOptions_926fbcf9,
    Rule as _Rule_c38e0b39,
)
from ..aws_iam import (
    Grant as _Grant_96af6d2d,
    IGrantable as _IGrantable_0fcfc53a,
    IPrincipal as _IPrincipal_97126874,
    IRole as _IRole_e69bbae4,
    PolicyStatement as _PolicyStatement_f75dc775,
)
from ..aws_kms import IKey as _IKey_3336c79d
from ..aws_s3 import IBucket as _IBucket_25bad983
from ..aws_secretsmanager import ISecret as _ISecret_75279d36


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.ArtifactsConfig",
    jsii_struct_bases=[],
    name_mapping={"artifacts_property": "artifactsProperty"},
)
class ArtifactsConfig:
    def __init__(self, *, artifacts_property: "CfnProject.ArtifactsProperty") -> None:
        """The type returned from {@link IArtifacts#bind}.

        :param artifacts_property: The low-level CloudFormation artifacts property.

        stability
        :stability: experimental
        """
        if isinstance(artifacts_property, dict):
            artifacts_property = CfnProject.ArtifactsProperty(**artifacts_property)
        self._values: typing.Dict[str, typing.Any] = {
            "artifacts_property": artifacts_property,
        }

    @builtins.property
    def artifacts_property(self) -> "CfnProject.ArtifactsProperty":
        """The low-level CloudFormation artifacts property.

        stability
        :stability: experimental
        """
        result = self._values.get("artifacts_property")
        assert result is not None, "Required property 'artifacts_property' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.ArtifactsProps",
    jsii_struct_bases=[],
    name_mapping={"identifier": "identifier"},
)
class ArtifactsProps:
    def __init__(self, *, identifier: typing.Optional[builtins.str] = None) -> None:
        """Properties common to all Artifacts classes.

        :param identifier: The artifact identifier. This property is required on secondary artifacts.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if identifier is not None:
            self._values["identifier"] = identifier

    @builtins.property
    def identifier(self) -> typing.Optional[builtins.str]:
        """The artifact identifier.

        This property is required on secondary artifacts.

        stability
        :stability: experimental
        """
        result = self._values.get("identifier")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.BindToCodePipelineOptions",
    jsii_struct_bases=[],
    name_mapping={"artifact_bucket": "artifactBucket"},
)
class BindToCodePipelineOptions:
    def __init__(self, *, artifact_bucket: _IBucket_25bad983) -> None:
        """The extra options passed to the {@link IProject.bindToCodePipeline} method.

        :param artifact_bucket: The artifact bucket that will be used by the action that invokes this project.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "artifact_bucket": artifact_bucket,
        }

    @builtins.property
    def artifact_bucket(self) -> _IBucket_25bad983:
        """The artifact bucket that will be used by the action that invokes this project.

        stability
        :stability: experimental
        """
        result = self._values.get("artifact_bucket")
        assert result is not None, "Required property 'artifact_bucket' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BindToCodePipelineOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BitBucketSourceCredentials(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.BitBucketSourceCredentials",
):
    """The source credentials used when contacting the BitBucket API.

    **Note**: CodeBuild only allows a single credential for BitBucket
    to be saved in a given AWS account in a given region -
    any attempt to add more than one will result in an error.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::CodeBuild::SourceCredential
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        password: _SecretValue_99478b8b,
        username: _SecretValue_99478b8b,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param password: Your BitBucket application password.
        :param username: Your BitBucket username.

        stability
        :stability: experimental
        """
        props = BitBucketSourceCredentialsProps(password=password, username=username)

        jsii.create(BitBucketSourceCredentials, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.BitBucketSourceCredentialsProps",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class BitBucketSourceCredentialsProps:
    def __init__(
        self,
        *,
        password: _SecretValue_99478b8b,
        username: _SecretValue_99478b8b,
    ) -> None:
        """Construction properties of {@link BitBucketSourceCredentials}.

        :param password: Your BitBucket application password.
        :param username: Your BitBucket username.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> _SecretValue_99478b8b:
        """Your BitBucket application password.

        stability
        :stability: experimental
        """
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return result

    @builtins.property
    def username(self) -> _SecretValue_99478b8b:
        """Your BitBucket username.

        stability
        :stability: experimental
        """
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BitBucketSourceCredentialsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.BucketCacheOptions",
    jsii_struct_bases=[],
    name_mapping={"prefix": "prefix"},
)
class BucketCacheOptions:
    def __init__(self, *, prefix: typing.Optional[builtins.str] = None) -> None:
        """
        :param prefix: The prefix to use to store the cache in the bucket.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        """The prefix to use to store the cache in the bucket.

        stability
        :stability: experimental
        """
        result = self._values.get("prefix")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BucketCacheOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.BuildEnvironment",
    jsii_struct_bases=[],
    name_mapping={
        "build_image": "buildImage",
        "compute_type": "computeType",
        "environment_variables": "environmentVariables",
        "privileged": "privileged",
    },
)
class BuildEnvironment:
    def __init__(
        self,
        *,
        build_image: typing.Optional["IBuildImage"] = None,
        compute_type: typing.Optional["ComputeType"] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, "BuildEnvironmentVariable"]] = None,
        privileged: typing.Optional[builtins.bool] = None,
    ) -> None:
        """
        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if build_image is not None:
            self._values["build_image"] = build_image
        if compute_type is not None:
            self._values["compute_type"] = compute_type
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if privileged is not None:
            self._values["privileged"] = privileged

    @builtins.property
    def build_image(self) -> typing.Optional["IBuildImage"]:
        """The image used for the builds.

        default
        :default: LinuxBuildImage.STANDARD_1_0

        stability
        :stability: experimental
        """
        result = self._values.get("build_image")
        return result

    @builtins.property
    def compute_type(self) -> typing.Optional["ComputeType"]:
        """The type of compute to use for this build.

        See the {@link ComputeType} enum for the possible values.

        default
        :default: taken from {@link #buildImage#defaultComputeType}

        stability
        :stability: experimental
        """
        result = self._values.get("compute_type")
        return result

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "BuildEnvironmentVariable"]]:
        """The environment variables that your builds can use.

        stability
        :stability: experimental
        """
        result = self._values.get("environment_variables")
        return result

    @builtins.property
    def privileged(self) -> typing.Optional[builtins.bool]:
        """Indicates how the project builds Docker images.

        Specify true to enable
        running the Docker daemon inside a Docker container. This value must be
        set to true only if this build project will be used to build Docker
        images, and the specified build environment image is not one provided by
        AWS CodeBuild with Docker support. Otherwise, all associated builds that
        attempt to interact with the Docker daemon will fail.

        default
        :default: false

        stability
        :stability: experimental
        """
        result = self._values.get("privileged")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.BuildEnvironmentVariable",
    jsii_struct_bases=[],
    name_mapping={"value": "value", "type": "type"},
)
class BuildEnvironmentVariable:
    def __init__(
        self,
        *,
        value: typing.Any,
        type: typing.Optional["BuildEnvironmentVariableType"] = None,
    ) -> None:
        """
        :param value: The value of the environment variable (or the name of the parameter in the SSM parameter store.).
        :param type: The type of environment variable. Default: PlainText

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "value": value,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def value(self) -> typing.Any:
        """The value of the environment variable (or the name of the parameter in the SSM parameter store.).

        stability
        :stability: experimental
        """
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return result

    @builtins.property
    def type(self) -> typing.Optional["BuildEnvironmentVariableType"]:
        """The type of environment variable.

        default
        :default: PlainText

        stability
        :stability: experimental
        """
        result = self._values.get("type")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildEnvironmentVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk-experiment.aws_codebuild.BuildEnvironmentVariableType")
class BuildEnvironmentVariableType(enum.Enum):
    """
    stability
    :stability: experimental
    """

    PLAINTEXT = "PLAINTEXT"
    """An environment variable in plaintext format.

    stability
    :stability: experimental
    """
    PARAMETER_STORE = "PARAMETER_STORE"
    """An environment variable stored in Systems Manager Parameter Store.

    stability
    :stability: experimental
    """
    SECRETS_MANAGER = "SECRETS_MANAGER"
    """An environment variable stored in AWS Secrets Manager.

    stability
    :stability: experimental
    """


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.BuildImageBindOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class BuildImageBindOptions:
    def __init__(self) -> None:
        """Optional arguments to {@link IBuildImage.binder} - currently empty.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildImageBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.BuildImageConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class BuildImageConfig:
    def __init__(self) -> None:
        """The return type from {@link IBuildImage.binder} - currently empty.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildImageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BuildSpec(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk-experiment.aws_codebuild.BuildSpec",
):
    """BuildSpec for CodeBuild projects.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _BuildSpecProxy

    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        jsii.create(BuildSpec, self, [])

    @jsii.member(jsii_name="fromObject")
    @builtins.classmethod
    def from_object(
        cls,
        value: typing.Mapping[builtins.str, typing.Any],
    ) -> "BuildSpec":
        """
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromObject", [value])

    @jsii.member(jsii_name="fromSourceFilename")
    @builtins.classmethod
    def from_source_filename(cls, filename: builtins.str) -> "BuildSpec":
        """Use a file from the source as buildspec.

        Use this if you want to use a file different from 'buildspec.yml'`

        :param filename: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromSourceFilename", [filename])

    @jsii.member(jsii_name="toBuildSpec")
    @abc.abstractmethod
    def to_build_spec(self) -> builtins.str:
        """Render the represented BuildSpec.

        stability
        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="isImmediate")
    @abc.abstractmethod
    def is_immediate(self) -> builtins.bool:
        """Whether the buildspec is directly available or deferred until build-time.

        stability
        :stability: experimental
        """
        ...


class _BuildSpecProxy(BuildSpec):
    @jsii.member(jsii_name="toBuildSpec")
    def to_build_spec(self) -> builtins.str:
        """Render the represented BuildSpec.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toBuildSpec", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="isImmediate")
    def is_immediate(self) -> builtins.bool:
        """Whether the buildspec is directly available or deferred until build-time.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isImmediate")


class Cache(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk-experiment.aws_codebuild.Cache",
):
    """Cache options for CodeBuild Project.

    A cache can store reusable pieces of your build environment and use them across multiple builds.

    see
    :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-caching.html
    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _CacheProxy

    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        jsii.create(Cache, self, [])

    @jsii.member(jsii_name="bucket")
    @builtins.classmethod
    def bucket(
        cls,
        bucket: _IBucket_25bad983,
        *,
        prefix: typing.Optional[builtins.str] = None,
    ) -> "Cache":
        """Create an S3 caching strategy.

        :param bucket: the S3 bucket to use for caching.
        :param prefix: The prefix to use to store the cache in the bucket.

        stability
        :stability: experimental
        """
        options = BucketCacheOptions(prefix=prefix)

        return jsii.sinvoke(cls, "bucket", [bucket, options])

    @jsii.member(jsii_name="local")
    @builtins.classmethod
    def local(cls, *modes: "LocalCacheMode") -> "Cache":
        """Create a local caching strategy.

        :param modes: the mode(s) to enable for local caching.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "local", [*modes])

    @jsii.member(jsii_name="none")
    @builtins.classmethod
    def none(cls) -> "Cache":
        """
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "none", [])


class _CacheProxy(Cache):
    pass


@jsii.implements(_IInspectable_051e6ed8)
class CfnProject(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.CfnProject",
):
    """A CloudFormation ``AWS::CodeBuild::Project``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeBuild::Project
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        artifacts: typing.Union["ArtifactsProperty", _IResolvable_9ceae33e],
        environment: typing.Union["EnvironmentProperty", _IResolvable_9ceae33e],
        service_role: builtins.str,
        source: typing.Union["SourceProperty", _IResolvable_9ceae33e],
        badge_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
        build_batch_config: typing.Optional[typing.Union["ProjectBuildBatchConfigProperty", _IResolvable_9ceae33e]] = None,
        cache: typing.Optional[typing.Union["ProjectCacheProperty", _IResolvable_9ceae33e]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        file_system_locations: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ProjectFileSystemLocationProperty", _IResolvable_9ceae33e]]]] = None,
        logs_config: typing.Optional[typing.Union["LogsConfigProperty", _IResolvable_9ceae33e]] = None,
        name: typing.Optional[builtins.str] = None,
        queued_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        secondary_artifacts: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ArtifactsProperty", _IResolvable_9ceae33e]]]] = None,
        secondary_sources: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["SourceProperty", _IResolvable_9ceae33e]]]] = None,
        secondary_source_versions: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ProjectSourceVersionProperty", _IResolvable_9ceae33e]]]] = None,
        source_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
        triggers: typing.Optional[typing.Union["ProjectTriggersProperty", _IResolvable_9ceae33e]] = None,
        vpc_config: typing.Optional[typing.Union["VpcConfigProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Create a new ``AWS::CodeBuild::Project``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param artifacts: ``AWS::CodeBuild::Project.Artifacts``.
        :param environment: ``AWS::CodeBuild::Project.Environment``.
        :param service_role: ``AWS::CodeBuild::Project.ServiceRole``.
        :param source: ``AWS::CodeBuild::Project.Source``.
        :param badge_enabled: ``AWS::CodeBuild::Project.BadgeEnabled``.
        :param build_batch_config: ``AWS::CodeBuild::Project.BuildBatchConfig``.
        :param cache: ``AWS::CodeBuild::Project.Cache``.
        :param description: ``AWS::CodeBuild::Project.Description``.
        :param encryption_key: ``AWS::CodeBuild::Project.EncryptionKey``.
        :param file_system_locations: ``AWS::CodeBuild::Project.FileSystemLocations``.
        :param logs_config: ``AWS::CodeBuild::Project.LogsConfig``.
        :param name: ``AWS::CodeBuild::Project.Name``.
        :param queued_timeout_in_minutes: ``AWS::CodeBuild::Project.QueuedTimeoutInMinutes``.
        :param secondary_artifacts: ``AWS::CodeBuild::Project.SecondaryArtifacts``.
        :param secondary_sources: ``AWS::CodeBuild::Project.SecondarySources``.
        :param secondary_source_versions: ``AWS::CodeBuild::Project.SecondarySourceVersions``.
        :param source_version: ``AWS::CodeBuild::Project.SourceVersion``.
        :param tags: ``AWS::CodeBuild::Project.Tags``.
        :param timeout_in_minutes: ``AWS::CodeBuild::Project.TimeoutInMinutes``.
        :param triggers: ``AWS::CodeBuild::Project.Triggers``.
        :param vpc_config: ``AWS::CodeBuild::Project.VpcConfig``.
        """
        props = CfnProjectProps(
            artifacts=artifacts,
            environment=environment,
            service_role=service_role,
            source=source,
            badge_enabled=badge_enabled,
            build_batch_config=build_batch_config,
            cache=cache,
            description=description,
            encryption_key=encryption_key,
            file_system_locations=file_system_locations,
            logs_config=logs_config,
            name=name,
            queued_timeout_in_minutes=queued_timeout_in_minutes,
            secondary_artifacts=secondary_artifacts,
            secondary_sources=secondary_sources,
            secondary_source_versions=secondary_source_versions,
            source_version=source_version,
            tags=tags,
            timeout_in_minutes=timeout_in_minutes,
            triggers=triggers,
            vpc_config=vpc_config,
        )

        jsii.create(CfnProject, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::CodeBuild::Project.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> typing.Union["ArtifactsProperty", _IResolvable_9ceae33e]:
        """``AWS::CodeBuild::Project.Artifacts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-artifacts
        """
        return jsii.get(self, "artifacts")

    @artifacts.setter # type: ignore
    def artifacts(
        self,
        value: typing.Union["ArtifactsProperty", _IResolvable_9ceae33e],
    ) -> None:
        jsii.set(self, "artifacts", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Union["EnvironmentProperty", _IResolvable_9ceae33e]:
        """``AWS::CodeBuild::Project.Environment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-environment
        """
        return jsii.get(self, "environment")

    @environment.setter # type: ignore
    def environment(
        self,
        value: typing.Union["EnvironmentProperty", _IResolvable_9ceae33e],
    ) -> None:
        jsii.set(self, "environment", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> builtins.str:
        """``AWS::CodeBuild::Project.ServiceRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-servicerole
        """
        return jsii.get(self, "serviceRole")

    @service_role.setter # type: ignore
    def service_role(self, value: builtins.str) -> None:
        jsii.set(self, "serviceRole", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="source")
    def source(self) -> typing.Union["SourceProperty", _IResolvable_9ceae33e]:
        """``AWS::CodeBuild::Project.Source``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-source
        """
        return jsii.get(self, "source")

    @source.setter # type: ignore
    def source(
        self,
        value: typing.Union["SourceProperty", _IResolvable_9ceae33e],
    ) -> None:
        jsii.set(self, "source", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="badgeEnabled")
    def badge_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
        """``AWS::CodeBuild::Project.BadgeEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-badgeenabled
        """
        return jsii.get(self, "badgeEnabled")

    @badge_enabled.setter # type: ignore
    def badge_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "badgeEnabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="buildBatchConfig")
    def build_batch_config(
        self,
    ) -> typing.Optional[typing.Union["ProjectBuildBatchConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeBuild::Project.BuildBatchConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-buildbatchconfig
        """
        return jsii.get(self, "buildBatchConfig")

    @build_batch_config.setter # type: ignore
    def build_batch_config(
        self,
        value: typing.Optional[typing.Union["ProjectBuildBatchConfigProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "buildBatchConfig", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cache")
    def cache(
        self,
    ) -> typing.Optional[typing.Union["ProjectCacheProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeBuild::Project.Cache``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-cache
        """
        return jsii.get(self, "cache")

    @cache.setter # type: ignore
    def cache(
        self,
        value: typing.Optional[typing.Union["ProjectCacheProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "cache", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeBuild::Project.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeBuild::Project.EncryptionKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-encryptionkey
        """
        return jsii.get(self, "encryptionKey")

    @encryption_key.setter # type: ignore
    def encryption_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "encryptionKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="fileSystemLocations")
    def file_system_locations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ProjectFileSystemLocationProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeBuild::Project.FileSystemLocations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-filesystemlocations
        """
        return jsii.get(self, "fileSystemLocations")

    @file_system_locations.setter # type: ignore
    def file_system_locations(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ProjectFileSystemLocationProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "fileSystemLocations", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="logsConfig")
    def logs_config(
        self,
    ) -> typing.Optional[typing.Union["LogsConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeBuild::Project.LogsConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-logsconfig
        """
        return jsii.get(self, "logsConfig")

    @logs_config.setter # type: ignore
    def logs_config(
        self,
        value: typing.Optional[typing.Union["LogsConfigProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "logsConfig", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeBuild::Project.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="queuedTimeoutInMinutes")
    def queued_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CodeBuild::Project.QueuedTimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-queuedtimeoutinminutes
        """
        return jsii.get(self, "queuedTimeoutInMinutes")

    @queued_timeout_in_minutes.setter # type: ignore
    def queued_timeout_in_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "queuedTimeoutInMinutes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secondaryArtifacts")
    def secondary_artifacts(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ArtifactsProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeBuild::Project.SecondaryArtifacts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondaryartifacts
        """
        return jsii.get(self, "secondaryArtifacts")

    @secondary_artifacts.setter # type: ignore
    def secondary_artifacts(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ArtifactsProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "secondaryArtifacts", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secondarySources")
    def secondary_sources(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["SourceProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeBuild::Project.SecondarySources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondarysources
        """
        return jsii.get(self, "secondarySources")

    @secondary_sources.setter # type: ignore
    def secondary_sources(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["SourceProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "secondarySources", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secondarySourceVersions")
    def secondary_source_versions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ProjectSourceVersionProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeBuild::Project.SecondarySourceVersions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondarysourceversions
        """
        return jsii.get(self, "secondarySourceVersions")

    @secondary_source_versions.setter # type: ignore
    def secondary_source_versions(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ProjectSourceVersionProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "secondarySourceVersions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sourceVersion")
    def source_version(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeBuild::Project.SourceVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-sourceversion
        """
        return jsii.get(self, "sourceVersion")

    @source_version.setter # type: ignore
    def source_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sourceVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="timeoutInMinutes")
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CodeBuild::Project.TimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-timeoutinminutes
        """
        return jsii.get(self, "timeoutInMinutes")

    @timeout_in_minutes.setter # type: ignore
    def timeout_in_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "timeoutInMinutes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="triggers")
    def triggers(
        self,
    ) -> typing.Optional[typing.Union["ProjectTriggersProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeBuild::Project.Triggers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-triggers
        """
        return jsii.get(self, "triggers")

    @triggers.setter # type: ignore
    def triggers(
        self,
        value: typing.Optional[typing.Union["ProjectTriggersProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "triggers", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union["VpcConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeBuild::Project.VpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-vpcconfig
        """
        return jsii.get(self, "vpcConfig")

    @vpc_config.setter # type: ignore
    def vpc_config(
        self,
        value: typing.Optional[typing.Union["VpcConfigProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.ArtifactsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "artifact_identifier": "artifactIdentifier",
            "encryption_disabled": "encryptionDisabled",
            "location": "location",
            "name": "name",
            "namespace_type": "namespaceType",
            "override_artifact_name": "overrideArtifactName",
            "packaging": "packaging",
            "path": "path",
        },
    )
    class ArtifactsProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            artifact_identifier: typing.Optional[builtins.str] = None,
            encryption_disabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
            location: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            namespace_type: typing.Optional[builtins.str] = None,
            override_artifact_name: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
            packaging: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param type: ``CfnProject.ArtifactsProperty.Type``.
            :param artifact_identifier: ``CfnProject.ArtifactsProperty.ArtifactIdentifier``.
            :param encryption_disabled: ``CfnProject.ArtifactsProperty.EncryptionDisabled``.
            :param location: ``CfnProject.ArtifactsProperty.Location``.
            :param name: ``CfnProject.ArtifactsProperty.Name``.
            :param namespace_type: ``CfnProject.ArtifactsProperty.NamespaceType``.
            :param override_artifact_name: ``CfnProject.ArtifactsProperty.OverrideArtifactName``.
            :param packaging: ``CfnProject.ArtifactsProperty.Packaging``.
            :param path: ``CfnProject.ArtifactsProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "type": type,
            }
            if artifact_identifier is not None:
                self._values["artifact_identifier"] = artifact_identifier
            if encryption_disabled is not None:
                self._values["encryption_disabled"] = encryption_disabled
            if location is not None:
                self._values["location"] = location
            if name is not None:
                self._values["name"] = name
            if namespace_type is not None:
                self._values["namespace_type"] = namespace_type
            if override_artifact_name is not None:
                self._values["override_artifact_name"] = override_artifact_name
            if packaging is not None:
                self._values["packaging"] = packaging
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnProject.ArtifactsProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def artifact_identifier(self) -> typing.Optional[builtins.str]:
            """``CfnProject.ArtifactsProperty.ArtifactIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-artifactidentifier
            """
            result = self._values.get("artifact_identifier")
            return result

        @builtins.property
        def encryption_disabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnProject.ArtifactsProperty.EncryptionDisabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-encryptiondisabled
            """
            result = self._values.get("encryption_disabled")
            return result

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            """``CfnProject.ArtifactsProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-location
            """
            result = self._values.get("location")
            return result

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """``CfnProject.ArtifactsProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-name
            """
            result = self._values.get("name")
            return result

        @builtins.property
        def namespace_type(self) -> typing.Optional[builtins.str]:
            """``CfnProject.ArtifactsProperty.NamespaceType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-namespacetype
            """
            result = self._values.get("namespace_type")
            return result

        @builtins.property
        def override_artifact_name(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnProject.ArtifactsProperty.OverrideArtifactName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-overrideartifactname
            """
            result = self._values.get("override_artifact_name")
            return result

        @builtins.property
        def packaging(self) -> typing.Optional[builtins.str]:
            """``CfnProject.ArtifactsProperty.Packaging``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-packaging
            """
            result = self._values.get("packaging")
            return result

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            """``CfnProject.ArtifactsProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-path
            """
            result = self._values.get("path")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArtifactsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.BatchRestrictionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compute_types_allowed": "computeTypesAllowed",
            "maximum_builds_allowed": "maximumBuildsAllowed",
        },
    )
    class BatchRestrictionsProperty:
        def __init__(
            self,
            *,
            compute_types_allowed: typing.Optional[typing.List[builtins.str]] = None,
            maximum_builds_allowed: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param compute_types_allowed: ``CfnProject.BatchRestrictionsProperty.ComputeTypesAllowed``.
            :param maximum_builds_allowed: ``CfnProject.BatchRestrictionsProperty.MaximumBuildsAllowed``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-batchrestrictions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if compute_types_allowed is not None:
                self._values["compute_types_allowed"] = compute_types_allowed
            if maximum_builds_allowed is not None:
                self._values["maximum_builds_allowed"] = maximum_builds_allowed

        @builtins.property
        def compute_types_allowed(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnProject.BatchRestrictionsProperty.ComputeTypesAllowed``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-batchrestrictions.html#cfn-codebuild-project-batchrestrictions-computetypesallowed
            """
            result = self._values.get("compute_types_allowed")
            return result

        @builtins.property
        def maximum_builds_allowed(self) -> typing.Optional[jsii.Number]:
            """``CfnProject.BatchRestrictionsProperty.MaximumBuildsAllowed``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-batchrestrictions.html#cfn-codebuild-project-batchrestrictions-maximumbuildsallowed
            """
            result = self._values.get("maximum_builds_allowed")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BatchRestrictionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.BuildStatusConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"context": "context", "target_url": "targetUrl"},
    )
    class BuildStatusConfigProperty:
        def __init__(
            self,
            *,
            context: typing.Optional[builtins.str] = None,
            target_url: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param context: ``CfnProject.BuildStatusConfigProperty.Context``.
            :param target_url: ``CfnProject.BuildStatusConfigProperty.TargetUrl``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-buildstatusconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if context is not None:
                self._values["context"] = context
            if target_url is not None:
                self._values["target_url"] = target_url

        @builtins.property
        def context(self) -> typing.Optional[builtins.str]:
            """``CfnProject.BuildStatusConfigProperty.Context``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-buildstatusconfig.html#cfn-codebuild-project-buildstatusconfig-context
            """
            result = self._values.get("context")
            return result

        @builtins.property
        def target_url(self) -> typing.Optional[builtins.str]:
            """``CfnProject.BuildStatusConfigProperty.TargetUrl``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-buildstatusconfig.html#cfn-codebuild-project-buildstatusconfig-targeturl
            """
            result = self._values.get("target_url")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BuildStatusConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.CloudWatchLogsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "status": "status",
            "group_name": "groupName",
            "stream_name": "streamName",
        },
    )
    class CloudWatchLogsConfigProperty:
        def __init__(
            self,
            *,
            status: builtins.str,
            group_name: typing.Optional[builtins.str] = None,
            stream_name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param status: ``CfnProject.CloudWatchLogsConfigProperty.Status``.
            :param group_name: ``CfnProject.CloudWatchLogsConfigProperty.GroupName``.
            :param stream_name: ``CfnProject.CloudWatchLogsConfigProperty.StreamName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "status": status,
            }
            if group_name is not None:
                self._values["group_name"] = group_name
            if stream_name is not None:
                self._values["stream_name"] = stream_name

        @builtins.property
        def status(self) -> builtins.str:
            """``CfnProject.CloudWatchLogsConfigProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html#cfn-codebuild-project-cloudwatchlogsconfig-status
            """
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return result

        @builtins.property
        def group_name(self) -> typing.Optional[builtins.str]:
            """``CfnProject.CloudWatchLogsConfigProperty.GroupName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html#cfn-codebuild-project-cloudwatchlogsconfig-groupname
            """
            result = self._values.get("group_name")
            return result

        @builtins.property
        def stream_name(self) -> typing.Optional[builtins.str]:
            """``CfnProject.CloudWatchLogsConfigProperty.StreamName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html#cfn-codebuild-project-cloudwatchlogsconfig-streamname
            """
            result = self._values.get("stream_name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.EnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compute_type": "computeType",
            "image": "image",
            "type": "type",
            "certificate": "certificate",
            "environment_variables": "environmentVariables",
            "image_pull_credentials_type": "imagePullCredentialsType",
            "privileged_mode": "privilegedMode",
            "registry_credential": "registryCredential",
        },
    )
    class EnvironmentProperty:
        def __init__(
            self,
            *,
            compute_type: builtins.str,
            image: builtins.str,
            type: builtins.str,
            certificate: typing.Optional[builtins.str] = None,
            environment_variables: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnProject.EnvironmentVariableProperty", _IResolvable_9ceae33e]]]] = None,
            image_pull_credentials_type: typing.Optional[builtins.str] = None,
            privileged_mode: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
            registry_credential: typing.Optional[typing.Union["CfnProject.RegistryCredentialProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param compute_type: ``CfnProject.EnvironmentProperty.ComputeType``.
            :param image: ``CfnProject.EnvironmentProperty.Image``.
            :param type: ``CfnProject.EnvironmentProperty.Type``.
            :param certificate: ``CfnProject.EnvironmentProperty.Certificate``.
            :param environment_variables: ``CfnProject.EnvironmentProperty.EnvironmentVariables``.
            :param image_pull_credentials_type: ``CfnProject.EnvironmentProperty.ImagePullCredentialsType``.
            :param privileged_mode: ``CfnProject.EnvironmentProperty.PrivilegedMode``.
            :param registry_credential: ``CfnProject.EnvironmentProperty.RegistryCredential``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "compute_type": compute_type,
                "image": image,
                "type": type,
            }
            if certificate is not None:
                self._values["certificate"] = certificate
            if environment_variables is not None:
                self._values["environment_variables"] = environment_variables
            if image_pull_credentials_type is not None:
                self._values["image_pull_credentials_type"] = image_pull_credentials_type
            if privileged_mode is not None:
                self._values["privileged_mode"] = privileged_mode
            if registry_credential is not None:
                self._values["registry_credential"] = registry_credential

        @builtins.property
        def compute_type(self) -> builtins.str:
            """``CfnProject.EnvironmentProperty.ComputeType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-computetype
            """
            result = self._values.get("compute_type")
            assert result is not None, "Required property 'compute_type' is missing"
            return result

        @builtins.property
        def image(self) -> builtins.str:
            """``CfnProject.EnvironmentProperty.Image``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-image
            """
            result = self._values.get("image")
            assert result is not None, "Required property 'image' is missing"
            return result

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnProject.EnvironmentProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def certificate(self) -> typing.Optional[builtins.str]:
            """``CfnProject.EnvironmentProperty.Certificate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-certificate
            """
            result = self._values.get("certificate")
            return result

        @builtins.property
        def environment_variables(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnProject.EnvironmentVariableProperty", _IResolvable_9ceae33e]]]]:
            """``CfnProject.EnvironmentProperty.EnvironmentVariables``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-environmentvariables
            """
            result = self._values.get("environment_variables")
            return result

        @builtins.property
        def image_pull_credentials_type(self) -> typing.Optional[builtins.str]:
            """``CfnProject.EnvironmentProperty.ImagePullCredentialsType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-imagepullcredentialstype
            """
            result = self._values.get("image_pull_credentials_type")
            return result

        @builtins.property
        def privileged_mode(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnProject.EnvironmentProperty.PrivilegedMode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-privilegedmode
            """
            result = self._values.get("privileged_mode")
            return result

        @builtins.property
        def registry_credential(
            self,
        ) -> typing.Optional[typing.Union["CfnProject.RegistryCredentialProperty", _IResolvable_9ceae33e]]:
            """``CfnProject.EnvironmentProperty.RegistryCredential``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-registrycredential
            """
            result = self._values.get("registry_credential")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.EnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value", "type": "type"},
    )
    class EnvironmentVariableProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            value: builtins.str,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param name: ``CfnProject.EnvironmentVariableProperty.Name``.
            :param value: ``CfnProject.EnvironmentVariableProperty.Value``.
            :param type: ``CfnProject.EnvironmentVariableProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "value": value,
            }
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnProject.EnvironmentVariableProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html#cfn-codebuild-project-environmentvariable-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnProject.EnvironmentVariableProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html#cfn-codebuild-project-environmentvariable-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            """``CfnProject.EnvironmentVariableProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html#cfn-codebuild-project-environmentvariable-type
            """
            result = self._values.get("type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.GitSubmodulesConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"fetch_submodules": "fetchSubmodules"},
    )
    class GitSubmodulesConfigProperty:
        def __init__(
            self,
            *,
            fetch_submodules: typing.Union[builtins.bool, _IResolvable_9ceae33e],
        ) -> None:
            """
            :param fetch_submodules: ``CfnProject.GitSubmodulesConfigProperty.FetchSubmodules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-gitsubmodulesconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "fetch_submodules": fetch_submodules,
            }

        @builtins.property
        def fetch_submodules(
            self,
        ) -> typing.Union[builtins.bool, _IResolvable_9ceae33e]:
            """``CfnProject.GitSubmodulesConfigProperty.FetchSubmodules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-gitsubmodulesconfig.html#cfn-codebuild-project-gitsubmodulesconfig-fetchsubmodules
            """
            result = self._values.get("fetch_submodules")
            assert result is not None, "Required property 'fetch_submodules' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitSubmodulesConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.LogsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_logs": "cloudWatchLogs", "s3_logs": "s3Logs"},
    )
    class LogsConfigProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs: typing.Optional[typing.Union["CfnProject.CloudWatchLogsConfigProperty", _IResolvable_9ceae33e]] = None,
            s3_logs: typing.Optional[typing.Union["CfnProject.S3LogsConfigProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param cloud_watch_logs: ``CfnProject.LogsConfigProperty.CloudWatchLogs``.
            :param s3_logs: ``CfnProject.LogsConfigProperty.S3Logs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-logsconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if cloud_watch_logs is not None:
                self._values["cloud_watch_logs"] = cloud_watch_logs
            if s3_logs is not None:
                self._values["s3_logs"] = s3_logs

        @builtins.property
        def cloud_watch_logs(
            self,
        ) -> typing.Optional[typing.Union["CfnProject.CloudWatchLogsConfigProperty", _IResolvable_9ceae33e]]:
            """``CfnProject.LogsConfigProperty.CloudWatchLogs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-logsconfig.html#cfn-codebuild-project-logsconfig-cloudwatchlogs
            """
            result = self._values.get("cloud_watch_logs")
            return result

        @builtins.property
        def s3_logs(
            self,
        ) -> typing.Optional[typing.Union["CfnProject.S3LogsConfigProperty", _IResolvable_9ceae33e]]:
            """``CfnProject.LogsConfigProperty.S3Logs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-logsconfig.html#cfn-codebuild-project-logsconfig-s3logs
            """
            result = self._values.get("s3_logs")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.ProjectBuildBatchConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "combine_artifacts": "combineArtifacts",
            "restrictions": "restrictions",
            "service_role": "serviceRole",
            "timeout_in_mins": "timeoutInMins",
        },
    )
    class ProjectBuildBatchConfigProperty:
        def __init__(
            self,
            *,
            combine_artifacts: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
            restrictions: typing.Optional[typing.Union["CfnProject.BatchRestrictionsProperty", _IResolvable_9ceae33e]] = None,
            service_role: typing.Optional[builtins.str] = None,
            timeout_in_mins: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param combine_artifacts: ``CfnProject.ProjectBuildBatchConfigProperty.CombineArtifacts``.
            :param restrictions: ``CfnProject.ProjectBuildBatchConfigProperty.Restrictions``.
            :param service_role: ``CfnProject.ProjectBuildBatchConfigProperty.ServiceRole``.
            :param timeout_in_mins: ``CfnProject.ProjectBuildBatchConfigProperty.TimeoutInMins``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectbuildbatchconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if combine_artifacts is not None:
                self._values["combine_artifacts"] = combine_artifacts
            if restrictions is not None:
                self._values["restrictions"] = restrictions
            if service_role is not None:
                self._values["service_role"] = service_role
            if timeout_in_mins is not None:
                self._values["timeout_in_mins"] = timeout_in_mins

        @builtins.property
        def combine_artifacts(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnProject.ProjectBuildBatchConfigProperty.CombineArtifacts``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectbuildbatchconfig.html#cfn-codebuild-project-projectbuildbatchconfig-combineartifacts
            """
            result = self._values.get("combine_artifacts")
            return result

        @builtins.property
        def restrictions(
            self,
        ) -> typing.Optional[typing.Union["CfnProject.BatchRestrictionsProperty", _IResolvable_9ceae33e]]:
            """``CfnProject.ProjectBuildBatchConfigProperty.Restrictions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectbuildbatchconfig.html#cfn-codebuild-project-projectbuildbatchconfig-restrictions
            """
            result = self._values.get("restrictions")
            return result

        @builtins.property
        def service_role(self) -> typing.Optional[builtins.str]:
            """``CfnProject.ProjectBuildBatchConfigProperty.ServiceRole``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectbuildbatchconfig.html#cfn-codebuild-project-projectbuildbatchconfig-servicerole
            """
            result = self._values.get("service_role")
            return result

        @builtins.property
        def timeout_in_mins(self) -> typing.Optional[jsii.Number]:
            """``CfnProject.ProjectBuildBatchConfigProperty.TimeoutInMins``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectbuildbatchconfig.html#cfn-codebuild-project-projectbuildbatchconfig-timeoutinmins
            """
            result = self._values.get("timeout_in_mins")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectBuildBatchConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.ProjectCacheProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "location": "location", "modes": "modes"},
    )
    class ProjectCacheProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            location: typing.Optional[builtins.str] = None,
            modes: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param type: ``CfnProject.ProjectCacheProperty.Type``.
            :param location: ``CfnProject.ProjectCacheProperty.Location``.
            :param modes: ``CfnProject.ProjectCacheProperty.Modes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "type": type,
            }
            if location is not None:
                self._values["location"] = location
            if modes is not None:
                self._values["modes"] = modes

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnProject.ProjectCacheProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html#cfn-codebuild-project-projectcache-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            """``CfnProject.ProjectCacheProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html#cfn-codebuild-project-projectcache-location
            """
            result = self._values.get("location")
            return result

        @builtins.property
        def modes(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnProject.ProjectCacheProperty.Modes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html#cfn-codebuild-project-projectcache-modes
            """
            result = self._values.get("modes")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectCacheProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.ProjectFileSystemLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "identifier": "identifier",
            "location": "location",
            "mount_point": "mountPoint",
            "type": "type",
            "mount_options": "mountOptions",
        },
    )
    class ProjectFileSystemLocationProperty:
        def __init__(
            self,
            *,
            identifier: builtins.str,
            location: builtins.str,
            mount_point: builtins.str,
            type: builtins.str,
            mount_options: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param identifier: ``CfnProject.ProjectFileSystemLocationProperty.Identifier``.
            :param location: ``CfnProject.ProjectFileSystemLocationProperty.Location``.
            :param mount_point: ``CfnProject.ProjectFileSystemLocationProperty.MountPoint``.
            :param type: ``CfnProject.ProjectFileSystemLocationProperty.Type``.
            :param mount_options: ``CfnProject.ProjectFileSystemLocationProperty.MountOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "identifier": identifier,
                "location": location,
                "mount_point": mount_point,
                "type": type,
            }
            if mount_options is not None:
                self._values["mount_options"] = mount_options

        @builtins.property
        def identifier(self) -> builtins.str:
            """``CfnProject.ProjectFileSystemLocationProperty.Identifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html#cfn-codebuild-project-projectfilesystemlocation-identifier
            """
            result = self._values.get("identifier")
            assert result is not None, "Required property 'identifier' is missing"
            return result

        @builtins.property
        def location(self) -> builtins.str:
            """``CfnProject.ProjectFileSystemLocationProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html#cfn-codebuild-project-projectfilesystemlocation-location
            """
            result = self._values.get("location")
            assert result is not None, "Required property 'location' is missing"
            return result

        @builtins.property
        def mount_point(self) -> builtins.str:
            """``CfnProject.ProjectFileSystemLocationProperty.MountPoint``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html#cfn-codebuild-project-projectfilesystemlocation-mountpoint
            """
            result = self._values.get("mount_point")
            assert result is not None, "Required property 'mount_point' is missing"
            return result

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnProject.ProjectFileSystemLocationProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html#cfn-codebuild-project-projectfilesystemlocation-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def mount_options(self) -> typing.Optional[builtins.str]:
            """``CfnProject.ProjectFileSystemLocationProperty.MountOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html#cfn-codebuild-project-projectfilesystemlocation-mountoptions
            """
            result = self._values.get("mount_options")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectFileSystemLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.ProjectSourceVersionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source_identifier": "sourceIdentifier",
            "source_version": "sourceVersion",
        },
    )
    class ProjectSourceVersionProperty:
        def __init__(
            self,
            *,
            source_identifier: builtins.str,
            source_version: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param source_identifier: ``CfnProject.ProjectSourceVersionProperty.SourceIdentifier``.
            :param source_version: ``CfnProject.ProjectSourceVersionProperty.SourceVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectsourceversion.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "source_identifier": source_identifier,
            }
            if source_version is not None:
                self._values["source_version"] = source_version

        @builtins.property
        def source_identifier(self) -> builtins.str:
            """``CfnProject.ProjectSourceVersionProperty.SourceIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectsourceversion.html#cfn-codebuild-project-projectsourceversion-sourceidentifier
            """
            result = self._values.get("source_identifier")
            assert result is not None, "Required property 'source_identifier' is missing"
            return result

        @builtins.property
        def source_version(self) -> typing.Optional[builtins.str]:
            """``CfnProject.ProjectSourceVersionProperty.SourceVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectsourceversion.html#cfn-codebuild-project-projectsourceversion-sourceversion
            """
            result = self._values.get("source_version")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectSourceVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.ProjectTriggersProperty",
        jsii_struct_bases=[],
        name_mapping={"filter_groups": "filterGroups", "webhook": "webhook"},
    )
    class ProjectTriggersProperty:
        def __init__(
            self,
            *,
            filter_groups: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnProject.WebhookFilterProperty", _IResolvable_9ceae33e]]]]]] = None,
            webhook: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param filter_groups: ``CfnProject.ProjectTriggersProperty.FilterGroups``.
            :param webhook: ``CfnProject.ProjectTriggersProperty.Webhook``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if filter_groups is not None:
                self._values["filter_groups"] = filter_groups
            if webhook is not None:
                self._values["webhook"] = webhook

        @builtins.property
        def filter_groups(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnProject.WebhookFilterProperty", _IResolvable_9ceae33e]]]]]]:
            """``CfnProject.ProjectTriggersProperty.FilterGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html#cfn-codebuild-project-projecttriggers-filtergroups
            """
            result = self._values.get("filter_groups")
            return result

        @builtins.property
        def webhook(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnProject.ProjectTriggersProperty.Webhook``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html#cfn-codebuild-project-projecttriggers-webhook
            """
            result = self._values.get("webhook")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectTriggersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.RegistryCredentialProperty",
        jsii_struct_bases=[],
        name_mapping={
            "credential": "credential",
            "credential_provider": "credentialProvider",
        },
    )
    class RegistryCredentialProperty:
        def __init__(
            self,
            *,
            credential: builtins.str,
            credential_provider: builtins.str,
        ) -> None:
            """
            :param credential: ``CfnProject.RegistryCredentialProperty.Credential``.
            :param credential_provider: ``CfnProject.RegistryCredentialProperty.CredentialProvider``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-registrycredential.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "credential": credential,
                "credential_provider": credential_provider,
            }

        @builtins.property
        def credential(self) -> builtins.str:
            """``CfnProject.RegistryCredentialProperty.Credential``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-registrycredential.html#cfn-codebuild-project-registrycredential-credential
            """
            result = self._values.get("credential")
            assert result is not None, "Required property 'credential' is missing"
            return result

        @builtins.property
        def credential_provider(self) -> builtins.str:
            """``CfnProject.RegistryCredentialProperty.CredentialProvider``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-registrycredential.html#cfn-codebuild-project-registrycredential-credentialprovider
            """
            result = self._values.get("credential_provider")
            assert result is not None, "Required property 'credential_provider' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegistryCredentialProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.S3LogsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "status": "status",
            "encryption_disabled": "encryptionDisabled",
            "location": "location",
        },
    )
    class S3LogsConfigProperty:
        def __init__(
            self,
            *,
            status: builtins.str,
            encryption_disabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
            location: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param status: ``CfnProject.S3LogsConfigProperty.Status``.
            :param encryption_disabled: ``CfnProject.S3LogsConfigProperty.EncryptionDisabled``.
            :param location: ``CfnProject.S3LogsConfigProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "status": status,
            }
            if encryption_disabled is not None:
                self._values["encryption_disabled"] = encryption_disabled
            if location is not None:
                self._values["location"] = location

        @builtins.property
        def status(self) -> builtins.str:
            """``CfnProject.S3LogsConfigProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html#cfn-codebuild-project-s3logsconfig-status
            """
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return result

        @builtins.property
        def encryption_disabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnProject.S3LogsConfigProperty.EncryptionDisabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html#cfn-codebuild-project-s3logsconfig-encryptiondisabled
            """
            result = self._values.get("encryption_disabled")
            return result

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            """``CfnProject.S3LogsConfigProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html#cfn-codebuild-project-s3logsconfig-location
            """
            result = self._values.get("location")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LogsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.SourceAuthProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "resource": "resource"},
    )
    class SourceAuthProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            resource: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param type: ``CfnProject.SourceAuthProperty.Type``.
            :param resource: ``CfnProject.SourceAuthProperty.Resource``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-sourceauth.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "type": type,
            }
            if resource is not None:
                self._values["resource"] = resource

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnProject.SourceAuthProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-sourceauth.html#cfn-codebuild-project-sourceauth-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def resource(self) -> typing.Optional[builtins.str]:
            """``CfnProject.SourceAuthProperty.Resource``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-sourceauth.html#cfn-codebuild-project-sourceauth-resource
            """
            result = self._values.get("resource")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceAuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "auth": "auth",
            "build_spec": "buildSpec",
            "build_status_config": "buildStatusConfig",
            "git_clone_depth": "gitCloneDepth",
            "git_submodules_config": "gitSubmodulesConfig",
            "insecure_ssl": "insecureSsl",
            "location": "location",
            "report_build_status": "reportBuildStatus",
            "source_identifier": "sourceIdentifier",
        },
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            auth: typing.Optional[typing.Union["CfnProject.SourceAuthProperty", _IResolvable_9ceae33e]] = None,
            build_spec: typing.Optional[builtins.str] = None,
            build_status_config: typing.Optional[typing.Union["CfnProject.BuildStatusConfigProperty", _IResolvable_9ceae33e]] = None,
            git_clone_depth: typing.Optional[jsii.Number] = None,
            git_submodules_config: typing.Optional[typing.Union["CfnProject.GitSubmodulesConfigProperty", _IResolvable_9ceae33e]] = None,
            insecure_ssl: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
            location: typing.Optional[builtins.str] = None,
            report_build_status: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
            source_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param type: ``CfnProject.SourceProperty.Type``.
            :param auth: ``CfnProject.SourceProperty.Auth``.
            :param build_spec: ``CfnProject.SourceProperty.BuildSpec``.
            :param build_status_config: ``CfnProject.SourceProperty.BuildStatusConfig``.
            :param git_clone_depth: ``CfnProject.SourceProperty.GitCloneDepth``.
            :param git_submodules_config: ``CfnProject.SourceProperty.GitSubmodulesConfig``.
            :param insecure_ssl: ``CfnProject.SourceProperty.InsecureSsl``.
            :param location: ``CfnProject.SourceProperty.Location``.
            :param report_build_status: ``CfnProject.SourceProperty.ReportBuildStatus``.
            :param source_identifier: ``CfnProject.SourceProperty.SourceIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "type": type,
            }
            if auth is not None:
                self._values["auth"] = auth
            if build_spec is not None:
                self._values["build_spec"] = build_spec
            if build_status_config is not None:
                self._values["build_status_config"] = build_status_config
            if git_clone_depth is not None:
                self._values["git_clone_depth"] = git_clone_depth
            if git_submodules_config is not None:
                self._values["git_submodules_config"] = git_submodules_config
            if insecure_ssl is not None:
                self._values["insecure_ssl"] = insecure_ssl
            if location is not None:
                self._values["location"] = location
            if report_build_status is not None:
                self._values["report_build_status"] = report_build_status
            if source_identifier is not None:
                self._values["source_identifier"] = source_identifier

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnProject.SourceProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def auth(
            self,
        ) -> typing.Optional[typing.Union["CfnProject.SourceAuthProperty", _IResolvable_9ceae33e]]:
            """``CfnProject.SourceProperty.Auth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-auth
            """
            result = self._values.get("auth")
            return result

        @builtins.property
        def build_spec(self) -> typing.Optional[builtins.str]:
            """``CfnProject.SourceProperty.BuildSpec``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-buildspec
            """
            result = self._values.get("build_spec")
            return result

        @builtins.property
        def build_status_config(
            self,
        ) -> typing.Optional[typing.Union["CfnProject.BuildStatusConfigProperty", _IResolvable_9ceae33e]]:
            """``CfnProject.SourceProperty.BuildStatusConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-buildstatusconfig
            """
            result = self._values.get("build_status_config")
            return result

        @builtins.property
        def git_clone_depth(self) -> typing.Optional[jsii.Number]:
            """``CfnProject.SourceProperty.GitCloneDepth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-gitclonedepth
            """
            result = self._values.get("git_clone_depth")
            return result

        @builtins.property
        def git_submodules_config(
            self,
        ) -> typing.Optional[typing.Union["CfnProject.GitSubmodulesConfigProperty", _IResolvable_9ceae33e]]:
            """``CfnProject.SourceProperty.GitSubmodulesConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-gitsubmodulesconfig
            """
            result = self._values.get("git_submodules_config")
            return result

        @builtins.property
        def insecure_ssl(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnProject.SourceProperty.InsecureSsl``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-insecuressl
            """
            result = self._values.get("insecure_ssl")
            return result

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            """``CfnProject.SourceProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-location
            """
            result = self._values.get("location")
            return result

        @builtins.property
        def report_build_status(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnProject.SourceProperty.ReportBuildStatus``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-reportbuildstatus
            """
            result = self._values.get("report_build_status")
            return result

        @builtins.property
        def source_identifier(self) -> typing.Optional[builtins.str]:
            """``CfnProject.SourceProperty.SourceIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-sourceidentifier
            """
            result = self._values.get("source_identifier")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnets": "subnets",
            "vpc_id": "vpcId",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
            subnets: typing.Optional[typing.List[builtins.str]] = None,
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param security_group_ids: ``CfnProject.VpcConfigProperty.SecurityGroupIds``.
            :param subnets: ``CfnProject.VpcConfigProperty.Subnets``.
            :param vpc_id: ``CfnProject.VpcConfigProperty.VpcId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnets is not None:
                self._values["subnets"] = subnets
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnProject.VpcConfigProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html#cfn-codebuild-project-vpcconfig-securitygroupids
            """
            result = self._values.get("security_group_ids")
            return result

        @builtins.property
        def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnProject.VpcConfigProperty.Subnets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html#cfn-codebuild-project-vpcconfig-subnets
            """
            result = self._values.get("subnets")
            return result

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            """``CfnProject.VpcConfigProperty.VpcId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html#cfn-codebuild-project-vpcconfig-vpcid
            """
            result = self._values.get("vpc_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnProject.WebhookFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "type": "type",
            "exclude_matched_pattern": "excludeMatchedPattern",
        },
    )
    class WebhookFilterProperty:
        def __init__(
            self,
            *,
            pattern: builtins.str,
            type: builtins.str,
            exclude_matched_pattern: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param pattern: ``CfnProject.WebhookFilterProperty.Pattern``.
            :param type: ``CfnProject.WebhookFilterProperty.Type``.
            :param exclude_matched_pattern: ``CfnProject.WebhookFilterProperty.ExcludeMatchedPattern``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "pattern": pattern,
                "type": type,
            }
            if exclude_matched_pattern is not None:
                self._values["exclude_matched_pattern"] = exclude_matched_pattern

        @builtins.property
        def pattern(self) -> builtins.str:
            """``CfnProject.WebhookFilterProperty.Pattern``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html#cfn-codebuild-project-webhookfilter-pattern
            """
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return result

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnProject.WebhookFilterProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html#cfn-codebuild-project-webhookfilter-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def exclude_matched_pattern(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnProject.WebhookFilterProperty.ExcludeMatchedPattern``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html#cfn-codebuild-project-webhookfilter-excludematchedpattern
            """
            result = self._values.get("exclude_matched_pattern")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebhookFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.CfnProjectProps",
    jsii_struct_bases=[],
    name_mapping={
        "artifacts": "artifacts",
        "environment": "environment",
        "service_role": "serviceRole",
        "source": "source",
        "badge_enabled": "badgeEnabled",
        "build_batch_config": "buildBatchConfig",
        "cache": "cache",
        "description": "description",
        "encryption_key": "encryptionKey",
        "file_system_locations": "fileSystemLocations",
        "logs_config": "logsConfig",
        "name": "name",
        "queued_timeout_in_minutes": "queuedTimeoutInMinutes",
        "secondary_artifacts": "secondaryArtifacts",
        "secondary_sources": "secondarySources",
        "secondary_source_versions": "secondarySourceVersions",
        "source_version": "sourceVersion",
        "tags": "tags",
        "timeout_in_minutes": "timeoutInMinutes",
        "triggers": "triggers",
        "vpc_config": "vpcConfig",
    },
)
class CfnProjectProps:
    def __init__(
        self,
        *,
        artifacts: typing.Union["CfnProject.ArtifactsProperty", _IResolvable_9ceae33e],
        environment: typing.Union["CfnProject.EnvironmentProperty", _IResolvable_9ceae33e],
        service_role: builtins.str,
        source: typing.Union["CfnProject.SourceProperty", _IResolvable_9ceae33e],
        badge_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
        build_batch_config: typing.Optional[typing.Union["CfnProject.ProjectBuildBatchConfigProperty", _IResolvable_9ceae33e]] = None,
        cache: typing.Optional[typing.Union["CfnProject.ProjectCacheProperty", _IResolvable_9ceae33e]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        file_system_locations: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnProject.ProjectFileSystemLocationProperty", _IResolvable_9ceae33e]]]] = None,
        logs_config: typing.Optional[typing.Union["CfnProject.LogsConfigProperty", _IResolvable_9ceae33e]] = None,
        name: typing.Optional[builtins.str] = None,
        queued_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        secondary_artifacts: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnProject.ArtifactsProperty", _IResolvable_9ceae33e]]]] = None,
        secondary_sources: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnProject.SourceProperty", _IResolvable_9ceae33e]]]] = None,
        secondary_source_versions: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnProject.ProjectSourceVersionProperty", _IResolvable_9ceae33e]]]] = None,
        source_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
        triggers: typing.Optional[typing.Union["CfnProject.ProjectTriggersProperty", _IResolvable_9ceae33e]] = None,
        vpc_config: typing.Optional[typing.Union["CfnProject.VpcConfigProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Properties for defining a ``AWS::CodeBuild::Project``.

        :param artifacts: ``AWS::CodeBuild::Project.Artifacts``.
        :param environment: ``AWS::CodeBuild::Project.Environment``.
        :param service_role: ``AWS::CodeBuild::Project.ServiceRole``.
        :param source: ``AWS::CodeBuild::Project.Source``.
        :param badge_enabled: ``AWS::CodeBuild::Project.BadgeEnabled``.
        :param build_batch_config: ``AWS::CodeBuild::Project.BuildBatchConfig``.
        :param cache: ``AWS::CodeBuild::Project.Cache``.
        :param description: ``AWS::CodeBuild::Project.Description``.
        :param encryption_key: ``AWS::CodeBuild::Project.EncryptionKey``.
        :param file_system_locations: ``AWS::CodeBuild::Project.FileSystemLocations``.
        :param logs_config: ``AWS::CodeBuild::Project.LogsConfig``.
        :param name: ``AWS::CodeBuild::Project.Name``.
        :param queued_timeout_in_minutes: ``AWS::CodeBuild::Project.QueuedTimeoutInMinutes``.
        :param secondary_artifacts: ``AWS::CodeBuild::Project.SecondaryArtifacts``.
        :param secondary_sources: ``AWS::CodeBuild::Project.SecondarySources``.
        :param secondary_source_versions: ``AWS::CodeBuild::Project.SecondarySourceVersions``.
        :param source_version: ``AWS::CodeBuild::Project.SourceVersion``.
        :param tags: ``AWS::CodeBuild::Project.Tags``.
        :param timeout_in_minutes: ``AWS::CodeBuild::Project.TimeoutInMinutes``.
        :param triggers: ``AWS::CodeBuild::Project.Triggers``.
        :param vpc_config: ``AWS::CodeBuild::Project.VpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "artifacts": artifacts,
            "environment": environment,
            "service_role": service_role,
            "source": source,
        }
        if badge_enabled is not None:
            self._values["badge_enabled"] = badge_enabled
        if build_batch_config is not None:
            self._values["build_batch_config"] = build_batch_config
        if cache is not None:
            self._values["cache"] = cache
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if file_system_locations is not None:
            self._values["file_system_locations"] = file_system_locations
        if logs_config is not None:
            self._values["logs_config"] = logs_config
        if name is not None:
            self._values["name"] = name
        if queued_timeout_in_minutes is not None:
            self._values["queued_timeout_in_minutes"] = queued_timeout_in_minutes
        if secondary_artifacts is not None:
            self._values["secondary_artifacts"] = secondary_artifacts
        if secondary_sources is not None:
            self._values["secondary_sources"] = secondary_sources
        if secondary_source_versions is not None:
            self._values["secondary_source_versions"] = secondary_source_versions
        if source_version is not None:
            self._values["source_version"] = source_version
        if tags is not None:
            self._values["tags"] = tags
        if timeout_in_minutes is not None:
            self._values["timeout_in_minutes"] = timeout_in_minutes
        if triggers is not None:
            self._values["triggers"] = triggers
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def artifacts(
        self,
    ) -> typing.Union["CfnProject.ArtifactsProperty", _IResolvable_9ceae33e]:
        """``AWS::CodeBuild::Project.Artifacts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-artifacts
        """
        result = self._values.get("artifacts")
        assert result is not None, "Required property 'artifacts' is missing"
        return result

    @builtins.property
    def environment(
        self,
    ) -> typing.Union["CfnProject.EnvironmentProperty", _IResolvable_9ceae33e]:
        """``AWS::CodeBuild::Project.Environment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-environment
        """
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return result

    @builtins.property
    def service_role(self) -> builtins.str:
        """``AWS::CodeBuild::Project.ServiceRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-servicerole
        """
        result = self._values.get("service_role")
        assert result is not None, "Required property 'service_role' is missing"
        return result

    @builtins.property
    def source(
        self,
    ) -> typing.Union["CfnProject.SourceProperty", _IResolvable_9ceae33e]:
        """``AWS::CodeBuild::Project.Source``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-source
        """
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return result

    @builtins.property
    def badge_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
        """``AWS::CodeBuild::Project.BadgeEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-badgeenabled
        """
        result = self._values.get("badge_enabled")
        return result

    @builtins.property
    def build_batch_config(
        self,
    ) -> typing.Optional[typing.Union["CfnProject.ProjectBuildBatchConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeBuild::Project.BuildBatchConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-buildbatchconfig
        """
        result = self._values.get("build_batch_config")
        return result

    @builtins.property
    def cache(
        self,
    ) -> typing.Optional[typing.Union["CfnProject.ProjectCacheProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeBuild::Project.Cache``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-cache
        """
        result = self._values.get("cache")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeBuild::Project.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeBuild::Project.EncryptionKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-encryptionkey
        """
        result = self._values.get("encryption_key")
        return result

    @builtins.property
    def file_system_locations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnProject.ProjectFileSystemLocationProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeBuild::Project.FileSystemLocations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-filesystemlocations
        """
        result = self._values.get("file_system_locations")
        return result

    @builtins.property
    def logs_config(
        self,
    ) -> typing.Optional[typing.Union["CfnProject.LogsConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeBuild::Project.LogsConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-logsconfig
        """
        result = self._values.get("logs_config")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeBuild::Project.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def queued_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CodeBuild::Project.QueuedTimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-queuedtimeoutinminutes
        """
        result = self._values.get("queued_timeout_in_minutes")
        return result

    @builtins.property
    def secondary_artifacts(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnProject.ArtifactsProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeBuild::Project.SecondaryArtifacts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondaryartifacts
        """
        result = self._values.get("secondary_artifacts")
        return result

    @builtins.property
    def secondary_sources(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnProject.SourceProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeBuild::Project.SecondarySources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondarysources
        """
        result = self._values.get("secondary_sources")
        return result

    @builtins.property
    def secondary_source_versions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnProject.ProjectSourceVersionProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeBuild::Project.SecondarySourceVersions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondarysourceversions
        """
        result = self._values.get("secondary_source_versions")
        return result

    @builtins.property
    def source_version(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeBuild::Project.SourceVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-sourceversion
        """
        result = self._values.get("source_version")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::CodeBuild::Project.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CodeBuild::Project.TimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-timeoutinminutes
        """
        result = self._values.get("timeout_in_minutes")
        return result

    @builtins.property
    def triggers(
        self,
    ) -> typing.Optional[typing.Union["CfnProject.ProjectTriggersProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeBuild::Project.Triggers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-triggers
        """
        result = self._values.get("triggers")
        return result

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union["CfnProject.VpcConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeBuild::Project.VpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-vpcconfig
        """
        result = self._values.get("vpc_config")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnReportGroup(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.CfnReportGroup",
):
    """A CloudFormation ``AWS::CodeBuild::ReportGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeBuild::ReportGroup
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        export_config: typing.Union["ReportExportConfigProperty", _IResolvable_9ceae33e],
        type: builtins.str,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Create a new ``AWS::CodeBuild::ReportGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param export_config: ``AWS::CodeBuild::ReportGroup.ExportConfig``.
        :param type: ``AWS::CodeBuild::ReportGroup.Type``.
        :param name: ``AWS::CodeBuild::ReportGroup.Name``.
        :param tags: ``AWS::CodeBuild::ReportGroup.Tags``.
        """
        props = CfnReportGroupProps(
            export_config=export_config, type=type, name=name, tags=tags
        )

        jsii.create(CfnReportGroup, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::CodeBuild::ReportGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="exportConfig")
    def export_config(
        self,
    ) -> typing.Union["ReportExportConfigProperty", _IResolvable_9ceae33e]:
        """``AWS::CodeBuild::ReportGroup.ExportConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-exportconfig
        """
        return jsii.get(self, "exportConfig")

    @export_config.setter # type: ignore
    def export_config(
        self,
        value: typing.Union["ReportExportConfigProperty", _IResolvable_9ceae33e],
    ) -> None:
        jsii.set(self, "exportConfig", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """``AWS::CodeBuild::ReportGroup.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-type
        """
        return jsii.get(self, "type")

    @type.setter # type: ignore
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeBuild::ReportGroup.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnReportGroup.ReportExportConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "export_config_type": "exportConfigType",
            "s3_destination": "s3Destination",
        },
    )
    class ReportExportConfigProperty:
        def __init__(
            self,
            *,
            export_config_type: builtins.str,
            s3_destination: typing.Optional[typing.Union["CfnReportGroup.S3ReportExportConfigProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param export_config_type: ``CfnReportGroup.ReportExportConfigProperty.ExportConfigType``.
            :param s3_destination: ``CfnReportGroup.ReportExportConfigProperty.S3Destination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-reportexportconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "export_config_type": export_config_type,
            }
            if s3_destination is not None:
                self._values["s3_destination"] = s3_destination

        @builtins.property
        def export_config_type(self) -> builtins.str:
            """``CfnReportGroup.ReportExportConfigProperty.ExportConfigType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-reportexportconfig.html#cfn-codebuild-reportgroup-reportexportconfig-exportconfigtype
            """
            result = self._values.get("export_config_type")
            assert result is not None, "Required property 'export_config_type' is missing"
            return result

        @builtins.property
        def s3_destination(
            self,
        ) -> typing.Optional[typing.Union["CfnReportGroup.S3ReportExportConfigProperty", _IResolvable_9ceae33e]]:
            """``CfnReportGroup.ReportExportConfigProperty.S3Destination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-reportexportconfig.html#cfn-codebuild-reportgroup-reportexportconfig-s3destination
            """
            result = self._values.get("s3_destination")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReportExportConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codebuild.CfnReportGroup.S3ReportExportConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "encryption_disabled": "encryptionDisabled",
            "encryption_key": "encryptionKey",
            "packaging": "packaging",
            "path": "path",
        },
    )
    class S3ReportExportConfigProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            encryption_disabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]] = None,
            encryption_key: typing.Optional[builtins.str] = None,
            packaging: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param bucket: ``CfnReportGroup.S3ReportExportConfigProperty.Bucket``.
            :param encryption_disabled: ``CfnReportGroup.S3ReportExportConfigProperty.EncryptionDisabled``.
            :param encryption_key: ``CfnReportGroup.S3ReportExportConfigProperty.EncryptionKey``.
            :param packaging: ``CfnReportGroup.S3ReportExportConfigProperty.Packaging``.
            :param path: ``CfnReportGroup.S3ReportExportConfigProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "bucket": bucket,
            }
            if encryption_disabled is not None:
                self._values["encryption_disabled"] = encryption_disabled
            if encryption_key is not None:
                self._values["encryption_key"] = encryption_key
            if packaging is not None:
                self._values["packaging"] = packaging
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def bucket(self) -> builtins.str:
            """``CfnReportGroup.S3ReportExportConfigProperty.Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-bucket
            """
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return result

        @builtins.property
        def encryption_disabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_9ceae33e]]:
            """``CfnReportGroup.S3ReportExportConfigProperty.EncryptionDisabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-encryptiondisabled
            """
            result = self._values.get("encryption_disabled")
            return result

        @builtins.property
        def encryption_key(self) -> typing.Optional[builtins.str]:
            """``CfnReportGroup.S3ReportExportConfigProperty.EncryptionKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-encryptionkey
            """
            result = self._values.get("encryption_key")
            return result

        @builtins.property
        def packaging(self) -> typing.Optional[builtins.str]:
            """``CfnReportGroup.S3ReportExportConfigProperty.Packaging``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-packaging
            """
            result = self._values.get("packaging")
            return result

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            """``CfnReportGroup.S3ReportExportConfigProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-path
            """
            result = self._values.get("path")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ReportExportConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.CfnReportGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "export_config": "exportConfig",
        "type": "type",
        "name": "name",
        "tags": "tags",
    },
)
class CfnReportGroupProps:
    def __init__(
        self,
        *,
        export_config: typing.Union["CfnReportGroup.ReportExportConfigProperty", _IResolvable_9ceae33e],
        type: builtins.str,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::CodeBuild::ReportGroup``.

        :param export_config: ``AWS::CodeBuild::ReportGroup.ExportConfig``.
        :param type: ``AWS::CodeBuild::ReportGroup.Type``.
        :param name: ``AWS::CodeBuild::ReportGroup.Name``.
        :param tags: ``AWS::CodeBuild::ReportGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "export_config": export_config,
            "type": type,
        }
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def export_config(
        self,
    ) -> typing.Union["CfnReportGroup.ReportExportConfigProperty", _IResolvable_9ceae33e]:
        """``AWS::CodeBuild::ReportGroup.ExportConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-exportconfig
        """
        result = self._values.get("export_config")
        assert result is not None, "Required property 'export_config' is missing"
        return result

    @builtins.property
    def type(self) -> builtins.str:
        """``AWS::CodeBuild::ReportGroup.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-type
        """
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeBuild::ReportGroup.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::CodeBuild::ReportGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReportGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnSourceCredential(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.CfnSourceCredential",
):
    """A CloudFormation ``AWS::CodeBuild::SourceCredential``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeBuild::SourceCredential
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        auth_type: builtins.str,
        server_type: builtins.str,
        token: builtins.str,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::CodeBuild::SourceCredential``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auth_type: ``AWS::CodeBuild::SourceCredential.AuthType``.
        :param server_type: ``AWS::CodeBuild::SourceCredential.ServerType``.
        :param token: ``AWS::CodeBuild::SourceCredential.Token``.
        :param username: ``AWS::CodeBuild::SourceCredential.Username``.
        """
        props = CfnSourceCredentialProps(
            auth_type=auth_type,
            server_type=server_type,
            token=token,
            username=username,
        )

        jsii.create(CfnSourceCredential, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        """``AWS::CodeBuild::SourceCredential.AuthType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-authtype
        """
        return jsii.get(self, "authType")

    @auth_type.setter # type: ignore
    def auth_type(self, value: builtins.str) -> None:
        jsii.set(self, "authType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serverType")
    def server_type(self) -> builtins.str:
        """``AWS::CodeBuild::SourceCredential.ServerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-servertype
        """
        return jsii.get(self, "serverType")

    @server_type.setter # type: ignore
    def server_type(self, value: builtins.str) -> None:
        jsii.set(self, "serverType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        """``AWS::CodeBuild::SourceCredential.Token``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-token
        """
        return jsii.get(self, "token")

    @token.setter # type: ignore
    def token(self, value: builtins.str) -> None:
        jsii.set(self, "token", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="username")
    def username(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeBuild::SourceCredential.Username``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-username
        """
        return jsii.get(self, "username")

    @username.setter # type: ignore
    def username(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "username", value)


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.CfnSourceCredentialProps",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "server_type": "serverType",
        "token": "token",
        "username": "username",
    },
)
class CfnSourceCredentialProps:
    def __init__(
        self,
        *,
        auth_type: builtins.str,
        server_type: builtins.str,
        token: builtins.str,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::CodeBuild::SourceCredential``.

        :param auth_type: ``AWS::CodeBuild::SourceCredential.AuthType``.
        :param server_type: ``AWS::CodeBuild::SourceCredential.ServerType``.
        :param token: ``AWS::CodeBuild::SourceCredential.Token``.
        :param username: ``AWS::CodeBuild::SourceCredential.Username``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "auth_type": auth_type,
            "server_type": server_type,
            "token": token,
        }
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def auth_type(self) -> builtins.str:
        """``AWS::CodeBuild::SourceCredential.AuthType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-authtype
        """
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return result

    @builtins.property
    def server_type(self) -> builtins.str:
        """``AWS::CodeBuild::SourceCredential.ServerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-servertype
        """
        result = self._values.get("server_type")
        assert result is not None, "Required property 'server_type' is missing"
        return result

    @builtins.property
    def token(self) -> builtins.str:
        """``AWS::CodeBuild::SourceCredential.Token``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-token
        """
        result = self._values.get("token")
        assert result is not None, "Required property 'token' is missing"
        return result

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeBuild::SourceCredential.Username``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-username
        """
        result = self._values.get("username")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSourceCredentialProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.CommonProjectProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all_outbound": "allowAllOutbound",
        "badge": "badge",
        "build_spec": "buildSpec",
        "cache": "cache",
        "description": "description",
        "encryption_key": "encryptionKey",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "file_system_locations": "fileSystemLocations",
        "grant_report_group_permissions": "grantReportGroupPermissions",
        "project_name": "projectName",
        "role": "role",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "timeout": "timeout",
        "vpc": "vpc",
    },
)
class CommonProjectProps:
    def __init__(
        self,
        *,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        badge: typing.Optional[builtins.bool] = None,
        build_spec: typing.Optional["BuildSpec"] = None,
        cache: typing.Optional["Cache"] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_IKey_3336c79d] = None,
        environment: typing.Optional["BuildEnvironment"] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, "BuildEnvironmentVariable"]] = None,
        file_system_locations: typing.Optional[typing.List["IFileSystemLocation"]] = None,
        grant_report_group_permissions: typing.Optional[builtins.bool] = None,
        project_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        subnet_selection: typing.Optional[_SubnetSelection_36a13cd6] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
    ) -> None:
        """
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param file_system_locations: An ProjectFileSystemLocation objects for a CodeBuild build project. A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint, and type of a file system created using Amazon Elastic File System. Default: - no file system locations
        :param grant_report_group_permissions: Add permissions to this project's role to create and use test report groups with name starting with the name of this project. That is the standard report group that gets created when a simple name (in contrast to an ARN) is used in the 'reports' section of the buildspec of this project. This is usually harmless, but you can turn these off if you don't plan on using test reports in this project. Default: true
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.

        stability
        :stability: experimental
        """
        if isinstance(environment, dict):
            environment = BuildEnvironment(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_36a13cd6(**subnet_selection)
        self._values: typing.Dict[str, typing.Any] = {}
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if badge is not None:
            self._values["badge"] = badge
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if cache is not None:
            self._values["cache"] = cache
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if file_system_locations is not None:
            self._values["file_system_locations"] = file_system_locations
        if grant_report_group_permissions is not None:
            self._values["grant_report_group_permissions"] = grant_report_group_permissions
        if project_name is not None:
            self._values["project_name"] = project_name
        if role is not None:
            self._values["role"] = role
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        """Whether to allow the CodeBuild to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        CodeBuild project to connect to network targets.

        Only used if 'vpc' is supplied.

        default
        :default: true

        stability
        :stability: experimental
        """
        result = self._values.get("allow_all_outbound")
        return result

    @builtins.property
    def badge(self) -> typing.Optional[builtins.bool]:
        """Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge.

        For more information, see Build Badges Sample
        in the AWS CodeBuild User Guide.

        default
        :default: false

        stability
        :stability: experimental
        """
        result = self._values.get("badge")
        return result

    @builtins.property
    def build_spec(self) -> typing.Optional["BuildSpec"]:
        """Filename or contents of buildspec in JSON format.

        default
        :default: - Empty buildspec.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-example
        stability
        :stability: experimental
        """
        result = self._values.get("build_spec")
        return result

    @builtins.property
    def cache(self) -> typing.Optional["Cache"]:
        """Caching strategy to use.

        default
        :default: Cache.none

        stability
        :stability: experimental
        """
        result = self._values.get("cache")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """A description of the project.

        Use the description to identify the purpose
        of the project.

        default
        :default: - No description.

        stability
        :stability: experimental
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """Encryption key to use to read and write artifacts.

        default
        :default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.

        stability
        :stability: experimental
        """
        result = self._values.get("encryption_key")
        return result

    @builtins.property
    def environment(self) -> typing.Optional["BuildEnvironment"]:
        """Build environment to use for the build.

        default
        :default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0

        stability
        :stability: experimental
        """
        result = self._values.get("environment")
        return result

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "BuildEnvironmentVariable"]]:
        """Additional environment variables to add to the build environment.

        default
        :default: - No additional environment variables are specified.

        stability
        :stability: experimental
        """
        result = self._values.get("environment_variables")
        return result

    @builtins.property
    def file_system_locations(
        self,
    ) -> typing.Optional[typing.List["IFileSystemLocation"]]:
        """An  ProjectFileSystemLocation objects for a CodeBuild build project.

        A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint,
        and type of a file system created using Amazon Elastic File System.

        default
        :default: - no file system locations

        stability
        :stability: experimental
        """
        result = self._values.get("file_system_locations")
        return result

    @builtins.property
    def grant_report_group_permissions(self) -> typing.Optional[builtins.bool]:
        """Add permissions to this project's role to create and use test report groups with name starting with the name of this project.

        That is the standard report group that gets created when a simple name
        (in contrast to an ARN)
        is used in the 'reports' section of the buildspec of this project.
        This is usually harmless, but you can turn these off if you don't plan on using test
        reports in this project.

        default
        :default: true

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/test-report-group-naming.html
        stability
        :stability: experimental
        """
        result = self._values.get("grant_report_group_permissions")
        return result

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        """The physical, human-readable name of the CodeBuild Project.

        default
        :default: - Name is automatically generated.

        stability
        :stability: experimental
        """
        result = self._values.get("project_name")
        return result

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Service Role to assume while running the build.

        default
        :default: - A role will be created.

        stability
        :stability: experimental
        """
        result = self._values.get("role")
        return result

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """What security group to associate with the codebuild project's network interfaces.

        If no security group is identified, one will be created automatically.

        Only used if 'vpc' is supplied.

        default
        :default: - Security group will be automatically created.

        stability
        :stability: experimental
        """
        result = self._values.get("security_groups")
        return result

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied.

        default
        :default: - All private subnets.

        stability
        :stability: experimental
        """
        result = self._values.get("subnet_selection")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        default
        :default: Duration.hours(1)

        stability
        :stability: experimental
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """VPC network to place codebuild network interfaces.

        Specify this if the codebuild project needs to access resources in a VPC.

        default
        :default: - No VPC is specified.

        stability
        :stability: experimental
        """
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk-experiment.aws_codebuild.ComputeType")
class ComputeType(enum.Enum):
    """Build machine compute type.

    stability
    :stability: experimental
    """

    SMALL = "SMALL"
    """
    stability
    :stability: experimental
    """
    MEDIUM = "MEDIUM"
    """
    stability
    :stability: experimental
    """
    LARGE = "LARGE"
    """
    stability
    :stability: experimental
    """
    X2_LARGE = "X2_LARGE"
    """
    stability
    :stability: experimental
    """


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.DockerImageOptions",
    jsii_struct_bases=[],
    name_mapping={"secrets_manager_credentials": "secretsManagerCredentials"},
)
class DockerImageOptions:
    def __init__(
        self,
        *,
        secrets_manager_credentials: typing.Optional[_ISecret_75279d36] = None,
    ) -> None:
        """The options when creating a CodeBuild Docker build image using {@link LinuxBuildImage.fromDockerRegistry} or {@link WindowsBuildImage.fromDockerRegistry}.

        :param secrets_manager_credentials: The credentials, stored in Secrets Manager, used for accessing the repository holding the image, if the repository is private. Default: no credentials will be used (we assume the repository is public)

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if secrets_manager_credentials is not None:
            self._values["secrets_manager_credentials"] = secrets_manager_credentials

    @builtins.property
    def secrets_manager_credentials(self) -> typing.Optional[_ISecret_75279d36]:
        """The credentials, stored in Secrets Manager, used for accessing the repository holding the image, if the repository is private.

        default
        :default: no credentials will be used (we assume the repository is public)

        stability
        :stability: experimental
        """
        result = self._values.get("secrets_manager_credentials")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.EfsFileSystemLocationProps",
    jsii_struct_bases=[],
    name_mapping={
        "identifier": "identifier",
        "location": "location",
        "mount_point": "mountPoint",
        "mount_options": "mountOptions",
    },
)
class EfsFileSystemLocationProps:
    def __init__(
        self,
        *,
        identifier: builtins.str,
        location: builtins.str,
        mount_point: builtins.str,
        mount_options: typing.Optional[builtins.str] = None,
    ) -> None:
        """Construction properties for {@link EfsFileSystemLocation}.

        :param identifier: The name used to access a file system created by Amazon EFS.
        :param location: A string that specifies the location of the file system, like Amazon EFS.
        :param mount_point: The location in the container where you mount the file system.
        :param mount_options: The mount options for a file system such as Amazon EFS. Default: 'nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2'.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "identifier": identifier,
            "location": location,
            "mount_point": mount_point,
        }
        if mount_options is not None:
            self._values["mount_options"] = mount_options

    @builtins.property
    def identifier(self) -> builtins.str:
        """The name used to access a file system created by Amazon EFS.

        stability
        :stability: experimental
        """
        result = self._values.get("identifier")
        assert result is not None, "Required property 'identifier' is missing"
        return result

    @builtins.property
    def location(self) -> builtins.str:
        """A string that specifies the location of the file system, like Amazon EFS.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "fs-abcd1234.efs.us-west-2.amazonaws.com:/my-efs-mount-directory".
        """
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return result

    @builtins.property
    def mount_point(self) -> builtins.str:
        """The location in the container where you mount the file system.

        stability
        :stability: experimental
        """
        result = self._values.get("mount_point")
        assert result is not None, "Required property 'mount_point' is missing"
        return result

    @builtins.property
    def mount_options(self) -> typing.Optional[builtins.str]:
        """The mount options for a file system such as Amazon EFS.

        default
        :default: 'nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2'.

        stability
        :stability: experimental
        """
        result = self._values.get("mount_options")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EfsFileSystemLocationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk-experiment.aws_codebuild.EventAction")
class EventAction(enum.Enum):
    """The types of webhook event actions.

    stability
    :stability: experimental
    """

    PUSH = "PUSH"
    """A push (of a branch, or a tag) to the repository.

    stability
    :stability: experimental
    """
    PULL_REQUEST_CREATED = "PULL_REQUEST_CREATED"
    """Creating a Pull Request.

    stability
    :stability: experimental
    """
    PULL_REQUEST_UPDATED = "PULL_REQUEST_UPDATED"
    """Updating a Pull Request.

    stability
    :stability: experimental
    """
    PULL_REQUEST_MERGED = "PULL_REQUEST_MERGED"
    """Merging a Pull Request.

    stability
    :stability: experimental
    """
    PULL_REQUEST_REOPENED = "PULL_REQUEST_REOPENED"
    """Re-opening a previously closed Pull Request.

    Note that this event is only supported for GitHub and GitHubEnterprise sources.

    stability
    :stability: experimental
    """


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.FileSystemConfig",
    jsii_struct_bases=[],
    name_mapping={"location": "location"},
)
class FileSystemConfig:
    def __init__(
        self,
        *,
        location: "CfnProject.ProjectFileSystemLocationProperty",
    ) -> None:
        """The type returned from {@link IFileSystemLocation#bind}.

        :param location: File system location wrapper property.

        stability
        :stability: experimental
        """
        if isinstance(location, dict):
            location = CfnProject.ProjectFileSystemLocationProperty(**location)
        self._values: typing.Dict[str, typing.Any] = {
            "location": location,
        }

    @builtins.property
    def location(self) -> "CfnProject.ProjectFileSystemLocationProperty":
        """File system location wrapper property.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html
        stability
        :stability: experimental
        """
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileSystemConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FileSystemLocation(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.FileSystemLocation",
):
    """FileSystemLocation provider definition for a CodeBuild Project.

    stability
    :stability: experimental
    """

    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        jsii.create(FileSystemLocation, self, [])

    @jsii.member(jsii_name="efs")
    @builtins.classmethod
    def efs(
        cls,
        *,
        identifier: builtins.str,
        location: builtins.str,
        mount_point: builtins.str,
        mount_options: typing.Optional[builtins.str] = None,
    ) -> "IFileSystemLocation":
        """EFS file system provider.

        :param identifier: The name used to access a file system created by Amazon EFS.
        :param location: A string that specifies the location of the file system, like Amazon EFS.
        :param mount_point: The location in the container where you mount the file system.
        :param mount_options: The mount options for a file system such as Amazon EFS. Default: 'nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2'.

        stability
        :stability: experimental
        """
        props = EfsFileSystemLocationProps(
            identifier=identifier,
            location=location,
            mount_point=mount_point,
            mount_options=mount_options,
        )

        return jsii.sinvoke(cls, "efs", [props])


class FilterGroup(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.FilterGroup",
):
    """An object that represents a group of filter conditions for a webhook.

    Every condition in a given FilterGroup must be true in order for the whole group to be true.
    You construct instances of it by calling the {@link #inEventOf} static factory method,
    and then calling various ``andXyz`` instance methods to create modified instances of it
    (this class is immutable).

    You pass instances of this class to the ``webhookFilters`` property when constructing a source.

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="inEventOf")
    @builtins.classmethod
    def in_event_of(cls, *actions: "EventAction") -> "FilterGroup":
        """Creates a new event FilterGroup that triggers on any of the provided actions.

        :param actions: the actions to trigger the webhook on.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "inEventOf", [*actions])

    @jsii.member(jsii_name="andActorAccountIs")
    def and_actor_account_is(self, pattern: builtins.str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the account ID of the actor initiating the event must match the given pattern.

        :param pattern: a regular expression.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "andActorAccountIs", [pattern])

    @jsii.member(jsii_name="andActorAccountIsNot")
    def and_actor_account_is_not(self, pattern: builtins.str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the account ID of the actor initiating the event must not match the given pattern.

        :param pattern: a regular expression.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "andActorAccountIsNot", [pattern])

    @jsii.member(jsii_name="andBaseBranchIs")
    def and_base_branch_is(self, branch_name: builtins.str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the Pull Request that is the source of the event must target the given base branch.

        Note that you cannot use this method if this Group contains the ``PUSH`` event action.

        :param branch_name: the name of the branch (can be a regular expression).

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "andBaseBranchIs", [branch_name])

    @jsii.member(jsii_name="andBaseBranchIsNot")
    def and_base_branch_is_not(self, branch_name: builtins.str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the Pull Request that is the source of the event must not target the given base branch.

        Note that you cannot use this method if this Group contains the ``PUSH`` event action.

        :param branch_name: the name of the branch (can be a regular expression).

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "andBaseBranchIsNot", [branch_name])

    @jsii.member(jsii_name="andBaseRefIs")
    def and_base_ref_is(self, pattern: builtins.str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the Pull Request that is the source of the event must target the given Git reference.

        Note that you cannot use this method if this Group contains the ``PUSH`` event action.

        :param pattern: a regular expression.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "andBaseRefIs", [pattern])

    @jsii.member(jsii_name="andBaseRefIsNot")
    def and_base_ref_is_not(self, pattern: builtins.str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the Pull Request that is the source of the event must not target the given Git reference.

        Note that you cannot use this method if this Group contains the ``PUSH`` event action.

        :param pattern: a regular expression.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "andBaseRefIsNot", [pattern])

    @jsii.member(jsii_name="andBranchIs")
    def and_branch_is(self, branch_name: builtins.str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must affect the given branch.

        :param branch_name: the name of the branch (can be a regular expression).

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "andBranchIs", [branch_name])

    @jsii.member(jsii_name="andBranchIsNot")
    def and_branch_is_not(self, branch_name: builtins.str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must not affect the given branch.

        :param branch_name: the name of the branch (can be a regular expression).

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "andBranchIsNot", [branch_name])

    @jsii.member(jsii_name="andFilePathIs")
    def and_file_path_is(self, pattern: builtins.str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the push that is the source of the event must affect a file that matches the given pattern.

        Note that you can only use this method if this Group contains only the ``PUSH`` event action,
        and only for GitHub and GitHubEnterprise sources.

        :param pattern: a regular expression.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "andFilePathIs", [pattern])

    @jsii.member(jsii_name="andFilePathIsNot")
    def and_file_path_is_not(self, pattern: builtins.str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the push that is the source of the event must not affect a file that matches the given pattern.

        Note that you can only use this method if this Group contains only the ``PUSH`` event action,
        and only for GitHub and GitHubEnterprise sources.

        :param pattern: a regular expression.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "andFilePathIsNot", [pattern])

    @jsii.member(jsii_name="andHeadRefIs")
    def and_head_ref_is(self, pattern: builtins.str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must affect a Git reference (ie., a branch or a tag) that matches the given pattern.

        :param pattern: a regular expression.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "andHeadRefIs", [pattern])

    @jsii.member(jsii_name="andHeadRefIsNot")
    def and_head_ref_is_not(self, pattern: builtins.str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must not affect a Git reference (ie., a branch or a tag) that matches the given pattern.

        :param pattern: a regular expression.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "andHeadRefIsNot", [pattern])

    @jsii.member(jsii_name="andTagIs")
    def and_tag_is(self, tag_name: builtins.str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must affect the given tag.

        :param tag_name: the name of the tag (can be a regular expression).

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "andTagIs", [tag_name])

    @jsii.member(jsii_name="andTagIsNot")
    def and_tag_is_not(self, tag_name: builtins.str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must not affect the given tag.

        :param tag_name: the name of the tag (can be a regular expression).

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "andTagIsNot", [tag_name])


class GitHubEnterpriseSourceCredentials(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.GitHubEnterpriseSourceCredentials",
):
    """The source credentials used when contacting the GitHub Enterprise API.

    **Note**: CodeBuild only allows a single credential for GitHub Enterprise
    to be saved in a given AWS account in a given region -
    any attempt to add more than one will result in an error.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::CodeBuild::SourceCredential
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        access_token: _SecretValue_99478b8b,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param access_token: The personal access token to use when contacting the instance of the GitHub Enterprise API.

        stability
        :stability: experimental
        """
        props = GitHubEnterpriseSourceCredentialsProps(access_token=access_token)

        jsii.create(GitHubEnterpriseSourceCredentials, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.GitHubEnterpriseSourceCredentialsProps",
    jsii_struct_bases=[],
    name_mapping={"access_token": "accessToken"},
)
class GitHubEnterpriseSourceCredentialsProps:
    def __init__(self, *, access_token: _SecretValue_99478b8b) -> None:
        """Creation properties for {@link GitHubEnterpriseSourceCredentials}.

        :param access_token: The personal access token to use when contacting the instance of the GitHub Enterprise API.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "access_token": access_token,
        }

    @builtins.property
    def access_token(self) -> _SecretValue_99478b8b:
        """The personal access token to use when contacting the instance of the GitHub Enterprise API.

        stability
        :stability: experimental
        """
        result = self._values.get("access_token")
        assert result is not None, "Required property 'access_token' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubEnterpriseSourceCredentialsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubSourceCredentials(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.GitHubSourceCredentials",
):
    """The source credentials used when contacting the GitHub API.

    **Note**: CodeBuild only allows a single credential for GitHub
    to be saved in a given AWS account in a given region -
    any attempt to add more than one will result in an error.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::CodeBuild::SourceCredential
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        access_token: _SecretValue_99478b8b,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param access_token: The personal access token to use when contacting the GitHub API.

        stability
        :stability: experimental
        """
        props = GitHubSourceCredentialsProps(access_token=access_token)

        jsii.create(GitHubSourceCredentials, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.GitHubSourceCredentialsProps",
    jsii_struct_bases=[],
    name_mapping={"access_token": "accessToken"},
)
class GitHubSourceCredentialsProps:
    def __init__(self, *, access_token: _SecretValue_99478b8b) -> None:
        """Creation properties for {@link GitHubSourceCredentials}.

        :param access_token: The personal access token to use when contacting the GitHub API.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "access_token": access_token,
        }

    @builtins.property
    def access_token(self) -> _SecretValue_99478b8b:
        """The personal access token to use when contacting the GitHub API.

        stability
        :stability: experimental
        """
        result = self._values.get("access_token")
        assert result is not None, "Required property 'access_token' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubSourceCredentialsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk-experiment.aws_codebuild.IArtifacts")
class IArtifacts(typing_extensions.Protocol):
    """The abstract interface of a CodeBuild build output.

    Implemented by {@link Artifacts}.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IArtifactsProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """The CodeBuild type of this artifact.

        stability
        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[builtins.str]:
        """The artifact identifier.

        This property is required on secondary artifacts.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_f50a3f53,
        project: "IProject",
    ) -> "ArtifactsConfig":
        """Callback when an Artifacts class is used in a CodeBuild Project.

        :param scope: a root Construct that allows creating new Constructs.
        :param project: the Project this Artifacts is used in.

        stability
        :stability: experimental
        """
        ...


class _IArtifactsProxy:
    """The abstract interface of a CodeBuild build output.

    Implemented by {@link Artifacts}.

    stability
    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk-experiment.aws_codebuild.IArtifacts"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """The CodeBuild type of this artifact.

        stability
        :stability: experimental
        """
        return jsii.get(self, "type")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[builtins.str]:
        """The artifact identifier.

        This property is required on secondary artifacts.

        stability
        :stability: experimental
        """
        return jsii.get(self, "identifier")

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_f50a3f53,
        project: "IProject",
    ) -> "ArtifactsConfig":
        """Callback when an Artifacts class is used in a CodeBuild Project.

        :param scope: a root Construct that allows creating new Constructs.
        :param project: the Project this Artifacts is used in.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope, project])


@jsii.interface(jsii_type="monocdk-experiment.aws_codebuild.IBuildImage")
class IBuildImage(typing_extensions.Protocol):
    """Represents a Docker image used for the CodeBuild Project builds.

    Use the concrete subclasses, either:
    {@link LinuxBuildImage} or {@link WindowsBuildImage}.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IBuildImageProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        """The default {@link ComputeType} to use with this image, if one was not specified in {@link BuildEnvironment#computeType} explicitly.

        stability
        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        """The Docker image identifier that the build environment uses.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
        stability
        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """The type of build environment.

        stability
        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imagePullPrincipalType")
    def image_pull_principal_type(self) -> typing.Optional["ImagePullPrincipalType"]:
        """The type of principal that CodeBuild will use to pull this build Docker image.

        default
        :default: ImagePullPrincipalType.SERVICE_ROLE

        stability
        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[_IRepository_aa6e452c]:
        """An optional ECR repository that the image is hosted in.

        default
        :default: no repository

        stability
        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretsManagerCredentials")
    def secrets_manager_credentials(self) -> typing.Optional[_ISecret_75279d36]:
        """The secretsManagerCredentials for access to a private registry.

        default
        :default: no credentials will be used

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: builtins.str) -> "BuildSpec":
        """Make a buildspec to run the indicated script.

        :param entrypoint: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="validate")
    def validate(
        self,
        *,
        build_image: typing.Optional["IBuildImage"] = None,
        compute_type: typing.Optional["ComputeType"] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, "BuildEnvironmentVariable"]] = None,
        privileged: typing.Optional[builtins.bool] = None,
    ) -> typing.List[builtins.str]:
        """Allows the image a chance to validate whether the passed configuration is correct.

        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false

        stability
        :stability: experimental
        """
        ...


class _IBuildImageProxy:
    """Represents a Docker image used for the CodeBuild Project builds.

    Use the concrete subclasses, either:
    {@link LinuxBuildImage} or {@link WindowsBuildImage}.

    stability
    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk-experiment.aws_codebuild.IBuildImage"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        """The default {@link ComputeType} to use with this image, if one was not specified in {@link BuildEnvironment#computeType} explicitly.

        stability
        :stability: experimental
        """
        return jsii.get(self, "defaultComputeType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        """The Docker image identifier that the build environment uses.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
        stability
        :stability: experimental
        """
        return jsii.get(self, "imageId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """The type of build environment.

        stability
        :stability: experimental
        """
        return jsii.get(self, "type")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imagePullPrincipalType")
    def image_pull_principal_type(self) -> typing.Optional["ImagePullPrincipalType"]:
        """The type of principal that CodeBuild will use to pull this build Docker image.

        default
        :default: ImagePullPrincipalType.SERVICE_ROLE

        stability
        :stability: experimental
        """
        return jsii.get(self, "imagePullPrincipalType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[_IRepository_aa6e452c]:
        """An optional ECR repository that the image is hosted in.

        default
        :default: no repository

        stability
        :stability: experimental
        """
        return jsii.get(self, "repository")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretsManagerCredentials")
    def secrets_manager_credentials(self) -> typing.Optional[_ISecret_75279d36]:
        """The secretsManagerCredentials for access to a private registry.

        default
        :default: no credentials will be used

        stability
        :stability: experimental
        """
        return jsii.get(self, "secretsManagerCredentials")

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: builtins.str) -> "BuildSpec":
        """Make a buildspec to run the indicated script.

        :param entrypoint: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "runScriptBuildspec", [entrypoint])

    @jsii.member(jsii_name="validate")
    def validate(
        self,
        *,
        build_image: typing.Optional["IBuildImage"] = None,
        compute_type: typing.Optional["ComputeType"] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, "BuildEnvironmentVariable"]] = None,
        privileged: typing.Optional[builtins.bool] = None,
    ) -> typing.List[builtins.str]:
        """Allows the image a chance to validate whether the passed configuration is correct.

        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false

        stability
        :stability: experimental
        """
        build_environment = BuildEnvironment(
            build_image=build_image,
            compute_type=compute_type,
            environment_variables=environment_variables,
            privileged=privileged,
        )

        return jsii.invoke(self, "validate", [build_environment])


@jsii.interface(jsii_type="monocdk-experiment.aws_codebuild.IFileSystemLocation")
class IFileSystemLocation(typing_extensions.Protocol):
    """The interface of a CodeBuild FileSystemLocation.

    Implemented by {@link EfsFileSystemLocation}.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IFileSystemLocationProxy

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_f50a3f53,
        project: "IProject",
    ) -> "FileSystemConfig":
        """Called by the project when a file system is added so it can perform binding operations on this file system location.

        :param scope: -
        :param project: -

        stability
        :stability: experimental
        """
        ...


class _IFileSystemLocationProxy:
    """The interface of a CodeBuild FileSystemLocation.

    Implemented by {@link EfsFileSystemLocation}.

    stability
    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk-experiment.aws_codebuild.IFileSystemLocation"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_f50a3f53,
        project: "IProject",
    ) -> "FileSystemConfig":
        """Called by the project when a file system is added so it can perform binding operations on this file system location.

        :param scope: -
        :param project: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope, project])


@jsii.interface(jsii_type="monocdk-experiment.aws_codebuild.IProject")
class IProject(
    _IResource_72f7ee7e,
    _IGrantable_0fcfc53a,
    _IConnectable_a587039f,
    typing_extensions.Protocol,
):
    """
    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IProjectProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="projectArn")
    def project_arn(self) -> builtins.str:
        """The ARN of this Project.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> builtins.str:
        """The human-visible name of this Project.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM service Role of this Project.

        Undefined for imported Projects.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, policy_statement: _PolicyStatement_f75dc775) -> None:
        """
        :param policy_statement: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """
        :param metric_name: The name of the metric.
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        return
        :return: a CloudWatch metric associated with this build project.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricBuilds")
    def metric_builds(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Measures the number of builds triggered.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Measures the duration of all builds over time.

        Units: Seconds

        Valid CloudWatch statistics: Average (recommended), Maximum, Minimum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricFailedBuilds")
    def metric_failed_builds(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Measures the number of builds that failed because of client error or because of a timeout.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricSucceededBuilds")
    def metric_succeeded_builds(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Measures the number of successful builds.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onBuildFailed")
    def on_build_failed(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines an event rule which triggers when a build fails.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onBuildStarted")
    def on_build_started(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines an event rule which triggers when a build starts.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onBuildSucceeded")
    def on_build_succeeded(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines an event rule which triggers when a build completes successfully.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule triggered when something happens with this project.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onPhaseChange")
    def on_phase_change(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule that triggers upon phase change of this build project.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule triggered when the build project state changes.

        You can filter specific build status events using an event
        pattern filter on the ``build-status`` detail field::

           const rule = project.onStateChange('OnBuildStarted', { target });
           rule.addEventPattern({
             detail: {
               'build-status': [
                 "IN_PROGRESS",
                 "SUCCEEDED",
                 "FAILED",
                 "STOPPED"
               ]
             }
           });

        You can also use the methods ``onBuildFailed`` and ``onBuildSucceeded`` to define rules for
        these specific state changes.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        stability
        :stability: experimental
        """
        ...


class _IProjectProxy(
    jsii.proxy_for(_IResource_72f7ee7e), # type: ignore
    jsii.proxy_for(_IGrantable_0fcfc53a), # type: ignore
    jsii.proxy_for(_IConnectable_a587039f), # type: ignore
):
    """
    stability
    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk-experiment.aws_codebuild.IProject"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="projectArn")
    def project_arn(self) -> builtins.str:
        """The ARN of this Project.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "projectArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> builtins.str:
        """The human-visible name of this Project.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "projectName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM service Role of this Project.

        Undefined for imported Projects.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, policy_statement: _PolicyStatement_f75dc775) -> None:
        """
        :param policy_statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToRolePolicy", [policy_statement])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """
        :param metric_name: The name of the metric.
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        return
        :return: a CloudWatch metric associated with this build project.

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricBuilds")
    def metric_builds(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Measures the number of builds triggered.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricBuilds", [props])

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Measures the duration of all builds over time.

        Units: Seconds

        Valid CloudWatch statistics: Average (recommended), Maximum, Minimum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricDuration", [props])

    @jsii.member(jsii_name="metricFailedBuilds")
    def metric_failed_builds(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Measures the number of builds that failed because of client error or because of a timeout.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricFailedBuilds", [props])

    @jsii.member(jsii_name="metricSucceededBuilds")
    def metric_succeeded_builds(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Measures the number of successful builds.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricSucceededBuilds", [props])

    @jsii.member(jsii_name="onBuildFailed")
    def on_build_failed(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines an event rule which triggers when a build fails.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onBuildFailed", [id, options])

    @jsii.member(jsii_name="onBuildStarted")
    def on_build_started(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines an event rule which triggers when a build starts.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onBuildStarted", [id, options])

    @jsii.member(jsii_name="onBuildSucceeded")
    def on_build_succeeded(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines an event rule which triggers when a build completes successfully.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onBuildSucceeded", [id, options])

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule triggered when something happens with this project.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onPhaseChange")
    def on_phase_change(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule that triggers upon phase change of this build project.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onPhaseChange", [id, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule triggered when the build project state changes.

        You can filter specific build status events using an event
        pattern filter on the ``build-status`` detail field::

           const rule = project.onStateChange('OnBuildStarted', { target });
           rule.addEventPattern({
             detail: {
               'build-status': [
                 "IN_PROGRESS",
                 "SUCCEEDED",
                 "FAILED",
                 "STOPPED"
               ]
             }
           });

        You can also use the methods ``onBuildFailed`` and ``onBuildSucceeded`` to define rules for
        these specific state changes.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onStateChange", [id, options])


@jsii.interface(jsii_type="monocdk-experiment.aws_codebuild.IReportGroup")
class IReportGroup(_IResource_72f7ee7e, typing_extensions.Protocol):
    """The interface representing the ReportGroup resource - either an existing one, imported using the {@link ReportGroup.fromReportGroupName} method, or a new one, created with the {@link ReportGroup} class.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IReportGroupProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="reportGroupArn")
    def report_group_arn(self) -> builtins.str:
        """The ARN of the ReportGroup.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="reportGroupName")
    def report_group_name(self) -> builtins.str:
        """The name of the ReportGroup.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, identity: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grants the given entity permissions to write (that is, upload reports to) this report group.

        :param identity: -

        stability
        :stability: experimental
        """
        ...


class _IReportGroupProxy(
    jsii.proxy_for(_IResource_72f7ee7e) # type: ignore
):
    """The interface representing the ReportGroup resource - either an existing one, imported using the {@link ReportGroup.fromReportGroupName} method, or a new one, created with the {@link ReportGroup} class.

    stability
    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk-experiment.aws_codebuild.IReportGroup"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="reportGroupArn")
    def report_group_arn(self) -> builtins.str:
        """The ARN of the ReportGroup.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "reportGroupArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="reportGroupName")
    def report_group_name(self) -> builtins.str:
        """The name of the ReportGroup.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "reportGroupName")

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, identity: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grants the given entity permissions to write (that is, upload reports to) this report group.

        :param identity: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantWrite", [identity])


@jsii.interface(jsii_type="monocdk-experiment.aws_codebuild.ISource")
class ISource(typing_extensions.Protocol):
    """The abstract interface of a CodeBuild source.

    Implemented by {@link Source}.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISourceProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="badgeSupported")
    def badge_supported(self) -> builtins.bool:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[builtins.str]:
        """
        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, project: "IProject") -> "SourceConfig":
        """
        :param scope: -
        :param project: -

        stability
        :stability: experimental
        """
        ...


class _ISourceProxy:
    """The abstract interface of a CodeBuild source.

    Implemented by {@link Source}.

    stability
    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk-experiment.aws_codebuild.ISource"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="badgeSupported")
    def badge_supported(self) -> builtins.bool:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "badgeSupported")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "type")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[builtins.str]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "identifier")

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, project: "IProject") -> "SourceConfig":
        """
        :param scope: -
        :param project: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope, project])


@jsii.enum(jsii_type="monocdk-experiment.aws_codebuild.ImagePullPrincipalType")
class ImagePullPrincipalType(enum.Enum):
    """The type of principal CodeBuild will use to pull your build Docker image.

    stability
    :stability: experimental
    """

    CODEBUILD = "CODEBUILD"
    """CODEBUILD specifies that CodeBuild uses its own identity when pulling the image.

    This means the resource policy of the ECR repository that hosts the image will be modified to trust
    CodeBuild's service principal.
    This is the required principal type when using CodeBuild's pre-defined images.

    stability
    :stability: experimental
    """
    SERVICE_ROLE = "SERVICE_ROLE"
    """SERVICE_ROLE specifies that AWS CodeBuild uses the project's role when pulling the image.

    The role will be granted pull permissions on the ECR repository hosting the image.

    stability
    :stability: experimental
    """


@jsii.implements(IBuildImage)
class LinuxBuildImage(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.LinuxBuildImage",
):
    """A CodeBuild image running Linux.

    This class has a bunch of public constants that represent the most popular images.

    You can also specify a custom image using one of the static methods:

    - LinuxBuildImage.fromDockerRegistry(image[, { secretsManagerCredentials }])
    - LinuxBuildImage.fromEcrRepository(repo[, tag])
    - LinuxBuildImage.fromAsset(parent, id, props)

    see
    :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(
        cls,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        directory: builtins.str,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file: typing.Optional[builtins.str] = None,
        repository_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional[_FollowMode_f74e7125] = None,
    ) -> "IBuildImage":
        """Uses an Docker image asset as a Linux build image.

        :param scope: -
        :param id: -
        :param directory: The directory where the Dockerfile is stored.
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - the default ECR repository for CDK assets
        :param target: Docker target to build to. Default: - no target
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never

        stability
        :stability: experimental
        """
        props = _DockerImageAssetProps_74635209(
            directory=directory,
            build_args=build_args,
            file=file,
            repository_name=repository_name,
            target=target,
            extra_hash=extra_hash,
            exclude=exclude,
            follow=follow,
        )

        return jsii.sinvoke(cls, "fromAsset", [scope, id, props])

    @jsii.member(jsii_name="fromCodeBuildImageId")
    @builtins.classmethod
    def from_code_build_image_id(cls, id: builtins.str) -> "IBuildImage":
        """Uses a Docker image provided by CodeBuild.

        :param id: The image identifier.

        return
        :return: A Docker image provided by CodeBuild.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "aws/codebuild/standard:4.0"
        """
        return jsii.sinvoke(cls, "fromCodeBuildImageId", [id])

    @jsii.member(jsii_name="fromDockerRegistry")
    @builtins.classmethod
    def from_docker_registry(
        cls,
        name: builtins.str,
        *,
        secrets_manager_credentials: typing.Optional[_ISecret_75279d36] = None,
    ) -> "IBuildImage":
        """
        :param name: -
        :param secrets_manager_credentials: The credentials, stored in Secrets Manager, used for accessing the repository holding the image, if the repository is private. Default: no credentials will be used (we assume the repository is public)

        return
        :return: a Linux build image from a Docker Hub image.

        stability
        :stability: experimental
        """
        options = DockerImageOptions(
            secrets_manager_credentials=secrets_manager_credentials
        )

        return jsii.sinvoke(cls, "fromDockerRegistry", [name, options])

    @jsii.member(jsii_name="fromEcrRepository")
    @builtins.classmethod
    def from_ecr_repository(
        cls,
        repository: _IRepository_aa6e452c,
        tag: typing.Optional[builtins.str] = None,
    ) -> "IBuildImage":
        """
        :param repository: The ECR repository.
        :param tag: Image tag (default "latest").

        return
        :return:

        A Linux build image from an ECR repository.

        NOTE: if the repository is external (i.e. imported), then we won't be able to add
        a resource policy statement for it so CodeBuild can pull the image.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-ecr.html
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromEcrRepository", [repository, tag])

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: builtins.str) -> "BuildSpec":
        """Make a buildspec to run the indicated script.

        :param entrypoint: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "runScriptBuildspec", [entrypoint])

    @jsii.member(jsii_name="validate")
    def validate(
        self,
        *,
        build_image: typing.Optional["IBuildImage"] = None,
        compute_type: typing.Optional["ComputeType"] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, "BuildEnvironmentVariable"]] = None,
        privileged: typing.Optional[builtins.bool] = None,
    ) -> typing.List[builtins.str]:
        """Allows the image a chance to validate whether the passed configuration is correct.

        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false

        stability
        :stability: experimental
        """
        _ = BuildEnvironment(
            build_image=build_image,
            compute_type=compute_type,
            environment_variables=environment_variables,
            privileged=privileged,
        )

        return jsii.invoke(self, "validate", [_])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="AMAZON_LINUX_2")
    def AMAZON_LINUX_2(cls) -> "IBuildImage":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "AMAZON_LINUX_2")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="AMAZON_LINUX_2_2")
    def AMAZON_LINUX_2_2(cls) -> "IBuildImage":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "AMAZON_LINUX_2_2")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="AMAZON_LINUX_2_3")
    def AMAZON_LINUX_2_3(cls) -> "IBuildImage":
        """The Amazon Linux 2 x86_64 standard image, version ``3.0``.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "AMAZON_LINUX_2_3")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="AMAZON_LINUX_2_ARM")
    def AMAZON_LINUX_2_ARM(cls) -> "IBuildImage":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "AMAZON_LINUX_2_ARM")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="STANDARD_1_0")
    def STANDARD_1_0(cls) -> "IBuildImage":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "STANDARD_1_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="STANDARD_2_0")
    def STANDARD_2_0(cls) -> "IBuildImage":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "STANDARD_2_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="STANDARD_3_0")
    def STANDARD_3_0(cls) -> "IBuildImage":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "STANDARD_3_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="STANDARD_4_0")
    def STANDARD_4_0(cls) -> "IBuildImage":
        """The ``aws/codebuild/standard:4.0`` build image.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "STANDARD_4_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_ANDROID_JAVA8_24_4_1")
    def UBUNTU_14_04_ANDROID_JAVA8_24_4_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_ANDROID_JAVA8_24_4_1")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_ANDROID_JAVA8_26_1_1")
    def UBUNTU_14_04_ANDROID_JAVA8_26_1_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_ANDROID_JAVA8_26_1_1")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_BASE")
    def UBUNTU_14_04_BASE(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_BASE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_DOCKER_17_09_0")
    def UBUNTU_14_04_DOCKER_17_09_0(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_DOCKER_17_09_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_DOCKER_18_09_0")
    def UBUNTU_14_04_DOCKER_18_09_0(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_DOCKER_18_09_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_DOTNET_CORE_1_1")
    def UBUNTU_14_04_DOTNET_CORE_1_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_DOTNET_CORE_1_1")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_DOTNET_CORE_2_0")
    def UBUNTU_14_04_DOTNET_CORE_2_0(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_DOTNET_CORE_2_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_DOTNET_CORE_2_1")
    def UBUNTU_14_04_DOTNET_CORE_2_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_DOTNET_CORE_2_1")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_GOLANG_1_10")
    def UBUNTU_14_04_GOLANG_1_10(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_GOLANG_1_10")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_GOLANG_1_11")
    def UBUNTU_14_04_GOLANG_1_11(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_GOLANG_1_11")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_NODEJS_10_1_0")
    def UBUNTU_14_04_NODEJS_10_1_0(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_NODEJS_10_1_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_NODEJS_10_14_1")
    def UBUNTU_14_04_NODEJS_10_14_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_NODEJS_10_14_1")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_NODEJS_6_3_1")
    def UBUNTU_14_04_NODEJS_6_3_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_NODEJS_6_3_1")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_NODEJS_8_11_0")
    def UBUNTU_14_04_NODEJS_8_11_0(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_NODEJS_8_11_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_OPEN_JDK_11")
    def UBUNTU_14_04_OPEN_JDK_11(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_OPEN_JDK_11")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_OPEN_JDK_8")
    def UBUNTU_14_04_OPEN_JDK_8(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_OPEN_JDK_8")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_OPEN_JDK_9")
    def UBUNTU_14_04_OPEN_JDK_9(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_OPEN_JDK_9")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_PHP_5_6")
    def UBUNTU_14_04_PHP_5_6(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PHP_5_6")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_PHP_7_0")
    def UBUNTU_14_04_PHP_7_0(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PHP_7_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_PHP_7_1")
    def UBUNTU_14_04_PHP_7_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PHP_7_1")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_2_7_12")
    def UBUNTU_14_04_PYTHON_2_7_12(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_2_7_12")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_3_6")
    def UBUNTU_14_04_PYTHON_3_3_6(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_3_6")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_4_5")
    def UBUNTU_14_04_PYTHON_3_4_5(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_4_5")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_5_2")
    def UBUNTU_14_04_PYTHON_3_5_2(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_5_2")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_6_5")
    def UBUNTU_14_04_PYTHON_3_6_5(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_6_5")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_7_1")
    def UBUNTU_14_04_PYTHON_3_7_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_7_1")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_RUBY_2_2_5")
    def UBUNTU_14_04_RUBY_2_2_5(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_RUBY_2_2_5")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_RUBY_2_3_1")
    def UBUNTU_14_04_RUBY_2_3_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_RUBY_2_3_1")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_RUBY_2_5_1")
    def UBUNTU_14_04_RUBY_2_5_1(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_RUBY_2_5_1")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UBUNTU_14_04_RUBY_2_5_3")
    def UBUNTU_14_04_RUBY_2_5_3(cls) -> "IBuildImage":
        """
        deprecated
        :deprecated: Use {@link STANDARD_2_0} and specify runtime in buildspec runtime-versions section

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "UBUNTU_14_04_RUBY_2_5_3")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        """The default {@link ComputeType} to use with this image, if one was not specified in {@link BuildEnvironment#computeType} explicitly.

        stability
        :stability: experimental
        """
        return jsii.get(self, "defaultComputeType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        """The Docker image identifier that the build environment uses.

        stability
        :stability: experimental
        """
        return jsii.get(self, "imageId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """The type of build environment.

        stability
        :stability: experimental
        """
        return jsii.get(self, "type")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imagePullPrincipalType")
    def image_pull_principal_type(self) -> typing.Optional["ImagePullPrincipalType"]:
        """The type of principal that CodeBuild will use to pull this build Docker image.

        stability
        :stability: experimental
        """
        return jsii.get(self, "imagePullPrincipalType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[_IRepository_aa6e452c]:
        """An optional ECR repository that the image is hosted in.

        stability
        :stability: experimental
        """
        return jsii.get(self, "repository")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretsManagerCredentials")
    def secrets_manager_credentials(self) -> typing.Optional[_ISecret_75279d36]:
        """The secretsManagerCredentials for access to a private registry.

        stability
        :stability: experimental
        """
        return jsii.get(self, "secretsManagerCredentials")


@jsii.enum(jsii_type="monocdk-experiment.aws_codebuild.LocalCacheMode")
class LocalCacheMode(enum.Enum):
    """Local cache modes to enable for the CodeBuild Project.

    stability
    :stability: experimental
    """

    SOURCE = "SOURCE"
    """Caches Git metadata for primary and secondary sources.

    stability
    :stability: experimental
    """
    DOCKER_LAYER = "DOCKER_LAYER"
    """Caches existing Docker layers.

    stability
    :stability: experimental
    """
    CUSTOM = "CUSTOM"
    """Caches directories you specify in the buildspec file.

    stability
    :stability: experimental
    """


class PhaseChangeEvent(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.PhaseChangeEvent",
):
    """Event fields for the CodeBuild "phase change" event.

    see
    :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html#sample-build-notifications-ref
    stability
    :stability: experimental
    """

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="buildComplete")
    def build_complete(cls) -> builtins.str:
        """Whether the build is complete.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "buildComplete")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="buildId")
    def build_id(cls) -> builtins.str:
        """The triggering build's id.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "buildId")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="completedPhase")
    def completed_phase(cls) -> builtins.str:
        """The phase that was just completed.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "completedPhase")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="completedPhaseDurationSeconds")
    def completed_phase_duration_seconds(cls) -> builtins.str:
        """The duration of the completed phase.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "completedPhaseDurationSeconds")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="completedPhaseStatus")
    def completed_phase_status(cls) -> builtins.str:
        """The status of the completed phase.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "completedPhaseStatus")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="projectName")
    def project_name(cls) -> builtins.str:
        """The triggering build's project name.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "projectName")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.PipelineProjectProps",
    jsii_struct_bases=[CommonProjectProps],
    name_mapping={
        "allow_all_outbound": "allowAllOutbound",
        "badge": "badge",
        "build_spec": "buildSpec",
        "cache": "cache",
        "description": "description",
        "encryption_key": "encryptionKey",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "file_system_locations": "fileSystemLocations",
        "grant_report_group_permissions": "grantReportGroupPermissions",
        "project_name": "projectName",
        "role": "role",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "timeout": "timeout",
        "vpc": "vpc",
    },
)
class PipelineProjectProps(CommonProjectProps):
    def __init__(
        self,
        *,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        badge: typing.Optional[builtins.bool] = None,
        build_spec: typing.Optional["BuildSpec"] = None,
        cache: typing.Optional["Cache"] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_IKey_3336c79d] = None,
        environment: typing.Optional["BuildEnvironment"] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, "BuildEnvironmentVariable"]] = None,
        file_system_locations: typing.Optional[typing.List["IFileSystemLocation"]] = None,
        grant_report_group_permissions: typing.Optional[builtins.bool] = None,
        project_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        subnet_selection: typing.Optional[_SubnetSelection_36a13cd6] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
    ) -> None:
        """
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param file_system_locations: An ProjectFileSystemLocation objects for a CodeBuild build project. A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint, and type of a file system created using Amazon Elastic File System. Default: - no file system locations
        :param grant_report_group_permissions: Add permissions to this project's role to create and use test report groups with name starting with the name of this project. That is the standard report group that gets created when a simple name (in contrast to an ARN) is used in the 'reports' section of the buildspec of this project. This is usually harmless, but you can turn these off if you don't plan on using test reports in this project. Default: true
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.

        stability
        :stability: experimental
        """
        if isinstance(environment, dict):
            environment = BuildEnvironment(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_36a13cd6(**subnet_selection)
        self._values: typing.Dict[str, typing.Any] = {}
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if badge is not None:
            self._values["badge"] = badge
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if cache is not None:
            self._values["cache"] = cache
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if file_system_locations is not None:
            self._values["file_system_locations"] = file_system_locations
        if grant_report_group_permissions is not None:
            self._values["grant_report_group_permissions"] = grant_report_group_permissions
        if project_name is not None:
            self._values["project_name"] = project_name
        if role is not None:
            self._values["role"] = role
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        """Whether to allow the CodeBuild to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        CodeBuild project to connect to network targets.

        Only used if 'vpc' is supplied.

        default
        :default: true

        stability
        :stability: experimental
        """
        result = self._values.get("allow_all_outbound")
        return result

    @builtins.property
    def badge(self) -> typing.Optional[builtins.bool]:
        """Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge.

        For more information, see Build Badges Sample
        in the AWS CodeBuild User Guide.

        default
        :default: false

        stability
        :stability: experimental
        """
        result = self._values.get("badge")
        return result

    @builtins.property
    def build_spec(self) -> typing.Optional["BuildSpec"]:
        """Filename or contents of buildspec in JSON format.

        default
        :default: - Empty buildspec.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-example
        stability
        :stability: experimental
        """
        result = self._values.get("build_spec")
        return result

    @builtins.property
    def cache(self) -> typing.Optional["Cache"]:
        """Caching strategy to use.

        default
        :default: Cache.none

        stability
        :stability: experimental
        """
        result = self._values.get("cache")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """A description of the project.

        Use the description to identify the purpose
        of the project.

        default
        :default: - No description.

        stability
        :stability: experimental
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """Encryption key to use to read and write artifacts.

        default
        :default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.

        stability
        :stability: experimental
        """
        result = self._values.get("encryption_key")
        return result

    @builtins.property
    def environment(self) -> typing.Optional["BuildEnvironment"]:
        """Build environment to use for the build.

        default
        :default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0

        stability
        :stability: experimental
        """
        result = self._values.get("environment")
        return result

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "BuildEnvironmentVariable"]]:
        """Additional environment variables to add to the build environment.

        default
        :default: - No additional environment variables are specified.

        stability
        :stability: experimental
        """
        result = self._values.get("environment_variables")
        return result

    @builtins.property
    def file_system_locations(
        self,
    ) -> typing.Optional[typing.List["IFileSystemLocation"]]:
        """An  ProjectFileSystemLocation objects for a CodeBuild build project.

        A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint,
        and type of a file system created using Amazon Elastic File System.

        default
        :default: - no file system locations

        stability
        :stability: experimental
        """
        result = self._values.get("file_system_locations")
        return result

    @builtins.property
    def grant_report_group_permissions(self) -> typing.Optional[builtins.bool]:
        """Add permissions to this project's role to create and use test report groups with name starting with the name of this project.

        That is the standard report group that gets created when a simple name
        (in contrast to an ARN)
        is used in the 'reports' section of the buildspec of this project.
        This is usually harmless, but you can turn these off if you don't plan on using test
        reports in this project.

        default
        :default: true

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/test-report-group-naming.html
        stability
        :stability: experimental
        """
        result = self._values.get("grant_report_group_permissions")
        return result

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        """The physical, human-readable name of the CodeBuild Project.

        default
        :default: - Name is automatically generated.

        stability
        :stability: experimental
        """
        result = self._values.get("project_name")
        return result

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Service Role to assume while running the build.

        default
        :default: - A role will be created.

        stability
        :stability: experimental
        """
        result = self._values.get("role")
        return result

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """What security group to associate with the codebuild project's network interfaces.

        If no security group is identified, one will be created automatically.

        Only used if 'vpc' is supplied.

        default
        :default: - Security group will be automatically created.

        stability
        :stability: experimental
        """
        result = self._values.get("security_groups")
        return result

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied.

        default
        :default: - All private subnets.

        stability
        :stability: experimental
        """
        result = self._values.get("subnet_selection")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        default
        :default: Duration.hours(1)

        stability
        :stability: experimental
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """VPC network to place codebuild network interfaces.

        Specify this if the codebuild project needs to access resources in a VPC.

        default
        :default: - No VPC is specified.

        stability
        :stability: experimental
        """
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IProject)
class Project(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.Project",
):
    """A representation of a CodeBuild Project.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        artifacts: typing.Optional["IArtifacts"] = None,
        secondary_artifacts: typing.Optional[typing.List["IArtifacts"]] = None,
        secondary_sources: typing.Optional[typing.List["ISource"]] = None,
        source: typing.Optional["ISource"] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        badge: typing.Optional[builtins.bool] = None,
        build_spec: typing.Optional["BuildSpec"] = None,
        cache: typing.Optional["Cache"] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_IKey_3336c79d] = None,
        environment: typing.Optional["BuildEnvironment"] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, "BuildEnvironmentVariable"]] = None,
        file_system_locations: typing.Optional[typing.List["IFileSystemLocation"]] = None,
        grant_report_group_permissions: typing.Optional[builtins.bool] = None,
        project_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        subnet_selection: typing.Optional[_SubnetSelection_36a13cd6] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param artifacts: Defines where build artifacts will be stored. Could be: PipelineBuildArtifacts, NoArtifacts and S3Artifacts. Default: NoArtifacts
        :param secondary_artifacts: The secondary artifacts for the Project. Can also be added after the Project has been created by using the {@link Project#addSecondaryArtifact} method. Default: - No secondary artifacts.
        :param secondary_sources: The secondary sources for the Project. Can be also added after the Project has been created by using the {@link Project#addSecondarySource} method. Default: - No secondary sources.
        :param source: The source of the build. *Note*: if {@link NoSource} is given as the source, then you need to provide an explicit ``buildSpec``. Default: - NoSource
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param file_system_locations: An ProjectFileSystemLocation objects for a CodeBuild build project. A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint, and type of a file system created using Amazon Elastic File System. Default: - no file system locations
        :param grant_report_group_permissions: Add permissions to this project's role to create and use test report groups with name starting with the name of this project. That is the standard report group that gets created when a simple name (in contrast to an ARN) is used in the 'reports' section of the buildspec of this project. This is usually harmless, but you can turn these off if you don't plan on using test reports in this project. Default: true
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.

        stability
        :stability: experimental
        """
        props = ProjectProps(
            artifacts=artifacts,
            secondary_artifacts=secondary_artifacts,
            secondary_sources=secondary_sources,
            source=source,
            allow_all_outbound=allow_all_outbound,
            badge=badge,
            build_spec=build_spec,
            cache=cache,
            description=description,
            encryption_key=encryption_key,
            environment=environment,
            environment_variables=environment_variables,
            file_system_locations=file_system_locations,
            grant_report_group_permissions=grant_report_group_permissions,
            project_name=project_name,
            role=role,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
        )

        jsii.create(Project, self, [scope, id, props])

    @jsii.member(jsii_name="fromProjectArn")
    @builtins.classmethod
    def from_project_arn(
        cls,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        project_arn: builtins.str,
    ) -> "IProject":
        """
        :param scope: -
        :param id: -
        :param project_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromProjectArn", [scope, id, project_arn])

    @jsii.member(jsii_name="fromProjectName")
    @builtins.classmethod
    def from_project_name(
        cls,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        project_name: builtins.str,
    ) -> "IProject":
        """Import a Project defined either outside the CDK, or in a different CDK Stack (and exported using the {@link export} method).

        :param scope: the parent Construct for this Construct.
        :param id: the logical name of this Construct.
        :param project_name: the name of the project to import.

        return
        :return: a reference to the existing Project

        stability
        :stability: experimental
        note:
        :note::

        if you're importing a CodeBuild Project for use
        in a CodePipeline, make sure the existing Project
        has permissions to access the S3 Bucket of that Pipeline -
        otherwise, builds in that Pipeline will always fail.
        """
        return jsii.sinvoke(cls, "fromProjectName", [scope, id, project_name])

    @jsii.member(jsii_name="serializeEnvVariables")
    @builtins.classmethod
    def serialize_env_variables(
        cls,
        environment_variables: typing.Mapping[builtins.str, "BuildEnvironmentVariable"],
    ) -> typing.List["CfnProject.EnvironmentVariableProperty"]:
        """Convert the environment variables map of string to {@link BuildEnvironmentVariable}, which is the customer-facing type, to a list of {@link CfnProject.EnvironmentVariableProperty}, which is the representation of environment variables in CloudFormation.

        :param environment_variables: the map of string to environment variables.

        return
        :return: an array of {@link CfnProject.EnvironmentVariableProperty} instances

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "serializeEnvVariables", [environment_variables])

    @jsii.member(jsii_name="addFileSystemLocation")
    def add_file_system_location(
        self,
        file_system_location: "IFileSystemLocation",
    ) -> None:
        """Adds a fileSystemLocation to the Project.

        :param file_system_location: the fileSystemLocation to add.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addFileSystemLocation", [file_system_location])

    @jsii.member(jsii_name="addSecondaryArtifact")
    def add_secondary_artifact(self, secondary_artifact: "IArtifacts") -> None:
        """Adds a secondary artifact to the Project.

        :param secondary_artifact: the artifact to add as a secondary artifact.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addSecondaryArtifact", [secondary_artifact])

    @jsii.member(jsii_name="addSecondarySource")
    def add_secondary_source(self, secondary_source: "ISource") -> None:
        """Adds a secondary source to the Project.

        :param secondary_source: the source to add as a secondary source.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addSecondarySource", [secondary_source])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: _PolicyStatement_f75dc775) -> None:
        """Add a permission only if there's a policy attached.

        :param statement: The permissions statement to add.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="bindToCodePipeline")
    def bind_to_code_pipeline(
        self,
        _scope: _Construct_f50a3f53,
        *,
        artifact_bucket: _IBucket_25bad983,
    ) -> None:
        """A callback invoked when the given project is added to a CodePipeline.

        :param _scope: the construct the binding is taking place in.
        :param artifact_bucket: The artifact bucket that will be used by the action that invokes this project.

        stability
        :stability: experimental
        """
        options = BindToCodePipelineOptions(artifact_bucket=artifact_bucket)

        return jsii.invoke(self, "bindToCodePipeline", [_scope, options])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """
        :param metric_name: The name of the metric.
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        return
        :return: a CloudWatch metric associated with this build project.

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricBuilds")
    def metric_builds(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Measures the number of builds triggered.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricBuilds", [props])

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Measures the duration of all builds over time.

        Units: Seconds

        Valid CloudWatch statistics: Average (recommended), Maximum, Minimum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricDuration", [props])

    @jsii.member(jsii_name="metricFailedBuilds")
    def metric_failed_builds(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Measures the number of builds that failed because of client error or because of a timeout.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricFailedBuilds", [props])

    @jsii.member(jsii_name="metricSucceededBuilds")
    def metric_succeeded_builds(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Measures the number of successful builds.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricSucceededBuilds", [props])

    @jsii.member(jsii_name="onBuildFailed")
    def on_build_failed(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines an event rule which triggers when a build fails.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onBuildFailed", [id, options])

    @jsii.member(jsii_name="onBuildStarted")
    def on_build_started(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines an event rule which triggers when a build starts.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onBuildStarted", [id, options])

    @jsii.member(jsii_name="onBuildSucceeded")
    def on_build_succeeded(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines an event rule which triggers when a build completes successfully.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onBuildSucceeded", [id, options])

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule triggered when something happens with this project.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onPhaseChange")
    def on_phase_change(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule that triggers upon phase change of this build project.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onPhaseChange", [id, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule triggered when the build project state changes.

        You can filter specific build status events using an event
        pattern filter on the ``build-status`` detail field::

           const rule = project.onStateChange('OnBuildStarted', { target });
           rule.addEventPattern({
             detail: {
               'build-status': [
                 "IN_PROGRESS",
                 "SUCCEEDED",
                 "FAILED",
                 "STOPPED"
               ]
             }
           });

        You can also use the methods ``onBuildFailed`` and ``onBuildSucceeded`` to define rules for
        these specific state changes.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onStateChange", [id, options])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        stability
        :stability: experimental
        override:
        :override:: true
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """Access the Connections object.

        Will fail if this Project does not have a VPC set.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_97126874:
        """The principal to grant permissions to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="projectArn")
    def project_arn(self) -> builtins.str:
        """The ARN of the project.

        stability
        :stability: experimental
        """
        return jsii.get(self, "projectArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> builtins.str:
        """The name of the project.

        stability
        :stability: experimental
        """
        return jsii.get(self, "projectName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role for this project.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.ProjectProps",
    jsii_struct_bases=[CommonProjectProps],
    name_mapping={
        "allow_all_outbound": "allowAllOutbound",
        "badge": "badge",
        "build_spec": "buildSpec",
        "cache": "cache",
        "description": "description",
        "encryption_key": "encryptionKey",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "file_system_locations": "fileSystemLocations",
        "grant_report_group_permissions": "grantReportGroupPermissions",
        "project_name": "projectName",
        "role": "role",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "timeout": "timeout",
        "vpc": "vpc",
        "artifacts": "artifacts",
        "secondary_artifacts": "secondaryArtifacts",
        "secondary_sources": "secondarySources",
        "source": "source",
    },
)
class ProjectProps(CommonProjectProps):
    def __init__(
        self,
        *,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        badge: typing.Optional[builtins.bool] = None,
        build_spec: typing.Optional["BuildSpec"] = None,
        cache: typing.Optional["Cache"] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_IKey_3336c79d] = None,
        environment: typing.Optional["BuildEnvironment"] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, "BuildEnvironmentVariable"]] = None,
        file_system_locations: typing.Optional[typing.List["IFileSystemLocation"]] = None,
        grant_report_group_permissions: typing.Optional[builtins.bool] = None,
        project_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        subnet_selection: typing.Optional[_SubnetSelection_36a13cd6] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
        artifacts: typing.Optional["IArtifacts"] = None,
        secondary_artifacts: typing.Optional[typing.List["IArtifacts"]] = None,
        secondary_sources: typing.Optional[typing.List["ISource"]] = None,
        source: typing.Optional["ISource"] = None,
    ) -> None:
        """
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param file_system_locations: An ProjectFileSystemLocation objects for a CodeBuild build project. A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint, and type of a file system created using Amazon Elastic File System. Default: - no file system locations
        :param grant_report_group_permissions: Add permissions to this project's role to create and use test report groups with name starting with the name of this project. That is the standard report group that gets created when a simple name (in contrast to an ARN) is used in the 'reports' section of the buildspec of this project. This is usually harmless, but you can turn these off if you don't plan on using test reports in this project. Default: true
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.
        :param artifacts: Defines where build artifacts will be stored. Could be: PipelineBuildArtifacts, NoArtifacts and S3Artifacts. Default: NoArtifacts
        :param secondary_artifacts: The secondary artifacts for the Project. Can also be added after the Project has been created by using the {@link Project#addSecondaryArtifact} method. Default: - No secondary artifacts.
        :param secondary_sources: The secondary sources for the Project. Can be also added after the Project has been created by using the {@link Project#addSecondarySource} method. Default: - No secondary sources.
        :param source: The source of the build. *Note*: if {@link NoSource} is given as the source, then you need to provide an explicit ``buildSpec``. Default: - NoSource

        stability
        :stability: experimental
        """
        if isinstance(environment, dict):
            environment = BuildEnvironment(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_36a13cd6(**subnet_selection)
        self._values: typing.Dict[str, typing.Any] = {}
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if badge is not None:
            self._values["badge"] = badge
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if cache is not None:
            self._values["cache"] = cache
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if file_system_locations is not None:
            self._values["file_system_locations"] = file_system_locations
        if grant_report_group_permissions is not None:
            self._values["grant_report_group_permissions"] = grant_report_group_permissions
        if project_name is not None:
            self._values["project_name"] = project_name
        if role is not None:
            self._values["role"] = role
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc
        if artifacts is not None:
            self._values["artifacts"] = artifacts
        if secondary_artifacts is not None:
            self._values["secondary_artifacts"] = secondary_artifacts
        if secondary_sources is not None:
            self._values["secondary_sources"] = secondary_sources
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        """Whether to allow the CodeBuild to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        CodeBuild project to connect to network targets.

        Only used if 'vpc' is supplied.

        default
        :default: true

        stability
        :stability: experimental
        """
        result = self._values.get("allow_all_outbound")
        return result

    @builtins.property
    def badge(self) -> typing.Optional[builtins.bool]:
        """Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge.

        For more information, see Build Badges Sample
        in the AWS CodeBuild User Guide.

        default
        :default: false

        stability
        :stability: experimental
        """
        result = self._values.get("badge")
        return result

    @builtins.property
    def build_spec(self) -> typing.Optional["BuildSpec"]:
        """Filename or contents of buildspec in JSON format.

        default
        :default: - Empty buildspec.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-example
        stability
        :stability: experimental
        """
        result = self._values.get("build_spec")
        return result

    @builtins.property
    def cache(self) -> typing.Optional["Cache"]:
        """Caching strategy to use.

        default
        :default: Cache.none

        stability
        :stability: experimental
        """
        result = self._values.get("cache")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """A description of the project.

        Use the description to identify the purpose
        of the project.

        default
        :default: - No description.

        stability
        :stability: experimental
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """Encryption key to use to read and write artifacts.

        default
        :default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.

        stability
        :stability: experimental
        """
        result = self._values.get("encryption_key")
        return result

    @builtins.property
    def environment(self) -> typing.Optional["BuildEnvironment"]:
        """Build environment to use for the build.

        default
        :default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0

        stability
        :stability: experimental
        """
        result = self._values.get("environment")
        return result

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "BuildEnvironmentVariable"]]:
        """Additional environment variables to add to the build environment.

        default
        :default: - No additional environment variables are specified.

        stability
        :stability: experimental
        """
        result = self._values.get("environment_variables")
        return result

    @builtins.property
    def file_system_locations(
        self,
    ) -> typing.Optional[typing.List["IFileSystemLocation"]]:
        """An  ProjectFileSystemLocation objects for a CodeBuild build project.

        A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint,
        and type of a file system created using Amazon Elastic File System.

        default
        :default: - no file system locations

        stability
        :stability: experimental
        """
        result = self._values.get("file_system_locations")
        return result

    @builtins.property
    def grant_report_group_permissions(self) -> typing.Optional[builtins.bool]:
        """Add permissions to this project's role to create and use test report groups with name starting with the name of this project.

        That is the standard report group that gets created when a simple name
        (in contrast to an ARN)
        is used in the 'reports' section of the buildspec of this project.
        This is usually harmless, but you can turn these off if you don't plan on using test
        reports in this project.

        default
        :default: true

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/test-report-group-naming.html
        stability
        :stability: experimental
        """
        result = self._values.get("grant_report_group_permissions")
        return result

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        """The physical, human-readable name of the CodeBuild Project.

        default
        :default: - Name is automatically generated.

        stability
        :stability: experimental
        """
        result = self._values.get("project_name")
        return result

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Service Role to assume while running the build.

        default
        :default: - A role will be created.

        stability
        :stability: experimental
        """
        result = self._values.get("role")
        return result

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """What security group to associate with the codebuild project's network interfaces.

        If no security group is identified, one will be created automatically.

        Only used if 'vpc' is supplied.

        default
        :default: - Security group will be automatically created.

        stability
        :stability: experimental
        """
        result = self._values.get("security_groups")
        return result

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied.

        default
        :default: - All private subnets.

        stability
        :stability: experimental
        """
        result = self._values.get("subnet_selection")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        default
        :default: Duration.hours(1)

        stability
        :stability: experimental
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """VPC network to place codebuild network interfaces.

        Specify this if the codebuild project needs to access resources in a VPC.

        default
        :default: - No VPC is specified.

        stability
        :stability: experimental
        """
        result = self._values.get("vpc")
        return result

    @builtins.property
    def artifacts(self) -> typing.Optional["IArtifacts"]:
        """Defines where build artifacts will be stored.

        Could be: PipelineBuildArtifacts, NoArtifacts and S3Artifacts.

        default
        :default: NoArtifacts

        stability
        :stability: experimental
        """
        result = self._values.get("artifacts")
        return result

    @builtins.property
    def secondary_artifacts(self) -> typing.Optional[typing.List["IArtifacts"]]:
        """The secondary artifacts for the Project.

        Can also be added after the Project has been created by using the {@link Project#addSecondaryArtifact} method.

        default
        :default: - No secondary artifacts.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html
        stability
        :stability: experimental
        """
        result = self._values.get("secondary_artifacts")
        return result

    @builtins.property
    def secondary_sources(self) -> typing.Optional[typing.List["ISource"]]:
        """The secondary sources for the Project.

        Can be also added after the Project has been created by using the {@link Project#addSecondarySource} method.

        default
        :default: - No secondary sources.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html
        stability
        :stability: experimental
        """
        result = self._values.get("secondary_sources")
        return result

    @builtins.property
    def source(self) -> typing.Optional["ISource"]:
        """The source of the build.

        *Note*: if {@link NoSource} is given as the source,
        then you need to provide an explicit ``buildSpec``.

        default
        :default: - NoSource

        stability
        :stability: experimental
        """
        result = self._values.get("source")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IReportGroup)
class ReportGroup(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.ReportGroup",
):
    """The ReportGroup resource class.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        export_bucket: typing.Optional[_IBucket_25bad983] = None,
        removal_policy: typing.Optional[_RemovalPolicy_5986e9f3] = None,
        report_group_name: typing.Optional[builtins.str] = None,
        zip_export: typing.Optional[builtins.bool] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param export_bucket: An optional S3 bucket to export the reports to. Default: - the reports will not be exported
        :param removal_policy: What to do when this resource is deleted from a stack. As CodeBuild does not allow deleting a ResourceGroup that has reports inside of it, this is set to retain the resource by default. Default: RemovalPolicy.RETAIN
        :param report_group_name: The physical name of the report group. Default: - CloudFormation-generated name
        :param zip_export: Whether to output the report files into the export bucket as-is, or create a ZIP from them before doing the export. Ignored if {@link exportBucket} has not been provided. Default: - false (the files will not be ZIPped)

        stability
        :stability: experimental
        """
        props = ReportGroupProps(
            export_bucket=export_bucket,
            removal_policy=removal_policy,
            report_group_name=report_group_name,
            zip_export=zip_export,
        )

        jsii.create(ReportGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromReportGroupName")
    @builtins.classmethod
    def from_report_group_name(
        cls,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        report_group_name: builtins.str,
    ) -> "IReportGroup":
        """Reference an existing ReportGroup, defined outside of the CDK code, by name.

        :param scope: -
        :param id: -
        :param report_group_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromReportGroupName", [scope, id, report_group_name])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, identity: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grants the given entity permissions to write (that is, upload reports to) this report group.

        :param identity: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantWrite", [identity])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="reportGroupArn")
    def report_group_arn(self) -> builtins.str:
        """The ARN of the ReportGroup.

        stability
        :stability: experimental
        """
        return jsii.get(self, "reportGroupArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="reportGroupName")
    def report_group_name(self) -> builtins.str:
        """The name of the ReportGroup.

        stability
        :stability: experimental
        """
        return jsii.get(self, "reportGroupName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="exportBucket")
    def _export_bucket(self) -> typing.Optional[_IBucket_25bad983]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "exportBucket")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.ReportGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "export_bucket": "exportBucket",
        "removal_policy": "removalPolicy",
        "report_group_name": "reportGroupName",
        "zip_export": "zipExport",
    },
)
class ReportGroupProps:
    def __init__(
        self,
        *,
        export_bucket: typing.Optional[_IBucket_25bad983] = None,
        removal_policy: typing.Optional[_RemovalPolicy_5986e9f3] = None,
        report_group_name: typing.Optional[builtins.str] = None,
        zip_export: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Construction properties for {@link ReportGroup}.

        :param export_bucket: An optional S3 bucket to export the reports to. Default: - the reports will not be exported
        :param removal_policy: What to do when this resource is deleted from a stack. As CodeBuild does not allow deleting a ResourceGroup that has reports inside of it, this is set to retain the resource by default. Default: RemovalPolicy.RETAIN
        :param report_group_name: The physical name of the report group. Default: - CloudFormation-generated name
        :param zip_export: Whether to output the report files into the export bucket as-is, or create a ZIP from them before doing the export. Ignored if {@link exportBucket} has not been provided. Default: - false (the files will not be ZIPped)

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if export_bucket is not None:
            self._values["export_bucket"] = export_bucket
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if report_group_name is not None:
            self._values["report_group_name"] = report_group_name
        if zip_export is not None:
            self._values["zip_export"] = zip_export

    @builtins.property
    def export_bucket(self) -> typing.Optional[_IBucket_25bad983]:
        """An optional S3 bucket to export the reports to.

        default
        :default: - the reports will not be exported

        stability
        :stability: experimental
        """
        result = self._values.get("export_bucket")
        return result

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_5986e9f3]:
        """What to do when this resource is deleted from a stack.

        As CodeBuild does not allow deleting a ResourceGroup that has reports inside of it,
        this is set to retain the resource by default.

        default
        :default: RemovalPolicy.RETAIN

        stability
        :stability: experimental
        """
        result = self._values.get("removal_policy")
        return result

    @builtins.property
    def report_group_name(self) -> typing.Optional[builtins.str]:
        """The physical name of the report group.

        default
        :default: - CloudFormation-generated name

        stability
        :stability: experimental
        """
        result = self._values.get("report_group_name")
        return result

    @builtins.property
    def zip_export(self) -> typing.Optional[builtins.bool]:
        """Whether to output the report files into the export bucket as-is, or create a ZIP from them before doing the export.

        Ignored if {@link exportBucket} has not been provided.

        default
        :default: - false (the files will not be ZIPped)

        stability
        :stability: experimental
        """
        result = self._values.get("zip_export")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReportGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.S3ArtifactsProps",
    jsii_struct_bases=[ArtifactsProps],
    name_mapping={
        "identifier": "identifier",
        "bucket": "bucket",
        "encryption": "encryption",
        "include_build_id": "includeBuildId",
        "name": "name",
        "package_zip": "packageZip",
        "path": "path",
    },
)
class S3ArtifactsProps(ArtifactsProps):
    def __init__(
        self,
        *,
        identifier: typing.Optional[builtins.str] = None,
        bucket: _IBucket_25bad983,
        encryption: typing.Optional[builtins.bool] = None,
        include_build_id: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        package_zip: typing.Optional[builtins.bool] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        """Construction properties for {@link S3Artifacts}.

        :param identifier: The artifact identifier. This property is required on secondary artifacts.
        :param bucket: The name of the output bucket.
        :param encryption: If this is false, build output will not be encrypted. This is useful if the artifact to publish a static website or sharing content with others Default: true - output will be encrypted
        :param include_build_id: Indicates if the build ID should be included in the path. If this is set to true, then the build artifact will be stored in "//". Default: true
        :param name: The name of the build output ZIP file or folder inside the bucket. The full S3 object key will be "//" or "/" depending on whether ``includeBuildId`` is set to true. If not set, ``overrideArtifactName`` will be set and the name from the buildspec will be used instead. Default: undefined, and use the name from the buildspec
        :param package_zip: If this is true, all build output will be packaged into a single .zip file. Otherwise, all files will be uploaded to /. Default: true - files will be archived
        :param path: The path inside of the bucket for the build output .zip file or folder. If a value is not specified, then build output will be stored at the root of the bucket (or under the directory if ``includeBuildId`` is set to true). Default: the root of the bucket

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
        }
        if identifier is not None:
            self._values["identifier"] = identifier
        if encryption is not None:
            self._values["encryption"] = encryption
        if include_build_id is not None:
            self._values["include_build_id"] = include_build_id
        if name is not None:
            self._values["name"] = name
        if package_zip is not None:
            self._values["package_zip"] = package_zip
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def identifier(self) -> typing.Optional[builtins.str]:
        """The artifact identifier.

        This property is required on secondary artifacts.

        stability
        :stability: experimental
        """
        result = self._values.get("identifier")
        return result

    @builtins.property
    def bucket(self) -> _IBucket_25bad983:
        """The name of the output bucket.

        stability
        :stability: experimental
        """
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return result

    @builtins.property
    def encryption(self) -> typing.Optional[builtins.bool]:
        """If this is false, build output will not be encrypted.

        This is useful if the artifact to publish a static website or sharing content with others

        default
        :default: true - output will be encrypted

        stability
        :stability: experimental
        """
        result = self._values.get("encryption")
        return result

    @builtins.property
    def include_build_id(self) -> typing.Optional[builtins.bool]:
        """Indicates if the build ID should be included in the path.

        If this is set to true,
        then the build artifact will be stored in "//".

        default
        :default: true

        stability
        :stability: experimental
        """
        result = self._values.get("include_build_id")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """The name of the build output ZIP file or folder inside the bucket.

        The full S3 object key will be "//" or
        "/" depending on whether ``includeBuildId`` is set to true.

        If not set, ``overrideArtifactName`` will be set and the name from the
        buildspec will be used instead.

        default
        :default: undefined, and use the name from the buildspec

        stability
        :stability: experimental
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def package_zip(self) -> typing.Optional[builtins.bool]:
        """If this is true, all build output will be packaged into a single .zip file. Otherwise, all files will be uploaded to /.

        default
        :default: true - files will be archived

        stability
        :stability: experimental
        """
        result = self._values.get("package_zip")
        return result

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        """The path inside of the bucket for the build output .zip file or folder. If a value is not specified, then build output will be stored at the root of the bucket (or under the  directory if ``includeBuildId`` is set to true).

        default
        :default: the root of the bucket

        stability
        :stability: experimental
        """
        result = self._values.get("path")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ArtifactsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISource)
class Source(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk-experiment.aws_codebuild.Source",
):
    """Source provider definition for a CodeBuild Project.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _SourceProxy

    def __init__(self, *, identifier: typing.Optional[builtins.str] = None) -> None:
        """
        :param identifier: The source identifier. This property is required on secondary sources.

        stability
        :stability: experimental
        """
        props = SourceProps(identifier=identifier)

        jsii.create(Source, self, [props])

    @jsii.member(jsii_name="bitBucket")
    @builtins.classmethod
    def bit_bucket(
        cls,
        *,
        owner: builtins.str,
        repo: builtins.str,
        branch_or_ref: typing.Optional[builtins.str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
        fetch_submodules: typing.Optional[builtins.bool] = None,
        report_build_status: typing.Optional[builtins.bool] = None,
        webhook: typing.Optional[builtins.bool] = None,
        webhook_filters: typing.Optional[typing.List["FilterGroup"]] = None,
        identifier: typing.Optional[builtins.str] = None,
    ) -> "ISource":
        """
        :param owner: The BitBucket account/user that owns the repo.
        :param repo: The name of the repo (without the username).
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param fetch_submodules: Whether to fetch submodules while cloning git repo. Default: false
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build
        :param identifier: The source identifier. This property is required on secondary sources.

        stability
        :stability: experimental
        """
        props = BitBucketSourceProps(
            owner=owner,
            repo=repo,
            branch_or_ref=branch_or_ref,
            clone_depth=clone_depth,
            fetch_submodules=fetch_submodules,
            report_build_status=report_build_status,
            webhook=webhook,
            webhook_filters=webhook_filters,
            identifier=identifier,
        )

        return jsii.sinvoke(cls, "bitBucket", [props])

    @jsii.member(jsii_name="codeCommit")
    @builtins.classmethod
    def code_commit(
        cls,
        *,
        repository: _IRepository_91f381de,
        branch_or_ref: typing.Optional[builtins.str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
        fetch_submodules: typing.Optional[builtins.bool] = None,
        identifier: typing.Optional[builtins.str] = None,
    ) -> "ISource":
        """
        :param repository: 
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param fetch_submodules: Whether to fetch submodules while cloning git repo. Default: false
        :param identifier: The source identifier. This property is required on secondary sources.

        stability
        :stability: experimental
        """
        props = CodeCommitSourceProps(
            repository=repository,
            branch_or_ref=branch_or_ref,
            clone_depth=clone_depth,
            fetch_submodules=fetch_submodules,
            identifier=identifier,
        )

        return jsii.sinvoke(cls, "codeCommit", [props])

    @jsii.member(jsii_name="gitHub")
    @builtins.classmethod
    def git_hub(
        cls,
        *,
        owner: builtins.str,
        repo: builtins.str,
        branch_or_ref: typing.Optional[builtins.str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
        fetch_submodules: typing.Optional[builtins.bool] = None,
        report_build_status: typing.Optional[builtins.bool] = None,
        webhook: typing.Optional[builtins.bool] = None,
        webhook_filters: typing.Optional[typing.List["FilterGroup"]] = None,
        identifier: typing.Optional[builtins.str] = None,
    ) -> "ISource":
        """
        :param owner: The GitHub account/user that owns the repo.
        :param repo: The name of the repo (without the username).
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param fetch_submodules: Whether to fetch submodules while cloning git repo. Default: false
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build
        :param identifier: The source identifier. This property is required on secondary sources.

        stability
        :stability: experimental
        """
        props = GitHubSourceProps(
            owner=owner,
            repo=repo,
            branch_or_ref=branch_or_ref,
            clone_depth=clone_depth,
            fetch_submodules=fetch_submodules,
            report_build_status=report_build_status,
            webhook=webhook,
            webhook_filters=webhook_filters,
            identifier=identifier,
        )

        return jsii.sinvoke(cls, "gitHub", [props])

    @jsii.member(jsii_name="gitHubEnterprise")
    @builtins.classmethod
    def git_hub_enterprise(
        cls,
        *,
        https_clone_url: builtins.str,
        branch_or_ref: typing.Optional[builtins.str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
        fetch_submodules: typing.Optional[builtins.bool] = None,
        ignore_ssl_errors: typing.Optional[builtins.bool] = None,
        report_build_status: typing.Optional[builtins.bool] = None,
        webhook: typing.Optional[builtins.bool] = None,
        webhook_filters: typing.Optional[typing.List["FilterGroup"]] = None,
        identifier: typing.Optional[builtins.str] = None,
    ) -> "ISource":
        """
        :param https_clone_url: The HTTPS URL of the repository in your GitHub Enterprise installation.
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param fetch_submodules: Whether to fetch submodules while cloning git repo. Default: false
        :param ignore_ssl_errors: Whether to ignore SSL errors when connecting to the repository. Default: false
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build
        :param identifier: The source identifier. This property is required on secondary sources.

        stability
        :stability: experimental
        """
        props = GitHubEnterpriseSourceProps(
            https_clone_url=https_clone_url,
            branch_or_ref=branch_or_ref,
            clone_depth=clone_depth,
            fetch_submodules=fetch_submodules,
            ignore_ssl_errors=ignore_ssl_errors,
            report_build_status=report_build_status,
            webhook=webhook,
            webhook_filters=webhook_filters,
            identifier=identifier,
        )

        return jsii.sinvoke(cls, "gitHubEnterprise", [props])

    @jsii.member(jsii_name="s3")
    @builtins.classmethod
    def s3(
        cls,
        *,
        bucket: _IBucket_25bad983,
        path: builtins.str,
        version: typing.Optional[builtins.str] = None,
        identifier: typing.Optional[builtins.str] = None,
    ) -> "ISource":
        """
        :param bucket: 
        :param path: 
        :param version: The version ID of the object that represents the build input ZIP file to use. Default: latest
        :param identifier: The source identifier. This property is required on secondary sources.

        stability
        :stability: experimental
        """
        props = S3SourceProps(
            bucket=bucket, path=path, version=version, identifier=identifier
        )

        return jsii.sinvoke(cls, "s3", [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, _project: "IProject") -> "SourceConfig":
        """Called by the project when the source is added so that the source can perform binding operations on the source.

        For example, it can grant permissions to the
        code build project to read from the S3 bucket.

        :param _scope: -
        :param _project: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _project])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="badgeSupported")
    def badge_supported(self) -> builtins.bool:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "badgeSupported")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    @abc.abstractmethod
    def type(self) -> builtins.str:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[builtins.str]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "identifier")


class _SourceProxy(Source):
    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "type")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.SourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "source_property": "sourceProperty",
        "build_triggers": "buildTriggers",
        "source_version": "sourceVersion",
    },
)
class SourceConfig:
    def __init__(
        self,
        *,
        source_property: "CfnProject.SourceProperty",
        build_triggers: typing.Optional["CfnProject.ProjectTriggersProperty"] = None,
        source_version: typing.Optional[builtins.str] = None,
    ) -> None:
        """The type returned from {@link ISource#bind}.

        :param source_property: 
        :param build_triggers: 
        :param source_version: ``AWS::CodeBuild::Project.SourceVersion``. Default: the latest version

        stability
        :stability: experimental
        """
        if isinstance(source_property, dict):
            source_property = CfnProject.SourceProperty(**source_property)
        if isinstance(build_triggers, dict):
            build_triggers = CfnProject.ProjectTriggersProperty(**build_triggers)
        self._values: typing.Dict[str, typing.Any] = {
            "source_property": source_property,
        }
        if build_triggers is not None:
            self._values["build_triggers"] = build_triggers
        if source_version is not None:
            self._values["source_version"] = source_version

    @builtins.property
    def source_property(self) -> "CfnProject.SourceProperty":
        """
        stability
        :stability: experimental
        """
        result = self._values.get("source_property")
        assert result is not None, "Required property 'source_property' is missing"
        return result

    @builtins.property
    def build_triggers(self) -> typing.Optional["CfnProject.ProjectTriggersProperty"]:
        """
        stability
        :stability: experimental
        """
        result = self._values.get("build_triggers")
        return result

    @builtins.property
    def source_version(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeBuild::Project.SourceVersion``.

        default
        :default: the latest version

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-sourceversion
        stability
        :stability: experimental
        """
        result = self._values.get("source_version")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.SourceProps",
    jsii_struct_bases=[],
    name_mapping={"identifier": "identifier"},
)
class SourceProps:
    def __init__(self, *, identifier: typing.Optional[builtins.str] = None) -> None:
        """Properties common to all Source classes.

        :param identifier: The source identifier. This property is required on secondary sources.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if identifier is not None:
            self._values["identifier"] = identifier

    @builtins.property
    def identifier(self) -> typing.Optional[builtins.str]:
        """The source identifier.

        This property is required on secondary sources.

        stability
        :stability: experimental
        """
        result = self._values.get("identifier")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StateChangeEvent(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.StateChangeEvent",
):
    """Event fields for the CodeBuild "state change" event.

    see
    :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html#sample-build-notifications-ref
    stability
    :stability: experimental
    """

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="buildId")
    def build_id(cls) -> builtins.str:
        """Return the build id.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "buildId")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="buildStatus")
    def build_status(cls) -> builtins.str:
        """The triggering build's status.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "buildStatus")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="currentPhase")
    def current_phase(cls) -> builtins.str:
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "currentPhase")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="projectName")
    def project_name(cls) -> builtins.str:
        """The triggering build's project name.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "projectName")


@jsii.implements(IBuildImage)
class WindowsBuildImage(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.WindowsBuildImage",
):
    """A CodeBuild image running Windows.

    This class has a bunch of public constants that represent the most popular images.

    You can also specify a custom image using one of the static methods:

    - WindowsBuildImage.fromDockerRegistry(image[, { secretsManagerCredentials }, imageType])
    - WindowsBuildImage.fromEcrRepository(repo[, tag, imageType])
    - WindowsBuildImage.fromAsset(parent, id, props, [, imageType])

    see
    :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(
        cls,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        props: _DockerImageAssetProps_74635209,
        image_type: typing.Optional["WindowsImageType"] = None,
    ) -> "IBuildImage":
        """Uses an Docker image asset as a Windows build image.

        :param scope: -
        :param id: -
        :param props: -
        :param image_type: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromAsset", [scope, id, props, image_type])

    @jsii.member(jsii_name="fromDockerRegistry")
    @builtins.classmethod
    def from_docker_registry(
        cls,
        name: builtins.str,
        options: typing.Optional["DockerImageOptions"] = None,
        image_type: typing.Optional["WindowsImageType"] = None,
    ) -> "IBuildImage":
        """
        :param name: -
        :param options: -
        :param image_type: -

        return
        :return: a Windows build image from a Docker Hub image.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromDockerRegistry", [name, options, image_type])

    @jsii.member(jsii_name="fromEcrRepository")
    @builtins.classmethod
    def from_ecr_repository(
        cls,
        repository: _IRepository_aa6e452c,
        tag: typing.Optional[builtins.str] = None,
        image_type: typing.Optional["WindowsImageType"] = None,
    ) -> "IBuildImage":
        """
        :param repository: The ECR repository.
        :param tag: Image tag (default "latest").
        :param image_type: -

        return
        :return:

        A Linux build image from an ECR repository.

        NOTE: if the repository is external (i.e. imported), then we won't be able to add
        a resource policy statement for it so CodeBuild can pull the image.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-ecr.html
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromEcrRepository", [repository, tag, image_type])

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: builtins.str) -> "BuildSpec":
        """Make a buildspec to run the indicated script.

        :param entrypoint: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "runScriptBuildspec", [entrypoint])

    @jsii.member(jsii_name="validate")
    def validate(
        self,
        *,
        build_image: typing.Optional["IBuildImage"] = None,
        compute_type: typing.Optional["ComputeType"] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, "BuildEnvironmentVariable"]] = None,
        privileged: typing.Optional[builtins.bool] = None,
    ) -> typing.List[builtins.str]:
        """Allows the image a chance to validate whether the passed configuration is correct.

        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false

        stability
        :stability: experimental
        """
        build_environment = BuildEnvironment(
            build_image=build_image,
            compute_type=compute_type,
            environment_variables=environment_variables,
            privileged=privileged,
        )

        return jsii.invoke(self, "validate", [build_environment])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="WIN_SERVER_CORE_2016_BASE")
    def WIN_SERVER_CORE_2016_BASE(cls) -> "IBuildImage":
        """Corresponds to the standard CodeBuild image ``aws/codebuild/windows-base:1.0``.

        deprecated
        :deprecated: ``WindowsBuildImage.WINDOWS_BASE_2_0`` should be used instead.

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "WIN_SERVER_CORE_2016_BASE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="WIN_SERVER_CORE_2019_BASE")
    def WIN_SERVER_CORE_2019_BASE(cls) -> "IBuildImage":
        """The standard CodeBuild image ``aws/codebuild/windows-base:2019-1.0``, which is based off Windows Server Core 2019.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "WIN_SERVER_CORE_2019_BASE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="WINDOWS_BASE_2_0")
    def WINDOWS_BASE_2_0(cls) -> "IBuildImage":
        """The standard CodeBuild image ``aws/codebuild/windows-base:2.0``, which is based off Windows Server Core 2016.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "WINDOWS_BASE_2_0")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        """The default {@link ComputeType} to use with this image, if one was not specified in {@link BuildEnvironment#computeType} explicitly.

        stability
        :stability: experimental
        """
        return jsii.get(self, "defaultComputeType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        """The Docker image identifier that the build environment uses.

        stability
        :stability: experimental
        """
        return jsii.get(self, "imageId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """The type of build environment.

        stability
        :stability: experimental
        """
        return jsii.get(self, "type")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imagePullPrincipalType")
    def image_pull_principal_type(self) -> typing.Optional["ImagePullPrincipalType"]:
        """The type of principal that CodeBuild will use to pull this build Docker image.

        stability
        :stability: experimental
        """
        return jsii.get(self, "imagePullPrincipalType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[_IRepository_aa6e452c]:
        """An optional ECR repository that the image is hosted in.

        stability
        :stability: experimental
        """
        return jsii.get(self, "repository")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretsManagerCredentials")
    def secrets_manager_credentials(self) -> typing.Optional[_ISecret_75279d36]:
        """The secretsManagerCredentials for access to a private registry.

        stability
        :stability: experimental
        """
        return jsii.get(self, "secretsManagerCredentials")


@jsii.enum(jsii_type="monocdk-experiment.aws_codebuild.WindowsImageType")
class WindowsImageType(enum.Enum):
    """Environment type for Windows Docker images.

    stability
    :stability: experimental
    """

    STANDARD = "STANDARD"
    """The standard environment type, WINDOWS_CONTAINER.

    stability
    :stability: experimental
    """
    SERVER_2019 = "SERVER_2019"
    """The WINDOWS_SERVER_2019_CONTAINER environment type.

    stability
    :stability: experimental
    """


@jsii.implements(IArtifacts)
class Artifacts(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk-experiment.aws_codebuild.Artifacts",
):
    """Artifacts definition for a CodeBuild Project.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ArtifactsProxy

    def __init__(self, *, identifier: typing.Optional[builtins.str] = None) -> None:
        """
        :param identifier: The artifact identifier. This property is required on secondary artifacts.

        stability
        :stability: experimental
        """
        props = ArtifactsProps(identifier=identifier)

        jsii.create(Artifacts, self, [props])

    @jsii.member(jsii_name="s3")
    @builtins.classmethod
    def s3(
        cls,
        *,
        bucket: _IBucket_25bad983,
        encryption: typing.Optional[builtins.bool] = None,
        include_build_id: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        package_zip: typing.Optional[builtins.bool] = None,
        path: typing.Optional[builtins.str] = None,
        identifier: typing.Optional[builtins.str] = None,
    ) -> "IArtifacts":
        """
        :param bucket: The name of the output bucket.
        :param encryption: If this is false, build output will not be encrypted. This is useful if the artifact to publish a static website or sharing content with others Default: true - output will be encrypted
        :param include_build_id: Indicates if the build ID should be included in the path. If this is set to true, then the build artifact will be stored in "//". Default: true
        :param name: The name of the build output ZIP file or folder inside the bucket. The full S3 object key will be "//" or "/" depending on whether ``includeBuildId`` is set to true. If not set, ``overrideArtifactName`` will be set and the name from the buildspec will be used instead. Default: undefined, and use the name from the buildspec
        :param package_zip: If this is true, all build output will be packaged into a single .zip file. Otherwise, all files will be uploaded to /. Default: true - files will be archived
        :param path: The path inside of the bucket for the build output .zip file or folder. If a value is not specified, then build output will be stored at the root of the bucket (or under the directory if ``includeBuildId`` is set to true). Default: the root of the bucket
        :param identifier: The artifact identifier. This property is required on secondary artifacts.

        stability
        :stability: experimental
        """
        props = S3ArtifactsProps(
            bucket=bucket,
            encryption=encryption,
            include_build_id=include_build_id,
            name=name,
            package_zip=package_zip,
            path=path,
            identifier=identifier,
        )

        return jsii.sinvoke(cls, "s3", [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _Construct_f50a3f53,
        _project: "IProject",
    ) -> "ArtifactsConfig":
        """Callback when an Artifacts class is used in a CodeBuild Project.

        :param _scope: -
        :param _project: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _project])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    @abc.abstractmethod
    def type(self) -> builtins.str:
        """The CodeBuild type of this artifact.

        stability
        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[builtins.str]:
        """The artifact identifier.

        This property is required on secondary artifacts.

        stability
        :stability: experimental
        """
        return jsii.get(self, "identifier")


class _ArtifactsProxy(Artifacts):
    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """The CodeBuild type of this artifact.

        stability
        :stability: experimental
        """
        return jsii.get(self, "type")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.BitBucketSourceProps",
    jsii_struct_bases=[SourceProps],
    name_mapping={
        "identifier": "identifier",
        "owner": "owner",
        "repo": "repo",
        "branch_or_ref": "branchOrRef",
        "clone_depth": "cloneDepth",
        "fetch_submodules": "fetchSubmodules",
        "report_build_status": "reportBuildStatus",
        "webhook": "webhook",
        "webhook_filters": "webhookFilters",
    },
)
class BitBucketSourceProps(SourceProps):
    def __init__(
        self,
        *,
        identifier: typing.Optional[builtins.str] = None,
        owner: builtins.str,
        repo: builtins.str,
        branch_or_ref: typing.Optional[builtins.str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
        fetch_submodules: typing.Optional[builtins.bool] = None,
        report_build_status: typing.Optional[builtins.bool] = None,
        webhook: typing.Optional[builtins.bool] = None,
        webhook_filters: typing.Optional[typing.List["FilterGroup"]] = None,
    ) -> None:
        """Construction properties for {@link BitBucketSource}.

        :param identifier: The source identifier. This property is required on secondary sources.
        :param owner: The BitBucket account/user that owns the repo.
        :param repo: The name of the repo (without the username).
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param fetch_submodules: Whether to fetch submodules while cloning git repo. Default: false
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "owner": owner,
            "repo": repo,
        }
        if identifier is not None:
            self._values["identifier"] = identifier
        if branch_or_ref is not None:
            self._values["branch_or_ref"] = branch_or_ref
        if clone_depth is not None:
            self._values["clone_depth"] = clone_depth
        if fetch_submodules is not None:
            self._values["fetch_submodules"] = fetch_submodules
        if report_build_status is not None:
            self._values["report_build_status"] = report_build_status
        if webhook is not None:
            self._values["webhook"] = webhook
        if webhook_filters is not None:
            self._values["webhook_filters"] = webhook_filters

    @builtins.property
    def identifier(self) -> typing.Optional[builtins.str]:
        """The source identifier.

        This property is required on secondary sources.

        stability
        :stability: experimental
        """
        result = self._values.get("identifier")
        return result

    @builtins.property
    def owner(self) -> builtins.str:
        """The BitBucket account/user that owns the repo.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "awslabs"
        """
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return result

    @builtins.property
    def repo(self) -> builtins.str:
        """The name of the repo (without the username).

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "aws-cdk"
        """
        result = self._values.get("repo")
        assert result is not None, "Required property 'repo' is missing"
        return result

    @builtins.property
    def branch_or_ref(self) -> typing.Optional[builtins.str]:
        """The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build.

        default
        :default: the default branch's HEAD commit ID is used

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "mybranch"
        """
        result = self._values.get("branch_or_ref")
        return result

    @builtins.property
    def clone_depth(self) -> typing.Optional[jsii.Number]:
        """The depth of history to download.

        Minimum value is 0.
        If this value is 0, greater than 25, or not provided,
        then the full history is downloaded with each build of the project.

        stability
        :stability: experimental
        """
        result = self._values.get("clone_depth")
        return result

    @builtins.property
    def fetch_submodules(self) -> typing.Optional[builtins.bool]:
        """Whether to fetch submodules while cloning git repo.

        default
        :default: false

        stability
        :stability: experimental
        """
        result = self._values.get("fetch_submodules")
        return result

    @builtins.property
    def report_build_status(self) -> typing.Optional[builtins.bool]:
        """Whether to send notifications on your build's start and end.

        default
        :default: true

        stability
        :stability: experimental
        """
        result = self._values.get("report_build_status")
        return result

    @builtins.property
    def webhook(self) -> typing.Optional[builtins.bool]:
        """Whether to create a webhook that will trigger a build every time an event happens in the repository.

        default
        :default: true if any ``webhookFilters`` were provided, false otherwise

        stability
        :stability: experimental
        """
        result = self._values.get("webhook")
        return result

    @builtins.property
    def webhook_filters(self) -> typing.Optional[typing.List["FilterGroup"]]:
        """A list of webhook filters that can constraint what events in the repository will trigger a build.

        A build is triggered if any of the provided filter groups match.
        Only valid if ``webhook`` was not provided as false.

        default
        :default: every push and every Pull Request (create or update) triggers a build

        stability
        :stability: experimental
        """
        result = self._values.get("webhook_filters")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BitBucketSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.CodeCommitSourceProps",
    jsii_struct_bases=[SourceProps],
    name_mapping={
        "identifier": "identifier",
        "repository": "repository",
        "branch_or_ref": "branchOrRef",
        "clone_depth": "cloneDepth",
        "fetch_submodules": "fetchSubmodules",
    },
)
class CodeCommitSourceProps(SourceProps):
    def __init__(
        self,
        *,
        identifier: typing.Optional[builtins.str] = None,
        repository: _IRepository_91f381de,
        branch_or_ref: typing.Optional[builtins.str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
        fetch_submodules: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Construction properties for {@link CodeCommitSource}.

        :param identifier: The source identifier. This property is required on secondary sources.
        :param repository: 
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param fetch_submodules: Whether to fetch submodules while cloning git repo. Default: false

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "repository": repository,
        }
        if identifier is not None:
            self._values["identifier"] = identifier
        if branch_or_ref is not None:
            self._values["branch_or_ref"] = branch_or_ref
        if clone_depth is not None:
            self._values["clone_depth"] = clone_depth
        if fetch_submodules is not None:
            self._values["fetch_submodules"] = fetch_submodules

    @builtins.property
    def identifier(self) -> typing.Optional[builtins.str]:
        """The source identifier.

        This property is required on secondary sources.

        stability
        :stability: experimental
        """
        result = self._values.get("identifier")
        return result

    @builtins.property
    def repository(self) -> _IRepository_91f381de:
        """
        stability
        :stability: experimental
        """
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return result

    @builtins.property
    def branch_or_ref(self) -> typing.Optional[builtins.str]:
        """The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build.

        default
        :default: the default branch's HEAD commit ID is used

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "mybranch"
        """
        result = self._values.get("branch_or_ref")
        return result

    @builtins.property
    def clone_depth(self) -> typing.Optional[jsii.Number]:
        """The depth of history to download.

        Minimum value is 0.
        If this value is 0, greater than 25, or not provided,
        then the full history is downloaded with each build of the project.

        stability
        :stability: experimental
        """
        result = self._values.get("clone_depth")
        return result

    @builtins.property
    def fetch_submodules(self) -> typing.Optional[builtins.bool]:
        """Whether to fetch submodules while cloning git repo.

        default
        :default: false

        stability
        :stability: experimental
        """
        result = self._values.get("fetch_submodules")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeCommitSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.GitHubEnterpriseSourceProps",
    jsii_struct_bases=[SourceProps],
    name_mapping={
        "identifier": "identifier",
        "https_clone_url": "httpsCloneUrl",
        "branch_or_ref": "branchOrRef",
        "clone_depth": "cloneDepth",
        "fetch_submodules": "fetchSubmodules",
        "ignore_ssl_errors": "ignoreSslErrors",
        "report_build_status": "reportBuildStatus",
        "webhook": "webhook",
        "webhook_filters": "webhookFilters",
    },
)
class GitHubEnterpriseSourceProps(SourceProps):
    def __init__(
        self,
        *,
        identifier: typing.Optional[builtins.str] = None,
        https_clone_url: builtins.str,
        branch_or_ref: typing.Optional[builtins.str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
        fetch_submodules: typing.Optional[builtins.bool] = None,
        ignore_ssl_errors: typing.Optional[builtins.bool] = None,
        report_build_status: typing.Optional[builtins.bool] = None,
        webhook: typing.Optional[builtins.bool] = None,
        webhook_filters: typing.Optional[typing.List["FilterGroup"]] = None,
    ) -> None:
        """Construction properties for {@link GitHubEnterpriseSource}.

        :param identifier: The source identifier. This property is required on secondary sources.
        :param https_clone_url: The HTTPS URL of the repository in your GitHub Enterprise installation.
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param fetch_submodules: Whether to fetch submodules while cloning git repo. Default: false
        :param ignore_ssl_errors: Whether to ignore SSL errors when connecting to the repository. Default: false
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "https_clone_url": https_clone_url,
        }
        if identifier is not None:
            self._values["identifier"] = identifier
        if branch_or_ref is not None:
            self._values["branch_or_ref"] = branch_or_ref
        if clone_depth is not None:
            self._values["clone_depth"] = clone_depth
        if fetch_submodules is not None:
            self._values["fetch_submodules"] = fetch_submodules
        if ignore_ssl_errors is not None:
            self._values["ignore_ssl_errors"] = ignore_ssl_errors
        if report_build_status is not None:
            self._values["report_build_status"] = report_build_status
        if webhook is not None:
            self._values["webhook"] = webhook
        if webhook_filters is not None:
            self._values["webhook_filters"] = webhook_filters

    @builtins.property
    def identifier(self) -> typing.Optional[builtins.str]:
        """The source identifier.

        This property is required on secondary sources.

        stability
        :stability: experimental
        """
        result = self._values.get("identifier")
        return result

    @builtins.property
    def https_clone_url(self) -> builtins.str:
        """The HTTPS URL of the repository in your GitHub Enterprise installation.

        stability
        :stability: experimental
        """
        result = self._values.get("https_clone_url")
        assert result is not None, "Required property 'https_clone_url' is missing"
        return result

    @builtins.property
    def branch_or_ref(self) -> typing.Optional[builtins.str]:
        """The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build.

        default
        :default: the default branch's HEAD commit ID is used

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "mybranch"
        """
        result = self._values.get("branch_or_ref")
        return result

    @builtins.property
    def clone_depth(self) -> typing.Optional[jsii.Number]:
        """The depth of history to download.

        Minimum value is 0.
        If this value is 0, greater than 25, or not provided,
        then the full history is downloaded with each build of the project.

        stability
        :stability: experimental
        """
        result = self._values.get("clone_depth")
        return result

    @builtins.property
    def fetch_submodules(self) -> typing.Optional[builtins.bool]:
        """Whether to fetch submodules while cloning git repo.

        default
        :default: false

        stability
        :stability: experimental
        """
        result = self._values.get("fetch_submodules")
        return result

    @builtins.property
    def ignore_ssl_errors(self) -> typing.Optional[builtins.bool]:
        """Whether to ignore SSL errors when connecting to the repository.

        default
        :default: false

        stability
        :stability: experimental
        """
        result = self._values.get("ignore_ssl_errors")
        return result

    @builtins.property
    def report_build_status(self) -> typing.Optional[builtins.bool]:
        """Whether to send notifications on your build's start and end.

        default
        :default: true

        stability
        :stability: experimental
        """
        result = self._values.get("report_build_status")
        return result

    @builtins.property
    def webhook(self) -> typing.Optional[builtins.bool]:
        """Whether to create a webhook that will trigger a build every time an event happens in the repository.

        default
        :default: true if any ``webhookFilters`` were provided, false otherwise

        stability
        :stability: experimental
        """
        result = self._values.get("webhook")
        return result

    @builtins.property
    def webhook_filters(self) -> typing.Optional[typing.List["FilterGroup"]]:
        """A list of webhook filters that can constraint what events in the repository will trigger a build.

        A build is triggered if any of the provided filter groups match.
        Only valid if ``webhook`` was not provided as false.

        default
        :default: every push and every Pull Request (create or update) triggers a build

        stability
        :stability: experimental
        """
        result = self._values.get("webhook_filters")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubEnterpriseSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.GitHubSourceProps",
    jsii_struct_bases=[SourceProps],
    name_mapping={
        "identifier": "identifier",
        "owner": "owner",
        "repo": "repo",
        "branch_or_ref": "branchOrRef",
        "clone_depth": "cloneDepth",
        "fetch_submodules": "fetchSubmodules",
        "report_build_status": "reportBuildStatus",
        "webhook": "webhook",
        "webhook_filters": "webhookFilters",
    },
)
class GitHubSourceProps(SourceProps):
    def __init__(
        self,
        *,
        identifier: typing.Optional[builtins.str] = None,
        owner: builtins.str,
        repo: builtins.str,
        branch_or_ref: typing.Optional[builtins.str] = None,
        clone_depth: typing.Optional[jsii.Number] = None,
        fetch_submodules: typing.Optional[builtins.bool] = None,
        report_build_status: typing.Optional[builtins.bool] = None,
        webhook: typing.Optional[builtins.bool] = None,
        webhook_filters: typing.Optional[typing.List["FilterGroup"]] = None,
    ) -> None:
        """Construction properties for {@link GitHubSource} and {@link GitHubEnterpriseSource}.

        :param identifier: The source identifier. This property is required on secondary sources.
        :param owner: The GitHub account/user that owns the repo.
        :param repo: The name of the repo (without the username).
        :param branch_or_ref: The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. Default: the default branch's HEAD commit ID is used
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param fetch_submodules: Whether to fetch submodules while cloning git repo. Default: false
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "owner": owner,
            "repo": repo,
        }
        if identifier is not None:
            self._values["identifier"] = identifier
        if branch_or_ref is not None:
            self._values["branch_or_ref"] = branch_or_ref
        if clone_depth is not None:
            self._values["clone_depth"] = clone_depth
        if fetch_submodules is not None:
            self._values["fetch_submodules"] = fetch_submodules
        if report_build_status is not None:
            self._values["report_build_status"] = report_build_status
        if webhook is not None:
            self._values["webhook"] = webhook
        if webhook_filters is not None:
            self._values["webhook_filters"] = webhook_filters

    @builtins.property
    def identifier(self) -> typing.Optional[builtins.str]:
        """The source identifier.

        This property is required on secondary sources.

        stability
        :stability: experimental
        """
        result = self._values.get("identifier")
        return result

    @builtins.property
    def owner(self) -> builtins.str:
        """The GitHub account/user that owns the repo.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "awslabs"
        """
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return result

    @builtins.property
    def repo(self) -> builtins.str:
        """The name of the repo (without the username).

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "aws-cdk"
        """
        result = self._values.get("repo")
        assert result is not None, "Required property 'repo' is missing"
        return result

    @builtins.property
    def branch_or_ref(self) -> typing.Optional[builtins.str]:
        """The commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build.

        default
        :default: the default branch's HEAD commit ID is used

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "mybranch"
        """
        result = self._values.get("branch_or_ref")
        return result

    @builtins.property
    def clone_depth(self) -> typing.Optional[jsii.Number]:
        """The depth of history to download.

        Minimum value is 0.
        If this value is 0, greater than 25, or not provided,
        then the full history is downloaded with each build of the project.

        stability
        :stability: experimental
        """
        result = self._values.get("clone_depth")
        return result

    @builtins.property
    def fetch_submodules(self) -> typing.Optional[builtins.bool]:
        """Whether to fetch submodules while cloning git repo.

        default
        :default: false

        stability
        :stability: experimental
        """
        result = self._values.get("fetch_submodules")
        return result

    @builtins.property
    def report_build_status(self) -> typing.Optional[builtins.bool]:
        """Whether to send notifications on your build's start and end.

        default
        :default: true

        stability
        :stability: experimental
        """
        result = self._values.get("report_build_status")
        return result

    @builtins.property
    def webhook(self) -> typing.Optional[builtins.bool]:
        """Whether to create a webhook that will trigger a build every time an event happens in the repository.

        default
        :default: true if any ``webhookFilters`` were provided, false otherwise

        stability
        :stability: experimental
        """
        result = self._values.get("webhook")
        return result

    @builtins.property
    def webhook_filters(self) -> typing.Optional[typing.List["FilterGroup"]]:
        """A list of webhook filters that can constraint what events in the repository will trigger a build.

        A build is triggered if any of the provided filter groups match.
        Only valid if ``webhook`` was not provided as false.

        default
        :default: every push and every Pull Request (create or update) triggers a build

        stability
        :stability: experimental
        """
        result = self._values.get("webhook_filters")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk-experiment.aws_codebuild.IBindableBuildImage")
class IBindableBuildImage(IBuildImage, typing_extensions.Protocol):
    """A variant of {@link IBuildImage} that allows binding to the project.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IBindableBuildImageProxy

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_f50a3f53,
        project: "IProject",
    ) -> "BuildImageConfig":
        """Function that allows the build image access to the construct tree.

        :param scope: -
        :param project: -

        stability
        :stability: experimental
        """
        ...


class _IBindableBuildImageProxy(
    jsii.proxy_for(IBuildImage) # type: ignore
):
    """A variant of {@link IBuildImage} that allows binding to the project.

    stability
    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk-experiment.aws_codebuild.IBindableBuildImage"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_f50a3f53,
        project: "IProject",
    ) -> "BuildImageConfig":
        """Function that allows the build image access to the construct tree.

        :param scope: -
        :param project: -

        stability
        :stability: experimental
        """
        options = BuildImageBindOptions()

        return jsii.invoke(self, "bind", [scope, project, options])


@jsii.implements(IBindableBuildImage)
class LinuxGpuBuildImage(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.LinuxGpuBuildImage",
):
    """A CodeBuild GPU image running Linux.

    This class has public constants that represent the most popular GPU images from AWS Deep Learning Containers.

    see
    :see: https://aws.amazon.com/releasenotes/available-deep-learning-containers-images
    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="awsDeepLearningContainersImage")
    @builtins.classmethod
    def aws_deep_learning_containers_image(
        cls,
        repository_name: builtins.str,
        tag: builtins.str,
        account: typing.Optional[builtins.str] = None,
    ) -> "IBuildImage":
        """Returns a Linux GPU build image from AWS Deep Learning Containers.

        :param repository_name: the name of the repository, for example "pytorch-inference".
        :param tag: the tag of the image, for example "1.5.0-gpu-py36-cu101-ubuntu16.04".
        :param account: the AWS account ID where the DLC repository for this region is hosted in. In many cases, the CDK can infer that for you, but for some newer region our information might be out of date; in that case, you can specify the region explicitly using this optional parameter

        see
        :see: https://aws.amazon.com/releasenotes/available-deep-learning-containers-images
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "awsDeepLearningContainersImage", [repository_name, tag, account])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_f50a3f53,
        project: "IProject",
    ) -> "BuildImageConfig":
        """Function that allows the build image access to the construct tree.

        :param scope: -
        :param project: -

        stability
        :stability: experimental
        """
        _options = BuildImageBindOptions()

        return jsii.invoke(self, "bind", [scope, project, _options])

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: builtins.str) -> "BuildSpec":
        """Make a buildspec to run the indicated script.

        :param entrypoint: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "runScriptBuildspec", [entrypoint])

    @jsii.member(jsii_name="validate")
    def validate(
        self,
        *,
        build_image: typing.Optional["IBuildImage"] = None,
        compute_type: typing.Optional["ComputeType"] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, "BuildEnvironmentVariable"]] = None,
        privileged: typing.Optional[builtins.bool] = None,
    ) -> typing.List[builtins.str]:
        """Allows the image a chance to validate whether the passed configuration is correct.

        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false

        stability
        :stability: experimental
        """
        build_environment = BuildEnvironment(
            build_image=build_image,
            compute_type=compute_type,
            environment_variables=environment_variables,
            privileged=privileged,
        )

        return jsii.invoke(self, "validate", [build_environment])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_MXNET_1_4_1")
    def DLC_MXNET_1_4_1(cls) -> "IBuildImage":
        """MXNet 1.4.1 GPU image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_MXNET_1_4_1")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_MXNET_1_6_0")
    def DLC_MXNET_1_6_0(cls) -> "IBuildImage":
        """MXNet 1.6.0 GPU image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_MXNET_1_6_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_PYTORCH_1_2_0")
    def DLC_PYTORCH_1_2_0(cls) -> "IBuildImage":
        """PyTorch 1.2.0 GPU image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_PYTORCH_1_2_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_PYTORCH_1_3_1")
    def DLC_PYTORCH_1_3_1(cls) -> "IBuildImage":
        """PyTorch 1.3.1 GPU image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_PYTORCH_1_3_1")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_PYTORCH_1_4_0_INFERENCE")
    def DLC_PYTORCH_1_4_0_INFERENCE(cls) -> "IBuildImage":
        """PyTorch 1.4.0 GPU inference image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_PYTORCH_1_4_0_INFERENCE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_PYTORCH_1_4_0_TRAINING")
    def DLC_PYTORCH_1_4_0_TRAINING(cls) -> "IBuildImage":
        """PyTorch 1.4.0 GPU training image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_PYTORCH_1_4_0_TRAINING")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_PYTORCH_1_5_0_INFERENCE")
    def DLC_PYTORCH_1_5_0_INFERENCE(cls) -> "IBuildImage":
        """PyTorch 1.5.0 GPU inference image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_PYTORCH_1_5_0_INFERENCE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_PYTORCH_1_5_0_TRAINING")
    def DLC_PYTORCH_1_5_0_TRAINING(cls) -> "IBuildImage":
        """PyTorch 1.5.0 GPU training image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_PYTORCH_1_5_0_TRAINING")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_TENSORFLOW_1_14_0")
    def DLC_TENSORFLOW_1_14_0(cls) -> "IBuildImage":
        """Tensorflow 1.14.0 GPU image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_TENSORFLOW_1_14_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_TENSORFLOW_1_15_0")
    def DLC_TENSORFLOW_1_15_0(cls) -> "IBuildImage":
        """Tensorflow 1.15.0 GPU image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_TENSORFLOW_1_15_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_TENSORFLOW_1_15_2_INFERENCE")
    def DLC_TENSORFLOW_1_15_2_INFERENCE(cls) -> "IBuildImage":
        """Tensorflow 1.15.2 GPU inference image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_TENSORFLOW_1_15_2_INFERENCE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_TENSORFLOW_1_15_2_TRAINING")
    def DLC_TENSORFLOW_1_15_2_TRAINING(cls) -> "IBuildImage":
        """Tensorflow 1.15.2 GPU training image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_TENSORFLOW_1_15_2_TRAINING")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_TENSORFLOW_2_0_0")
    def DLC_TENSORFLOW_2_0_0(cls) -> "IBuildImage":
        """Tensorflow 2.0.0 GPU image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_TENSORFLOW_2_0_0")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_TENSORFLOW_2_0_1")
    def DLC_TENSORFLOW_2_0_1(cls) -> "IBuildImage":
        """Tensorflow 2.0.1 GPU image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_TENSORFLOW_2_0_1")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_TENSORFLOW_2_1_0_INFERENCE")
    def DLC_TENSORFLOW_2_1_0_INFERENCE(cls) -> "IBuildImage":
        """Tensorflow 2.1.0 GPU inference image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_TENSORFLOW_2_1_0_INFERENCE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_TENSORFLOW_2_1_0_TRAINING")
    def DLC_TENSORFLOW_2_1_0_TRAINING(cls) -> "IBuildImage":
        """Tensorflow 2.1.0 GPU training image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_TENSORFLOW_2_1_0_TRAINING")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="DLC_TENSORFLOW_2_2_0_TRAINING")
    def DLC_TENSORFLOW_2_2_0_TRAINING(cls) -> "IBuildImage":
        """Tensorflow 2.2.0 GPU training image from AWS Deep Learning Containers.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DLC_TENSORFLOW_2_2_0_TRAINING")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        """The default {@link ComputeType} to use with this image, if one was not specified in {@link BuildEnvironment#computeType} explicitly.

        stability
        :stability: experimental
        """
        return jsii.get(self, "defaultComputeType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        """The Docker image identifier that the build environment uses.

        stability
        :stability: experimental
        """
        return jsii.get(self, "imageId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """The type of build environment.

        stability
        :stability: experimental
        """
        return jsii.get(self, "type")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imagePullPrincipalType")
    def image_pull_principal_type(self) -> typing.Optional["ImagePullPrincipalType"]:
        """The type of principal that CodeBuild will use to pull this build Docker image.

        stability
        :stability: experimental
        """
        return jsii.get(self, "imagePullPrincipalType")


class PipelineProject(
    Project,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codebuild.PipelineProject",
):
    """A convenience class for CodeBuild Projects that are used in CodePipeline.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        badge: typing.Optional[builtins.bool] = None,
        build_spec: typing.Optional["BuildSpec"] = None,
        cache: typing.Optional["Cache"] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_IKey_3336c79d] = None,
        environment: typing.Optional["BuildEnvironment"] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, "BuildEnvironmentVariable"]] = None,
        file_system_locations: typing.Optional[typing.List["IFileSystemLocation"]] = None,
        grant_report_group_permissions: typing.Optional[builtins.bool] = None,
        project_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        subnet_selection: typing.Optional[_SubnetSelection_36a13cd6] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param file_system_locations: An ProjectFileSystemLocation objects for a CodeBuild build project. A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint, and type of a file system created using Amazon Elastic File System. Default: - no file system locations
        :param grant_report_group_permissions: Add permissions to this project's role to create and use test report groups with name starting with the name of this project. That is the standard report group that gets created when a simple name (in contrast to an ARN) is used in the 'reports' section of the buildspec of this project. This is usually harmless, but you can turn these off if you don't plan on using test reports in this project. Default: true
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.

        stability
        :stability: experimental
        """
        props = PipelineProjectProps(
            allow_all_outbound=allow_all_outbound,
            badge=badge,
            build_spec=build_spec,
            cache=cache,
            description=description,
            encryption_key=encryption_key,
            environment=environment,
            environment_variables=environment_variables,
            file_system_locations=file_system_locations,
            grant_report_group_permissions=grant_report_group_permissions,
            project_name=project_name,
            role=role,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
        )

        jsii.create(PipelineProject, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codebuild.S3SourceProps",
    jsii_struct_bases=[SourceProps],
    name_mapping={
        "identifier": "identifier",
        "bucket": "bucket",
        "path": "path",
        "version": "version",
    },
)
class S3SourceProps(SourceProps):
    def __init__(
        self,
        *,
        identifier: typing.Optional[builtins.str] = None,
        bucket: _IBucket_25bad983,
        path: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        """Construction properties for {@link S3Source}.

        :param identifier: The source identifier. This property is required on secondary sources.
        :param bucket: 
        :param path: 
        :param version: The version ID of the object that represents the build input ZIP file to use. Default: latest

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "path": path,
        }
        if identifier is not None:
            self._values["identifier"] = identifier
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def identifier(self) -> typing.Optional[builtins.str]:
        """The source identifier.

        This property is required on secondary sources.

        stability
        :stability: experimental
        """
        result = self._values.get("identifier")
        return result

    @builtins.property
    def bucket(self) -> _IBucket_25bad983:
        """
        stability
        :stability: experimental
        """
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return result

    @builtins.property
    def path(self) -> builtins.str:
        """
        stability
        :stability: experimental
        """
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return result

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        """The version ID of the object that represents the build input ZIP file to use.

        default
        :default: latest

        stability
        :stability: experimental
        """
        result = self._values.get("version")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3SourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Artifacts",
    "ArtifactsConfig",
    "ArtifactsProps",
    "BindToCodePipelineOptions",
    "BitBucketSourceCredentials",
    "BitBucketSourceCredentialsProps",
    "BitBucketSourceProps",
    "BucketCacheOptions",
    "BuildEnvironment",
    "BuildEnvironmentVariable",
    "BuildEnvironmentVariableType",
    "BuildImageBindOptions",
    "BuildImageConfig",
    "BuildSpec",
    "Cache",
    "CfnProject",
    "CfnProjectProps",
    "CfnReportGroup",
    "CfnReportGroupProps",
    "CfnSourceCredential",
    "CfnSourceCredentialProps",
    "CodeCommitSourceProps",
    "CommonProjectProps",
    "ComputeType",
    "DockerImageOptions",
    "EfsFileSystemLocationProps",
    "EventAction",
    "FileSystemConfig",
    "FileSystemLocation",
    "FilterGroup",
    "GitHubEnterpriseSourceCredentials",
    "GitHubEnterpriseSourceCredentialsProps",
    "GitHubEnterpriseSourceProps",
    "GitHubSourceCredentials",
    "GitHubSourceCredentialsProps",
    "GitHubSourceProps",
    "IArtifacts",
    "IBindableBuildImage",
    "IBuildImage",
    "IFileSystemLocation",
    "IProject",
    "IReportGroup",
    "ISource",
    "ImagePullPrincipalType",
    "LinuxBuildImage",
    "LinuxGpuBuildImage",
    "LocalCacheMode",
    "PhaseChangeEvent",
    "PipelineProject",
    "PipelineProjectProps",
    "Project",
    "ProjectProps",
    "ReportGroup",
    "ReportGroupProps",
    "S3ArtifactsProps",
    "S3SourceProps",
    "Source",
    "SourceConfig",
    "SourceProps",
    "StateChangeEvent",
    "WindowsBuildImage",
    "WindowsImageType",
]

publication.publish()
