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
    Construct as _Construct_f50a3f53,
    IInspectable as _IInspectable_051e6ed8,
    IResolvable as _IResolvable_9ceae33e,
    TagManager as _TagManager_2508893f,
    TreeInspector as _TreeInspector_154f5999,
)


@jsii.implements(_IInspectable_051e6ed8)
class CfnChannel(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_medialive.CfnChannel",
):
    """A CloudFormation ``AWS::MediaLive::Channel``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html
    cloudformationResource:
    :cloudformationResource:: AWS::MediaLive::Channel
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        channel_class: typing.Optional[builtins.str] = None,
        destinations: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["OutputDestinationProperty", _IResolvable_9ceae33e]]]] = None,
        encoder_settings: typing.Any = None,
        input_attachments: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InputAttachmentProperty", _IResolvable_9ceae33e]]]] = None,
        input_specification: typing.Optional[typing.Union["InputSpecificationProperty", _IResolvable_9ceae33e]] = None,
        log_level: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        """Create a new ``AWS::MediaLive::Channel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param channel_class: ``AWS::MediaLive::Channel.ChannelClass``.
        :param destinations: ``AWS::MediaLive::Channel.Destinations``.
        :param encoder_settings: ``AWS::MediaLive::Channel.EncoderSettings``.
        :param input_attachments: ``AWS::MediaLive::Channel.InputAttachments``.
        :param input_specification: ``AWS::MediaLive::Channel.InputSpecification``.
        :param log_level: ``AWS::MediaLive::Channel.LogLevel``.
        :param name: ``AWS::MediaLive::Channel.Name``.
        :param role_arn: ``AWS::MediaLive::Channel.RoleArn``.
        :param tags: ``AWS::MediaLive::Channel.Tags``.
        """
        props = CfnChannelProps(
            channel_class=channel_class,
            destinations=destinations,
            encoder_settings=encoder_settings,
            input_attachments=input_attachments,
            input_specification=input_specification,
            log_level=log_level,
            name=name,
            role_arn=role_arn,
            tags=tags,
        )

        jsii.create(CfnChannel, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrInputs")
    def attr_inputs(self) -> typing.List[builtins.str]:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Inputs
        """
        return jsii.get(self, "attrInputs")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::MediaLive::Channel.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encoderSettings")
    def encoder_settings(self) -> typing.Any:
        """``AWS::MediaLive::Channel.EncoderSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-encodersettings
        """
        return jsii.get(self, "encoderSettings")

    @encoder_settings.setter # type: ignore
    def encoder_settings(self, value: typing.Any) -> None:
        jsii.set(self, "encoderSettings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="channelClass")
    def channel_class(self) -> typing.Optional[builtins.str]:
        """``AWS::MediaLive::Channel.ChannelClass``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-channelclass
        """
        return jsii.get(self, "channelClass")

    @channel_class.setter # type: ignore
    def channel_class(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "channelClass", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="destinations")
    def destinations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["OutputDestinationProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::MediaLive::Channel.Destinations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-destinations
        """
        return jsii.get(self, "destinations")

    @destinations.setter # type: ignore
    def destinations(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["OutputDestinationProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "destinations", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="inputAttachments")
    def input_attachments(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InputAttachmentProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::MediaLive::Channel.InputAttachments``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-inputattachments
        """
        return jsii.get(self, "inputAttachments")

    @input_attachments.setter # type: ignore
    def input_attachments(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InputAttachmentProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "inputAttachments", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="inputSpecification")
    def input_specification(
        self,
    ) -> typing.Optional[typing.Union["InputSpecificationProperty", _IResolvable_9ceae33e]]:
        """``AWS::MediaLive::Channel.InputSpecification``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-inputspecification
        """
        return jsii.get(self, "inputSpecification")

    @input_specification.setter # type: ignore
    def input_specification(
        self,
        value: typing.Optional[typing.Union["InputSpecificationProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "inputSpecification", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> typing.Optional[builtins.str]:
        """``AWS::MediaLive::Channel.LogLevel``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-loglevel
        """
        return jsii.get(self, "logLevel")

    @log_level.setter # type: ignore
    def log_level(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "logLevel", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::MediaLive::Channel.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::MediaLive::Channel.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter # type: ignore
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "roleArn", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.AribSourceSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class AribSourceSettingsProperty:
        def __init__(self) -> None:
            """
            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-aribsourcesettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AribSourceSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.AudioLanguageSelectionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "language_code": "languageCode",
            "language_selection_policy": "languageSelectionPolicy",
        },
    )
    class AudioLanguageSelectionProperty:
        def __init__(
            self,
            *,
            language_code: typing.Optional[builtins.str] = None,
            language_selection_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param language_code: ``CfnChannel.AudioLanguageSelectionProperty.LanguageCode``.
            :param language_selection_policy: ``CfnChannel.AudioLanguageSelectionProperty.LanguageSelectionPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-audiolanguageselection.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if language_code is not None:
                self._values["language_code"] = language_code
            if language_selection_policy is not None:
                self._values["language_selection_policy"] = language_selection_policy

        @builtins.property
        def language_code(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.AudioLanguageSelectionProperty.LanguageCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-audiolanguageselection.html#cfn-medialive-channel-audiolanguageselection-languagecode
            """
            result = self._values.get("language_code")
            return result

        @builtins.property
        def language_selection_policy(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.AudioLanguageSelectionProperty.LanguageSelectionPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-audiolanguageselection.html#cfn-medialive-channel-audiolanguageselection-languageselectionpolicy
            """
            result = self._values.get("language_selection_policy")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioLanguageSelectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.AudioPidSelectionProperty",
        jsii_struct_bases=[],
        name_mapping={"pid": "pid"},
    )
    class AudioPidSelectionProperty:
        def __init__(self, *, pid: typing.Optional[jsii.Number] = None) -> None:
            """
            :param pid: ``CfnChannel.AudioPidSelectionProperty.Pid``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-audiopidselection.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if pid is not None:
                self._values["pid"] = pid

        @builtins.property
        def pid(self) -> typing.Optional[jsii.Number]:
            """``CfnChannel.AudioPidSelectionProperty.Pid``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-audiopidselection.html#cfn-medialive-channel-audiopidselection-pid
            """
            result = self._values.get("pid")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioPidSelectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.AudioSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "selector_settings": "selectorSettings"},
    )
    class AudioSelectorProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            selector_settings: typing.Optional[typing.Union["CfnChannel.AudioSelectorSettingsProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param name: ``CfnChannel.AudioSelectorProperty.Name``.
            :param selector_settings: ``CfnChannel.AudioSelectorProperty.SelectorSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-audioselector.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if selector_settings is not None:
                self._values["selector_settings"] = selector_settings

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.AudioSelectorProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-audioselector.html#cfn-medialive-channel-audioselector-name
            """
            result = self._values.get("name")
            return result

        @builtins.property
        def selector_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.AudioSelectorSettingsProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.AudioSelectorProperty.SelectorSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-audioselector.html#cfn-medialive-channel-audioselector-selectorsettings
            """
            result = self._values.get("selector_settings")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.AudioSelectorSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "audio_language_selection": "audioLanguageSelection",
            "audio_pid_selection": "audioPidSelection",
        },
    )
    class AudioSelectorSettingsProperty:
        def __init__(
            self,
            *,
            audio_language_selection: typing.Optional[typing.Union["CfnChannel.AudioLanguageSelectionProperty", _IResolvable_9ceae33e]] = None,
            audio_pid_selection: typing.Optional[typing.Union["CfnChannel.AudioPidSelectionProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param audio_language_selection: ``CfnChannel.AudioSelectorSettingsProperty.AudioLanguageSelection``.
            :param audio_pid_selection: ``CfnChannel.AudioSelectorSettingsProperty.AudioPidSelection``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-audioselectorsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if audio_language_selection is not None:
                self._values["audio_language_selection"] = audio_language_selection
            if audio_pid_selection is not None:
                self._values["audio_pid_selection"] = audio_pid_selection

        @builtins.property
        def audio_language_selection(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.AudioLanguageSelectionProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.AudioSelectorSettingsProperty.AudioLanguageSelection``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-audioselectorsettings.html#cfn-medialive-channel-audioselectorsettings-audiolanguageselection
            """
            result = self._values.get("audio_language_selection")
            return result

        @builtins.property
        def audio_pid_selection(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.AudioPidSelectionProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.AudioSelectorSettingsProperty.AudioPidSelection``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-audioselectorsettings.html#cfn-medialive-channel-audioselectorsettings-audiopidselection
            """
            result = self._values.get("audio_pid_selection")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioSelectorSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.CaptionSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "language_code": "languageCode",
            "name": "name",
            "selector_settings": "selectorSettings",
        },
    )
    class CaptionSelectorProperty:
        def __init__(
            self,
            *,
            language_code: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            selector_settings: typing.Optional[typing.Union["CfnChannel.CaptionSelectorSettingsProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param language_code: ``CfnChannel.CaptionSelectorProperty.LanguageCode``.
            :param name: ``CfnChannel.CaptionSelectorProperty.Name``.
            :param selector_settings: ``CfnChannel.CaptionSelectorProperty.SelectorSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-captionselector.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if language_code is not None:
                self._values["language_code"] = language_code
            if name is not None:
                self._values["name"] = name
            if selector_settings is not None:
                self._values["selector_settings"] = selector_settings

        @builtins.property
        def language_code(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.CaptionSelectorProperty.LanguageCode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-captionselector.html#cfn-medialive-channel-captionselector-languagecode
            """
            result = self._values.get("language_code")
            return result

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.CaptionSelectorProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-captionselector.html#cfn-medialive-channel-captionselector-name
            """
            result = self._values.get("name")
            return result

        @builtins.property
        def selector_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.CaptionSelectorSettingsProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.CaptionSelectorProperty.SelectorSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-captionselector.html#cfn-medialive-channel-captionselector-selectorsettings
            """
            result = self._values.get("selector_settings")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CaptionSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.CaptionSelectorSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arib_source_settings": "aribSourceSettings",
            "dvb_sub_source_settings": "dvbSubSourceSettings",
            "embedded_source_settings": "embeddedSourceSettings",
            "scte20_source_settings": "scte20SourceSettings",
            "scte27_source_settings": "scte27SourceSettings",
            "teletext_source_settings": "teletextSourceSettings",
        },
    )
    class CaptionSelectorSettingsProperty:
        def __init__(
            self,
            *,
            arib_source_settings: typing.Optional[typing.Union["CfnChannel.AribSourceSettingsProperty", _IResolvable_9ceae33e]] = None,
            dvb_sub_source_settings: typing.Optional[typing.Union["CfnChannel.DvbSubSourceSettingsProperty", _IResolvable_9ceae33e]] = None,
            embedded_source_settings: typing.Optional[typing.Union["CfnChannel.EmbeddedSourceSettingsProperty", _IResolvable_9ceae33e]] = None,
            scte20_source_settings: typing.Optional[typing.Union["CfnChannel.Scte20SourceSettingsProperty", _IResolvable_9ceae33e]] = None,
            scte27_source_settings: typing.Optional[typing.Union["CfnChannel.Scte27SourceSettingsProperty", _IResolvable_9ceae33e]] = None,
            teletext_source_settings: typing.Optional[typing.Union["CfnChannel.TeletextSourceSettingsProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param arib_source_settings: ``CfnChannel.CaptionSelectorSettingsProperty.AribSourceSettings``.
            :param dvb_sub_source_settings: ``CfnChannel.CaptionSelectorSettingsProperty.DvbSubSourceSettings``.
            :param embedded_source_settings: ``CfnChannel.CaptionSelectorSettingsProperty.EmbeddedSourceSettings``.
            :param scte20_source_settings: ``CfnChannel.CaptionSelectorSettingsProperty.Scte20SourceSettings``.
            :param scte27_source_settings: ``CfnChannel.CaptionSelectorSettingsProperty.Scte27SourceSettings``.
            :param teletext_source_settings: ``CfnChannel.CaptionSelectorSettingsProperty.TeletextSourceSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-captionselectorsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if arib_source_settings is not None:
                self._values["arib_source_settings"] = arib_source_settings
            if dvb_sub_source_settings is not None:
                self._values["dvb_sub_source_settings"] = dvb_sub_source_settings
            if embedded_source_settings is not None:
                self._values["embedded_source_settings"] = embedded_source_settings
            if scte20_source_settings is not None:
                self._values["scte20_source_settings"] = scte20_source_settings
            if scte27_source_settings is not None:
                self._values["scte27_source_settings"] = scte27_source_settings
            if teletext_source_settings is not None:
                self._values["teletext_source_settings"] = teletext_source_settings

        @builtins.property
        def arib_source_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.AribSourceSettingsProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.CaptionSelectorSettingsProperty.AribSourceSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-captionselectorsettings.html#cfn-medialive-channel-captionselectorsettings-aribsourcesettings
            """
            result = self._values.get("arib_source_settings")
            return result

        @builtins.property
        def dvb_sub_source_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.DvbSubSourceSettingsProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.CaptionSelectorSettingsProperty.DvbSubSourceSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-captionselectorsettings.html#cfn-medialive-channel-captionselectorsettings-dvbsubsourcesettings
            """
            result = self._values.get("dvb_sub_source_settings")
            return result

        @builtins.property
        def embedded_source_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.EmbeddedSourceSettingsProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.CaptionSelectorSettingsProperty.EmbeddedSourceSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-captionselectorsettings.html#cfn-medialive-channel-captionselectorsettings-embeddedsourcesettings
            """
            result = self._values.get("embedded_source_settings")
            return result

        @builtins.property
        def scte20_source_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.Scte20SourceSettingsProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.CaptionSelectorSettingsProperty.Scte20SourceSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-captionselectorsettings.html#cfn-medialive-channel-captionselectorsettings-scte20sourcesettings
            """
            result = self._values.get("scte20_source_settings")
            return result

        @builtins.property
        def scte27_source_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.Scte27SourceSettingsProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.CaptionSelectorSettingsProperty.Scte27SourceSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-captionselectorsettings.html#cfn-medialive-channel-captionselectorsettings-scte27sourcesettings
            """
            result = self._values.get("scte27_source_settings")
            return result

        @builtins.property
        def teletext_source_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.TeletextSourceSettingsProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.CaptionSelectorSettingsProperty.TeletextSourceSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-captionselectorsettings.html#cfn-medialive-channel-captionselectorsettings-teletextsourcesettings
            """
            result = self._values.get("teletext_source_settings")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CaptionSelectorSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.DvbSubSourceSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"pid": "pid"},
    )
    class DvbSubSourceSettingsProperty:
        def __init__(self, *, pid: typing.Optional[jsii.Number] = None) -> None:
            """
            :param pid: ``CfnChannel.DvbSubSourceSettingsProperty.Pid``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-dvbsubsourcesettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if pid is not None:
                self._values["pid"] = pid

        @builtins.property
        def pid(self) -> typing.Optional[jsii.Number]:
            """``CfnChannel.DvbSubSourceSettingsProperty.Pid``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-dvbsubsourcesettings.html#cfn-medialive-channel-dvbsubsourcesettings-pid
            """
            result = self._values.get("pid")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DvbSubSourceSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.EmbeddedSourceSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "convert608_to708": "convert608To708",
            "scte20_detection": "scte20Detection",
            "source608_channel_number": "source608ChannelNumber",
            "source608_track_number": "source608TrackNumber",
        },
    )
    class EmbeddedSourceSettingsProperty:
        def __init__(
            self,
            *,
            convert608_to708: typing.Optional[builtins.str] = None,
            scte20_detection: typing.Optional[builtins.str] = None,
            source608_channel_number: typing.Optional[jsii.Number] = None,
            source608_track_number: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param convert608_to708: ``CfnChannel.EmbeddedSourceSettingsProperty.Convert608To708``.
            :param scte20_detection: ``CfnChannel.EmbeddedSourceSettingsProperty.Scte20Detection``.
            :param source608_channel_number: ``CfnChannel.EmbeddedSourceSettingsProperty.Source608ChannelNumber``.
            :param source608_track_number: ``CfnChannel.EmbeddedSourceSettingsProperty.Source608TrackNumber``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-embeddedsourcesettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if convert608_to708 is not None:
                self._values["convert608_to708"] = convert608_to708
            if scte20_detection is not None:
                self._values["scte20_detection"] = scte20_detection
            if source608_channel_number is not None:
                self._values["source608_channel_number"] = source608_channel_number
            if source608_track_number is not None:
                self._values["source608_track_number"] = source608_track_number

        @builtins.property
        def convert608_to708(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.EmbeddedSourceSettingsProperty.Convert608To708``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-embeddedsourcesettings.html#cfn-medialive-channel-embeddedsourcesettings-convert608to708
            """
            result = self._values.get("convert608_to708")
            return result

        @builtins.property
        def scte20_detection(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.EmbeddedSourceSettingsProperty.Scte20Detection``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-embeddedsourcesettings.html#cfn-medialive-channel-embeddedsourcesettings-scte20detection
            """
            result = self._values.get("scte20_detection")
            return result

        @builtins.property
        def source608_channel_number(self) -> typing.Optional[jsii.Number]:
            """``CfnChannel.EmbeddedSourceSettingsProperty.Source608ChannelNumber``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-embeddedsourcesettings.html#cfn-medialive-channel-embeddedsourcesettings-source608channelnumber
            """
            result = self._values.get("source608_channel_number")
            return result

        @builtins.property
        def source608_track_number(self) -> typing.Optional[jsii.Number]:
            """``CfnChannel.EmbeddedSourceSettingsProperty.Source608TrackNumber``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-embeddedsourcesettings.html#cfn-medialive-channel-embeddedsourcesettings-source608tracknumber
            """
            result = self._values.get("source608_track_number")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmbeddedSourceSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.HlsInputSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bandwidth": "bandwidth",
            "buffer_segments": "bufferSegments",
            "retries": "retries",
            "retry_interval": "retryInterval",
        },
    )
    class HlsInputSettingsProperty:
        def __init__(
            self,
            *,
            bandwidth: typing.Optional[jsii.Number] = None,
            buffer_segments: typing.Optional[jsii.Number] = None,
            retries: typing.Optional[jsii.Number] = None,
            retry_interval: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param bandwidth: ``CfnChannel.HlsInputSettingsProperty.Bandwidth``.
            :param buffer_segments: ``CfnChannel.HlsInputSettingsProperty.BufferSegments``.
            :param retries: ``CfnChannel.HlsInputSettingsProperty.Retries``.
            :param retry_interval: ``CfnChannel.HlsInputSettingsProperty.RetryInterval``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-hlsinputsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if bandwidth is not None:
                self._values["bandwidth"] = bandwidth
            if buffer_segments is not None:
                self._values["buffer_segments"] = buffer_segments
            if retries is not None:
                self._values["retries"] = retries
            if retry_interval is not None:
                self._values["retry_interval"] = retry_interval

        @builtins.property
        def bandwidth(self) -> typing.Optional[jsii.Number]:
            """``CfnChannel.HlsInputSettingsProperty.Bandwidth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-hlsinputsettings.html#cfn-medialive-channel-hlsinputsettings-bandwidth
            """
            result = self._values.get("bandwidth")
            return result

        @builtins.property
        def buffer_segments(self) -> typing.Optional[jsii.Number]:
            """``CfnChannel.HlsInputSettingsProperty.BufferSegments``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-hlsinputsettings.html#cfn-medialive-channel-hlsinputsettings-buffersegments
            """
            result = self._values.get("buffer_segments")
            return result

        @builtins.property
        def retries(self) -> typing.Optional[jsii.Number]:
            """``CfnChannel.HlsInputSettingsProperty.Retries``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-hlsinputsettings.html#cfn-medialive-channel-hlsinputsettings-retries
            """
            result = self._values.get("retries")
            return result

        @builtins.property
        def retry_interval(self) -> typing.Optional[jsii.Number]:
            """``CfnChannel.HlsInputSettingsProperty.RetryInterval``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-hlsinputsettings.html#cfn-medialive-channel-hlsinputsettings-retryinterval
            """
            result = self._values.get("retry_interval")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsInputSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.InputAttachmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "input_attachment_name": "inputAttachmentName",
            "input_id": "inputId",
            "input_settings": "inputSettings",
        },
    )
    class InputAttachmentProperty:
        def __init__(
            self,
            *,
            input_attachment_name: typing.Optional[builtins.str] = None,
            input_id: typing.Optional[builtins.str] = None,
            input_settings: typing.Optional[typing.Union["CfnChannel.InputSettingsProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param input_attachment_name: ``CfnChannel.InputAttachmentProperty.InputAttachmentName``.
            :param input_id: ``CfnChannel.InputAttachmentProperty.InputId``.
            :param input_settings: ``CfnChannel.InputAttachmentProperty.InputSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputattachment.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if input_attachment_name is not None:
                self._values["input_attachment_name"] = input_attachment_name
            if input_id is not None:
                self._values["input_id"] = input_id
            if input_settings is not None:
                self._values["input_settings"] = input_settings

        @builtins.property
        def input_attachment_name(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.InputAttachmentProperty.InputAttachmentName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputattachment.html#cfn-medialive-channel-inputattachment-inputattachmentname
            """
            result = self._values.get("input_attachment_name")
            return result

        @builtins.property
        def input_id(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.InputAttachmentProperty.InputId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputattachment.html#cfn-medialive-channel-inputattachment-inputid
            """
            result = self._values.get("input_id")
            return result

        @builtins.property
        def input_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.InputSettingsProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.InputAttachmentProperty.InputSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputattachment.html#cfn-medialive-channel-inputattachment-inputsettings
            """
            result = self._values.get("input_settings")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputAttachmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.InputSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "audio_selectors": "audioSelectors",
            "caption_selectors": "captionSelectors",
            "deblock_filter": "deblockFilter",
            "denoise_filter": "denoiseFilter",
            "filter_strength": "filterStrength",
            "input_filter": "inputFilter",
            "network_input_settings": "networkInputSettings",
            "source_end_behavior": "sourceEndBehavior",
            "video_selector": "videoSelector",
        },
    )
    class InputSettingsProperty:
        def __init__(
            self,
            *,
            audio_selectors: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnChannel.AudioSelectorProperty", _IResolvable_9ceae33e]]]] = None,
            caption_selectors: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnChannel.CaptionSelectorProperty", _IResolvable_9ceae33e]]]] = None,
            deblock_filter: typing.Optional[builtins.str] = None,
            denoise_filter: typing.Optional[builtins.str] = None,
            filter_strength: typing.Optional[jsii.Number] = None,
            input_filter: typing.Optional[builtins.str] = None,
            network_input_settings: typing.Optional[typing.Union["CfnChannel.NetworkInputSettingsProperty", _IResolvable_9ceae33e]] = None,
            source_end_behavior: typing.Optional[builtins.str] = None,
            video_selector: typing.Optional[typing.Union["CfnChannel.VideoSelectorProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param audio_selectors: ``CfnChannel.InputSettingsProperty.AudioSelectors``.
            :param caption_selectors: ``CfnChannel.InputSettingsProperty.CaptionSelectors``.
            :param deblock_filter: ``CfnChannel.InputSettingsProperty.DeblockFilter``.
            :param denoise_filter: ``CfnChannel.InputSettingsProperty.DenoiseFilter``.
            :param filter_strength: ``CfnChannel.InputSettingsProperty.FilterStrength``.
            :param input_filter: ``CfnChannel.InputSettingsProperty.InputFilter``.
            :param network_input_settings: ``CfnChannel.InputSettingsProperty.NetworkInputSettings``.
            :param source_end_behavior: ``CfnChannel.InputSettingsProperty.SourceEndBehavior``.
            :param video_selector: ``CfnChannel.InputSettingsProperty.VideoSelector``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if audio_selectors is not None:
                self._values["audio_selectors"] = audio_selectors
            if caption_selectors is not None:
                self._values["caption_selectors"] = caption_selectors
            if deblock_filter is not None:
                self._values["deblock_filter"] = deblock_filter
            if denoise_filter is not None:
                self._values["denoise_filter"] = denoise_filter
            if filter_strength is not None:
                self._values["filter_strength"] = filter_strength
            if input_filter is not None:
                self._values["input_filter"] = input_filter
            if network_input_settings is not None:
                self._values["network_input_settings"] = network_input_settings
            if source_end_behavior is not None:
                self._values["source_end_behavior"] = source_end_behavior
            if video_selector is not None:
                self._values["video_selector"] = video_selector

        @builtins.property
        def audio_selectors(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnChannel.AudioSelectorProperty", _IResolvable_9ceae33e]]]]:
            """``CfnChannel.InputSettingsProperty.AudioSelectors``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputsettings.html#cfn-medialive-channel-inputsettings-audioselectors
            """
            result = self._values.get("audio_selectors")
            return result

        @builtins.property
        def caption_selectors(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnChannel.CaptionSelectorProperty", _IResolvable_9ceae33e]]]]:
            """``CfnChannel.InputSettingsProperty.CaptionSelectors``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputsettings.html#cfn-medialive-channel-inputsettings-captionselectors
            """
            result = self._values.get("caption_selectors")
            return result

        @builtins.property
        def deblock_filter(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.InputSettingsProperty.DeblockFilter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputsettings.html#cfn-medialive-channel-inputsettings-deblockfilter
            """
            result = self._values.get("deblock_filter")
            return result

        @builtins.property
        def denoise_filter(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.InputSettingsProperty.DenoiseFilter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputsettings.html#cfn-medialive-channel-inputsettings-denoisefilter
            """
            result = self._values.get("denoise_filter")
            return result

        @builtins.property
        def filter_strength(self) -> typing.Optional[jsii.Number]:
            """``CfnChannel.InputSettingsProperty.FilterStrength``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputsettings.html#cfn-medialive-channel-inputsettings-filterstrength
            """
            result = self._values.get("filter_strength")
            return result

        @builtins.property
        def input_filter(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.InputSettingsProperty.InputFilter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputsettings.html#cfn-medialive-channel-inputsettings-inputfilter
            """
            result = self._values.get("input_filter")
            return result

        @builtins.property
        def network_input_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.NetworkInputSettingsProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.InputSettingsProperty.NetworkInputSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputsettings.html#cfn-medialive-channel-inputsettings-networkinputsettings
            """
            result = self._values.get("network_input_settings")
            return result

        @builtins.property
        def source_end_behavior(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.InputSettingsProperty.SourceEndBehavior``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputsettings.html#cfn-medialive-channel-inputsettings-sourceendbehavior
            """
            result = self._values.get("source_end_behavior")
            return result

        @builtins.property
        def video_selector(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.VideoSelectorProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.InputSettingsProperty.VideoSelector``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputsettings.html#cfn-medialive-channel-inputsettings-videoselector
            """
            result = self._values.get("video_selector")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.InputSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "codec": "codec",
            "maximum_bitrate": "maximumBitrate",
            "resolution": "resolution",
        },
    )
    class InputSpecificationProperty:
        def __init__(
            self,
            *,
            codec: typing.Optional[builtins.str] = None,
            maximum_bitrate: typing.Optional[builtins.str] = None,
            resolution: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param codec: ``CfnChannel.InputSpecificationProperty.Codec``.
            :param maximum_bitrate: ``CfnChannel.InputSpecificationProperty.MaximumBitrate``.
            :param resolution: ``CfnChannel.InputSpecificationProperty.Resolution``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputspecification.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if codec is not None:
                self._values["codec"] = codec
            if maximum_bitrate is not None:
                self._values["maximum_bitrate"] = maximum_bitrate
            if resolution is not None:
                self._values["resolution"] = resolution

        @builtins.property
        def codec(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.InputSpecificationProperty.Codec``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputspecification.html#cfn-medialive-channel-inputspecification-codec
            """
            result = self._values.get("codec")
            return result

        @builtins.property
        def maximum_bitrate(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.InputSpecificationProperty.MaximumBitrate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputspecification.html#cfn-medialive-channel-inputspecification-maximumbitrate
            """
            result = self._values.get("maximum_bitrate")
            return result

        @builtins.property
        def resolution(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.InputSpecificationProperty.Resolution``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-inputspecification.html#cfn-medialive-channel-inputspecification-resolution
            """
            result = self._values.get("resolution")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.MediaPackageOutputDestinationSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"channel_id": "channelId"},
    )
    class MediaPackageOutputDestinationSettingsProperty:
        def __init__(self, *, channel_id: typing.Optional[builtins.str] = None) -> None:
            """
            :param channel_id: ``CfnChannel.MediaPackageOutputDestinationSettingsProperty.ChannelId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-mediapackageoutputdestinationsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if channel_id is not None:
                self._values["channel_id"] = channel_id

        @builtins.property
        def channel_id(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.MediaPackageOutputDestinationSettingsProperty.ChannelId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-mediapackageoutputdestinationsettings.html#cfn-medialive-channel-mediapackageoutputdestinationsettings-channelid
            """
            result = self._values.get("channel_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MediaPackageOutputDestinationSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.MultiplexProgramChannelDestinationSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"multiplex_id": "multiplexId", "program_name": "programName"},
    )
    class MultiplexProgramChannelDestinationSettingsProperty:
        def __init__(
            self,
            *,
            multiplex_id: typing.Optional[builtins.str] = None,
            program_name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param multiplex_id: ``CfnChannel.MultiplexProgramChannelDestinationSettingsProperty.MultiplexId``.
            :param program_name: ``CfnChannel.MultiplexProgramChannelDestinationSettingsProperty.ProgramName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-multiplexprogramchanneldestinationsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if multiplex_id is not None:
                self._values["multiplex_id"] = multiplex_id
            if program_name is not None:
                self._values["program_name"] = program_name

        @builtins.property
        def multiplex_id(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.MultiplexProgramChannelDestinationSettingsProperty.MultiplexId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-multiplexprogramchanneldestinationsettings.html#cfn-medialive-channel-multiplexprogramchanneldestinationsettings-multiplexid
            """
            result = self._values.get("multiplex_id")
            return result

        @builtins.property
        def program_name(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.MultiplexProgramChannelDestinationSettingsProperty.ProgramName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-multiplexprogramchanneldestinationsettings.html#cfn-medialive-channel-multiplexprogramchanneldestinationsettings-programname
            """
            result = self._values.get("program_name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultiplexProgramChannelDestinationSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.NetworkInputSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hls_input_settings": "hlsInputSettings",
            "server_validation": "serverValidation",
        },
    )
    class NetworkInputSettingsProperty:
        def __init__(
            self,
            *,
            hls_input_settings: typing.Optional[typing.Union["CfnChannel.HlsInputSettingsProperty", _IResolvable_9ceae33e]] = None,
            server_validation: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param hls_input_settings: ``CfnChannel.NetworkInputSettingsProperty.HlsInputSettings``.
            :param server_validation: ``CfnChannel.NetworkInputSettingsProperty.ServerValidation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-networkinputsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if hls_input_settings is not None:
                self._values["hls_input_settings"] = hls_input_settings
            if server_validation is not None:
                self._values["server_validation"] = server_validation

        @builtins.property
        def hls_input_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.HlsInputSettingsProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.NetworkInputSettingsProperty.HlsInputSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-networkinputsettings.html#cfn-medialive-channel-networkinputsettings-hlsinputsettings
            """
            result = self._values.get("hls_input_settings")
            return result

        @builtins.property
        def server_validation(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.NetworkInputSettingsProperty.ServerValidation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-networkinputsettings.html#cfn-medialive-channel-networkinputsettings-servervalidation
            """
            result = self._values.get("server_validation")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkInputSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.OutputDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "media_package_settings": "mediaPackageSettings",
            "multiplex_settings": "multiplexSettings",
            "settings": "settings",
        },
    )
    class OutputDestinationProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            media_package_settings: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnChannel.MediaPackageOutputDestinationSettingsProperty", _IResolvable_9ceae33e]]]] = None,
            multiplex_settings: typing.Optional[typing.Union["CfnChannel.MultiplexProgramChannelDestinationSettingsProperty", _IResolvable_9ceae33e]] = None,
            settings: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnChannel.OutputDestinationSettingsProperty", _IResolvable_9ceae33e]]]] = None,
        ) -> None:
            """
            :param id: ``CfnChannel.OutputDestinationProperty.Id``.
            :param media_package_settings: ``CfnChannel.OutputDestinationProperty.MediaPackageSettings``.
            :param multiplex_settings: ``CfnChannel.OutputDestinationProperty.MultiplexSettings``.
            :param settings: ``CfnChannel.OutputDestinationProperty.Settings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-outputdestination.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if media_package_settings is not None:
                self._values["media_package_settings"] = media_package_settings
            if multiplex_settings is not None:
                self._values["multiplex_settings"] = multiplex_settings
            if settings is not None:
                self._values["settings"] = settings

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.OutputDestinationProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-outputdestination.html#cfn-medialive-channel-outputdestination-id
            """
            result = self._values.get("id")
            return result

        @builtins.property
        def media_package_settings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnChannel.MediaPackageOutputDestinationSettingsProperty", _IResolvable_9ceae33e]]]]:
            """``CfnChannel.OutputDestinationProperty.MediaPackageSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-outputdestination.html#cfn-medialive-channel-outputdestination-mediapackagesettings
            """
            result = self._values.get("media_package_settings")
            return result

        @builtins.property
        def multiplex_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.MultiplexProgramChannelDestinationSettingsProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.OutputDestinationProperty.MultiplexSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-outputdestination.html#cfn-medialive-channel-outputdestination-multiplexsettings
            """
            result = self._values.get("multiplex_settings")
            return result

        @builtins.property
        def settings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnChannel.OutputDestinationSettingsProperty", _IResolvable_9ceae33e]]]]:
            """``CfnChannel.OutputDestinationProperty.Settings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-outputdestination.html#cfn-medialive-channel-outputdestination-settings
            """
            result = self._values.get("settings")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.OutputDestinationSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "password_param": "passwordParam",
            "stream_name": "streamName",
            "url": "url",
            "username": "username",
        },
    )
    class OutputDestinationSettingsProperty:
        def __init__(
            self,
            *,
            password_param: typing.Optional[builtins.str] = None,
            stream_name: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param password_param: ``CfnChannel.OutputDestinationSettingsProperty.PasswordParam``.
            :param stream_name: ``CfnChannel.OutputDestinationSettingsProperty.StreamName``.
            :param url: ``CfnChannel.OutputDestinationSettingsProperty.Url``.
            :param username: ``CfnChannel.OutputDestinationSettingsProperty.Username``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-outputdestinationsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if password_param is not None:
                self._values["password_param"] = password_param
            if stream_name is not None:
                self._values["stream_name"] = stream_name
            if url is not None:
                self._values["url"] = url
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def password_param(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.OutputDestinationSettingsProperty.PasswordParam``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-outputdestinationsettings.html#cfn-medialive-channel-outputdestinationsettings-passwordparam
            """
            result = self._values.get("password_param")
            return result

        @builtins.property
        def stream_name(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.OutputDestinationSettingsProperty.StreamName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-outputdestinationsettings.html#cfn-medialive-channel-outputdestinationsettings-streamname
            """
            result = self._values.get("stream_name")
            return result

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.OutputDestinationSettingsProperty.Url``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-outputdestinationsettings.html#cfn-medialive-channel-outputdestinationsettings-url
            """
            result = self._values.get("url")
            return result

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.OutputDestinationSettingsProperty.Username``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-outputdestinationsettings.html#cfn-medialive-channel-outputdestinationsettings-username
            """
            result = self._values.get("username")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputDestinationSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.Scte20SourceSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "convert608_to708": "convert608To708",
            "source608_channel_number": "source608ChannelNumber",
        },
    )
    class Scte20SourceSettingsProperty:
        def __init__(
            self,
            *,
            convert608_to708: typing.Optional[builtins.str] = None,
            source608_channel_number: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param convert608_to708: ``CfnChannel.Scte20SourceSettingsProperty.Convert608To708``.
            :param source608_channel_number: ``CfnChannel.Scte20SourceSettingsProperty.Source608ChannelNumber``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-scte20sourcesettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if convert608_to708 is not None:
                self._values["convert608_to708"] = convert608_to708
            if source608_channel_number is not None:
                self._values["source608_channel_number"] = source608_channel_number

        @builtins.property
        def convert608_to708(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.Scte20SourceSettingsProperty.Convert608To708``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-scte20sourcesettings.html#cfn-medialive-channel-scte20sourcesettings-convert608to708
            """
            result = self._values.get("convert608_to708")
            return result

        @builtins.property
        def source608_channel_number(self) -> typing.Optional[jsii.Number]:
            """``CfnChannel.Scte20SourceSettingsProperty.Source608ChannelNumber``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-scte20sourcesettings.html#cfn-medialive-channel-scte20sourcesettings-source608channelnumber
            """
            result = self._values.get("source608_channel_number")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Scte20SourceSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.Scte27SourceSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"pid": "pid"},
    )
    class Scte27SourceSettingsProperty:
        def __init__(self, *, pid: typing.Optional[jsii.Number] = None) -> None:
            """
            :param pid: ``CfnChannel.Scte27SourceSettingsProperty.Pid``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-scte27sourcesettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if pid is not None:
                self._values["pid"] = pid

        @builtins.property
        def pid(self) -> typing.Optional[jsii.Number]:
            """``CfnChannel.Scte27SourceSettingsProperty.Pid``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-scte27sourcesettings.html#cfn-medialive-channel-scte27sourcesettings-pid
            """
            result = self._values.get("pid")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Scte27SourceSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.TeletextSourceSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"page_number": "pageNumber"},
    )
    class TeletextSourceSettingsProperty:
        def __init__(
            self,
            *,
            page_number: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param page_number: ``CfnChannel.TeletextSourceSettingsProperty.PageNumber``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-teletextsourcesettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if page_number is not None:
                self._values["page_number"] = page_number

        @builtins.property
        def page_number(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.TeletextSourceSettingsProperty.PageNumber``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-teletextsourcesettings.html#cfn-medialive-channel-teletextsourcesettings-pagenumber
            """
            result = self._values.get("page_number")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TeletextSourceSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.VideoSelectorPidProperty",
        jsii_struct_bases=[],
        name_mapping={"pid": "pid"},
    )
    class VideoSelectorPidProperty:
        def __init__(self, *, pid: typing.Optional[jsii.Number] = None) -> None:
            """
            :param pid: ``CfnChannel.VideoSelectorPidProperty.Pid``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-videoselectorpid.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if pid is not None:
                self._values["pid"] = pid

        @builtins.property
        def pid(self) -> typing.Optional[jsii.Number]:
            """``CfnChannel.VideoSelectorPidProperty.Pid``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-videoselectorpid.html#cfn-medialive-channel-videoselectorpid-pid
            """
            result = self._values.get("pid")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VideoSelectorPidProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.VideoSelectorProgramIdProperty",
        jsii_struct_bases=[],
        name_mapping={"program_id": "programId"},
    )
    class VideoSelectorProgramIdProperty:
        def __init__(self, *, program_id: typing.Optional[jsii.Number] = None) -> None:
            """
            :param program_id: ``CfnChannel.VideoSelectorProgramIdProperty.ProgramId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-videoselectorprogramid.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if program_id is not None:
                self._values["program_id"] = program_id

        @builtins.property
        def program_id(self) -> typing.Optional[jsii.Number]:
            """``CfnChannel.VideoSelectorProgramIdProperty.ProgramId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-videoselectorprogramid.html#cfn-medialive-channel-videoselectorprogramid-programid
            """
            result = self._values.get("program_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VideoSelectorProgramIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.VideoSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "color_space": "colorSpace",
            "color_space_usage": "colorSpaceUsage",
            "selector_settings": "selectorSettings",
        },
    )
    class VideoSelectorProperty:
        def __init__(
            self,
            *,
            color_space: typing.Optional[builtins.str] = None,
            color_space_usage: typing.Optional[builtins.str] = None,
            selector_settings: typing.Optional[typing.Union["CfnChannel.VideoSelectorSettingsProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param color_space: ``CfnChannel.VideoSelectorProperty.ColorSpace``.
            :param color_space_usage: ``CfnChannel.VideoSelectorProperty.ColorSpaceUsage``.
            :param selector_settings: ``CfnChannel.VideoSelectorProperty.SelectorSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-videoselector.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if color_space is not None:
                self._values["color_space"] = color_space
            if color_space_usage is not None:
                self._values["color_space_usage"] = color_space_usage
            if selector_settings is not None:
                self._values["selector_settings"] = selector_settings

        @builtins.property
        def color_space(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.VideoSelectorProperty.ColorSpace``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-videoselector.html#cfn-medialive-channel-videoselector-colorspace
            """
            result = self._values.get("color_space")
            return result

        @builtins.property
        def color_space_usage(self) -> typing.Optional[builtins.str]:
            """``CfnChannel.VideoSelectorProperty.ColorSpaceUsage``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-videoselector.html#cfn-medialive-channel-videoselector-colorspaceusage
            """
            result = self._values.get("color_space_usage")
            return result

        @builtins.property
        def selector_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.VideoSelectorSettingsProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.VideoSelectorProperty.SelectorSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-videoselector.html#cfn-medialive-channel-videoselector-selectorsettings
            """
            result = self._values.get("selector_settings")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VideoSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnChannel.VideoSelectorSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "video_selector_pid": "videoSelectorPid",
            "video_selector_program_id": "videoSelectorProgramId",
        },
    )
    class VideoSelectorSettingsProperty:
        def __init__(
            self,
            *,
            video_selector_pid: typing.Optional[typing.Union["CfnChannel.VideoSelectorPidProperty", _IResolvable_9ceae33e]] = None,
            video_selector_program_id: typing.Optional[typing.Union["CfnChannel.VideoSelectorProgramIdProperty", _IResolvable_9ceae33e]] = None,
        ) -> None:
            """
            :param video_selector_pid: ``CfnChannel.VideoSelectorSettingsProperty.VideoSelectorPid``.
            :param video_selector_program_id: ``CfnChannel.VideoSelectorSettingsProperty.VideoSelectorProgramId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-videoselectorsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if video_selector_pid is not None:
                self._values["video_selector_pid"] = video_selector_pid
            if video_selector_program_id is not None:
                self._values["video_selector_program_id"] = video_selector_program_id

        @builtins.property
        def video_selector_pid(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.VideoSelectorPidProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.VideoSelectorSettingsProperty.VideoSelectorPid``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-videoselectorsettings.html#cfn-medialive-channel-videoselectorsettings-videoselectorpid
            """
            result = self._values.get("video_selector_pid")
            return result

        @builtins.property
        def video_selector_program_id(
            self,
        ) -> typing.Optional[typing.Union["CfnChannel.VideoSelectorProgramIdProperty", _IResolvable_9ceae33e]]:
            """``CfnChannel.VideoSelectorSettingsProperty.VideoSelectorProgramId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-channel-videoselectorsettings.html#cfn-medialive-channel-videoselectorsettings-videoselectorprogramid
            """
            result = self._values.get("video_selector_program_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VideoSelectorSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_medialive.CfnChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_class": "channelClass",
        "destinations": "destinations",
        "encoder_settings": "encoderSettings",
        "input_attachments": "inputAttachments",
        "input_specification": "inputSpecification",
        "log_level": "logLevel",
        "name": "name",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnChannelProps:
    def __init__(
        self,
        *,
        channel_class: typing.Optional[builtins.str] = None,
        destinations: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnChannel.OutputDestinationProperty", _IResolvable_9ceae33e]]]] = None,
        encoder_settings: typing.Any = None,
        input_attachments: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnChannel.InputAttachmentProperty", _IResolvable_9ceae33e]]]] = None,
        input_specification: typing.Optional[typing.Union["CfnChannel.InputSpecificationProperty", _IResolvable_9ceae33e]] = None,
        log_level: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        """Properties for defining a ``AWS::MediaLive::Channel``.

        :param channel_class: ``AWS::MediaLive::Channel.ChannelClass``.
        :param destinations: ``AWS::MediaLive::Channel.Destinations``.
        :param encoder_settings: ``AWS::MediaLive::Channel.EncoderSettings``.
        :param input_attachments: ``AWS::MediaLive::Channel.InputAttachments``.
        :param input_specification: ``AWS::MediaLive::Channel.InputSpecification``.
        :param log_level: ``AWS::MediaLive::Channel.LogLevel``.
        :param name: ``AWS::MediaLive::Channel.Name``.
        :param role_arn: ``AWS::MediaLive::Channel.RoleArn``.
        :param tags: ``AWS::MediaLive::Channel.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if channel_class is not None:
            self._values["channel_class"] = channel_class
        if destinations is not None:
            self._values["destinations"] = destinations
        if encoder_settings is not None:
            self._values["encoder_settings"] = encoder_settings
        if input_attachments is not None:
            self._values["input_attachments"] = input_attachments
        if input_specification is not None:
            self._values["input_specification"] = input_specification
        if log_level is not None:
            self._values["log_level"] = log_level
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def channel_class(self) -> typing.Optional[builtins.str]:
        """``AWS::MediaLive::Channel.ChannelClass``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-channelclass
        """
        result = self._values.get("channel_class")
        return result

    @builtins.property
    def destinations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnChannel.OutputDestinationProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::MediaLive::Channel.Destinations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-destinations
        """
        result = self._values.get("destinations")
        return result

    @builtins.property
    def encoder_settings(self) -> typing.Any:
        """``AWS::MediaLive::Channel.EncoderSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-encodersettings
        """
        result = self._values.get("encoder_settings")
        return result

    @builtins.property
    def input_attachments(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnChannel.InputAttachmentProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::MediaLive::Channel.InputAttachments``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-inputattachments
        """
        result = self._values.get("input_attachments")
        return result

    @builtins.property
    def input_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnChannel.InputSpecificationProperty", _IResolvable_9ceae33e]]:
        """``AWS::MediaLive::Channel.InputSpecification``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-inputspecification
        """
        result = self._values.get("input_specification")
        return result

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        """``AWS::MediaLive::Channel.LogLevel``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-loglevel
        """
        result = self._values.get("log_level")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::MediaLive::Channel.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::MediaLive::Channel.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-rolearn
        """
        result = self._values.get("role_arn")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::MediaLive::Channel.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-channel.html#cfn-medialive-channel-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnInput(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_medialive.CfnInput",
):
    """A CloudFormation ``AWS::MediaLive::Input``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html
    cloudformationResource:
    :cloudformationResource:: AWS::MediaLive::Input
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        destinations: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InputDestinationRequestProperty", _IResolvable_9ceae33e]]]] = None,
        input_security_groups: typing.Optional[typing.List[builtins.str]] = None,
        media_connect_flows: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["MediaConnectFlowRequestProperty", _IResolvable_9ceae33e]]]] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InputSourceRequestProperty", _IResolvable_9ceae33e]]]] = None,
        tags: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[typing.Union["InputVpcRequestProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Create a new ``AWS::MediaLive::Input``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destinations: ``AWS::MediaLive::Input.Destinations``.
        :param input_security_groups: ``AWS::MediaLive::Input.InputSecurityGroups``.
        :param media_connect_flows: ``AWS::MediaLive::Input.MediaConnectFlows``.
        :param name: ``AWS::MediaLive::Input.Name``.
        :param role_arn: ``AWS::MediaLive::Input.RoleArn``.
        :param sources: ``AWS::MediaLive::Input.Sources``.
        :param tags: ``AWS::MediaLive::Input.Tags``.
        :param type: ``AWS::MediaLive::Input.Type``.
        :param vpc: ``AWS::MediaLive::Input.Vpc``.
        """
        props = CfnInputProps(
            destinations=destinations,
            input_security_groups=input_security_groups,
            media_connect_flows=media_connect_flows,
            name=name,
            role_arn=role_arn,
            sources=sources,
            tags=tags,
            type=type,
            vpc=vpc,
        )

        jsii.create(CfnInput, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrDestinations")
    def attr_destinations(self) -> typing.List[builtins.str]:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Destinations
        """
        return jsii.get(self, "attrDestinations")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrSources")
    def attr_sources(self) -> typing.List[builtins.str]:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Sources
        """
        return jsii.get(self, "attrSources")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::MediaLive::Input.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="destinations")
    def destinations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InputDestinationRequestProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::MediaLive::Input.Destinations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-destinations
        """
        return jsii.get(self, "destinations")

    @destinations.setter # type: ignore
    def destinations(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InputDestinationRequestProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "destinations", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="inputSecurityGroups")
    def input_security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::MediaLive::Input.InputSecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-inputsecuritygroups
        """
        return jsii.get(self, "inputSecurityGroups")

    @input_security_groups.setter # type: ignore
    def input_security_groups(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "inputSecurityGroups", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="mediaConnectFlows")
    def media_connect_flows(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["MediaConnectFlowRequestProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::MediaLive::Input.MediaConnectFlows``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-mediaconnectflows
        """
        return jsii.get(self, "mediaConnectFlows")

    @media_connect_flows.setter # type: ignore
    def media_connect_flows(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["MediaConnectFlowRequestProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "mediaConnectFlows", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::MediaLive::Input.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::MediaLive::Input.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter # type: ignore
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InputSourceRequestProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::MediaLive::Input.Sources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-sources
        """
        return jsii.get(self, "sources")

    @sources.setter # type: ignore
    def sources(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InputSourceRequestProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "sources", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        """``AWS::MediaLive::Input.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-type
        """
        return jsii.get(self, "type")

    @type.setter # type: ignore
    def type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "type", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpc")
    def vpc(
        self,
    ) -> typing.Optional[typing.Union["InputVpcRequestProperty", _IResolvable_9ceae33e]]:
        """``AWS::MediaLive::Input.Vpc``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-vpc
        """
        return jsii.get(self, "vpc")

    @vpc.setter # type: ignore
    def vpc(
        self,
        value: typing.Optional[typing.Union["InputVpcRequestProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "vpc", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnInput.InputDestinationRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_name": "streamName"},
    )
    class InputDestinationRequestProperty:
        def __init__(
            self,
            *,
            stream_name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param stream_name: ``CfnInput.InputDestinationRequestProperty.StreamName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-input-inputdestinationrequest.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if stream_name is not None:
                self._values["stream_name"] = stream_name

        @builtins.property
        def stream_name(self) -> typing.Optional[builtins.str]:
            """``CfnInput.InputDestinationRequestProperty.StreamName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-input-inputdestinationrequest.html#cfn-medialive-input-inputdestinationrequest-streamname
            """
            result = self._values.get("stream_name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputDestinationRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnInput.InputSourceRequestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "password_param": "passwordParam",
            "url": "url",
            "username": "username",
        },
    )
    class InputSourceRequestProperty:
        def __init__(
            self,
            *,
            password_param: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param password_param: ``CfnInput.InputSourceRequestProperty.PasswordParam``.
            :param url: ``CfnInput.InputSourceRequestProperty.Url``.
            :param username: ``CfnInput.InputSourceRequestProperty.Username``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-input-inputsourcerequest.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if password_param is not None:
                self._values["password_param"] = password_param
            if url is not None:
                self._values["url"] = url
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def password_param(self) -> typing.Optional[builtins.str]:
            """``CfnInput.InputSourceRequestProperty.PasswordParam``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-input-inputsourcerequest.html#cfn-medialive-input-inputsourcerequest-passwordparam
            """
            result = self._values.get("password_param")
            return result

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            """``CfnInput.InputSourceRequestProperty.Url``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-input-inputsourcerequest.html#cfn-medialive-input-inputsourcerequest-url
            """
            result = self._values.get("url")
            return result

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            """``CfnInput.InputSourceRequestProperty.Username``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-input-inputsourcerequest.html#cfn-medialive-input-inputsourcerequest-username
            """
            result = self._values.get("username")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputSourceRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnInput.InputVpcRequestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class InputVpcRequestProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param security_group_ids: ``CfnInput.InputVpcRequestProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnInput.InputVpcRequestProperty.SubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-input-inputvpcrequest.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnInput.InputVpcRequestProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-input-inputvpcrequest.html#cfn-medialive-input-inputvpcrequest-securitygroupids
            """
            result = self._values.get("security_group_ids")
            return result

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnInput.InputVpcRequestProperty.SubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-input-inputvpcrequest.html#cfn-medialive-input-inputvpcrequest-subnetids
            """
            result = self._values.get("subnet_ids")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputVpcRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnInput.MediaConnectFlowRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"flow_arn": "flowArn"},
    )
    class MediaConnectFlowRequestProperty:
        def __init__(self, *, flow_arn: typing.Optional[builtins.str] = None) -> None:
            """
            :param flow_arn: ``CfnInput.MediaConnectFlowRequestProperty.FlowArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-input-mediaconnectflowrequest.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if flow_arn is not None:
                self._values["flow_arn"] = flow_arn

        @builtins.property
        def flow_arn(self) -> typing.Optional[builtins.str]:
            """``CfnInput.MediaConnectFlowRequestProperty.FlowArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-input-mediaconnectflowrequest.html#cfn-medialive-input-mediaconnectflowrequest-flowarn
            """
            result = self._values.get("flow_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MediaConnectFlowRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_medialive.CfnInputProps",
    jsii_struct_bases=[],
    name_mapping={
        "destinations": "destinations",
        "input_security_groups": "inputSecurityGroups",
        "media_connect_flows": "mediaConnectFlows",
        "name": "name",
        "role_arn": "roleArn",
        "sources": "sources",
        "tags": "tags",
        "type": "type",
        "vpc": "vpc",
    },
)
class CfnInputProps:
    def __init__(
        self,
        *,
        destinations: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnInput.InputDestinationRequestProperty", _IResolvable_9ceae33e]]]] = None,
        input_security_groups: typing.Optional[typing.List[builtins.str]] = None,
        media_connect_flows: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnInput.MediaConnectFlowRequestProperty", _IResolvable_9ceae33e]]]] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnInput.InputSourceRequestProperty", _IResolvable_9ceae33e]]]] = None,
        tags: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[typing.Union["CfnInput.InputVpcRequestProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Properties for defining a ``AWS::MediaLive::Input``.

        :param destinations: ``AWS::MediaLive::Input.Destinations``.
        :param input_security_groups: ``AWS::MediaLive::Input.InputSecurityGroups``.
        :param media_connect_flows: ``AWS::MediaLive::Input.MediaConnectFlows``.
        :param name: ``AWS::MediaLive::Input.Name``.
        :param role_arn: ``AWS::MediaLive::Input.RoleArn``.
        :param sources: ``AWS::MediaLive::Input.Sources``.
        :param tags: ``AWS::MediaLive::Input.Tags``.
        :param type: ``AWS::MediaLive::Input.Type``.
        :param vpc: ``AWS::MediaLive::Input.Vpc``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if destinations is not None:
            self._values["destinations"] = destinations
        if input_security_groups is not None:
            self._values["input_security_groups"] = input_security_groups
        if media_connect_flows is not None:
            self._values["media_connect_flows"] = media_connect_flows
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if sources is not None:
            self._values["sources"] = sources
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def destinations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnInput.InputDestinationRequestProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::MediaLive::Input.Destinations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-destinations
        """
        result = self._values.get("destinations")
        return result

    @builtins.property
    def input_security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::MediaLive::Input.InputSecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-inputsecuritygroups
        """
        result = self._values.get("input_security_groups")
        return result

    @builtins.property
    def media_connect_flows(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnInput.MediaConnectFlowRequestProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::MediaLive::Input.MediaConnectFlows``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-mediaconnectflows
        """
        result = self._values.get("media_connect_flows")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::MediaLive::Input.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::MediaLive::Input.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-rolearn
        """
        result = self._values.get("role_arn")
        return result

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnInput.InputSourceRequestProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::MediaLive::Input.Sources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-sources
        """
        result = self._values.get("sources")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::MediaLive::Input.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        """``AWS::MediaLive::Input.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-type
        """
        result = self._values.get("type")
        return result

    @builtins.property
    def vpc(
        self,
    ) -> typing.Optional[typing.Union["CfnInput.InputVpcRequestProperty", _IResolvable_9ceae33e]]:
        """``AWS::MediaLive::Input.Vpc``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-input.html#cfn-medialive-input-vpc
        """
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInputProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnInputSecurityGroup(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_medialive.CfnInputSecurityGroup",
):
    """A CloudFormation ``AWS::MediaLive::InputSecurityGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-inputsecuritygroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::MediaLive::InputSecurityGroup
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: builtins.str,
        *,
        tags: typing.Any = None,
        whitelist_rules: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InputWhitelistRuleCidrProperty", _IResolvable_9ceae33e]]]] = None,
    ) -> None:
        """Create a new ``AWS::MediaLive::InputSecurityGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param tags: ``AWS::MediaLive::InputSecurityGroup.Tags``.
        :param whitelist_rules: ``AWS::MediaLive::InputSecurityGroup.WhitelistRules``.
        """
        props = CfnInputSecurityGroupProps(tags=tags, whitelist_rules=whitelist_rules)

        jsii.create(CfnInputSecurityGroup, self, [scope, id, props])

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
        """``AWS::MediaLive::InputSecurityGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-inputsecuritygroup.html#cfn-medialive-inputsecuritygroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="whitelistRules")
    def whitelist_rules(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InputWhitelistRuleCidrProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::MediaLive::InputSecurityGroup.WhitelistRules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-inputsecuritygroup.html#cfn-medialive-inputsecuritygroup-whitelistrules
        """
        return jsii.get(self, "whitelistRules")

    @whitelist_rules.setter # type: ignore
    def whitelist_rules(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InputWhitelistRuleCidrProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "whitelistRules", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_medialive.CfnInputSecurityGroup.InputWhitelistRuleCidrProperty",
        jsii_struct_bases=[],
        name_mapping={"cidr": "cidr"},
    )
    class InputWhitelistRuleCidrProperty:
        def __init__(self, *, cidr: typing.Optional[builtins.str] = None) -> None:
            """
            :param cidr: ``CfnInputSecurityGroup.InputWhitelistRuleCidrProperty.Cidr``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-inputsecuritygroup-inputwhitelistrulecidr.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if cidr is not None:
                self._values["cidr"] = cidr

        @builtins.property
        def cidr(self) -> typing.Optional[builtins.str]:
            """``CfnInputSecurityGroup.InputWhitelistRuleCidrProperty.Cidr``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-medialive-inputsecuritygroup-inputwhitelistrulecidr.html#cfn-medialive-inputsecuritygroup-inputwhitelistrulecidr-cidr
            """
            result = self._values.get("cidr")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputWhitelistRuleCidrProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_medialive.CfnInputSecurityGroupProps",
    jsii_struct_bases=[],
    name_mapping={"tags": "tags", "whitelist_rules": "whitelistRules"},
)
class CfnInputSecurityGroupProps:
    def __init__(
        self,
        *,
        tags: typing.Any = None,
        whitelist_rules: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnInputSecurityGroup.InputWhitelistRuleCidrProperty", _IResolvable_9ceae33e]]]] = None,
    ) -> None:
        """Properties for defining a ``AWS::MediaLive::InputSecurityGroup``.

        :param tags: ``AWS::MediaLive::InputSecurityGroup.Tags``.
        :param whitelist_rules: ``AWS::MediaLive::InputSecurityGroup.WhitelistRules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-inputsecuritygroup.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if tags is not None:
            self._values["tags"] = tags
        if whitelist_rules is not None:
            self._values["whitelist_rules"] = whitelist_rules

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::MediaLive::InputSecurityGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-inputsecuritygroup.html#cfn-medialive-inputsecuritygroup-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def whitelist_rules(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnInputSecurityGroup.InputWhitelistRuleCidrProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::MediaLive::InputSecurityGroup.WhitelistRules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-medialive-inputsecuritygroup.html#cfn-medialive-inputsecuritygroup-whitelistrules
        """
        result = self._values.get("whitelist_rules")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInputSecurityGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnChannel",
    "CfnChannelProps",
    "CfnInput",
    "CfnInputProps",
    "CfnInputSecurityGroup",
    "CfnInputSecurityGroupProps",
]

publication.publish()
