## **背景描述**
本练习赛与葡萄牙银行机构的营销活动相关。这些营销活动一般以电话为基础，银行的客服人员至少联系客户一次，以确认客户是否有意愿购买该银行的产品（定期存款）。

任务是基本类型为分类任务，即预测客户是否购买该银行的产品。

## **数据说明**

|NO	|字段名称| 数据类型|字段描述|
| -------- | -------- | -------- | -------- |
|1|ID|Int|客户唯一标识
|2|	age|	Int|	客户年龄
|3|	job|	String	|客户的职业
|4|	marital	|String	|婚姻状况
|5	|education|	String|	受教育水平
|6	|default	|String|	是否有违约记录
|7	|balance	|Int	|每年账户的平均余额
|8	|housing	|String|	是否有住房贷款
|9	|loan	|String|	是否有个人贷款
|10|	contact	|String	|与客户联系的沟通方式
|11	|day	|Int	|最后一次联系的时间（几号）
|12	|month	|String	|最后一次联系的时间（月份）
|13	|duration	|Int	|最后一次联系的交流时长
|14	|campaign	|Int	|在本次活动中，与该客户交流过的次数
|15	|pdays	|Int	|距离上次活动最后一次联系该客户，过去了多久（999表示没有联系过）
|16	|previous	|Int	|在本次活动之前，与该客户交流过的次数
|17	|poutcome	|String	|上一次活动的结果
|18|	y|	Int	|预测客户是否会订购定期存款业务


## **数据来源**
数据参考：Citation: [Moro et al., 2014] S. Moro, P. Cortez and P. Rita. A Data-Driven Approach to Predict the Success of Bank Telemarketing. Decision Support Systems, Elsevier, 62:22-31, June 2014


## **引用格式**
```
@misc{purchase_pred8546,
    title = { 预测分析·客户购买预测 数据集 },
    author = { 小鲸 },
    howpublished = { \url{https://www.heywhale.com/org/series_5ffbf4d2a96f9e0036c2bffb/dataset/6193594c86227300178e4c33} },
    year = { 2021 },
}
```