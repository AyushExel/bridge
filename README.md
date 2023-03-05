# Bridge
Bridge the communication gap in dataset lifecycle .

Bridge is a data lifecycle management tool that allows:
* Users to ensure data quality
* Orgs to set enforcable programmatic data contracts across teams (data, dev, infra etc.)
* Seamless validation and monitoring across varios stages of data pipelines

Bridge is available as a command line tool to simply enforce contracts. 

## Python sdk
Bridge can be easily customized to build, enforce and any custom dataset. For this, we provide a python interface.

### Introduction
Bridge consists of 3 main components:
* <b> Contract </b>: A contract can be seen as a check that analyses an aspect of the given data. It can accept both mandatory and optional arguments. 

* <b> Result </b>: A result object is the result of enforcing a contract

* <b> Executor </b>: This is the engine that parses contracts from data-contract language( json temporarily ) to python and enforces the checks

Detailed python docs coming soon.

## Installation
Git clone the repo and run `pip install .`
Pip package coming soon

## Contract Language
Currently we're using json to write and ship contracts. You can use the following structure

```json
{
"contract1": {"param1": value, "param2": value},
"contract2": {"param1": value, "param2": value}
}
```
See a live example in example/ folder
