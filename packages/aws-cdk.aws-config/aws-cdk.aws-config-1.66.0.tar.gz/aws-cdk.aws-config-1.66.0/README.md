## AWS Config Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Developer Preview](https://img.shields.io/badge/cdk--constructs-developer--preview-informational.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are in **developer preview** before they become stable. We will only make breaking changes to address unforeseen API issues. Therefore, these APIs are not subject to [Semantic Versioning](https://semver.org/), and breaking changes will be announced in release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

Supported:

* Config rules

Not supported

* Configuration recorder
* Delivery channel
* Aggregation

### Initial Setup

Before using the constructs provided in this module, you need to setup
AWS Config in the region you plan on using it in. This setup includes:

* `ConfigurationRecorder`: Configure which resources will be recorded for config changes.
* `DeliveryChannel`: Configure where to store the recorded data.

Following are the guides to setup AWS Config:

* [Using the AWS Console](https://docs.aws.amazon.com/config/latest/developerguide/gs-console.html)
* [Using the AWS CLI](https://docs.aws.amazon.com/config/latest/developerguide/gs-cli.html)

### Rules

#### AWS managed rules

To set up a managed rule, define a `ManagedRule` and specify its identifier:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
ManagedRule(self, "AccessKeysRotated",
    identifier="ACCESS_KEYS_ROTATED"
)
```

Available identifiers and parameters are listed in the [List of AWS Config Managed Rules](https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html).

Higher level constructs for managed rules are available, see [Managed Rules](https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-config/lib/managed-rules.ts). Prefer to use those constructs when available (PRs welcome to add more of those).

#### Custom rules

To set up a custom rule, define a `CustomRule` and specify the Lambda Function to run and the trigger types:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
CustomRule(self, "CustomRule",
    lambda_function=my_fn,
    configuration_changes=True,
    periodic=True
)
```

#### Restricting the scope

By default rules are triggered by changes to all [resources](https://docs.aws.amazon.com/config/latest/developerguide/resource-config-reference.html#supported-resources). Use the `scopeToResource()`, `scopeToResources()` or `scopeToTag()` methods to restrict the scope of both managed and custom rules:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
ssh_rule = ManagedRule(self, "SSH",
    identifier="INCOMING_SSH_DISABLED"
)

# Restrict to a specific security group
rule.scope_to_resource("AWS::EC2::SecurityGroup", "sg-1234567890abcdefgh")

custom_rule = CustomRule(self, "CustomRule",
    lambda_function=my_fn,
    configuration_changes=True
)

# Restrict to a specific tag
custom_rule.scope_to_tag("Cost Center", "MyApp")
```

Only one type of scope restriction can be added to a rule (the last call to `scopeToXxx()` sets the scope).

#### Events

To define Amazon CloudWatch event rules, use the `onComplianceChange()` or `onReEvaluationStatus()` methods:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
rule = CloudFormationStackDriftDetectionCheck(self, "Drift")
rule.on_compliance_change("TopicEvent",
    target=targets.SnsTopic(topic)
)
```

#### Example

Creating custom and managed rules with scope restriction and events:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# A custom rule that runs on configuration changes of EC2 instances
fn = lambda_.Function(self, "CustomFunction",
    code=lambda_.AssetCode.from_inline("exports.handler = (event) => console.log(event);"),
    handler="index.handler",
    runtime=lambda_.Runtime.NODEJS_10_X
)

custom_rule = config.CustomRule(self, "Custom",
    configuration_changes=True,
    lambda_function=fn
)

custom_rule.scope_to_resource("AWS::EC2::Instance")

# A rule to detect stacks drifts
drift_rule = config.CloudFormationStackDriftDetectionCheck(self, "Drift")

# Topic for compliance events
compliance_topic = sns.Topic(self, "ComplianceTopic")

# Send notification on compliance change
drift_rule.on_compliance_change("ComplianceChange",
    target=targets.SnsTopic(compliance_topic)
)
```
