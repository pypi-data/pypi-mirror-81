# DynamoDB Package for detech.ai

This is detech.ai's package to access Dynamodb.

# Imports
```python
import detech_query_pkg

from detech_query_pkg import dynamodb_queries

from detech_query_pkg.utils import dynamodb_utils

#Start DynamoDB Client
create_dynamodb_client(aws_access_key_id=AWS_ACCESS_KEY_ID, 
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)

```

# Initialize Client
```python
def create_dynamodb_client(aws_access_key_id,aws_secret_access_key, region_name)

```

# Functions
## dynamodb

<details>
  <summary>insert_alert</summary>

  ```python
  def insert_alert(alert_id, metric_id, org_id, app_id, team_id, assigned_to, start_time, end_time, alert_description, is_acknowledged, anomalies_dict, related_prev_anomalies,  service_graph, significance_score, dynamodb)

  #Example
  insert_alert(alert_id = "256828", metric_id = 123, org_id = 'org_id', app_id = 'app_id', team_id = 'team_id', assigned_to = 'Jorge', \
  start_time = '2020-09-03 12:00:00', end_time = '2020-09-03 12:20:00', alert_description = 'Spike in costs',\
  is_acknowledged = 'True', anomalies_dict = {}, related_prev_anomalies = {},
  service_graph = {}, significance_score = '34.3')
  ``` 
</details>

<details>
  <summary>get_alert_item_by_key</summary>

  ```python
  def get_alert_item_by_key(anom_id, dynamodb)
  ```
</details>

<details>
  <summary>update_alert_with_related_anomalies</summary>

  ```python
  def update_alert_with_related_anomalies(alert_id,start_time, corr_anoms_dict, related_prev_anomalies, dynamodb)
  ```
</details>

<details>
  <summary>terminate_alert</summary>

  ```python
  def terminate_alert(alert_id,start_time, end_timestamp, dynamodb)
  ```
</details>

<details>
  <summary>create_metric</summary>

  ```python
  def create_metric(metric_id, date_bucket, metric_name, provider, namespace,
  agent, org_id, app_id, alignment, groupby, dimensions, data_points_list, dynamodb)

  #Example
  create_metric(
    metric_id = "test1", date_bucket = "2020-10-02", metric_name = "error_rate",
    provider = "aws", namespace = "dynamodb", agent = "CloudWatch", org_id = "test",
    app_id = "app1", alignment = "Sum",
    dimensions = [{"Name": "TableName", "Value": "alerts.config"}],
    last = 1535530432, data_points_list = [
      { 'val': 55, 'time' : 1535530430}, 
      { 'val': 56, 'time': 1535530432}], dynamodb=dynamodb
  )
  ```
</details>

<details>
  <summary>get_metric_details</summary>

  ```python
  def get_metric_details(metric_id, dynamodb)
  #Fetches all the details for a specific metric_id
  ```
</details>

<details>
  <summary>get_metric_item_by_key</summary>

  ```python
  def get_metric_item_by_key(metric_id, curr_date, dynamodb)
  ```
</details>

<details>
  <summary>scan_metrics_by_encrypted_id</summary>

  ```python
  def scan_metrics_by_encrypted_id(anom_alarm_id, dynamodb)
  ```
</details>

<details>
  <summary>query_alerts_configs_by_key</summary>

  ```python
  def query_alerts_configs_by_key(metric_id, dynamodb)
  ```
</details>

<details>
  <summary>insert_alert_config</summary>

  ```python
  def insert_alert_config(metric_id, alert_title, severity, alert_type, alert_direction, description, duration, duration_unit, rule_dict, recipients_list, owner_dict, dynamodb)

  #Example
  insert_alert_config(
    metric_id = "metric1245", alert_title = "Anomaly by Cluster", severity = "critical",
    alert_type = "anomaly", alert_direction = "spikes/drops", description = "Relevant to Play Store billing user journey",
    duration= 12, duration_unit = "hours", rule_dict = {}, recipients_list = [{
      "channel" : "webhook", 
      "contact" : "j.velez2210@gmail.com"
      },{
        "channel" : "slack",
        "contact" : "j.velez2210@gmail.com"
      }
    ], 
    owner_dict = {
      "user_id" : "user12341",
      "user_name" : "João Tótó",
    }
  )
  ```
</details>

<details>
  <summary>query_most_recent_metric_fetching_log</summary>

  ```python
  def query_most_recent_metric_fetching_log(component_id, dynamodb)
  #Fetches the log with the highest timestamp, from all the logs between start & end ts
  ```
</details>

## dynamodb_utils
<details>
  <summary>put_item</summary>

  ```python
  def put_item(item_dict, table_name, dynamodb)
  #Inserts json item into DynamoDB table

  #Example
  item_dict = {
    "attr" : "value",
    "attr2" : "value2"
  }
  table_name = "alerts"
  ```
</details>

<details>
  <summary>get_item</summary>

  ```python

  def get_item(key_dict, table_name, dynamodb)
  #Retrieves item from DynamoDB table

  #Example
  key_dict = {
    "prim_key" = "value",
    "sort_key" = "value"
  }
  ```
</details>

<details>
  <summary>get_item_and_retrieve_specific_attributes</summary>

  ```python

  def get_item_and_retrieve_specific_attributes(key_dict, attr_list, table_name, dynamodb)
  #Retrieves item from DynamoDB table and retrieve specific attributes

  #Example
  key_dict = {
    "prim_key" :"value",
    "sort_key" : "value"
  }
  attr_list = ['attr1', 'attr2']
  ```
</details>


<details>
  <summary>update_item</summary>

  ```python
  def update_item(key_dict, update_expression, expression_attr_values, table_name, dynamodb)
  #Retrieves item from DynamoDB table
  
  #Example
  key_dict = {
    "prim_key" = "value",
    "sort_key" = "value"
  }
  update_expression = "set service_graph=:i, metric_list=:l, significance_score=:s"
  expression_attr_values = {
    ':i': {'s1':['s2', 's3']},
    ':l': ['124','123'],
    ':s': Decimal(35.5)
  }
  #example to append to list
  UpdateExpression="SET some_attr = list_append(if_not_exists(some_attr, :empty_list), :i)",
  ExpressionAttributeValues={
    ':i': [some_value],
    "empty_list" : []
  }
  
  ```
</details>

<details>
  <summary>update_item_conditionally</summary>

  ```python
  def update_item_conditionally(key_dict, condition_expression, update_expression, expression_attr_values, table_name, dynamodb)
  #Retrieves item from DynamoDB table

  #Example
  key_dict = {
    "prim_key" = "value",
    "sort_key" = "value"
  }
  update_expression = "set service_graph=:i, metric_list=:l, significance_score=:s"
  expression_attr_values = {
    ':i': {'s1':['s2', 's3']},
    ':l': ['124','123'],
    ':s': Decimal(35.5)
  }
  condition_expression = "significance_score <= :val"
    
  ```
</details>

<details>
  <summary>delete_item_conditionally</summary>

  ```python
  def delete_item_conditionally(key_dict, condition_expression, expression_attr_values, table_name, dynamodb)
    
  #Example
  condition_expression = "significance_score <= :val"
  expression_attr_values = {
    ":val": Decimal(50)
  }
  key_dict = {
    'org_id': 'Aptoide',
    'start_time': '2020-09-03 12:00:00'
  }
  '''
  ```
</details>

<details>
  <summary>query_by_key</summary>

  ```python
  def query_by_key(key_condition, table_name, dynamodb)
  #Queries from DynamoDB table by key condition

  #Example
  key_condition = Key('org_id').eq('Aptoide')
    
  ```
</details>

<details>
  <summary>query_and_project_by_key_condition</summary>

  ```python
  def query_and_project_by_key_condition(projection_expr, expr_attr_names, key_condition, table_name, dynamodb)  
  #Queries from DynamoDB table by key condition and only returns some attrs

  #Example
  key_condition = Key('year').eq(year) & Key('title').between(title_range[0], title_range[1])
  projection_expr = "#yr, title, info.genres, info.actors[0]"
  expr_attr_names = {"#yr": "year"}
  ```
</details>

<details>
  <summary>scan_table</summary>

  ```python
  def scan_table(scan_kwargs, table_name, dynamodb)
  #Scans entire table looking for items that match the filter expression

  #Example
  scan_kwargs = {
    'FilterExpression': Key('year').between(*year_range),
    'ProjectionExpression': "#yr, title, info.rating",
    'ExpressionAttributeNames': {"#yr": "year"}
  }
    
  ```
</details>

<details>
  <summary>query_by_key_min_max</summary>

  ```python
  def query_by_key_min_max(key_condition, table_name, is_min, dynamodb)
  #Queries from DynamoDB table by key condition

  #Example
  key_condition = Key('part_id').eq(partId) & Key('range_key').between(start, end)
  #or 
  key_condition = Key('part_id').eq(partId)
  
  ```
</details>

<details>
  <summary>get_all_items_in_table</summary>

  ```python
  def get_all_items_in_table(table_name, dynamodb)
  ```
</details>
