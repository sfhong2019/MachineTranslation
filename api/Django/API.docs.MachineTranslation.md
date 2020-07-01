# 文本翻译接口文档 
### 0. 部署依赖
 - python 3.x

### 1. 接口功能
将输入的中文(英文)的文本翻译成英文(中文)

### 2. 接口详情
#### 2.1 访问 
访问| - 
---|---
地址 | 待部署
请求方式 | POST

#### 2.2 参数 
参数| 必填| 说明
---|---|---
to_lang| 是| 指定翻译结果的语言，英/中：en/zh 
input_text| 是| 需要翻译的文本 

#### 2.3 访问状态 
结果| status 
---|---
翻译成功| 'ok'| 
翻译失败| 'failed to translate'| 

### 3. 示例 
#### 3.1 翻译成功 
英-中

    {
        "status": "ok",
        "data": [
            {
                "output_text": "那只敏捷的棕色狐狸跳过那只懒狗。"
            }
        ]
    }
    
中 - 英

    {
        "status": "ok",
        "data": [
            {
                "output_text": "Where to eat tonight?"
            }
        ]
    }

#### 3.1 翻译失败 

    {
        "status": "failed to translate",
        "data": []
    }
