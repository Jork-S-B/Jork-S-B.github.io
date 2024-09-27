The Elastic Stack，包括 Elasticsearch、Logstash、Kibana 和 Beats，也简称为ELK Stack，能够安全可靠地存储、搜索和可视化数据。

其中 Elasticsearch，简称ES，是一个开源的高扩展的分布式全文搜索引擎，也是 ELK Stack 的核心，负责近乎实时的存储和搜索数据，此外还能用于监控与分析。

Lucene 提供了一个全文搜索引擎的实现，需要搭配完整的服务框架进行应用。而 Elasticsearch 则是 Lucene 的一个分布式实现，它把索引和搜索功能封装成RESTful API，使其易上手易扩展。

## 📌 数据格式

Elasticsearch 是面向文档型数据库，一条数据在这里是指一个文档，文档可以包含多个字段，每个字段可以包含多个值。

* Index-索引，类似Database-数据库。
* Type-类型，类似Table-表；该概念被逐渐弱化，7.X版本已被删除。
* Document-文档，类似Row-行。
* Field-字段，类似Column-列。

正排索引，通过 key 找 value

倒排索引，分词，通过 value 找 key

## 📌 索引操作

### 🚁 创建索引

PUT: http://localhost:9200/index_name

PUT协议具有幂等性，重复发送时要求返回相同的结果。

### 🚁 查询指定索引

GET: http://localhost:9200/index_name

### 🚁 查询所有索引

GET: http://localhost:9200/_cat/indices?v

### 🚁 删除索引

DELETE: http://localhost:9200/index_name

## 📌 文档操作

### 🚁 创建文档

POST: http://localhost:9200/index_name/_doc

{ "json_field": "json_value" }

此时返回结果的"_id"即为文档的ID，随机生成的唯一标识。

保存时es会将文本分词，并建立倒排索引。

#### 🔧 创建文档，并指定_id

POST: http://localhost:9200/index_name/_create/1001

{ "json_field": "json_value" }

此时返回结果的"_id"即1001，用户自定义的ID。

### 🚁 修改文档

#### 🔧 全量更新

PUT: http://localhost:9200/index_name/_doc/1001

{ "json_field": "json_value1" }

#### 🔧 局部更新

POST: http://localhost:9200/index_name/_update/1001

{ "doc": { "json_field": "json_value1" } }

### 🚁 删除文档

DELETE: http://localhost:9200/index_name/_doc/1001

### 🚁 查询文档

#### 🔧 根据主键查询

GET: http://localhost:9200/index_name/_doc/1001

#### 🔧 查询索引下所有文档

GET: http://localhost:9200/index_name/_search

#### 🔧 条件查询

GET: http://localhost:9200/index_name/_search?q=json_field:json_value

或者使用请求体传参数

GET: http://localhost:9200/index_name/_search

{ "query": { "match": { "json_field": "json_value" } }

#### 🔧 分页与排序

GET: http://localhost:9200/index_name/_search

```json
{
  "query": {
    "match_all": {},
    "from": 0,
    "size": 10,
    "_source": [  // 限制返回的字段
      "json_field"
    ],
    "highlight": {  // 高亮显示
      "fields": {
        "json_field": {}
      }
    },
    "sort": [
      {
        "json_field": "desc"
      }
    ]
  }
}

```

#### 🔧 多条件查询

GET: http://localhost:9200/index_name/_search

```json
{
  "query": {
    "bool": {
      "must": [  // must类似于and，should类似于or
        {
          "match": {  // 全文检索匹配，查询时关键字会进行分词
            "json_field": "json_value"
          }
        },
        {
          "match_phrase": {  // 完全匹配
            "json_field1": "json_value1"
          }
        }
      ],
      "filter": {
        "range": {  // 范围查询
          "num": {
            "gt": 100
          }
        }
      }
    }
  }
}

```

#### 🔧 聚合查询

GET: http://localhost:9200/index_name/_search

```json
{
  "aggs": {
//    "field_group": {
//      "terms": {  // 分组
//        "field": "json_field"
//      }
//    },
    "field_avg": {
      "avg": {  // 平均值
        "field": "json_field"
      }
    }
  },
  "size": 0  // 不返回文档，只返回聚合结果
}
```

### 🚁 设置映射关系

PUT: http://localhost:9200/index_name/_mapping

```json
{
  "properties": {
    "json_field1": {
      "type": "text",  // 允许查询时分词效果
      "index": "true"
    },
    "json_field2": {
      "type": "keyword",  // 设置为关键字，不能分词；即必须完全匹配
      "index": "true"
    },
    "json_field3": {
      "type": "keyword",  // false-不能用该字段进行查询
      "index": "false"
    }
  }
}
```

## 📌 查看集群状态

GET: http://localhost:port/_cluster/health


## 📌 Kibana

数据可视化、实时查询、系统监控、日志分析

[KQL查询语法](https://www.cnblogs.com/hellosiyu/p/15689203.html)