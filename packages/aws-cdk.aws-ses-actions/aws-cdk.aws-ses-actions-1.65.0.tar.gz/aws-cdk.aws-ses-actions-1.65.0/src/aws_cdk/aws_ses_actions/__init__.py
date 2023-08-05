"""
## Amazon Simple Email Service Actions Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module contains integration classes to add action to SES email receiving rules.
Instances of these classes should be passed to the `rule.addAction()` method.

Currently supported are:

* [Add header](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-add-header.html)
* [Bounce](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-bounce.html)
* [Lambda](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-lambda.html)
* [S3](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-s3.html)
* [SNS](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-sns.html)
* [Stop](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-stop.html)

See the README of `@aws-cdk/aws-ses` for more information.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.aws_ses
import aws_cdk.aws_sns


@jsii.implements(aws_cdk.aws_ses.IReceiptRuleAction)
class AddHeader(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses-actions.AddHeader",
):
    """Adds a header to the received email.

    stability
    :stability: experimental
    """

    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        """
        :param name: The name of the header to add. Must be between 1 and 50 characters, inclusive, and consist of alphanumeric (a-z, A-Z, 0-9) characters and dashes only.
        :param value: The value of the header to add. Must be less than 2048 characters, and must not contain newline characters ("\r" or "\n").

        stability
        :stability: experimental
        """
        props = AddHeaderProps(name=name, value=value)

        jsii.create(AddHeader, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: aws_cdk.aws_ses.IReceiptRule,
    ) -> aws_cdk.aws_ses.ReceiptRuleActionConfig:
        """Returns the receipt rule action specification.

        :param _rule: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_rule])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses-actions.AddHeaderProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class AddHeaderProps:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        """Construction properties for a add header action.

        :param name: The name of the header to add. Must be between 1 and 50 characters, inclusive, and consist of alphanumeric (a-z, A-Z, 0-9) characters and dashes only.
        :param value: The value of the header to add. Must be less than 2048 characters, and must not contain newline characters ("\r" or "\n").

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        """The name of the header to add.

        Must be between 1 and 50 characters,
        inclusive, and consist of alphanumeric (a-z, A-Z, 0-9) characters
        and dashes only.

        stability
        :stability: experimental
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def value(self) -> builtins.str:
        """The value of the header to add.

        Must be less than 2048 characters,
        and must not contain newline characters ("\r" or "\n").

        stability
        :stability: experimental
        """
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddHeaderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_ses.IReceiptRuleAction)
class Bounce(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses-actions.Bounce"):
    """Rejects the received email by returning a bounce response to the sender and, optionally, publishes a notification to Amazon SNS.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        *,
        sender: builtins.str,
        template: "BounceTemplate",
        topic: typing.Optional[aws_cdk.aws_sns.ITopic] = None,
    ) -> None:
        """
        :param sender: The email address of the sender of the bounced email. This is the address from which the bounce message will be sent.
        :param template: The template containing the message, reply code and status code.
        :param topic: The SNS topic to notify when the bounce action is taken. Default: no notification

        stability
        :stability: experimental
        """
        props = BounceProps(sender=sender, template=template, topic=topic)

        jsii.create(Bounce, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: aws_cdk.aws_ses.IReceiptRule,
    ) -> aws_cdk.aws_ses.ReceiptRuleActionConfig:
        """Returns the receipt rule action specification.

        :param _rule: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_rule])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses-actions.BounceProps",
    jsii_struct_bases=[],
    name_mapping={"sender": "sender", "template": "template", "topic": "topic"},
)
class BounceProps:
    def __init__(
        self,
        *,
        sender: builtins.str,
        template: "BounceTemplate",
        topic: typing.Optional[aws_cdk.aws_sns.ITopic] = None,
    ) -> None:
        """Construction properties for a bounce action.

        :param sender: The email address of the sender of the bounced email. This is the address from which the bounce message will be sent.
        :param template: The template containing the message, reply code and status code.
        :param topic: The SNS topic to notify when the bounce action is taken. Default: no notification

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "sender": sender,
            "template": template,
        }
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def sender(self) -> builtins.str:
        """The email address of the sender of the bounced email.

        This is the address
        from which the bounce message will be sent.

        stability
        :stability: experimental
        """
        result = self._values.get("sender")
        assert result is not None, "Required property 'sender' is missing"
        return result

    @builtins.property
    def template(self) -> "BounceTemplate":
        """The template containing the message, reply code and status code.

        stability
        :stability: experimental
        """
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return result

    @builtins.property
    def topic(self) -> typing.Optional[aws_cdk.aws_sns.ITopic]:
        """The SNS topic to notify when the bounce action is taken.

        default
        :default: no notification

        stability
        :stability: experimental
        """
        result = self._values.get("topic")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BounceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BounceTemplate(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses-actions.BounceTemplate",
):
    """A bounce template.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        *,
        message: builtins.str,
        smtp_reply_code: builtins.str,
        status_code: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param message: Human-readable text to include in the bounce message.
        :param smtp_reply_code: The SMTP reply code, as defined by RFC 5321.
        :param status_code: The SMTP enhanced status code, as defined by RFC 3463.

        stability
        :stability: experimental
        """
        props = BounceTemplateProps(
            message=message, smtp_reply_code=smtp_reply_code, status_code=status_code
        )

        jsii.create(BounceTemplate, self, [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MAILBOX_DOES_NOT_EXIST")
    def MAILBOX_DOES_NOT_EXIST(cls) -> "BounceTemplate":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "MAILBOX_DOES_NOT_EXIST")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MAILBOX_FULL")
    def MAILBOX_FULL(cls) -> "BounceTemplate":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "MAILBOX_FULL")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MESSAGE_CONTENT_REJECTED")
    def MESSAGE_CONTENT_REJECTED(cls) -> "BounceTemplate":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "MESSAGE_CONTENT_REJECTED")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MESSAGE_TOO_LARGE")
    def MESSAGE_TOO_LARGE(cls) -> "BounceTemplate":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "MESSAGE_TOO_LARGE")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="TEMPORARY_FAILURE")
    def TEMPORARY_FAILURE(cls) -> "BounceTemplate":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "TEMPORARY_FAILURE")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="props")
    def props(self) -> "BounceTemplateProps":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "props")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses-actions.BounceTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "message": "message",
        "smtp_reply_code": "smtpReplyCode",
        "status_code": "statusCode",
    },
)
class BounceTemplateProps:
    def __init__(
        self,
        *,
        message: builtins.str,
        smtp_reply_code: builtins.str,
        status_code: typing.Optional[builtins.str] = None,
    ) -> None:
        """Construction properties for a BounceTemplate.

        :param message: Human-readable text to include in the bounce message.
        :param smtp_reply_code: The SMTP reply code, as defined by RFC 5321.
        :param status_code: The SMTP enhanced status code, as defined by RFC 3463.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "message": message,
            "smtp_reply_code": smtp_reply_code,
        }
        if status_code is not None:
            self._values["status_code"] = status_code

    @builtins.property
    def message(self) -> builtins.str:
        """Human-readable text to include in the bounce message.

        stability
        :stability: experimental
        """
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return result

    @builtins.property
    def smtp_reply_code(self) -> builtins.str:
        """The SMTP reply code, as defined by RFC 5321.

        see
        :see: https://tools.ietf.org/html/rfc5321
        stability
        :stability: experimental
        """
        result = self._values.get("smtp_reply_code")
        assert result is not None, "Required property 'smtp_reply_code' is missing"
        return result

    @builtins.property
    def status_code(self) -> typing.Optional[builtins.str]:
        """The SMTP enhanced status code, as defined by RFC 3463.

        see
        :see: https://tools.ietf.org/html/rfc3463
        stability
        :stability: experimental
        """
        result = self._values.get("status_code")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BounceTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-ses-actions.EmailEncoding")
class EmailEncoding(enum.Enum):
    """The type of email encoding to use for a SNS action.

    stability
    :stability: experimental
    """

    BASE64 = "BASE64"
    """Base 64.

    stability
    :stability: experimental
    """
    UTF8 = "UTF8"
    """UTF-8.

    stability
    :stability: experimental
    """


@jsii.implements(aws_cdk.aws_ses.IReceiptRuleAction)
class Lambda(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses-actions.Lambda"):
    """Calls an AWS Lambda function, and optionally, publishes a notification to Amazon SNS.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        *,
        function: aws_cdk.aws_lambda.IFunction,
        invocation_type: typing.Optional["LambdaInvocationType"] = None,
        topic: typing.Optional[aws_cdk.aws_sns.ITopic] = None,
    ) -> None:
        """
        :param function: The Lambda function to invoke.
        :param invocation_type: The invocation type of the Lambda function. Default: Event
        :param topic: The SNS topic to notify when the Lambda action is taken. Default: no notification

        stability
        :stability: experimental
        """
        props = LambdaProps(
            function=function, invocation_type=invocation_type, topic=topic
        )

        jsii.create(Lambda, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: aws_cdk.aws_ses.IReceiptRule,
    ) -> aws_cdk.aws_ses.ReceiptRuleActionConfig:
        """Returns the receipt rule action specification.

        :param rule: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [rule])


@jsii.enum(jsii_type="@aws-cdk/aws-ses-actions.LambdaInvocationType")
class LambdaInvocationType(enum.Enum):
    """The type of invocation to use for a Lambda Action.

    stability
    :stability: experimental
    """

    EVENT = "EVENT"
    """The function will be invoked asynchronously.

    stability
    :stability: experimental
    """
    REQUEST_RESPONSE = "REQUEST_RESPONSE"
    """The function will be invoked sychronously.

    Use RequestResponse only when
    you want to make a mail flow decision, such as whether to stop the receipt
    rule or the receipt rule set.

    stability
    :stability: experimental
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses-actions.LambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "function": "function",
        "invocation_type": "invocationType",
        "topic": "topic",
    },
)
class LambdaProps:
    def __init__(
        self,
        *,
        function: aws_cdk.aws_lambda.IFunction,
        invocation_type: typing.Optional["LambdaInvocationType"] = None,
        topic: typing.Optional[aws_cdk.aws_sns.ITopic] = None,
    ) -> None:
        """Construction properties for a Lambda action.

        :param function: The Lambda function to invoke.
        :param invocation_type: The invocation type of the Lambda function. Default: Event
        :param topic: The SNS topic to notify when the Lambda action is taken. Default: no notification

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "function": function,
        }
        if invocation_type is not None:
            self._values["invocation_type"] = invocation_type
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def function(self) -> aws_cdk.aws_lambda.IFunction:
        """The Lambda function to invoke.

        stability
        :stability: experimental
        """
        result = self._values.get("function")
        assert result is not None, "Required property 'function' is missing"
        return result

    @builtins.property
    def invocation_type(self) -> typing.Optional["LambdaInvocationType"]:
        """The invocation type of the Lambda function.

        default
        :default: Event

        stability
        :stability: experimental
        """
        result = self._values.get("invocation_type")
        return result

    @builtins.property
    def topic(self) -> typing.Optional[aws_cdk.aws_sns.ITopic]:
        """The SNS topic to notify when the Lambda action is taken.

        default
        :default: no notification

        stability
        :stability: experimental
        """
        result = self._values.get("topic")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_ses.IReceiptRuleAction)
class S3(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses-actions.S3"):
    """Saves the received message to an Amazon S3 bucket and, optionally, publishes a notification to Amazon SNS.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        kms_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        object_key_prefix: typing.Optional[builtins.str] = None,
        topic: typing.Optional[aws_cdk.aws_sns.ITopic] = None,
    ) -> None:
        """
        :param bucket: The S3 bucket that incoming email will be saved to.
        :param kms_key: The master key that SES should use to encrypt your emails before saving them to the S3 bucket. Default: no encryption
        :param object_key_prefix: The key prefix of the S3 bucket. Default: no prefix
        :param topic: The SNS topic to notify when the S3 action is taken. Default: no notification

        stability
        :stability: experimental
        """
        props = S3Props(
            bucket=bucket,
            kms_key=kms_key,
            object_key_prefix=object_key_prefix,
            topic=topic,
        )

        jsii.create(S3, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: aws_cdk.aws_ses.IReceiptRule,
    ) -> aws_cdk.aws_ses.ReceiptRuleActionConfig:
        """Returns the receipt rule action specification.

        :param rule: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [rule])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses-actions.S3Props",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "kms_key": "kmsKey",
        "object_key_prefix": "objectKeyPrefix",
        "topic": "topic",
    },
)
class S3Props:
    def __init__(
        self,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        kms_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        object_key_prefix: typing.Optional[builtins.str] = None,
        topic: typing.Optional[aws_cdk.aws_sns.ITopic] = None,
    ) -> None:
        """Construction properties for a S3 action.

        :param bucket: The S3 bucket that incoming email will be saved to.
        :param kms_key: The master key that SES should use to encrypt your emails before saving them to the S3 bucket. Default: no encryption
        :param object_key_prefix: The key prefix of the S3 bucket. Default: no prefix
        :param topic: The SNS topic to notify when the S3 action is taken. Default: no notification

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if object_key_prefix is not None:
            self._values["object_key_prefix"] = object_key_prefix
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The S3 bucket that incoming email will be saved to.

        stability
        :stability: experimental
        """
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return result

    @builtins.property
    def kms_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The master key that SES should use to encrypt your emails before saving them to the S3 bucket.

        default
        :default: no encryption

        stability
        :stability: experimental
        """
        result = self._values.get("kms_key")
        return result

    @builtins.property
    def object_key_prefix(self) -> typing.Optional[builtins.str]:
        """The key prefix of the S3 bucket.

        default
        :default: no prefix

        stability
        :stability: experimental
        """
        result = self._values.get("object_key_prefix")
        return result

    @builtins.property
    def topic(self) -> typing.Optional[aws_cdk.aws_sns.ITopic]:
        """The SNS topic to notify when the S3 action is taken.

        default
        :default: no notification

        stability
        :stability: experimental
        """
        result = self._values.get("topic")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_ses.IReceiptRuleAction)
class Sns(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses-actions.Sns"):
    """Publishes the email content within a notification to Amazon SNS.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        *,
        topic: aws_cdk.aws_sns.ITopic,
        encoding: typing.Optional["EmailEncoding"] = None,
    ) -> None:
        """
        :param topic: The SNS topic to notify.
        :param encoding: The encoding to use for the email within the Amazon SNS notification. Default: UTF-8

        stability
        :stability: experimental
        """
        props = SnsProps(topic=topic, encoding=encoding)

        jsii.create(Sns, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: aws_cdk.aws_ses.IReceiptRule,
    ) -> aws_cdk.aws_ses.ReceiptRuleActionConfig:
        """Returns the receipt rule action specification.

        :param _rule: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_rule])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses-actions.SnsProps",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic", "encoding": "encoding"},
)
class SnsProps:
    def __init__(
        self,
        *,
        topic: aws_cdk.aws_sns.ITopic,
        encoding: typing.Optional["EmailEncoding"] = None,
    ) -> None:
        """Construction properties for a SNS action.

        :param topic: The SNS topic to notify.
        :param encoding: The encoding to use for the email within the Amazon SNS notification. Default: UTF-8

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "topic": topic,
        }
        if encoding is not None:
            self._values["encoding"] = encoding

    @builtins.property
    def topic(self) -> aws_cdk.aws_sns.ITopic:
        """The SNS topic to notify.

        stability
        :stability: experimental
        """
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return result

    @builtins.property
    def encoding(self) -> typing.Optional["EmailEncoding"]:
        """The encoding to use for the email within the Amazon SNS notification.

        default
        :default: UTF-8

        stability
        :stability: experimental
        """
        result = self._values.get("encoding")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_ses.IReceiptRuleAction)
class Stop(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses-actions.Stop"):
    """Terminates the evaluation of the receipt rule set and optionally publishes a notification to Amazon SNS.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        *,
        topic: typing.Optional[aws_cdk.aws_sns.ITopic] = None,
    ) -> None:
        """
        :param topic: The SNS topic to notify when the stop action is taken.

        stability
        :stability: experimental
        """
        props = StopProps(topic=topic)

        jsii.create(Stop, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: aws_cdk.aws_ses.IReceiptRule,
    ) -> aws_cdk.aws_ses.ReceiptRuleActionConfig:
        """Returns the receipt rule action specification.

        :param _rule: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_rule])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses-actions.StopProps",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic"},
)
class StopProps:
    def __init__(
        self,
        *,
        topic: typing.Optional[aws_cdk.aws_sns.ITopic] = None,
    ) -> None:
        """Construction properties for a stop action.

        :param topic: The SNS topic to notify when the stop action is taken.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def topic(self) -> typing.Optional[aws_cdk.aws_sns.ITopic]:
        """The SNS topic to notify when the stop action is taken.

        stability
        :stability: experimental
        """
        result = self._values.get("topic")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StopProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddHeader",
    "AddHeaderProps",
    "Bounce",
    "BounceProps",
    "BounceTemplate",
    "BounceTemplateProps",
    "EmailEncoding",
    "Lambda",
    "LambdaInvocationType",
    "LambdaProps",
    "S3",
    "S3Props",
    "Sns",
    "SnsProps",
    "Stop",
    "StopProps",
]

publication.publish()
