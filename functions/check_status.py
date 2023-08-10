def check_vault_seal_status(client):
    seal_status = client.sys.read_seal_status()
    return seal_status['sealed']


provider "aws" {
  region = "eu-west-2"  # Replace with your desired AWS region
}

variable "rds_instance_id" {
  description = "The ID of the RDS instance to monitor"
}

locals {
  thresholds = {
    missing_75 = 0.75,
    critical_90 = 0.9
  }

  include_metrics = [
    {
      name       = "ACUUtilization"
      statistic  = "Average"
      namespace  = "AWS/RDS"
      dimensions = { DBInstanceIdentifier = var.rds_instance_id }
      comparison_operator = "GreaterThanOrEqualToThreshold"  # Use GreaterThanOrEqualToThreshold for ACUUtilization and CPUUtilization
    },
    {
      name       = "ServerlessDatabaseCapacity"
      statistic  = "Maximum"
      namespace  = "AWS/RDS"
      dimensions = { DBClusterIdentifier = var.rds_instance_id }
      comparison_operator = "LessThanOrEqualToThreshold"  # Use LessThanOrEqualToThreshold for ServerlessDatabaseCapacity
    }
  ]

  alarms_75 = {
    for metric in local.include_metrics : metric.name => {
      alarm_name          = "RDS-${metric.name}-75-Alarm"
      comparison_operator = metric.comparison_operator
      evaluation_periods  = 1
      metric_name         = metric.name
      namespace           = metric.namespace
      period              = 60
      statistic           = metric.statistic
      dimensions          = metric.dimensions
      threshold           = local.thresholds.missing_75
      alarm_description   = "Alarm when ${metric.name} is 75%"
      alarm_actions       = [aws_sns_topic.example_sns.arn]
    }
  }

  alarms_90 = {
    for metric in local.include_metrics : metric.name => {
      alarm_name          = "RDS-${metric.name}-90-Alarm"
      comparison_operator = metric.comparison_operator
      evaluation_periods  = 1
      metric_name         = metric.name
      namespace           = metric.namespace
      period              = 60
      statistic           = metric.statistic
      dimensions          = metric.dimensions
      threshold           = local.thresholds.critical_90
      alarm_description   = "Alarm when ${metric.name} is 90%"
      alarm_actions       = [aws_sns_topic.example_sns.arn]
    }
  }
}

resource "aws_cloudwatch_metric_alarm" "rds_alarms_75" {
  for_each = local.alarms_75

  alarm_name          = each.value.alarm_name
  comparison_operator = each.value.comparison_operator
  evaluation_periods  = each.value.evaluation_periods
  metric_name         = each.value.metric_name
  namespace           = each.value.namespace
  period              = each.value.period
  statistic           = each.value.statistic
  dimensions          = each.value.dimensions
  threshold           = each.value.threshold
  alarm_description   = each.value.alarm_description
  alarm_actions       = each.value.alarm_actions
}

resource "aws_cloudwatch_metric_alarm" "rds_alarms_90" {
  for_each = local.alarms_90

  alarm_name          = each.value.alarm_name
  comparison_operator = each.value.comparison_operator
  evaluation_periods  = each.value.evaluation_periods
  metric_name         = each.value.metric_name
  namespace           = each.value.namespace
  period              = each.value.period
  statistic           = each.value.statistic
  dimensions          = each.value.dimensions
  threshold           = each.value.threshold
  alarm_description   = each.value.alarm_description
  alarm_actions       = each.value.alarm_actions
}

resource "aws_sns_topic" "example_sns" {
  name = "example-sns-topic"
}


#!/bin/bash

# Prompt for Azure AD credentials
read -p "Enter your Azure AD username: " azure_ad_username
read -s -p "Enter your Azure AD password: " azure_ad_password
echo  # Print a new line after password input

# Install saml2aws if not already installed
if ! command -v saml2aws &> /dev/null; then
    echo "saml2aws not found. Installing..."
    curl -Lo /usr/local/bin/saml2aws https://github.com/Versent/saml2aws/releases/latest/download/saml2aws_$(uname -s)_amd64
    chmod +x /usr/local/bin/saml2aws
fi

# Configure saml2aws
saml2aws configure \
  --url 'https://account.activedirectory.windowsazure.com' \
  --username "$azure_ad_username" \
  --idp-provider 'AzureAD' \
  --profile default \
  --region eu-west-2 \
  --app-id 'xxxxxxxxxxxxxxxxxxxxxxxxxx' \
  --skip-prompt \
  --mfa 'Auto'

# Authenticate and obtain AWS credentials
saml2aws login
